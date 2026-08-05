from fastapi import APIRouter, Response, status

from dependencies.type_dependencies import CartItemServiceDep, CurrentUserDep
from schemas.cart_schema import (
    CartAddItemSchema,
    CartDeleteItemSchema,
    CartResponseSchema,
)

router = APIRouter(prefix="/cart", tags=["Carts"])


@router.get(path="", response_model=CartResponseSchema)
def get_user_cart(current_user: CurrentUserDep, cart_item_service: CartItemServiceDep):

    return cart_item_service.get_cart(current_user_id=current_user.id)


@router.post(path="/items", response_model=CartAddItemSchema)
def add_product_to_cart(
    current_user: CurrentUserDep,
    cart_item_service: CartItemServiceDep,
    product: CartAddItemSchema,
):

    return cart_item_service.add_to_cart(
        current_user_id=current_user.id,
        product_id=product.product_id,
        quantity=product.quantity,
    )


@router.patch(path="/items", response_model=CartAddItemSchema)
def change_quantity_product(
    current_user: CurrentUserDep,
    cart_item_service: CartItemServiceDep,
    product: CartAddItemSchema,
):

    return cart_item_service.change_quantity(
        current_user_id=current_user.id,
        product_id=product.product_id,
        new_quantity=product.quantity,
    )


@router.delete(path="/items")
def delete_from_cart(
    current_user: CurrentUserDep,
    cart_item_service: CartItemServiceDep,
    product: CartDeleteItemSchema,
):

    cart_item_service.remove_from_cart(
        current_user_id=current_user.id, product_id=product.product_id
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
