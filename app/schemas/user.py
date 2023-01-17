from typing import Union
from pydantic import BaseModel


class PersonalInformationBase(BaseModel):
    weight: float
    height: float
    age: int
    allergies: str
    pathologies: str
    name: str
    lastname:str


class PersonalInformationCreate(PersonalInformationBase):
    pass

class PersonalInformation(PersonalInformationBase):
    id: int
    user_id: int

    class Config:
        orm_mode=True

class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: int
    is_active:bool
    user_data: PersonalInformation

    class Config:
        orm_mode=True

class UserCreate(UserBase):
    password: str
