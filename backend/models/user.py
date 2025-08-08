from sqlalchemy import Column, String, Boolean
from db.base import Base  # db/base.py에서 정의한 Base 클래스를 임포트


class User(Base):
    """
    사용자 정보
    """

    email = Column(String, unique=True, index=True, nullable=False)
    nick_name = Column(String, index=True, unique=True)
    is_active = Column(Boolean(), default=True)
    hashed_password = Column(String, nullable=False)
