from fastapi import FastAPI
from fastapi.testclient import TestClient
from train_routes_mock import change_all_models_to_error, router

from models import TrainingState

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_get_training_info():
    response = client.get(
        url="/training-info",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 200
    response = response.json()
    assert response["id"] == "2"
    assert response["name"] == "prueba2"
    assert response["training_state"] == TrainingState.PROCESSING


def test_get_training_info_by_id():
    response = client.get(
        url="/training-info/1",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 200
    response = response.json()
    assert response["id"] == "1"
    assert response["name"] == "prueba1"
    assert response["training_state"] == TrainingState.FINISHED


def test_get_training_info_unauthorized():
    response = client.get(
        url="/training-info/1",
        headers={"Authorization": "wrong"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_training_info_not_found():
    response = client.get(
        url="/training-info/100",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No se encontró el entrenamiento con el id especificado"}


def test_get_train_state():
    response = client.get(
        url="/train-state",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response) == 2
    assert "Amor" in response
    assert "Alegria" in response


def test_get_train_state_unauthorized():
    response = client.get(
        url="/train-state",
        headers={"Authorization": "wrong"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_actual_model():
    response = client.get(
        url="/actual-model",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 200
    response = response.json()
    assert response["id"] == "1"
    assert response["name"] == "prueba1"
    assert response["training_state"] == TrainingState.FINISHED


def test_get_actual_model_unauthorized():
    response = client.get(
        url="/actual-model",
        headers={"Authorization": "wrong"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}


def test_get_actual_model_not_found():
    # Change all training states to error
    change_all_models_to_error()

    response = client.get(
        url="/actual-model",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No se encontró ningún modelo entrenado"}


def test_train_model():
    response = client.get(
        url="/train/100",
        headers={"Authorization": "secret"},
    )
    assert response.status_code == 200
    response = response.json()
    assert response[0] == "proceso de entrenamiento iniciado con éxito"


def test_train_model_unauthorized():
    response = client.get(
        url="/train/100",
        headers={"Authorization": "wrong"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
