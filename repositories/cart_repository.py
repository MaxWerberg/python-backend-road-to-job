from sqlalchemy import select
from sqlalchemy.orm import Session

from models.cart import Cart


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cart: Cart) -> Cart:
        """Создает корзину пользователя в базе данных"""
        self.db.add(cart)
        self.db.flush()
        return cart

    def get_by_user_id(self, current_user_id: int) -> Cart:
        """Поиск корзины по ID"""
        query = select(Cart).where(Cart.user_id == current_user_id)
        return self.db.execute(query).scalar_one_or_none()
