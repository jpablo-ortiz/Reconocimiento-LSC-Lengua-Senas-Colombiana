import abc
import base64
import os

from models.signal import Image, Signal
from settings import signal_table as db
from settings import signal_table_tinydb as db_tiny
from tinydb import Query


class SignalRepository(metaclass=abc.ABCMeta):
    def __init__(self, path):
        self.path = path
        # Verify if the path exists
        if not os.path.exists(self.path):
            raise Exception(f"Path {self.path} does not exist")

    def create_signal(self, signal: Signal):
        # Create a new folder with the signal name
        folder_name = f"{self.path}/{signal.name}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Save images
        images = [(image.name, base64.b64decode(image.image)) for image in signal.images]

        for name, image in images:
            with open(
                f"{folder_name}/{name}_{'processed' if signal.processed_signal else 'notprocessed'}.jpg", "wb"
            ) as file:
                file.write(image)

    def get_images_by_signal_name(self, signal_name: str) -> Signal:
        # Get all images from a folder
        folder_name = f"{self.path}/{signal_name}"

        images_path = os.listdir(folder_name)
        images = [
            Image(
                image=base64.b64encode(open(image_path, "rb").read()),
                name=image_path.split("_")[-2],  # .../NAME_notprocessed.jpg
                processed=False if "notprocessed" in image_path else True,
            )
            for image_path in images_path
        ]

        return images

    def add_images_to_signal(self, signal_name: str, images: list[Image]):
        try:
            folder_name = f"{self.path}/{signal_name}"

            for image in images:
                with open(
                    f"{folder_name}/{image.name}_{'processed' if image.processed_image else 'notprocessed'}.jpg",
                    "wb",
                ) as file:
                    file.write(base64.b64decode(image.image))
        except Exception as e:
            raise e

    def get_signals_with_unprocessed_images(self) -> list[Signal]:
        signals = self.get_all_signals()

        signals_with_unprocessed_images = []
        for signal in signals:
            folder_name = f"{self.path}/{signal.name}"
            images_path = os.listdir(folder_name)
            if any("notprocessed" in image_path for image_path in images_path):
                signals_with_unprocessed_images.append(signal)

        return signals_with_unprocessed_images

    @abc.abstractmethod
    def get_signal_by_name(self, signal_name: str, with_images: bool = True) -> Signal:
        pass

    @abc.abstractmethod
    def update_signal(self, signal: Signal) -> int:
        pass

    @abc.abstractmethod
    def get_all_signals(self) -> list[Signal]:
        pass


class SignalRepositoryNoSQL(SignalRepository):
    def __init__(self):
        pass

    def create_signal(self, signal: Signal) -> int:
        raise NotImplementedError

    def get_signal_by_name(self, signal_name: str, with_images: bool = True) -> Signal:
        raise NotImplementedError

    def update_signal(self, signal: Signal) -> int:
        raise NotImplementedError

    def get_all_signals(self) -> list[Signal]:
        raise NotImplementedError


class SignalRepositoryTinyDB(SignalRepository):
    def __init__(self):
        self.query = Query()

    def create_signal(self, signal: Signal) -> int:
        super().create_signal(signal)
        signal.images = None
        return db_tiny.insert(signal.dict())

    def get_signal_by_name(self, signal_name: str, with_images: bool = True) -> Signal:
        result = db_tiny.search(self.query.name == signal_name)

        if len(result) == 0:
            return None

        result = Signal(**result[0])

        if with_images:
            images = super().get_images_by_signal_name(signal_name)
            result.images = images

        return result

    def update_signal(self, signal: Signal) -> int:
        return db_tiny.update(signal.dict(), self.query.name == signal.name)[0]

    def get_all_signals(self) -> list[Signal]:
        return [Signal(**signal) for signal in db_tiny.all()]
