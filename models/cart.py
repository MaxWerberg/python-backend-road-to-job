from sqlalchemy import Column, ForeignKey, Integer

from database.database import Base


class Cart(Base):
    """Описывает связующую модель 'пользователь <-> корзина'"""

    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
