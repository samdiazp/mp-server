from typing import TypeVar, Union, Any, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException

T = TypeVar("T")


class BaseRepo:

    def __init__(self, db: Session, model: T) -> None:
        self.model = model
        self.db = db
    
    def get(self, offset: int = 0, limit: int = 0 , *querys: list[tuple]) -> list[T]:
        if len(querys) > 0:
            return self.db.query(self.model).offset(offset).limit(limit).filter(querys).all()
        return self.db.query(self.model).offset(offset).limit(limit)

    def get_by_id(self, id: int) -> Union[T, None]:
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, schema: T) -> T:
        self.db.add(schema)
        self.db.commit()
        self.db.refresh(schema)
        return schema
    
    def update(self, mod: T, **values: dict) -> T:
        for key in values:
           setattr(mod, key, values[key])
        self.db.commit()
        self.db.refresh(mod)
        return mod
    
    def delete(self, id: int) -> None:
        self.db.query(self.model).filter(self.model.id == id).delete()
        self.db.commit()