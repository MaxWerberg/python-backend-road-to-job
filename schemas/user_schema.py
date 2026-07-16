from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    """Схема регистрации юзера"""

    username: str
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    """Схема ответа юзеру"""

    id: int
    username: str
    email: EmailStr
