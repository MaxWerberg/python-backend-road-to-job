from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from database.database import Base


class CartItem(Base):
    """Описывает модель корзины"""

    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("cart_id", "product_id", name="uq_cart_id_product_id"),
    )
