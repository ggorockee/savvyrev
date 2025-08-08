from fastapi import APIRouter, status, Response

router = APIRouter(prefix="/v1", tags=['Health Check'])

@router.get("/healthz/ready")
async def healthz():
    return Response(status_code=status.HTTP_200_OK)