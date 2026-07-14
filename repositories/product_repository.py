from sqlalchemy import select
from sqlalchemy.orm import Session

from models.product import Product


class ProductRepository:
    """Управляет сохранением и извлечением данных продуктов в базе данных"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        """Создает новый продукт в базе данных"""
        self.db.add(product)
        self.db.flush()
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        """Ищет продукт в базе данных по его ID"""
        return self.db.get(Product, product_id)

    def get_by_sku(self, product_sku: int) -> Product | None:
        """Ищет продукт в базе данных по его SKU"""
        query = select(Product).where(Product.sku == product_sku)
        return self.db.execute(query).scalar_one_or_none()

    def update(self, updated_product: Product) -> Product:
        """Фиксирует изменения данных продукта в текущей сессии"""
        self.db.flush()
        return updated_product

    def delete(self, product_id: int) -> bool:
        """Удаляет продукт из базы данных по его ID"""
        product = self.db.get(Product, product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.flush()
        return True
