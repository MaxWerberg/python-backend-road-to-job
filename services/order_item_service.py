from errors import InvalidQuantityError, OutOfStockError, ProductNotFoundError
from models.order_item import OrderItem
from repositories.order_item_repository import OrderItemRepository
from repositories.product_repository import ProductRepository


class OrderItemService:
    def __init__(
        self,
        product_repository: ProductRepository,
        order_item_repository: OrderItemRepository,
    ):
        self.product_repository = product_repository
        self.order_item_repository = order_item_repository

    def create(self, product_id, quantity, order_id: int) -> OrderItem:

        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise ProductNotFoundError("Товар отсутствует в каталоге")
        if quantity <= 0:
            raise InvalidQuantityError("Отрицательное количество продукта")
        if product.stock_quantity < quantity:
            raise OutOfStockError("Недостаточно товара на складе")

        product.stock_quantity -= quantity
        self.product_repository.update(product)

        result = OrderItem(
            order_id=order_id,
            product_id=product.id,
            quantity=quantity,
            product_price_at_purchase=product.product_cost,
            product_title_at_purchase=product.product_name,
        )

        return self.order_item_repository.create(result)
