from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    클라이언트에 전달할 Access token Schema
    """

    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """
    토큰 내부의 데이터를 위한 스키마 (페이로드)
    """

    email: Optional[str] = None


class TokenRefreshRequest(BaseModel):
    refresh_token: str
