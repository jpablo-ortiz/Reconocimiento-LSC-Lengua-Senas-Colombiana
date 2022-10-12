import base64
import os

from LSC_recognizer_model.src.coordenates.data.split_dataset import SplitDataset
from LSC_recognizer_model.src.coordenates.models.coordenates_models import (
    INPUT_SHAPE_FIX,
    get_model_coord_dense_2,
)
from LSC_recognizer_model.src.utils.sign_model import SignModel
from models.coord_signal import CoordSignal
from models.signal import Signal
from repositories.signal_repository import SignalRepository
from settings import PATH_CHECKPOINTS_LOAD, PATH_PREDICTED_IMG, PATH_RAW_NUMPY
from utils.holistic.holistic_detector import HolisticDetector


class SignalController:
    def __init__(self, signal_repository: SignalRepository):
        self.signal_repository = signal_repository

    def save_image_on_mediapipe_numpy_file(self, signal: Signal):
        raise NotImplementedError

    def create_signal(self, signal: Signal):
        # Save signal on database
        return self.signal_repository.create_signal(signal)

    def save_image_on_disk(self, signal: Signal):

        # convert list of base64 to list of images
        photos = [base64.b64decode(photo) for photo in signal.photos]

        # Create folder if not exists
        folder: str = PATH_PREDICTED_IMG + "/" + signal.name
        if not os.path.exists(folder):
            os.makedirs(folder)

        # save images on disk
        for i, photo in enumerate(photos):
            with open(f"{PATH_PREDICTED_IMG}/{signal.name}/{i}.jpg", "wb") as file:
                file.write(photo)

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
