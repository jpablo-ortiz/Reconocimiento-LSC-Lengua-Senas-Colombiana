import asyncio
from urllib.request import Request

from fastapi import APIRouter, HTTPException, Request

from controllers.model_controller import ModelController
from controllers.signal_controller import SignalController
from repositories.model_repository import ModelRepositoryTinyDB
from repositories.signal_repository import SignalRepositoryTinyDB
from settings import PATH_RAW_SIGNS
from utils.auth.auth_service import AuthService

# -------------------------------------------------
# ------------- Inicialzando el router ------------
# -------------------------------------------------

router = APIRouter()

auth_service = AuthService()

signal_repository = SignalRepositoryTinyDB(path=PATH_RAW_SIGNS)
model_repository = ModelRepositoryTinyDB()

# -------------------------------------------------
# --------------- SERVICIOS REST ------------------
# -------------------------------------------------


@router.get("/train/{epochs}")
async def train_model(epochs: int, req: Request):
    if not auth_service.verify_credentials(req):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if epochs < 1:
        raise HTTPException(status_code=422, detail="La cantidad de épocas debe ser mayor que 1")
    try:
        signal_controller = SignalController(
            signal_repository=signal_repository,
            model_repository=model_repository,
        )
        model_controller = ModelController(
            signal_controller=signal_controller,
            model_repository=model_repository,
        )
        signal_controller = SignalController(signal_repository, model_repository)

        callback_variable = model_controller.callback_training_creation(epochs)
        asyncio.create_task(model_controller.train_model(epochs, callback_variable))
        return {"proceso de entrenamiento iniciado con éxito"}
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Error al iniciar el proceso de entrenamiento",
        ) from error


@router.get("/training-info/{id_training}")
def get_training_info(id_training: str, req: Request):
    if not auth_service.verify_credentials(req):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        signal_controller = SignalController(
            signal_repository=signal_repository,
            model_repository=model_repository,
        )
        model_controller = ModelController(
            signal_controller=signal_controller,
            model_repository=model_repository,
        )
        res = model_controller.get_training_info(
            id_training=id_training,
        )
        if res is None:
            raise HTTPException(
                status_code=404, detail="No se encontró el entrenamiento con el id especificado"
            )
        return res
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/training-info")
async def get_training_info_actual(req: Request):
    if not auth_service.verify_credentials(req):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        signal_controller = SignalController(
            signal_repository=signal_repository,
            model_repository=model_repository,
        )
        model_controller = ModelController(
            signal_controller=signal_controller,
            model_repository=model_repository,
        )
        res = model_controller.get_training_info_actual()
        if res is None:
            raise HTTPException(status_code=404, detail="No se encontró ningún entrenamiento")
        return res
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/train-state")
def get_train_state(req: Request):
    if not auth_service.verify_credentials(req):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        signal_controller = SignalController(
            signal_repository=signal_repository,
            model_repository=model_repository,
        )
        return signal_controller.get_signals_with_unprocessed_images()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/actual-model")
def get_actual_model(req: Request):
    if not auth_service.verify_credentials(req):
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        signal_controller = SignalController(
            signal_repository=signal_repository,
            model_repository=model_repository,
        )
        model_controller = ModelController(
            signal_controller=signal_controller,
            model_repository=model_repository,
        )
        res = model_controller.get_actual_model()
        if res is None:
            raise HTTPException(status_code=404, detail="No se encontró ningún modelo entrenado")
        return res
    except HTTPException as error:
        raise error
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
