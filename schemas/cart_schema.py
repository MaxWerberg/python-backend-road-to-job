from pydantic import BaseModel


class CartItemSchema(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartResponseSchema(BaseModel):
    id: int
    user_id: int
    items: list[CartItemSchema]

    class Config:
        from_attributes = True


class CartAddItemSchema(BaseModel):
    product_id: int
    quantity: int


class CartDeleteItemSchema(BaseModel):
    product_id: int
