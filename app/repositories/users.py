from . import BaseRepo
from sqlalchemy.orm import Session
from app.models.user import User, PersonalInformation

class UserRepo(BaseRepo):

    def __init__(self, db: Session) -> None:
       super().__init__(db, User)

    def get_by_email(self, email: str) -> User:
        return self.db.query(self.model).filter(User.email == email).first()


class PersonalInfoRepo(BaseRepo):
    def __init__(self, db: Session) -> None:
        super().__init__(db, PersonalInformation)
    
