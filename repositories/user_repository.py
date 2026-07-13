from models.user import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    def create(self, user: User) -> User:
        """Создает юзера"""
        return

    def get_by_id(self, user_id: int) -> User | None:
        """Поиск юзера по ID"""
        return

    def get_by_email(self, email: str) -> User | None:
        """Поиск юзера по EMAIL"""
        return

    def update(self, user: User) -> User:
        """Сохраняет изменения юзера в базу данных"""
        return

    def delete(self, user_id: int) -> bool:
        """Удаляет юзера по ID"""
        return
