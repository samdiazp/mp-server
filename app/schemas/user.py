from typing import Optional
from pydantic import BaseModel
from enum import Enum

class Role(Enum):
    USER="USER"
    ADMIN="ADMIN"
class PersonalInformationBase(BaseModel):
    weight: float
    height: float
    age: int
    allergies: str
    pathologies: str
    name: str
    lastname:str


class PersonalInformationCreate(PersonalInformationBase):
    user_id: Optional[int] = None

class PersonalInformation(PersonalInformationBase):
    id: int
    user_id: int

    class Config:
        orm_mode=True

class UserBase(BaseModel):
    email: str
    role: Role = Role.USER
    is_active: bool = True

class User(UserBase):
    id: int
    user_data: PersonalInformation = None

    class Config:
        orm_mode=True
        use_enum_values=True

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

