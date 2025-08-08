from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import as_declarative, declared_attr
from sqlalchemy.sql import func


@as_declarative()
class Base:
    """
    모든 SQLAlchemy 모델의 기반이 되는 클래스.
    """

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    # 테이블 이름을 클래스 이름의 소문자 버전으로 자동 설정
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
