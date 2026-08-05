from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from exceptions.exceptions import (
    CartNotFoundError,
    InvalidCredentialsError,
    InvalidPasswordError,
    InvalidPriceError,
    InvalidQuantityError,
    InvalidTokenError,
    ItemNotInCartError,
    NotAnAdminError,
    OutOfStockError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    RoleAlreadyAssignedError,
    TokenExpiredError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


def register_error_handlers(app: FastAPI) -> None:
    """Регистрирует все глобальные обработчики ошибок в приложении."""

    # 422 Unprocessable Content
    @app.exception_handler(RoleAlreadyAssignedError)
    def unprocessable_content_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": str(exc)},
        )

    # 409 Conflict
    @app.exception_handler(ProductAlreadyExistsError)
    @app.exception_handler(UserAlreadyExistsError)
    def conflict_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    # 403 Forbidden
    @app.exception_handler(NotAnAdminError)
    def forbidden_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
        )

    # 404 Not Found
    @app.exception_handler(CartNotFoundError)
    @app.exception_handler(ProductNotFoundError)
    @app.exception_handler(ItemNotInCartError)
    @app.exception_handler(UserNotFoundError)
    def not_found_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    # 401 Unauthorized
    @app.exception_handler(TokenExpiredError)
    @app.exception_handler(InvalidTokenError)
    @app.exception_handler(InvalidCredentialsError)
    def unauthorized_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    # 400 Bad Request
    @app.exception_handler(InvalidPriceError)
    @app.exception_handler(InvalidQuantityError)
    @app.exception_handler(OutOfStockError)
    @app.exception_handler(InvalidPasswordError)
    def bad_request_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )
