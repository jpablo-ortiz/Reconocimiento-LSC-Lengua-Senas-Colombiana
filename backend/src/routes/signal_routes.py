import json

from fastapi import APIRouter, HTTPException, Request, WebSocket

from controllers.signal_controller import SignalController
from models.coord_signal import CoordSignal
from models.signal import RequestSignal
from repositories.model_repository import ModelRepositoryTinyDB
from repositories.signal_repository import SignalRepositoryTinyDB
from utils.auth.auth_service import AuthService
from settings import PATH_RAW_SIGNS

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


@router.post("/new-signal")
def save_signal(signal: RequestSignal, req: Request):
    if not auth_service.verify_credentials(req):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if signal.name == "":
        raise HTTPException(status_code=422, detail="El nombre de la señal está vacío")
    try:
        signal_controller = SignalController(
            signal_repository=signal_repository,
            model_repository=model_repository,
        )
        result = signal_controller.create_signal(signal)
        return {"message": "Señal creada correctamente", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/predict-signal")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    signal_controller = SignalController(
        signal_repository=signal_repository,
        model_repository=model_repository,
    )
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
