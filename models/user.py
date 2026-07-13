import bcrypt


class User:
    def __init__(self, id: int, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt)

    def check_password(self, password: str) -> bool:
        """Проверяет пароль"""
        return bcrypt.checkpw(password.encode(), self.password_hash)

    def update_profile_password(self, old_pass: str, new_pass: str) -> bool:
        """Заменяет старый пароль на новый"""
        if self.check_password(old_pass):
            salt = bcrypt.gensalt()
            self.password_hash = bcrypt.hashpw(new_pass.encode(), salt)
            return True
        else:
            return False

    def update_profile_username(self, new_username: str) -> None:
        """Заменяет старое имя на новое"""
        self.username = new_username

    def update_profile_email(self, new_email: str) -> None:
        """Заменяет старую почту на новую"""
        self.email = new_email
