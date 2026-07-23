from typing import Literal

from pydantic import BaseModel, EmailStr


class AdminGetUserSchema(BaseModel):
    """Схема ответа админу"""

    id: int
    username: str
    email: EmailStr
    role: str


class GiveRoleSchema(BaseModel):
    """Схема изменения роли"""

    user_id: int
    role: Literal["user", "admin"]
