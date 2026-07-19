from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    """Схема регистрации пользователя"""

    username: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    """Схема ответа пользователю"""

    id: int
    username: str
    email: EmailStr


class UserPasswordChangeSchema(BaseModel):
    """Схема изменения пароля пользователя"""

    old_pass: str
    new_pass: str
