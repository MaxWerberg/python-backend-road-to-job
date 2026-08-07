from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database.database import Base


class Address(Base):
    """Описывает модель адреса доставки пользователя"""

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    house = Column(String, nullable=False)
    apartment = Column(String, nullable=True)
    is_default = Column(Boolean, nullable=False)
