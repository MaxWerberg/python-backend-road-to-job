from fastapi import APIRouter, Depends

from dependencies.service_dependencies import get_user_service as serv_dep
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users(user_service: UserService = Depends(serv_dep)):
    return {"message": "UserService ok"}
