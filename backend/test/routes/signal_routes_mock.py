from fastapi import APIRouter, HTTPException, Request

from models import RequestSignal

fake_secret_token = "secret"

mock_db = {"1": RequestSignal(name="name1", images=["images1"])}

router = APIRouter()


@router.post("/new-signal")
async def save_signal(signal: RequestSignal, req: Request):
    if req.headers["Authorization"] != fake_secret_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if signal.name == "":
        raise HTTPException(status_code=422, detail="El nombre de la señal está vacío")
    mock_db["2"] = signal
    return {"message": "Señal creada correctamente", "result": signal}


# the signal - la señal
