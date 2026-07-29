from sqlalchemy import select
from sqlalchemy.orm import Session

from models.cart_item import CartItem


class CartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cart_item: CartItem) -> CartItem:
        """Добавляет продукт в корзину пользователя"""
        self.db.add(cart_item)
        self.db.flush()
        return cart_item

    def get_item(self, cart_id: int, product_id: int) -> CartItem | None:
        cart_query = select(CartItem).where(
            CartItem.cart_id == cart_id, CartItem.product_id == product_id
        )
        return self.db.execute(cart_query).scalar_one_or_none()

    def update(self, cart_item: CartItem) -> CartItem:
        """Обновляет элемент в корзине"""
        self.db.flush()
        return cart_item

    def delete(self, cart_id: int, product_id: int):
        """Удаляет продукт из корзину пользователя"""
        item = self.get_item(cart_id, product_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.flush()
        return True
