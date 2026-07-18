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
