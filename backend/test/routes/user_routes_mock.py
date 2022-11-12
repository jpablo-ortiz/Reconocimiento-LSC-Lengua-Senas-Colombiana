from fastapi import APIRouter, HTTPException
from models import UserLogin, UserModel

fake_secret_token = "secret"

users_db = {
    "1": {
        "username": "admin@admin.com",
        "password": "admin",
        "role": "admin",
        "name": "admin",
    }
}

router = APIRouter()


@router.post("/signup")
def signup(user_details: UserModel):
    if user_details.username == users_db["1"]["username"]:
        raise HTTPException(status_code=409, detail="Cuenta ya existe")
    return "Usuario creado Correctamente"


@router.post("/login")
def login(user_details: UserLogin):
    if user_details.username != users_db["1"]["username"]:
        raise HTTPException(status_code=409, detail="Usuario no existe")
    if user_details.password != users_db["1"]["password"]:
        raise HTTPException(status_code=409, detail="Contraseña incorrecta")
    return {"access_token": fake_secret_token, "role": users_db["1"]["role"], "name": users_db["1"]["name"]}
