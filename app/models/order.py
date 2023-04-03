from sqlalchemy import DateTime, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .base import BaseModel


class Product(Base, BaseModel):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    benefits = Column(String)
    orders = relationship(
        "Order", secondary="order_products", back_populates="products")


class Order(Base, BaseModel):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    status = Column(Integer, default=0)
    products = relationship(
        "Product", secondary="order_products", back_populates="orders")
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")


class OrderProducts(Base, BaseModel):
    __tablename__ = "order_products"
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
