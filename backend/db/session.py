from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# 데이터베이스 엔진 생성
# 이 엔진은 프로젝트 전체에서 단 하나만 존재해야 함
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)


# 세션 생성기
# API 요청이 들어올 때마다 이 생성기를 통해 DB 세션을 만듬
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    API 요청 처리 중에 사용할 데이터베이스 세션을 제공하는 의존성 함수.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
