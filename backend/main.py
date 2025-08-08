from typing import Union
from routes import healthz
from fastapi import FastAPI

v1_app = FastAPI()
v1_app.include_router(healthz.router)

app = FastAPI()
app.mount("/v1", v1_app)