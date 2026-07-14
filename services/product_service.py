from models.product import Product
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(
        self,
        id: int,
        sku: int,
        product_name: str,
        product_cost: int,
        stock_quantity: int,
    ) -> Product:
        """Создает продукт"""
        existing_product = self.repository.get_by_sku(sku)
        if existing_product:
            raise ValueError("Товар с таким SKU уже существует")

        product = Product(
            id=id,
            sku=sku,
            product_name=product_name,
            product_cost=product_cost,
            stock_quantity=stock_quantity,
        )
        created_product = self.repository.create(product)
        return created_product

    def get_product(self, product_id: int) -> Product:
        """Поиск продукта по ID"""
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError("Продукт не найден")
        return product

    def change_cost(self, product_id: int, new_cost: int) -> Product:
        """Изменяет стоимость продукта"""
        product = self.get_product(product_id)
        product.change_product_cost(new_cost)
        return self.repository.update(product)

    def receive_stock(self, product_id: int, quantity: int) -> Product:
        """Пополнение продукта на склад"""
        product = self.get_product(product_id)

        if not product.increase_stock(quantity):
            raise ValueError("Количество для пополнения должно быть положительным")

        return self.repository.update(product)

    def ship_stock(self, product_id: int, quantity: int) -> Product:
        """Отбытие продукта со склада"""
        product = self.get_product(product_id)

        if not product.is_available(quantity):
            raise ValueError("Недостаточно товара на складе")

        if not product.decrease_stock(quantity):
            raise ValueError("Некорректное количество для отгрузки")

        return self.repository.update(product)
