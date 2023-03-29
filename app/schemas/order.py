from pydantic import BaseModel, validator
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
    user: Optional[User] = None

    @validator('products', pre=True)
    def validate(cls, products_relationship, **kwargs):
        return [Product.from_orm(product) for product in products_relationship]
    
    class Config:
        orm_mode = True

class OrderUpdate(BaseModel):
    status: int
    date: Optional[datetime] = None

class AddProductOrder(BaseModel):
    products_id: List[int]
