from typing import Annotated

from pydantic import BaseModel, BeforeValidator

ValidStr = Annotated[
    str, BeforeValidator(lambda v: v.strip() if isinstance(v, str) else v)
]


class AddressResponseSchema(BaseModel):
    country: ValidStr
    city: ValidStr
    street: ValidStr
    house: ValidStr
    apartment: ValidStr
    is_default: bool | None


class AddressAddSchema(BaseModel):
    country: ValidStr
    city: ValidStr
    street: ValidStr
    house: ValidStr
    apartment: ValidStr
    is_default: bool | None


class AddressIdSchema(BaseModel):
    address_id: int
