from fastapi import APIRouter, Response, Depends, HTTPException, status
from services import user_service

from schemas import UserCreate, UserResponse
from models.user import User


from sqlalchemy.orm import Session
from db.session import get_db

# http://localhost:8000/v1/users
router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> User:
    """
    **회원가입 API**

    새로운 사용자를 시스템에 등록.
    - `email`: 사용자 이메일 (ID로 사용)
    - `password`: 비밀번호
    - `nick_name`: 닉네임
    """
    user = user_service.get_by_email(
        db,
        email=user_in.email,
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이런, 이 이메일은 이미 우리 동료다!!. 다른 이메일로 가입해주세요.",
        )

    user = user_service.create(db, obj_in=user_in)
    return user
