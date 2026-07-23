from sqlalchemy import Column, Integer, LargeBinary, String

from database.database import Base


class User(Base):
    """Описывает модель пользователя и его личные данные"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(LargeBinary, nullable=False)
    role = Column(String, default="user", nullable=False)

    def update_password_hash(self, new_hash: bytes) -> None:
        """Обновляет хэш пароля пользователя"""
        self.password_hash = new_hash

    def update_profile_username(self, new_username: str) -> None:
        """Обновляет имя пользователя"""
        self.username = new_username

    def update_profile_email(self, new_email: str) -> None:
        """Обновляет email пользователя"""
        self.email = new_email
