from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Создает юзера"""
        self.db.add(user)
        self.db.flush()
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """Поиск юзера по ID"""
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Поиск юзера по EMAIL"""
        query = select(User).where(User.email == email)
        return self.db.execute(query).scalar_one_or_none()

    def update(self, updated_user: User) -> User | None:
        """Сохраняет изменения юзера в базу данных"""
        self.db.flush()
        return updated_user

    def delete(self, user_id: int) -> bool:
        """Удаляет юзера по ID"""
        user = self.db.get(User, user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.flush()
        return True
