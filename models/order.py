from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String

from database.database import Base


class Order(Base):
    """Описывает модель сформированного заказа"""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address_id = Column(Integer, nullable=False)
    total_price = Column(DECIMAL, nullable=False)
    status = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    recipient_phone = Column(String, nullable=True)
