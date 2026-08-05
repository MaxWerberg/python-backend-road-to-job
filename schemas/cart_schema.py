from pydantic import BaseModel


class CartResponseSchema(BaseModel):
    id: int
    user_id: int


class CartAddItemSchema(BaseModel):
    product_id: int
    quantity: int


class CartDeleteItemSchema(BaseModel):
    product_id: int
