from exceptions.exceptions import (
    CartNotFoundError,
    InvalidQuantityError,
    ItemNotInCartError,
    OutOfStockError,
    ProductNotFoundError,
)
from models.cart import Cart
from models.cart_item import CartItem
from repositories.cart_item_repository import CartItemRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository


class CartItemService:
    def __init__(
        self,
        cart_item_repository: CartItemRepository,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    def get_cart(self, current_user_id: int) -> Cart:
        cart = self.cart_repository.get_by_current_user_id(current_user_id)
        if not cart:
            raise CartNotFoundError("Корзина пользователя не найдена")

        cart.items = self.cart_item_repository.get_all_items_by_cart_id(cart.id)
        return cart

    def add_to_cart(
        self, current_user_id: int, product_id: int, quantity: int
    ) -> CartItem:

        if quantity <= 0:
            raise InvalidQuantityError("Значение не может быть отрицательным")
        cart = self.get_cart(current_user_id)

        check_item = self.product_repository.get_by_id(product_id)
        check_item_cart = self.cart_item_repository.get_item(cart.id, product_id)

        if check_item is None:
            raise ProductNotFoundError("Товар отсутствует в каталоге")

        if (
            check_item.stock_quantity < quantity
            or check_item.stock_quantity <= check_item_cart.quantity
        ):
            raise OutOfStockError("Недостаточно товара на складе")

        print(check_item_cart.quantity)

        if not check_item_cart:
            new_item = CartItem(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )

            return self.cart_item_repository.create(new_item)

        check_item_cart.quantity += quantity
        return self.cart_item_repository.update(check_item_cart)

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
