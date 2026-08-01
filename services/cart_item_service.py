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

    def get_cart(self, current_user_id: int) -> Cart | None:
        return self.cart_repository.get_by_user_id(current_user_id)

    def add_to_cart(self, cart_id: int, product_id: int, quantity: int) -> CartItem:
        check_item = self.cart_item_repository.get_item(cart_id, product_id)
        if quantity < 0:
            raise ValueError("Значение не может быть отрицательным")
        if not check_item:
            new_item = CartItem(
                cart_id=cart_id, product_id=product_id, quantity=quantity
            )
            return self.cart_item_repository.create(new_item)
        check_item.quantity += quantity
        return self.cart_item_repository.update(check_item)

    def remove_from_cart(self, cart_id: int, product_id: int) -> None:
        item_for_delete = self.cart_item_repository.get_item(cart_id, product_id)
        if not item_for_delete:
            raise ValueError("Товар отсутствует в корзине")
        self.cart_item_repository.delete(cart_id, product_id)

    def change_quantity(
        self, cart_id: int, product_id: int, new_quantity: int
    ) -> CartItem | None:

        check_item = self.cart_item_repository.get_item(cart_id, product_id)

        if not check_item:
            raise ValueError("Товар отсутствует в корзине")

        check_item.quantity = max(0, check_item.quantity + new_quantity)

        if check_item.quantity == 0:
            self.cart_item_repository.delete(check_item.cart_id, check_item.product_id)
            return None

        return self.cart_item_repository.update(check_item)
