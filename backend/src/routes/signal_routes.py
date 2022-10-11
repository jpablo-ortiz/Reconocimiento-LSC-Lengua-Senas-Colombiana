import json

from controllers.signal_controller import SignalController
from fastapi import APIRouter, HTTPException, Security, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models.coord_signal import CoordSignal
from models.signal import Signal
from repositories.signal_repository import (SignalRepositoryNoSQL,
                                            SignalRepositoryTinyDB)
from services.auth_service import AuthService

# -------------------------------------------------
# ------------- Inicialzando el router ------------
# -------------------------------------------------

router = APIRouter()

security = HTTPBearer()
auth_handler = AuthService()

# signal_repository = SignalRepositoryNoSQL()
signal_repository = SignalRepositoryTinyDB()

# -------------------------------------------------
# --------------- SERVICIOS REST ------------------
# -------------------------------------------------


@router.get("/")
def home():
    return {"message": "Conectado con éxito"}


@router.post("/new-signal")
def save_signal(signal: Signal, credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        if not verify_credentials(credentials):
            raise HTTPException(status_code=401, detail="Unauthorized")

        signal_controller = SignalController(signal_repository)
        result = signal_controller.create_signal(signal)
        signal_controller.save_image_on_disk(signal)
        return {"message": "Signal created successfully", "result": result}
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
