from typing import Any

from fastapi import APIRouter, Response, Depends, HTTPException, status

from auth.password import verify_password
from auth.security import get_current_active_user
from schemas.user import UserCreate, UserResponse, PasswordChange, UserDelete

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
    user = user_service.get_user_by_email(
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


@router.post("/delete", status_code=status.HTTP_200_OK)
async def delete_user(
    *,
    db: Session = Depends(get_db),
    user_to_delete: UserDelete,
    current_user: User = Depends(get_current_active_user),
):
    """
    사용자를 삭제합니다. 관리자('is_superuser' == 'Y')만 이 API를 호출할 수 있습니다.

    - **user_to_delete**: 삭제할 사용자의 ID를 포함하는 요청 본문.
    - **current_user**: API를 호출하는 현재 인증된 사용자.
    """
    if not current_user or current_user.is_superuser != "Y":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="오직 관리자만 사용할 수 있는 기능이에요! (´•̥ω•̥`)",
        )

    # user_id로 삭제할 사용자 조회
    user = user_service.get_user_by_id(id=current_user.id)

    # 삭제할 사용자가 DB에 없는 경우
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="앗, 찾으시는 사용자가 존재하지 않아요. ( •́ ̯•̀ )",
        )
    
    # 자기 자신을 삭제하려는 경우 (선택적)
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자기 자신은 삭제할 수 없어요! Σ(°Д°)",
        )

     # 3. 사용자 삭제
    db.delete(user)
    db.commit()

    return {
        "message": f"사용자 ID {user_to_delete.user_id} 님의 정보가 안전하게 삭제되었어요. ✨",
        }

