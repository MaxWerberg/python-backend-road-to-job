from models.user import User


class UserRepository:
    def __init__(self):
        self.db = []

    def create(self, user: User) -> User:
        """Создает юзера"""
        self.db.append(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """Поиск юзера по ID"""
        for user in self.db:
            if user.id == user_id:
                return user
        return None

    def get_by_email(self, email: str) -> User | None:
        """Поиск юзера по EMAIL"""
        for user in self.db:
            if user.email == email:
                return user
        return None

    def update(self, updated_user: User) -> User | None:
        """Сохраняет изменения юзера в базу данных"""
        for index, existing_user in enumerate(self.db):
            if existing_user.id == updated_user.id:
                self.db[index] = updated_user
                return updated_user
        return None

    def delete(self, user_id: int) -> bool:
        """Удаляет юзера по ID"""
        for user in self.db:
            if user.id == user_id:
                self.db.remove(user)
                return True
        return False
