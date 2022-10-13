import json

from controllers.model_controller import ModelController
from controllers.signal_controller import SignalController
from fastapi import APIRouter, HTTPException, Security, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.coord_signal import CoordSignal
from models.signal import Signal
from repositories.callback_repository import CallbackRepositoryNoSQL, CallbackRepositoryTinyDB
from repositories.signal_repository import SignalRepositoryNoSQL, SignalRepositoryTinyDB
from services.auth_service import AuthService

# -------------------------------------------------
# ------------- Inicialzando el router ------------
# -------------------------------------------------

router = APIRouter()

security = HTTPBearer()
auth_handler = AuthService()

# signal_repository = SignalRepositoryNoSQL()
signal_repository = SignalRepositoryTinyDB()

# model_repository = CallbackRepositoryNoSQL()
model_repository = CallbackRepositoryTinyDB()

# -------------------------------------------------
# --------------- SERVICIOS REST ------------------
# -------------------------------------------------


@router.get("/")
def home():
    return {"message": "Conectado con éxito"}


@router.get("/train")
def train_model(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        if not verify_credentials(credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")

        model_controller = ModelController(model_repository)
        signal_controller = SignalController(signal_repository)

        signals_with_unprocessed_images = signal_controller.get_signals_with_unprocessed_images()

        if len(signals_with_unprocessed_images) > 0:
            model_controller.process_images_not_processed()
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Error al procesar las imágenes que no habían sido procesadas: " + str(error),
        ) from error

    try:
        model_controller.train_model()
        return {"message": "Inicio de entrenamiento exitoso"}
    except Exception as error:
        raise HTTPException(
            status_code=500, detail="Error al iniciar el entrenamiento: " + str(error)
        ) from error


@router.get("/training-info")
def get_training_info(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        if not verify_credentials(credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")

        model_controller = ModelController(model_repository)
        return model_controller.get_training_info()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.get("/train-state")
def get_train_state(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        if not verify_credentials(credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")

        signal_controller = SignalController(signal_repository)
        return signal_controller.get_signals_with_unprocessed_images()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/new-signal")
def save_signal(signal: Signal, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        if not verify_credentials(credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")

        signal_controller = SignalController(signal_repository)

        result = signal_controller.create_signal(signal)
        return {"message": "La seña se ha guardado exitosamente", "result": result}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.websocket("/predict-signal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    signal_controller = SignalController(signal_repository)
    try:
        while True:
            # Recieve data and transform it to CoordSignal
            data = await websocket.receive_json()
            coord_signal = CoordSignal(**data)

            prediction = signal_controller.predict_signal(coord_signal)

            await websocket.send_json(json.dumps(prediction))
            del coord_signal
    except Exception as error:
        print("Conexión cerrada: " + str(error))


# -------------------------------------------------
# --------------- EXTRA FUNCTIONS -----------------
# -------------------------------------------------


def verify_credentials(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    auth_handler.decode_token(token)
