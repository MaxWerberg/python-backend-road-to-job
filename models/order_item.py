from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String

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
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    quantity = Column(Integer, nullable=False)
    product_price_at_purchase = Column(DECIMAL(precision=10, scale=2), nullable=False)
    product_title_at_purchase = Column(String, nullable=False)
