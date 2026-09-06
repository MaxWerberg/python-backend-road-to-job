from sqlalchemy import select
from sqlalchemy.orm import Session

from models.order import Order


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()
        return order

    def delete(self, user_id: int):
        query = select(Order).where(Order.user_id == user_id)
        result = self.db.execute(query).scalar_one_or_none()
        if not result:
            return False

        self.db.delete(result)
        self.db.flush()
        return True
