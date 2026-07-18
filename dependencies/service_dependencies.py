from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from services.jwt_service import JWTService
from services.product_service import ProductService
from services.user_service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    jwt_service = JWTService()
    user_repository = UserRepository(db)
    return UserService(user_repository, jwt_service)


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = ProductRepository(db)
    return ProductService(repo)
