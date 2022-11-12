from datetime import datetime

from fastapi import APIRouter, HTTPException, Request

from models import ModelVariables, TrainingState

fake_secret_token = "secret"

mock_db = {
    "signals": {
        "1": {
            "name": "prueba1",
            "images": None,
            "processed_signal": False,
        }
    },
    "models": {
        "1": {
            "id": "1",
            "name": "prueba1",
            "loss": 0.316,
            "val_loss": 0.316,
            "accuracy": 0.932,
            "val_accuracy": 0.932,
            "mean_time_execution": 0.6396115562799787,
            "epoch": 1000,
            "cant_epochs": 1000,
            "training_state": 3,
            "begin_time": "{TinyDate}:2022-10-21T02:18:09.589691",
            "end_time": "{TinyDate}:2022-10-21T02:20:15.966698",
        },
        "2": {
            "id": "2",
            "name": "prueba2",
            "loss": 0.316,
            "val_loss": 0.316,
            "accuracy": 0.932,
            "val_accuracy": 0.932,
            "mean_time_execution": 0.6396115562799787,
            "epoch": 1000,
            "cant_epochs": 1000,
            "training_state": 2,
            "begin_time": "{TinyDate}:2022-10-21T02:18:09.589691",
            "end_time": "{TinyDate}:2022-10-21T02:20:15.966698",
        },
    },
}

images_db = {
    "notprocessed": ["Amor", "Alegria"],
    "processed": ["Tristeza", "Enojo", "Sorpresa", "Asco", "Miedo"],
}

router = APIRouter()


@router.get("/train/{epochs}")
async def train_model(epochs: int, req: Request):
    if req.headers["Authorization"] != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if epochs < 1:
        raise HTTPException(status_code=422, detail="La cantidad de épocas debe ser mayor que 1")

    today = datetime.now()
    num_model = "3"

    model_variables = ModelVariables(
        id=num_model,
        name=f"{num_model}-Modelo_{today.strftime('%Y-%m-%d_%H-%M-%S')}",
        loss=0.0,
        val_loss=0.0,
        accuracy=0.0,
        val_accuracy=0.0,
        mean_time_execution=0.0,
        epoch=0,
        cant_epochs=epochs,
        training_state=TrainingState.CREATED,
        begin_time=datetime.now(),
        end_time=datetime.now(),
    )

    mock_db["models"][str(num_model)] = model_variables.dict()

    return {"proceso de entrenamiento iniciado con éxito"}


@router.get("/training-info/{id_training}")
async def get_training_info(id_training: str, req: Request):
    if req.headers["Authorization"] != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if id_training not in mock_db["models"].keys():
        raise HTTPException(status_code=404, detail="No se encontró el entrenamiento con el id especificado")
    return mock_db["models"][id_training]


@router.get("/training-info")
async def get_training_info_actual(req: Request):
    if req.headers["Authorization"] != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if len(mock_db["models"]) == 0:
        raise HTTPException(status_code=404, detail="No se encontraron entrenamientos")
    for _, v in reversed(mock_db["models"].items()):
        return v


@router.get("/train-state")
async def get_train_state(req: Request):
    if req.headers["Authorization"] != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return images_db["notprocessed"]


@router.get("/actual-model")
async def get_actual_model(req: Request):
    if req.headers["Authorization"] != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if len(mock_db["models"]) == 0 or all(
        callback["training_state"] != 3 for callback in mock_db["models"].values()
    ):
        raise HTTPException(status_code=404, detail="No se encontró ningún modelo entrenado")

    # Get only models with training_state = 3 (trained)
    trained_models = [model for model in mock_db["models"].values() if model["training_state"] == 3]
    return trained_models[-1]


# -------------- Auxiliar functions --------------


def change_all_models_to_error():
    for model in mock_db["models"].values():
        model["training_state"] = 4
