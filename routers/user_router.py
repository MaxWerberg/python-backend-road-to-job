from typing import Annotated

from fastapi import APIRouter, Depends

from dependencies.auth_dependencies import get_current_user
from dependencies.service_dependencies import get_user_service as serv_user_dep
from models.user import User
from schemas.auth_schema import LoginSchema, TokenSchema
from schemas.user_schema import (
    UserPasswordChangeSchema,
    UserRegisterSchema,
    UserResponseSchema,
)
from services.user_service import UserService

user_router = APIRouter(prefix="/users", tags=["Users"])
UserServiceDep = Annotated[UserService, Depends(serv_user_dep)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@user_router.get("/my_account", response_model=UserResponseSchema)
def get_current_user_info(
    current_user: CurrentUserDep,
):
    return current_user


@user_router.patch("/my_account/password")
def refresh_password_user(
    user_data: UserPasswordChangeSchema,
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
):

    user_service.change_password(
        user_id=current_user.id,
        old_pass=user_data.old_pass,
        new_pass=user_data.new_pass,
    )
    return {"message": "Пароль успешно изменён"}


@user_router.delete("/my_account")
def delete_user(
    user_service: UserServiceDep,
    current_user: CurrentUserDep,
):

    user_service.delete_user(
        user_id=current_user.id,
    )
    return {"message": "Аккаунт удален"}


@user_router.post("/register", response_model=UserResponseSchema)
def register_user(user_data: UserRegisterSchema, user_service: UserServiceDep):

    return user_service.registration(
        username=user_data.username,
        email=user_data.email,
        raw_password=user_data.password,
    )


@user_router.post("/login", response_model=TokenSchema)
def login_user(user_data: LoginSchema, user_service: UserServiceDep):

    access_token = user_service.login_user(
        email=user_data.email, password=user_data.password
    )
    return {"access_token": access_token, "token_type": "bearer"}
