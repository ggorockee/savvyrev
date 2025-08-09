from fastapi import APIRouter
from api.v1.endpoints import healthz, users, auth

api_router = APIRouter()

# endpoint 라우터 병합
api_router.include_router(
    healthz.router,
    prefix="/healthz",
    tags=["Health Check"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["User"],
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
