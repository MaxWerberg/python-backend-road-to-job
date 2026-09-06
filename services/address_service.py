from exceptions.exceptions import AddressLimitExceededError, AddressNotFoundError
from models.address import Address
from repositories.address_repository import AddressRepository


class AddressService:
    def __init__(self, repository: AddressRepository):
        self.repository = repository

    def get_address(self, user_id) -> Address:
        address = self.repository.get_by_user_id(user_id)
        if not address:
            raise AddressNotFoundError("Адрес не найден")
        return address

    def create(
        self,
        current_user_id: int,
        country: str,
        city: str,
        street: str,
        house: str,
        apartment: str | None,
        is_default: bool | None = False,
    ):

        addresses = self.repository.get_all_by_user_id(current_user_id)
        check_summ = len(addresses)
        if check_summ >= 5:
            raise AddressLimitExceededError(
                "Превышено максимальное количество сохраненных адресов (5)"
            )
        if check_summ > 0:
            is_default = False
        if check_summ == 0:
            is_default = True

        new_address = Address(
            user_id=current_user_id,
            country=country,
            city=city,
            street=street,
            house=house,
            apartment=apartment,
            is_default=is_default,
        )
        self.repository.create(new_address)
        return new_address

    def delete_per_address_id(self, current_user_id: int, address_id: int):
        address = self.repository.get_by_address_id(address_id)
        self.delete_per_address_id(address)
