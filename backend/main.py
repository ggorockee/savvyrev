from fastapi import FastAPI

from api.v1.router import api_router
from core.config import settings
from logs import RichLoggingMiddleware


v1_app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/openapi.json",
)

v1_app.include_router(api_router)

app = FastAPI()

app.add_middleware(RichLoggingMiddleware)
app.mount("/v1", v1_app)
