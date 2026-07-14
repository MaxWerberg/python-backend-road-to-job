from sqlalchemy import Column, Integer, LargeBinary, String

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(LargeBinary, nullable=False)

    def update_password_hash(self, new_hash: bytes) -> None:
        self.password_hash = new_hash

    def update_profile_username(self, new_username: str) -> None:
        """Заменяет старое имя на новое"""
        self.username = new_username

    def update_profile_email(self, new_email: str) -> None:
        """Заменяет старую почту на новую"""
        self.email = new_email
