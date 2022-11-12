import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routes import signal_routes, train_routes, user_routes

# -------------------------------------------------
# -------------- API INICIALIZATION ---------------
# -------------------------------------------------

app = FastAPI()

# ================= Routers and configs =================

app.include_router(signal_routes.router)
app.include_router(train_routes.router)
app.include_router(user_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= Main =================

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, debug=True, reload=True)
