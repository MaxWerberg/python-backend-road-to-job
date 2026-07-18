from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    """Схема авторизации пользователя"""

    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    """Схема токена пользователя"""

    access_token: str
    token_type: str
