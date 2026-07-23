from repositories.user_repository import UserRepository


class AdminService:
    """Администрирование"""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def give_role_admin(self, user_id: int):
        """Дает пользователю роль admin"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if user.role != "admin":
            user.role = "admin"
            return self.repository.update(user)
        else:
            raise ValueError("Пользователь уже является 'admin'")

    def give_role_user(self, user_id: int):
        """Дает пользователю роль user"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        if user.role != "user":
            user.role = "user"
            return self.repository.update(user)
        else:
            raise ValueError("Пользователь уже является 'user'")
