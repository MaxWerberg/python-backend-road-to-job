from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def registration(self, user: User) -> User:
        """Регистрация пользователя"""
        existing_user = self.repository.get_by_email(user.email)

        if existing_user:
            raise ValueError("Пользователь существует")

        created_user = self.repository.create(user)
        return created_user

    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        is_delete = self.repository.delete(user_id)
        if not is_delete:
            raise ValueError("Пользователь не найден")
        return is_delete

    def change_password(self, user_id: int, old_pass: str, new_pass: str) -> User:
        """Изменение пароля пользователя"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        is_password_updated = user.update_profile_password(old_pass, new_pass)
        if not is_password_updated:
            raise ValueError("Неверный старый пароль")

        return self.repository.update(user)
