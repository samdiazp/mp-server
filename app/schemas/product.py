from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    benefits: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
