import abc

from models.signal import Signal
from settings import signal_table as db
from settings import signal_table_tinydb as db_tiny
from tinydb import Query


class SignalRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_signal(self, signal: Signal):
        pass


class SignalRepositoryNoSQL(SignalRepository):
    def __init__(self):
        pass

    def create_signal(self, signal: Signal):
        raise NotImplementedError


class SignalRepositoryTinyDB(SignalRepository):
    def __init__(self):
        self.query = Query()

    def create_signal(self, signal: Signal):
        # TODO: esto debería estar en controller, repository solo se encarga de concectar con la base de datos

        # TODO: la imagen que sea un objeto porque debo decir si es una imagen nueva o no independiente de su clase general de señal

        # Search if signal name already exists
        result = db_tiny.search(self.query.name == signal.name)

        if result:  # If signal name already exists
            # Append photos to signal
            signal.photos.extend(result[0]["photos"])

            # Counter of photos
            signal.counter = len(signal.photos)
            signal.new_signal = True

            # Update photos on database
            return db_tiny.update(
                {"photos": signal.photos, "counter": signal.counter},
                self.query.name == signal.name,
            )

        # Counter of photos
        signal.counter = len(signal.photos)

        signal.new_signal = True

        # Insert new signal
        return db_tiny.insert(signal.dict())
