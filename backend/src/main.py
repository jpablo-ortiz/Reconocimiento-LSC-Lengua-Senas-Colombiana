import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# -------------------------------------------------
# -------------- API INICIALIZATION ---------------
# -------------------------------------------------

app = FastAPI()

# ================= Routers and configs =================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= Main =================

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, debug=True, reload=True)
