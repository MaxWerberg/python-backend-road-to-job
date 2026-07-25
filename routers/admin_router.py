from fastapi import APIRouter, HTTPException, status

from dependencies.type_dependencies import AdminServiceDep, CurrentAdminDep
from schemas.admin_schema import GiveRoleSchema

router = APIRouter(prefix="/admin", tags=["Users"])


@router.patch("/users/role", status_code=status.HTTP_200_OK)
def change_role(
    changes: GiveRoleSchema,
    admin_service: AdminServiceDep,
    current_user: CurrentAdminDep,
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуется роль администратора",
        )

    try:
        if changes.role == "admin":
            admin_service.give_role_admin(user_id=changes.user_id)
        elif changes.role == "user":
            admin_service.give_role_user(user_id=changes.user_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_admin(
    user_id: int,
    user_service: AdminServiceDep,
    current_user: CurrentAdminDep,
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Требуется роль администратора",
        )

    try:
        user_service.delete_user(user_id=user_id)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)
        )
