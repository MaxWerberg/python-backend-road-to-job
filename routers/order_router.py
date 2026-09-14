from fastapi import APIRouter

from dependencies.type_dependencies import CurrentUserDep, OrderServiceDep
from schemas.order_schema import OrderCreateSchema

order_router = APIRouter(prefix="/order", tags=["Orders"])


@order_router.post(path="")
def create_order(
    current_user: CurrentUserDep,
    order_service: OrderServiceDep,
    user_data: OrderCreateSchema,
):

    return order_service.create(
        current_user_id=current_user.id,
        recipient_name=user_data.recipient_name,
        recipient_phone=user_data.recipient_phone,
    )
