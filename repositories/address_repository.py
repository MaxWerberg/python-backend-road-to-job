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

    def get_by_address_id(self, address_id: int) -> Address | None:
        address = self.db.get(Address, address_id)
        return address

    def get_by_user_id(self, user_id: int) -> Address | None:
        query = select(Address).where(Address.user_id == user_id)
        result = self.db.execute(query).scalar_one_or_none()
        return result

    def get_all_by_user_id(self, user_id) -> list[Address]:
        query = select(Address).where(Address.user_id == user_id)
        result = self.db.execute(query).scalars().all()
        return result

    def get_by_address_id_default(self, user_id: int) -> Address | None:
        query = select(Address).where(
            Address.user_id == user_id, Address.is_default == True
        )
        return self.db.execute(query).scalar_one_or_none()

    def update(self, address: list[Address]) -> list[Address]:
        self.db.flush()
        return address

    def delete(self, address_id: int) -> bool:
        address = self.get_by_address_id(address_id)
        if address is None:
            return False
        self.db.delete(address)
        self.db.flush()
        return True
