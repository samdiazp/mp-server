from typing import List
from . import BaseRepo
from sqlalchemy.orm import Session
from models.order import Order, OrderProducts


class OrderRepo(BaseRepo):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Order)
    
    def add_products_to_order(self, order_id: int, products_id: List[int]) -> None:
        for product_id in products_id:
            self.db.add(OrderProducts(product_id=product_id, order_id = order_id))

        self.db.commit()

