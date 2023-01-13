from sqlalchemy import Boolean, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_data = relationship("PersonalInformation", back_populates="user")


class PersonalInformation(Base):
    __tablename__ = "personal_information"
    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, index=True)
    height = Column(Float, index=True)
    age = Column(Integer, index=True)
    allergies = Column(String)
    pathologies = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="user_data")
