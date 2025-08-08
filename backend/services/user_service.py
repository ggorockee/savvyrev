from sqlalchemy.orm import Session
from db.repository.user_repository import user_repo
from schemas.user import UserCreate
from models.user import User


class UserService:
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스.
    """

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        return user_repo.get_by_email(db, email=email)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        return user_repo.create(db, obj_in=obj_in)


user_service = UserService()
