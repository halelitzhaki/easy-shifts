from sqlalchemy.orm import Session
from Backend.db.models import User
from Backend.db.repositories.base_repository import BaseRepository


class UsersRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def custom_operation_for_test_only(self):
        return 30
