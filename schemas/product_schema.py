from pydantic import BaseModel


class ProductRegisterSchema(BaseModel):
    """Схема регистрации продукта"""

    sku: int
    product_name: str
    product_cost: int
    stock_quantity: int


class ProductResponseSchema(BaseModel):
    """Схема ответа продукта"""

    sku: int
    product_name: str
    product_cost: int
    stock_quantity: int
