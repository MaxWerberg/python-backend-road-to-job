from models.product import Product


class ProductRepository:
    def __init__(self):
        self.db = []

    def create(self, product: Product) -> Product:
        """Создает продукт"""
        self.db.append(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        """Поиск продукта по ID"""
        for product in self.db:
            if product.id == product_id:
                return product
        return None

    def get_by_sku(self, product_sku: int) -> Product | None:
        """Поиск продукта по SKU"""
        for product in self.db:
            if product.sku == product_sku:
                return product
        return None

    def update(self, updated_product: Product) -> Product | None:
        """Сохраняет изменения продукта в базу данных"""
        for index, existing_product in enumerate(self.db):
            if existing_product.id == updated_product.id:
                self.db[index] = updated_product
                return updated_product
        return None

    def delete(self, product_id: int) -> bool:
        """Удаляет продукт по ID"""
        for product in self.db:
            if product.id == product_id:
                self.db.remove(product)
                return True
        return False
