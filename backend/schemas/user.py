from typing import Optional

from pydantic import BaseModel, EmailStr

from models.user import UserRole


class UserBase(BaseModel):
    """모든 User 스키마의 기본. 공통 필드를 정의."""

    email: EmailStr
    nick_name: str


class UserLogin(BaseModel):
    """login 스키마"""

    email: EmailStr
    password: str


class UserCreate(UserBase):
    """회원가입 시 받을 데이터. 비밀번호를 포함."""

    password: str
    admin_key: Optional[str] = None


class UserResponse(UserBase):
    """API 응답으로 보낼 데이터. 보안상 비밀번호는 제외."""

    id: int
    is_active: bool
    is_superuser: UserRole

    class Config:
        # SQLAlchemy 모델 객체를 Pydantic 모델로 자동 변환해주는 설정
        from_attributes = True


class PasswordChange(BaseModel):
    """비밀번호 변경 시 받을 데이터 스키마"""

    current_password: str
    new_password: str
