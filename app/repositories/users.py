from . import BaseRepo
from sqlalchemy.orm import Session
from models.user import User, PersonalInformation

class UserRepo(BaseRepo):

    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def get_one(self, id: int) -> User:
        return self.db.query(User).filter(User.id == id).first()