from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from auth.jwt import ALGORITHM
from core import settings
from db import get_db
from models.user import User
from schemas.token import TokenData

from services import user_service

# 비밀번호 해싱을 위한 컨텍스트 설정. bcrypt 알고리즘 사용
pwd_context = CryptContext(schemes=["bcrypt"])
bearer_scheme = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="음... 이 암호는 우리와 맞지 않네요. 👽",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = user_service.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="헛... 비활성화된 계정이네요. 👽",
        )
    return current_user
