import abc

from models.callback_variables import CallbackVariables
from settings import callback_table as db
from settings import callback_table_tinydb as db_tiny
from tinydb import Query


class CallbackRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, callback_variables: CallbackVariables) -> int:
        pass

    @abc.abstractmethod
    def update(self, callback_variables: CallbackVariables) -> int:
        pass

    @abc.abstractmethod
    def get_training_info(self, id_training: int):
        pass


class CallbackRepositoryNoSQL(CallbackRepository):
    def __init__(self):
        pass

    def create(self, callback_variables: CallbackVariables) -> int:
        raise NotImplementedError

    def update(self, callback_variables: CallbackVariables) -> int:
        raise NotImplementedError

    def get_training_info(self, id_training: int):
        raise NotImplementedError


class CallbackRepositoryTinyDB(CallbackRepository):
    def __init__(self):
        self.query = Query()

    def create(self, callback_variables: CallbackVariables) -> int:
        id = db_tiny.insert(callback_variables.dict())
        db_tiny.update({"id": id}, doc_ids=[id])
        return id

    def update(self, callback_variables: CallbackVariables) -> int:
        id = db_tiny.update(callback_variables.dict(), doc_ids=[callback_variables.id])
        return id

    def get_training_info(self, id_training: int):
        return db_tiny.get(doc_id=id_training)
