from datetime import timedelta, datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

from jose import jwt
from core.config import settings

ALGORITHM = "HS256"


def create_access_token(
    subject: str | Any,
    expires_delta: timedelta | None = None,
) -> str:
    """
    JWT 액세스 토큰을 생성합니다.
    마치 놀이공원 자유이용권처럼, 정해진 시간 동안만 유효해요!
    - subject: 토큰에 담을 주체 (보통 사용자 ID나 이메일)
    """
    seoul_tz = ZoneInfo(settings.TIMEZONE)
    if expires_delta:
        expire = datetime.now(seoul_tz) + expires_delta
    else:
        expire = datetime.now(seoul_tz) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt
