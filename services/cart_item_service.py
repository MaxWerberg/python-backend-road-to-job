from exceptions.exceptions import (
    CartNotFoundError,
    InvalidQuantityError,
    ItemNotInCartError,
    OutOfStockError,
    ProductNotFoundError,
)
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
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

    def _get_product(self, product_id: int) -> Product:
        """Вспомогательный метод для получения товара"""
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError("Товар отсутствует в каталоге")
        return product

    def _get_cart_item(self, cart_id: int, product_id: int) -> CartItem:
        """Вспомогательный метод для получения элемента корзины"""
        cart_item = self.cart_item_repository.get_item(cart_id, product_id)
        if cart_item is None:
            raise ItemNotInCartError("Товар отсутствует в корзине")
        return cart_item

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
        product = self._get_product(product_id)
        item_cart = self.cart_item_repository.get_item(cart.id, product_id)

        current_quantity = item_cart.quantity if item_cart else 0
        total_requested_quantity = current_quantity + quantity

        if product.stock_quantity < total_requested_quantity:
            raise OutOfStockError("Недостаточно товара на складе")

        if item_cart is None:
            new_item = CartItem(
                cart_id=cart.id, product_id=product_id, quantity=quantity
            )
            return self.cart_item_repository.create(new_item)

        item_cart.quantity = total_requested_quantity
        return self.cart_item_repository.update(item_cart)

    def change_quantity(
        self, current_user_id: int, product_id: int, quantity_delta: int
    ) -> CartItem:

        cart = self.get_cart(current_user_id)
        db_product = self._get_product(product_id)
        item_cart = self._get_cart_item(cart.id, product_id)

        target_quantity = item_cart.quantity + quantity_delta

        if quantity_delta > 0 and db_product.stock_quantity < target_quantity:
            raise OutOfStockError("Недостаточно товара на складе")

        if target_quantity == 0:
            self.cart_item_repository.delete(item_cart.cart_id, item_cart.product_id)
            item_cart.quantity = 0
            return item_cart

        item_cart.quantity = target_quantity
        return self.cart_item_repository.update(item_cart)

    def remove_from_cart(self, current_user_id: int, product_id: int) -> None:
        cart = self.get_cart(current_user_id)

        item_for_delete = self.cart_item_repository.get_item(cart.id, product_id)

        if item_for_delete is None:
            raise ItemNotInCartError("Товар отсутствует в корзине")

        self.cart_item_repository.delete(cart.id, product_id)
