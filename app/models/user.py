from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey, inspect
from sqlalchemy.orm import relationship
from app.database import Base
from .base import BaseModel 

class User(Base, BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    user_data = relationship("PersonalInformation", back_populates="user", uselist=False)


class PersonalInformation(Base, BaseModel):
    __tablename__ = "personal_information"
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    lastname=Column(String)
    weight = Column(Float)
    height = Column(Float)
    age = Column(Integer)
    allergies = Column(String)
    pathologies = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="user_data")
