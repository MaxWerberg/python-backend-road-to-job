from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.address_repository import AddressRepository
from repositories.cart_item_repository import CartItemRepository
from repositories.cart_repository import CartRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.address_service import AddressService
from services.admin_service import AdminService
from services.cart_item_service import CartItemService
from services.jwt_service import JWTService
from services.product_service import ProductService
from services.user_service import UserService

db_session = Annotated[Session, Depends(get_db)]


def get_admin_service(db: db_session) -> AdminService:
    user_repository = UserRepository(db)
    return AdminService(user_repository)


def get_user_service(db: db_session) -> UserService:
    jwt_service = JWTService()
    user_repository = UserRepository(db)
    repo_cart = CartRepository(db)
    return UserService(user_repository, jwt_service, repo_cart)


def get_address_service(db: db_session) -> AddressService:
    address_repository = AddressRepository(db)
    return AddressService(address_repository)


def get_product_service(db: db_session) -> ProductService:
    repo = ProductRepository(db)
    return ProductService(repo)


def get_cart_item_service(db: db_session) -> CartItemService:
    repo_cart_item = CartItemRepository(db)
    repo_cart = CartRepository(db)
    repo_product = ProductRepository(db)
    return CartItemService(repo_cart_item, repo_cart, repo_product)
