from fastapi import FastAPI

from api.v1.router import api_router
from core.config import settings
# from logs import RichLoggingMiddleware
from prometheus_fastapi_instrumentator import Instrumentator


v1_app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/openapi.json",
)

v1_app.include_router(api_router)

app = FastAPI()
Instrumentator().instrument(app).expose(app)

app.mount("/v1", v1_app)
