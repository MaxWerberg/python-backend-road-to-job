from exceptions.exceptions import (
    CartNotFoundError,
    InvalidQuantityError,
    ItemNotInCartError,
)
from models.cart import Cart
from models.cart_item import CartItem
from repositories.cart_item_repository import CartItemRepository
from repositories.cart_repository import CartRepository


class CartItemService:
    def __init__(
        self,
        cart_item_repository: CartItemRepository,
        cart_repository: CartRepository,
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository

    def get_cart(self, current_user_id: int) -> Cart:
        cart = self.cart_repository.get_by_current_user_id(current_user_id)
        if not cart:
            raise CartNotFoundError("Корзина пользователя не найдена")
        return cart

    def add_to_cart(
        self, current_user_id: int, product_id: int, quantity: int
    ) -> CartItem:
        cart = self.get_cart(current_user_id)
        check_item = self.cart_item_repository.get_item(cart.id, product_id)

        if quantity < 0:
            raise InvalidQuantityError("Значение не может быть отрицательным")
        if not check_item:
            new_item = CartItem(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )

            return self.cart_item_repository.create(new_item)

        check_item.quantity += quantity
        return self.cart_item_repository.update(check_item)

    def change_quantity(
        self, current_user_id: int, product_id: int, new_quantity: int
    ) -> CartItem | None:

        cart = self.get_cart(current_user_id)
        check_item = self.cart_item_repository.get_item(cart.id, product_id)

        if not check_item:
            raise ItemNotInCartError("Товар отсутствует в корзине")

        check_item.quantity = max(0, check_item.quantity + new_quantity)

        if check_item.quantity == 0:
            self.cart_item_repository.delete(check_item.cart_id, check_item.product_id)
            return None

        return self.cart_item_repository.update(check_item)

    def remove_from_cart(self, current_user_id: int, product_id: int) -> None:
        cart = self.get_cart(current_user_id)
        item_for_delete = self.cart_item_repository.get_item(cart.id, product_id)

        if not item_for_delete:
            raise ItemNotInCartError("Товар отсутствует в корзине")

        self.cart_item_repository.delete(cart.id, product_id)

    def delete_cart(self, user_id: int) -> bool:

        delete_the_cart = self.cart_repository.delete(user_id)
        if not delete_the_cart:
            raise CartNotFoundError(f"Корзина пользователя с ID {user_id} не найден")
        return delete_the_cart
