from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from dependencies.db_dependencies import get_user_repository
from models.user import User
from repositories.user_repository import UserRepository
from services.jwt_service import JWTService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:

    payload = JWTService().verify_access_token(token)
    user_id = int(payload["sub"])
    user = user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
        )
    return user
