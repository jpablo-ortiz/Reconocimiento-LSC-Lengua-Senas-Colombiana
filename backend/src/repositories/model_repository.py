import abc

from tinydb import Query

from models.model_variables import ModelVariables, TrainingState
from settings import models_table as db_tiny


class ModelRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, model_variables: ModelVariables) -> int:
        pass

    @abc.abstractmethod
    def update(self, model_variables: ModelVariables) -> int:
        pass

    @abc.abstractmethod
    def get_training_info(self, id_training: int):
        pass

    @abc.abstractmethod
    def get_training_info_actual(self):
        pass

    @abc.abstractmethod
    def get_next_model_number(self):
        pass

    @abc.abstractmethod
    def get_actual_model(self) -> ModelVariables:
        pass


class ModelRepositoryTinyDB(ModelRepository):
    def __init__(self):
        self.query = Query()

    def create(self, model_variables: ModelVariables) -> int:
        id = db_tiny.insert(model_variables.dict())
        db_tiny.update({"id": id}, doc_ids=[id])
        return id

    def update(self, model_variables: ModelVariables) -> int:
        id = db_tiny.update(model_variables.dict(), doc_ids=[model_variables.id])
        return id

    def get_training_info(self, id_training: int):
        return db_tiny.get(doc_id=id_training)

    def get_training_info_actual(self):
        # Order by id desc
        result = db_tiny.all()
        result = sorted(result, key=lambda k: k["id"])
        if len(result) == 0:
            return None
        return result[-1]

    def get_next_model_number(self):
        result = db_tiny.all()
        result = sorted(result, key=lambda k: k["id"])
        if len(result) == 0:
            return 1
        return result[-1]["id"] + 1

    def get_actual_model(self) -> ModelVariables:
        result = db_tiny.all()
        result = sorted(result, key=lambda k: k["id"])

        # Get last model with status FINISHED = 3
        for model in reversed(result):
            model_variables = ModelVariables(**model)
            if model_variables.training_state == TrainingState.FINISHED:
                return model_variables

        return None
