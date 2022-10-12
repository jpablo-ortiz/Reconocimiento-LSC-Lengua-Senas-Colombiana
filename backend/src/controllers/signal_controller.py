import base64
import os

from LSC_recognizer_model.src.coordenates.data.split_dataset import SplitDataset
from LSC_recognizer_model.src.coordenates.models.coordenates_models import (
    INPUT_SHAPE_FIX,
    get_model_coord_dense_2,
)
from LSC_recognizer_model.src.utils.sign_model import SignModel
from models.coord_signal import CoordSignal
from models.signal import Image, RequestSignal, Signal
from repositories.signal_repository import SignalRepository
from settings import PATH_CHECKPOINTS_LOAD, PATH_PREDICTED_IMG, PATH_RAW_NUMPY
from utils.holistic.holistic_detector import HolisticDetector


class SignalController:
    def __init__(self, signal_repository: SignalRepository):
        self.signal_repository = signal_repository

    def save_image_on_mediapipe_numpy_file(self, signal: Signal):
        raise NotImplementedError

    def create_signal(self, signal: RequestSignal):
        result_signal = self.signal_repository.get_signal_by_name(signal.name, with_images=False)
        if result_signal is None:
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
        split_dataset = SplitDataset(path_raw_numpy=PATH_RAW_NUMPY)

        classes = split_dataset.get_classes()

        signal_model = SignModel(
            model=get_model_coord_dense_2(INPUT_SHAPE_FIX, len(classes)),
            path_to_load_weights=PATH_CHECKPOINTS_LOAD,
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
