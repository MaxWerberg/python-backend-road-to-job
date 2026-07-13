class User:
    def __init__(self, id: int, username: str, email: str, password_hash: bytes):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def update_password_hash(self, new_hash: bytes) -> None:
        self.password_hash = new_hash

    def update_profile_username(self, new_username: str) -> None:
        """Заменяет старое имя на новое"""
        self.username = new_username

    def update_profile_email(self, new_email: str) -> None:
        """Заменяет старую почту на новую"""
        self.email = new_email
