from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    recipient_name: str
    recipient_phone: str
