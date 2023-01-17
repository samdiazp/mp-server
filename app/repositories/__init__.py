from typing import TypeVar
from sqlalchemy.orm import Session


T = TypeVar("T")

class BaseRepo():

    def __init__(self, db: Session, model: T) -> None:
        self.model = model
        self.db = db
    
    def get(self, skip: int = 0, limit: int = 100) -> list[T]:
       return self.db.query(self.model).offset(skip).limit(limit).all()
