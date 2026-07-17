from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.service_dependencies import get_user_service as serv_user_dep
from schemas.user_schema import UserRegisterSchema, UserResponseSchema
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, user_service: UserService = Depends(serv_user_dep)):
    try:
        return user_service.get_user(user_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("/register", response_model=UserResponseSchema)
def register_user(
    user_data: UserRegisterSchema, user_service: UserService = Depends(serv_user_dep)
):

    try:
        return user_service.registration(
            username=user_data.username,
            email=user_data.email,
            raw_password=user_data.password,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))
