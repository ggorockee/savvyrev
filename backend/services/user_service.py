from sqlalchemy.orm import Session

from auth.password import verify_password, get_password_hash
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

    def authenticate(self, db: Session, *, email: str, password: str) -> User | None:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def change_password(
        self, db: Session, *, user_obj: User, new_password: str
    ) -> None:
        """
        사용자의 비밀번호를 변경하고 DB에 저장합니다.
        "새로운 자물쇠로 교체해 드릴게요. 더 안전할 거예요!"
        """
        user_obj.hashed_password = get_password_hash(new_password)
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)


user_service = UserService()
