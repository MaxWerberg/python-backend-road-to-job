from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import exceptions, jwt

from config.settings import settings


class JWTService:
    def create_access_token(self, user_id: int) -> str:
        """Генерирует Access-Token"""

        payload = {
            "sub": str(user_id),
            "exp": datetime.now()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        }

        token = jwt.encode(
            payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return token

    def verify_access_token(self, token: str) -> dict:

        try:
            check_token = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )

        except exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Время токена истекло"
            )
        except exceptions.JWEError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен"
            )

        return check_token
