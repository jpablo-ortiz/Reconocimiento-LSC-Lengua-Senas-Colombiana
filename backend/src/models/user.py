from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    password: str
    role: str
    name: str


class UserLogin(BaseModel):
    username: str
    password: str
