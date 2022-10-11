import abc

from tinydb import Query
from models.signal import Signal
from settings import signal_table as db
from settings import signal_table_tinydb as db_tiny


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
        # Search if signal name already exists
        result = db_tiny.search(self.query.name == signal.name)

        if result:  # If signal name already exists
            # Append photos to signal
            signal.photos.extend(result[0]["photos"])

            # Counter of photos
            signal.counter = len(signal.photos)
            signal.new_signal = False

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
