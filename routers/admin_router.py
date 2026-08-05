from fastapi import APIRouter, status

from dependencies.type_dependencies import AdminServiceDep, CurrentAdminDep
from schemas.admin_schema import GiveRoleSchema

router = APIRouter(prefix="/admin", tags=["Users"])


@router.patch("/users/role", status_code=status.HTTP_200_OK)
def change_role(
    user_role_update: GiveRoleSchema,
    admin_service: AdminServiceDep,
    current_user: CurrentAdminDep,
):

    return admin_service.give_role(
        user_id=user_role_update.user_id, role=user_role_update.role
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_admin(
    user_id: int,
    user_service: AdminServiceDep,
    current_user: CurrentAdminDep,
):
    user_service.delete_user(user_id=user_id)
