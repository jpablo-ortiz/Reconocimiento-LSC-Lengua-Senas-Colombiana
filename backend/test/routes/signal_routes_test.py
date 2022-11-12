from fastapi import FastAPI
from fastapi.testclient import TestClient
from signal_routes_mock import router

from models import RequestSignal

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_save_signal():
    response = client.post(
        url="/new-signal",
        json=RequestSignal(name="test", images=["test"]).dict(),
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 200
    response = response.json()
    assert response["result"] == RequestSignal(name="test", images=["test"]).dict()
    assert response["message"] == "Señal creada correctamente"


def test_save_signal_unauthorized():
    response = client.post(
        url="/new-signal",
        json=RequestSignal(name="test", images=["test"]).dict(),
        headers={"Authorization": "wrong"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_save_signal_incorrect_name():
    response = client.post(
        url="/new-signal",
        json=RequestSignal(name="", images=["test"]).dict(),
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 422
    assert response.json() == {"detail": "El nombre de la señal está vacío"}
