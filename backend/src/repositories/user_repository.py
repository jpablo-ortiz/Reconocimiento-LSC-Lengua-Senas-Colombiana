import abc

from tinydb import Query, where

from models.user import UserModel
from settings import users_table as db_tiny


class UserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_user(self, user: UserModel):
        pass

    @abc.abstractmethod
    def get_by_username(self, username):
        pass


class UserRepositoryTinyDB(UserRepository):
    def __init__(self):
        self.query = Query

    def create_user(self, user: UserModel):
        return db_tiny.insert(user.dict())

    def get_by_username(self, username):
        result = db_tiny.search(where("username") == username)
        if len(result) > 0:
            return UserModel(**result[0])
        return None
