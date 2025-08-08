from fastapi import APIRouter, status, Response

router = APIRouter()


@router.get("/ready")
async def healthz():
    return Response(status_code=status.HTTP_200_OK)
