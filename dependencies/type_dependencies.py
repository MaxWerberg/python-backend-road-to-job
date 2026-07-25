from typing import Annotated

from fastapi import Depends

from dependencies.auth_dependencies import get_current_user, require_admin
from dependencies.service_dependencies import (
    get_admin_service,
    get_product_service,
    get_user_service,
)
from models.user import User
from services.admin_service import AdminService
from services.product_service import ProductService
from services.user_service import UserService

AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

ProductServiceDep = Annotated[ProductService, Depends(get_product_service)]

CurrentUserDep = Annotated[User, Depends(get_current_user)]

CurrentAdminDep = Annotated[User, Depends(require_admin)]
