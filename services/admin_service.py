from exceptions.exceptions import (
    RoleAlreadyAssignedError,
    UserNotFoundError,
)
from models.user import User
from repositories.user_repository import UserRepository


class AdminService:
    """Администрирование"""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: int) -> User:
        """Получение пользователя"""

        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("Пользователь не найден")
        return user

    def give_role(self, user_id: int, role: str) -> None:
        """Меняет пользователю роль"""

        user = self.get_user(user_id)
        if user.role == role:
            raise RoleAlreadyAssignedError(f"Пользователь уже является {role}")
        else:
            user.role = role

        self.repository.update(user)
