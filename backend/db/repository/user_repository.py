from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from auth.security import get_password_hash


class UserRepository:
    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """email로 사용자를 조회"""
        return db.query(User).filter(User.email == email).first()

    def create(selfself, db: Session, *, obj_in: UserCreate) -> User:
        """
        새로운 사용자를 생성합니다.
        비밀번호는 해시하여 저장합니다.
        """
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            nick_name=obj_in.nick_name,
            hashed_password=hashed_password,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user_repo = UserRepository()
