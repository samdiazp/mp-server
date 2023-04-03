from . import BaseRepo
from models.order import Product
from sqlalchemy.orm import Session

class ProductRepo(BaseRepo):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Product)
