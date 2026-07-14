from sqlalchemy import Column, Integer, String

from database.database import Base


class Product(Base):
    """Описывает модель  продукта и его бизнес-логику"""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True, nullable=False, index=True)
    product_name = Column(String, nullable=False)
    product_cost = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    def change_product_cost(self, new_product_cost: int) -> None:
        """Изменяет стоимость продукта на новое значение"""
        self.product_cost = new_product_cost

    def is_available(self, expected_quantity: int) -> bool:
        """Проверяет наличие запрашиваемого количества товара на складе"""
        if expected_quantity <= self.stock_quantity and expected_quantity > 0:
            return True
        else:
            return False

    def decrease_stock(self, quantity: int) -> bool:
        """Уменьшает количество доступного товара на складе при валидном значении"""
        if quantity <= 0:
            return False

        if self.stock_quantity >= quantity:
            self.stock_quantity = self.stock_quantity - quantity
            return True
        else:
            return False

    def increase_stock(self, quantity: int) -> bool:
        """Увеличивает количество доступного товара на складе"""
        if quantity > 0:
            self.stock_quantity = self.stock_quantity + quantity
            return True
        else:
            return False
