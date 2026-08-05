from datetime import datetime, timedelta, timezone

from jose import exceptions, jwt

from config.settings import settings
from exceptions.exceptions import InvalidTokenError, TokenExpiredError


class JWTService:
    def create_access_token(self, user_id: int) -> str:
        """Генерирует Access-Token"""

        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc)
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
            raise TokenExpiredError("Срок действия токена истек")

        except exceptions.JWTError:
            raise InvalidTokenError("Предоставлен недействительный токен")

        return check_token
