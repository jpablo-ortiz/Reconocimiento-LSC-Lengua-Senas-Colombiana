import os

from LSC_recognizer_model.src.utils.sign_model import SignModel
from models.coord_signal import CoordSignal
from models.signal import Image, RequestSignal, Signal
from repositories.model_repository import ModelRepository
from repositories.signal_repository import SignalRepository
from settings import INPUT, PATH_MODELS, neuronal_network
from utils.holistic.holistic_detector import HolisticDetector


class SignalController:
    def __init__(self, signal_repository: SignalRepository, model_repository: ModelRepository):
        self.model_repository = model_repository
        self.signal_repository = signal_repository

    def save_image_on_mediapipe_numpy_file(self, signal: Signal):
        raise NotImplementedError

    def create_signal(self, signal: RequestSignal):
        result_signal = self.signal_repository.get_signal_by_name(signal.name, with_images=False)
        if result_signal is None:  # Not exists
            new_signal = Signal(
                name=signal.name,
                images=[
                    Image(image=img, name=i, processed_image=False) for i, img in enumerate(signal.images)
                ],
                processed_signal=False,
            )

            self.signal_repository.create_signal(new_signal)
        else:
            self.signal_repository.add_images_to_signal(
                signal_name=signal.name,
                images=[
                    Image(image=img, name=i, processed_image=False) for i, img in enumerate(signal.images)
                ],
            )

        return signal.name

    def predict_signal(self, coord_signal: CoordSignal):
        PATH_CHECKPOINTS_LOAD = self.get_checkpoint_path()
        model_dir = f"{PATH_CHECKPOINTS_LOAD}/weights.hdf5"

        if not os.path.exists(model_dir):
            model_dir = PATH_CHECKPOINTS_LOAD

        classes = self.get_signals_of_the_actual_model()

        signal_model = SignModel(
            model=neuronal_network(INPUT, len(classes)),
            path_to_load_weights=model_dir,
        )

        predictions = signal_model.get_prediction(
            keypoints=HolisticDetector().get_coordenates(
                coord_signal, used_parts=["pose", "right_hand", "left_hand"]
            ),
            classes=classes,
        )

        predictions = {prediction[0]: prediction[1] for prediction in predictions}

        return predictions

    def get_signals_with_unprocessed_images(self):
        signals = self.signal_repository.get_signals_with_unprocessed_images()
        return signals

    def update_all_signals_to_processed(self):
        return self.signal_repository.update_all_signals_to_processed()

    def get_signals_of_the_actual_model(self) -> dict[str, str]:
        classes = self.model_repository.get_actual_model().trained_signals
        return [(int(k), v) for k, v in classes.items()]

    def get_checkpoint_path(self) -> str:
        return os.path.join(PATH_MODELS, self.model_repository.get_actual_model().name)
