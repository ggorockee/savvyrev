import enum
from sqlalchemy import Column, String, Boolean, Enum
from db.base import Base  # db/base.py에서 정의한 Base 클래스를 임포트


# is_superuser 컬럼에 들어갈 값을 'Y'와 'N'으로 제한하는 Enum
class UserRole(str, enum.Enum):
    ADMIN = "Y"
    USER = "N"


class User(Base):
    """
    사용자 정보
    """

    email = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, index=True, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(
        Enum(UserRole, native_enum=False),
        default=UserRole.USER,
        nullable=False,
        server_default=UserRole.USER,
    )
