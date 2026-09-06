from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String

from database.database import Base


class Order(Base):
    """Описывает модель сформированного заказа"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=False, index=True
    )
    address_id = Column(
        Integer,
        ForeignKey("addresses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    total_price = Column(DECIMAL(precision=10, scale=2), nullable=False)
    status = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_phone = Column(String, nullable=True)
    delivery_address_saved = Column(String, nullable=False)
