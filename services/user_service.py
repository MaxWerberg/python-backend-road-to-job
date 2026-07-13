import bcrypt

from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def _hash_password(self, password: str) -> bytes:
        """Внутренний метод, создает хэщ"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def _verify_password(self, password: str, password_hash: bytes) -> bool:
        """Внутренний метод, проверяет хэш"""
        return bcrypt.checkpw(password.encode(), password_hash)

    def registration(
        self, id: int, username: str, email: str, raw_password: str
    ) -> User:
        """Регистрация пользователя"""
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            raise ValueError("Пользователь существует")

        password_hash = self._hash_password(raw_password)
        user = User(id=id, username=username, email=email, password_hash=password_hash)
        created_user = self.repository.create(user)
        return created_user

    def change_password(self, user_id: int, old_pass: str, new_pass: str) -> User:
        """Изменение пароля пользователя"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if not self._verify_password(old_pass, user.password_hash):
            raise ValueError("Неверный старый пароль")

        new_hash = self._hash_password(new_pass)
        user.update_password_hash(new_hash)

        return self.repository.update(user)

    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        is_delete = self.repository.delete(user_id)
        if not is_delete:
            raise ValueError("Пользователь не найден")
        return is_delete
