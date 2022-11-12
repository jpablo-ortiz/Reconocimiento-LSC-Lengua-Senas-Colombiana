from fastapi import APIRouter, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from controllers.user_controller import (
    ACCOUNT_LOGIN_PASSWORD_ERROR,
    ACCOUNT_LOGIN_USER_ERROR,
    ACCOUNT_SIGNUP_ERROR,
    ACCOUNT_SIGNUP_EXIST,
    UserController,
)
from models.user import UserLogin, UserModel
from repositories.user_repository import UserRepositoryTinyDB
from utils.auth.auth_service import AuthService

# -------------------------------------------------
# ------------- Inicialzando el router ------------
# -------------------------------------------------

router = APIRouter()

security = HTTPBearer()
auth_handler = AuthService()

user_repository = UserRepositoryTinyDB()

# -------------------------------------------------
# --------------- SERVICIOS REST ------------------
# -------------------------------------------------


@router.get("/")
def home():
    return {"message": "Conectado con éxito"}


@router.post("/signup")
def signup(user_details: UserModel):
    user_controller = UserController(user_repository, auth_handler)
    result = user_controller.signup(user_details)

    if result == ACCOUNT_SIGNUP_EXIST:
        raise HTTPException(status_code=409, detail=ACCOUNT_SIGNUP_EXIST)
    if result == ACCOUNT_SIGNUP_ERROR:
        raise HTTPException(status_code=500, detail=ACCOUNT_SIGNUP_ERROR)

    return result


@router.post("/login")
def login(user_details: UserLogin):
    user_controller = UserController(user_repository, auth_handler)
    result = user_controller.login(user_details.username, user_details.password)

    if result == ACCOUNT_LOGIN_USER_ERROR:
        raise HTTPException(status_code=409, detail=ACCOUNT_LOGIN_USER_ERROR)
    if result == ACCOUNT_LOGIN_PASSWORD_ERROR:
        raise HTTPException(status_code=409, detail=ACCOUNT_LOGIN_PASSWORD_ERROR)

    return result


@router.get("/refresh_token")
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    expired_token = credentials.credentials
    new_token = auth_handler.encode_refresh_token(expired_token)
    return {"access_token": new_token}


@router.get("/notsecret")
def not_secret_data():
    return "Not secret data"


@router.post("/secret")
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    if not verify_credentials(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return "Top Secret data only authorized users can access this info"


# -------------------------------------------------
# --------------- EXTRA FUNCTIONS -----------------
# -------------------------------------------------


def verify_credentials(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    auth_handler.decode_token(token)
