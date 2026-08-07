from fastapi import APIRouter, Depends, status

from dependencies.auth_dependencies import require_admin
from dependencies.type_dependencies import (
    AdminServiceDep,
    UserServiceDep,
)
from schemas.admin_schema import GiveRoleSchema

admin_router = APIRouter(
    prefix="/admin", tags=["Users"], dependencies=[Depends(require_admin)]
)


@admin_router.patch("/users/role", status_code=status.HTTP_200_OK)
def change_role(
    user_role_update: GiveRoleSchema,
    admin_service: AdminServiceDep,
):

    return admin_service.give_role(
        user_id=user_role_update.user_id, role=user_role_update.role
    )


@admin_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_admin(
    user_id: int,
    user_service: UserServiceDep,
):
    user_service.delete_user(user_id=user_id)
