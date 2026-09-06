from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.address import Address


class AddressRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, address: Address) -> Address:
        self.db.add(address)
        self.db.flush()
        self.db.refresh(address)
        return address

    def get_by_address_id(self, address_id: int) -> Address:
        address = self.db.get(Address, address_id)
        if not address:
            return False
        return address

    def get_by_user_id(self, user_id: int) -> Address:
        query = select(Address).where(Address.user_id == user_id)
        result = self.db.execute(query).scalar_one_or_none()
        if not result:
            return False
        return result

    def get_all_by_user_id(self, user_id) -> Sequence[Address]:
        query = select(Address).where(Address.user_id == user_id)
        result = self.db.execute(query).scalars().all()
        return result

    def delete(self, address_id: int) -> None:
        address = self.get_by_address_id(address_id)
        self.db.delete(address)
        self.db.flush()
