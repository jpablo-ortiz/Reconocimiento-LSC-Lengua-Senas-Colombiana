from models.user import UserModel
from repositories.user_repository import UserRepository
from utils.auth.auth_service import AuthService

ACCOUNT_SIGNUP_CREATED = "Usuario creado Correctamente"

ACCOUNT_SIGNUP_EXIST = "Cuenta ya existe"
ACCOUNT_SIGNUP_ERROR = "Error al crear la cuenta"

ACCOUNT_LOGIN_USER_ERROR = "Usuario no existe"
ACCOUNT_LOGIN_PASSWORD_ERROR = "Contraseña Inválida"


class UserController:
    def __init__(self, user_repository: UserRepository, auth_handler: AuthService):
        self.user_repository = user_repository
        self.auth_handler = auth_handler

    def signup(self, user: UserModel):
        if self.user_repository.get_by_username(user.username) is not None:
            return ACCOUNT_SIGNUP_EXIST

        try:
            hashed_password = self.auth_handler.encode_password(user.password)
            user.password = hashed_password
            self.user_repository.create_user(user)

            return ACCOUNT_SIGNUP_CREATED
        except Exception as error:
            print(error)
            return ACCOUNT_SIGNUP_ERROR

    def login(self, username, password):
        user: UserModel = self.user_repository.get_by_username(username)
        if user is None:
            return ACCOUNT_LOGIN_USER_ERROR
        if not self.auth_handler.verify_password(password, user.password):
            return ACCOUNT_LOGIN_PASSWORD_ERROR

        access_token = self.auth_handler.encode_token(user.username)
        return {"access_token": access_token, "role": user.role, "name": user.name}
