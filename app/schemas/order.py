from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .user import User
from .product import Product

class OrderBase(BaseModel):
    total:float
    status: int
    date: datetime

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    products: Optional[List[Product]] = None
    user: User


class AddProductOrder(BaseModel):
    products_id: List[int]
