from sqlalchemy import select
from sqlalchemy.orm import Session

from models.order_item import OrderItem


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order_item: OrderItem) -> OrderItem:
        self.db.add(order_item)
        self.db.flush()
        return order_item

    def delete(self, item_id: int):
        query = select(OrderItem).where(OrderItem.id == item_id)
        result = self.db.execute(query).scalar_one_or_none()
        if not result:
            return False

        self.db.delete(result)
        self.db.flush()
        return True
