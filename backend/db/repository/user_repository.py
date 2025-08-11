from sqlalchemy.orm import Session
from models.user import User, UserRole
from schemas.user import UserCreate
from auth.password import get_password_hash  # <<< 여기서 임포트
from core.config import settings


class UserRepository:
    def get_user_by_id(self, *, db: Session, id: int, **kwargs) -> User | None:
        """id로 사용자를 조회"""
        return db.query(User).filter(User.id == id).first()

    def get_user_by_email(self, db: Session, *, email: str) -> User | None:
        """email로 사용자를 조회"""
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        새로운 사용자를 생성합니다.
        만약 admin_key가 유효하면, 관리자(is_superuser='Y')로 생성합니다.
        """
        hashed_password = get_password_hash(obj_in.password)

        # 관리자 키가 일치하는지 확인
        is_superuser_flag = UserRole.USER

        if obj_in.admin_key and obj_in.admin_key == settings.ADMIN_KEY:
            print("✨ 관리자 키가 확인되었습니다. 슈퍼파워를 부여합니다! ✨")
            is_superuser_flag = UserRole.ADMIN

        db_obj = User(
            email=obj_in.email,
            nick_name=obj_in.nick_name,
            hashed_password=hashed_password,
            is_superuser=is_superuser_flag,  # 플래그에 따라 'Y' 또는 'N' 저장
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user_repo = UserRepository()
