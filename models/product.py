class Product:
    def __init__(
        self,
        id: int,
        sku: int,
        product_name: str,
        product_cost: int,
        stock_quantity: int,
    ):
        self.id = id
        self.sku = sku
        self.product_name = product_name
        self.product_cost = product_cost
        self.stock_quantity = stock_quantity

    def change_product_cost(self, new_product_cost: int) -> None:
        self.product_cost = new_product_cost

    def is_available(self, expected_quantity: int) -> bool:
        """Проверка нужного количества товара на складе"""
        if expected_quantity <= self.stock_quantity and expected_quantity > 0:
            return True
        else:
            return False

    def decrease_stock(self, quantity: int) -> bool:
        """Уменьшение количества товара на складе"""
        if quantity <= 0:
            return False

        if self.stock_quantity >= quantity:
            self.stock_quantity = self.stock_quantity - quantity
            return True
        else:
            return False

    def increase_stock(self, quantity: int) -> bool:
        """Увеличение количества товара на складе"""
        if quantity > 0:
            self.stock_quantity = self.stock_quantity + quantity
            return True
        else:
            return False
