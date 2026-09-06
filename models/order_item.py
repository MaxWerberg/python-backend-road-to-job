from sqlalchemy import DECIMAL, Column, ForeignKey, Integer

from database.database import Base


class OrderItem(Base):
    """Описывает модель завершенного заказа"""

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(DECIMAL(precision=10, scale=2), nullable=False)
