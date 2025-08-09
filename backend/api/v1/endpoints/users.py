from typing import Any

from fastapi import APIRouter, Response, Depends, HTTPException, status

from auth.password import verify_password
from auth.security import get_current_active_user
from schemas.user import UserCreate, UserResponse, PasswordChange

from models.user import User


from sqlalchemy.orm import Session
from db.session import get_db
from services import user_service

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


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: User = Depends(get_current_active_user),
) -> User:
    return current_user


@router.post("/me/change-password", status_code=status.HTTP_200_OK)
async def change_current_user_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    **현재 로그인된 사용자의 비밀번호를 변경합니다.**
    """
    # 현재 비밀번호가 맞는지 확인
    if not verify_password(
        password_data.current_password,
        current_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="앗! 현재 비밀번호가 일치하지 않아요. 다시 확인해주시겠어요?",
        )

    # 새 비밀번호로 변경
    user_service.change_password(
        db,
        user_obj=current_user,
        new_password=password_data.new_password,
    )

    return {
        "message": "비밀번호가 안전하게 변경되었습니다. 다음 로그인부터 새 비밀번호를 사용해주세요!"
    }
