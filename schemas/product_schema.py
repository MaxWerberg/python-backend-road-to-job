from typing import Optional

from pydantic import BaseModel, model_validator


class ProductRegisterSchema(BaseModel):
    """Схема регистрации продукта"""

    sku: int
    product_name: str
    product_cost: int
    stock_quantity: int


class ProductResponseSchema(BaseModel):
    """Схема ответа продукта"""

    id: int
    sku: int
    product_name: str
    product_cost: int
    stock_quantity: int


class ProductSearchSchema(BaseModel):
    """Схема поиска продукта по SKU или по ID"""

    id: Optional[int] = None
    sku: Optional[int] = None

    @model_validator(mode="after")
    def check_search(self):
        if (self.id is None) == (self.sku is None):
            raise ValueError("Укажите 'ID', либо 'SKU'")
        return self


class ProductChangeCostSchema(BaseModel):
    """Схема изменения стоимости продукта"""

    id: Optional[int] = None
    sku: Optional[int] = None
    new_cost: int

    @model_validator(mode="after")
    def check_search(self):
        if (self.id is None) == (self.sku is None):
            raise ValueError("Укажите 'ID', либо 'SKU'")
        return self
