from typing import Union
from routes import healthz
from fastapi import FastAPI

app = FastAPI()
app.include_router(healthz.router)