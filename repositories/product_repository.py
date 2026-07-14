from sqlalchemy import select
from sqlalchemy.orm import Session

from models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:
        """Создает продукт"""
        self.db.add(product)
        self.db.flush()
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        """Поиск продукта по ID"""
        return self.db.get(Product, product_id)

    def get_by_sku(self, product_sku: int) -> Product | None:
        """Поиск продукта по SKU"""
        query = select(Product).where(Product.sku == product_sku)
        return self.db.execute(query).scalar_one_or_none()

    def update(self, updated_product: Product) -> Product | None:
        """Сохраняет изменения продукта в базу данных"""
        self.db.flush()
        return updated_product

    def delete(self, product_id: int) -> bool:
        """Удаляет продукт по ID"""
        product = self.db.get(Product, product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.flush()
        return True
