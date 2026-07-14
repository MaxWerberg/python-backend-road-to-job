from sqlalchemy import select
from sqlalchemy.orm import Session

from models.user import User


class UserRepository:
    """Управляет сохранением и извлечением данных пользователей в базе данных"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        """Создает нового пользователя в базе данных"""
        self.db.add(user)
        self.db.flush()
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """Ищет пользователя в базе данных по его ID"""
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Ищет пользователя в базе данных по его электронной почте"""
        query = select(User).where(User.email == email)
        return self.db.execute(query).scalar_one_or_none()

    def update(self, updated_user: User) -> User:
        """Фиксирует изменения данных пользователя в текущей сессии"""
        self.db.flush()
        return updated_user

    def delete(self, user_id: int) -> bool:
        """Удаляет пользователя из базы данных по его ID"""
        user = self.db.get(User, user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.flush()
        return True
