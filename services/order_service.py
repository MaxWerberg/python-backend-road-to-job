from decimal import Decimal

from errors import (
    AddressNotFoundError,
    CartNotFoundError,
    ItemNotInCartError,
    OrderAlreadyExistsError,
)
from models.order import Order
from repositories.address_repository import AddressRepository
from repositories.cart_item_repository import CartItemRepository
from repositories.cart_repository import CartRepository
from repositories.order_repository import OrderRepository
from services.order_item_service import OrderItemService


class OrderService:
    def __init__(
        self,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
        address_repository: AddressRepository,
        order_repository: OrderRepository,
        order_item_service: OrderItemService,
    ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.address_repository = address_repository
        self.order_repository = order_repository
        self.order_item_service = order_item_service

    def create(
        self,
        current_user_id: int,
        recipient_name: str,
        recipient_phone: str,
    ) -> Order:

        check_order = self.order_repository.get_by_user_id(current_user_id)
        if check_order and check_order.status == "pending":
            raise OrderAlreadyExistsError("Заказ уже оформлен")

        cart = self.cart_repository.get_by_current_user_id(current_user_id)
        if not cart:
            raise CartNotFoundError(
                f"Корзина пользователя с id {current_user_id} не найдена"
            )

        cart_items = self.cart_item_repository.get_all_items_by_cart_id(cart.id)
        if not cart_items:
            raise ItemNotInCartError("Нельзя оформить заказ с пустой корзиной")

        address = self.address_repository.get_by_user_id(current_user_id)
        if not address:
            raise AddressNotFoundError(
                f"Адрес пользователя с id {current_user_id} не найден"
            )

        total_price = Decimal("0.0")
        for item in cart_items:
            product = self.order_item_service.product_repository.get_by_id(
                item.product_id
            )
            if not product or product.stock_quantity < item.quantity:
                from errors import OutOfStockError

                raise OutOfStockError(
                    f"Недостаточно товара {product.product_name if product else ''} на складе"
                )

            total_price += product.product_cost * item.quantity

        address_str = f"{address.country}, {address.city}, {address.street}, {address.house}, {address.apartment}"

        new_order = Order(
            user_id=current_user_id,
            address_id=address.id,
            total_price=total_price,
            status="pending",
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            delivery_address_saved=address_str,
        )
        saved_order = self.order_repository.create(new_order)

        for item in cart_items:
            self.order_item_service.create(
                product_id=item.product_id,
                quantity=item.quantity,
                order_id=saved_order.id,
            )

        self.cart_item_repository.delete_all_items(cart.id)

        return saved_order
