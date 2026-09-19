from fastapi import APIRouter, Response, status

from dependencies.type_dependencies import AddressServiceDep, CurrentUserDep
from schemas.address_schema import (
    AddressAddSchema,
    AddressIdSchema,
    AddressResponseSchema,
)

address_router = APIRouter(prefix="/address", tags=["Addresses"])


@address_router.post("/add", response_model=AddressResponseSchema)
def add_address(
    new_address: AddressAddSchema,
    address_service: AddressServiceDep,
    current_user: CurrentUserDep,
):
    return address_service.create(
        current_user_id=current_user.id,
        country=new_address.country,
        city=new_address.city,
        street=new_address.street,
        house=new_address.house,
        apartment=new_address.apartment,
        is_default=new_address.is_default,
    )


@address_router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: AddressIdSchema,
    address_service: AddressServiceDep,
    current_user: CurrentUserDep,
):
    address_service.delete(user_id=current_user.id, address_id=address_id.address_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
