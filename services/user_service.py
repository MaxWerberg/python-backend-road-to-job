import bcrypt

from models.user import User
from repositories.user_repository import UserRepository
from services.jwt_service import JWTService


class UserService:
    """Управляет бизнес-логикой работы с пользователями"""

    def __init__(self, repository: UserRepository, jwt_service: JWTService):
        self.repository = repository
        self.jwt_service = jwt_service

    def _hash_password(self, password: str) -> bytes:
        """Хэширует строку пароля с использованием соли"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt)

    def _verify_password(self, password: str, password_hash: bytes) -> bool:
        """Проверяет соответствие сырого пароля его хэшу"""
        return bcrypt.checkpw(password.encode(), password_hash)

    def registration(self, username: str, email: str, raw_password: str) -> User:
        """Регистрирует нового пользователя"""
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            raise ValueError(f"Пользователь c почтой {existing_user.email} существует")

        password_hash = self._hash_password(raw_password)
        user = User(username=username, email=email, password_hash=password_hash)
        created_user = self.repository.create(user)
        return created_user

    def get_user(self, user_id: int) -> User:
        """Ищет пользователя по ID"""
        user = self.repository.get_by_id(user_id)

        if not user:
            raise ValueError(f"Пользователь c ID {user_id} не найден")
        return user

    def change_password(self, user_id: int, old_pass: str, new_pass: str) -> User:
        """Изменяет текущий пароль пользователя на новый"""
        user = self.get_user(user_id)

        if not self._verify_password(old_pass, user.password_hash):
            raise ValueError("Неверный старый пароль")

        new_hash = self._hash_password(new_pass)
        user.update_password_hash(new_hash)

        return self.repository.update(user)

    def login_user(self, email: str, password: str) -> str:
        """Авторизует пользователя и возвращает Access Token"""
        user = self.repository.get_by_email(email)
        if not user:
            raise ValueError("Неверный email или пароль")

        if not self._verify_password(password, user.password_hash):
            raise ValueError("Неверный email или пароль")

        return self.jwt_service.create_access_token(user.id)

    def delete_user(self, user_id: int) -> bool:
        """Удаляет пользователя по его идентификатору"""
        is_delete = self.repository.delete(user_id)
        if not is_delete:
            raise ValueError(f"Пользователь c ID {user_id} не найден")
        return is_delete
