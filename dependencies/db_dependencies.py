from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db
from repositories.user_repository import UserRepository


def get_user_repository(
    db: Session = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)
