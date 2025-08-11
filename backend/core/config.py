import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()


class Settings(BaseSettings):
    """
    애플리케이션 설정을 관리하는 클래스.
    K8S Secret이나 .env 파일에서 환경 변수를 읽어옴.
    """

    PROJECT_NAME: str = "SavvyReview APP"
    API_V1_STR: str = "/v1"

    # 데이터베이스 설정
    # DATABASE_URL: str = "postgresql://user:password@host:port/db"
    POSTGRES_USER: str = os.getenv(
        "POSTGRES_USER",
        "default_user",
    )
    POSTGRES_PASSWORD: str = os.getenv(
        "POSTGRES_PASSWORD",
        "default_password",
    )
    POSTGRES_SERVER: str = os.getenv(
        "POSTGRES_SERVER",
        "localhost",
    )
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT",
        "5432",
    )
    POSTGRES_DB: str = os.getenv(
        "POSTGRES_DB",
        "app",
    )
    DATABASE_URL: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # FASTAPI 설정
    # SECRET_KEY: str = os.getenv(
    #     "SECRET_KEY",
    #     "a_very_secret_key_that_should_be_changed",
    # )
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    TIMEZONE: str = "Asia/Seoul"

    ADMIN_KEY: str = os.getenv("ADMIN_KEY", "default_admin_key")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv(
        "JWT_REFRESH_SECRET_KEY", "JWT_REFRESH_SECRET_KEY"
    )

    REFRESH_TOKEN_EXPIRE_MINUTES: str = os.getenv(
        "REFRESH_TOKEN_EXPIRE_MINUTES", "10080"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    class Config:
        case_sensitive = True


settings = Settings()
