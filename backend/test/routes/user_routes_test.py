from fastapi import FastAPI
from fastapi.testclient import TestClient
from user_routes_mock import router

from models import UserModel

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_signup():
    response = client.post(
        url="/signup",
        json={
            "username": "test@test.com",
            "password": "test",
            "role": "user",
            "name": "test",
        },
    )
    assert response.status_code == 200
    response = response.json()
    assert response == "Usuario creado Correctamente"


def test_signup_user_already_exists():
    response = client.post(
        url="/signup",
        json=UserModel(
            username="admin@admin.com",
            password="admin",
            role="admin",
            name="admin",
        ).dict(),
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Cuenta ya existe"}


def test_login():
    response = client.post(
        url="/login",
        json={
            "username": "admin@admin.com",
            "password": "admin",
        },
    )
    assert response.status_code == 200
    response = response.json()
    assert response["access_token"] == "secret"
    assert response["role"] == "admin"
    assert response["name"] == "admin"


def test_login_user_not_exists():
    response = client.post(
        url="/login",
        json={
            "username": "test",
            "password": "test",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Usuario no existe"}


def test_login_wrong_password():
    response = client.post(
        url="/login",
        json={
            "username": "admin@admin.com",
            "password": "test",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Contraseña incorrecta"}
