from decimal import Decimal

from errors import (
    AddressNotFoundError,
    CartNotFoundError,
    ItemNotInCartError,
    OrderAlreadyExistsError,
    OutOfStockError,
)
from models.order import Order
from repositories.address_repository import AddressRepository
from repositories.cart_item_repository import CartItemRepository
from repositories.cart_repository import CartRepository
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from services.order_item_service import OrderItemService


class OrderService:
    def __init__(
        self,
        cart_repository: CartRepository,
        cart_item_repository: CartItemRepository,
        address_repository: AddressRepository,
        order_repository: OrderRepository,
        product_repository: ProductRepository,
        order_item_service: OrderItemService,
    ):
        self.product_repository = product_repository
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

        db_order = self.order_repository.get_by_user_id(current_user_id)
        if db_order and db_order.status == "pending":
            raise OrderAlreadyExistsError("Заказ уже оформлен")

        db_cart = self.cart_repository.get_by_current_user_id(current_user_id)
        if db_cart is None:
            raise CartNotFoundError(
                f"Корзина пользователя с id {current_user_id} не найдена"
            )

        db_cart_items = self.cart_item_repository.get_all_items_by_cart_id(db_cart.id)
        if not db_cart_items:
            raise ItemNotInCartError("Нельзя оформить заказ с пустой корзиной")

        db_address = self.address_repository.get_by_address_id_default(current_user_id)
        if db_address is None:
            raise AddressNotFoundError("Необходимо указать адрес доставки")

        total_price = Decimal("0.0")
        for item in db_cart_items:
            db_product = self.product_repository.get_by_id(item.product_id)
            if not db_product or db_product.stock_quantity < item.quantity:
                raise OutOfStockError(
                    f"Недостаточно товара {db_product.product_name if db_product else ''} на складе"
                )

            total_price += db_product.product_cost * item.quantity

        address_str = f"{db_address.country}, {db_address.city}, ул. {db_address.street}, дом {db_address.house}, кв. {db_address.apartment}"

        new_order = Order(
            user_id=current_user_id,
            address_id=db_address.id,
            total_price=total_price,
            status="pending",
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            delivery_address_saved=address_str,
        )
        saved_order = self.order_repository.create(new_order)

        for item in db_cart_items:
            self.order_item_service.create(
                product_id=item.product_id,
                quantity=item.quantity,
                order_id=saved_order.id,
            )

        self.cart_item_repository.delete_all_items(db_cart.id)

        return saved_order
