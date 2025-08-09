from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.jwt import create_access_token
from auth.security import get_current_active_user
from db import get_db
from schemas.token import Token
from schemas.user import UserLogin

from services import user_service

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(
    user_credentials: UserLogin,
    db: Session = Depends(get_db),
) -> Any:
    """
    **로그인 및 JWT 액세스 토큰 발급 API**

    이제 Request body에 간단한 JSON 형식으로 이메일과 비밀번호를 보내주세요.
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```
    """
    user = user_service.authenticate(
        db,
        email=user_credentials.email,
        password=user_credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일이나 비밀번호가 틀렸어요. ㅠㅠ",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    # 이 엔드포인트는 토큰이 유효한지 검사하는 것만으로도 충분합니다.
    # 실제 로그아웃 로직은 클라이언트에서 토큰을 삭제하는 것입니다.
    current_user: str = Depends(get_current_active_user),
):
    """
    **로그아웃**

    서버는 특별한 작업을 수행하지 않습니다.
    클라이언트 측에서 저장된 JWT를 삭제하여 로그아웃을 완료하세요.

    (참고: 더 높은 보안을 위해 서버 측에 토큰 블랙리스트를 구현할 수도 있습니다.)
    """
    return {"message": "성공적으로 로그아웃되었습니다. 안녕히 가세요! 👋"}
