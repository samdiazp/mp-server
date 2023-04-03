from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from schemas.user import PersonalInformationCreate
from schemas.base import BasicResponse
from models.user import PersonalInformation
from repositories.users import PersonalInfoRepo, UserRepo
from schemas.user import User, PersonalInformation as PersonalInformationSCH
from database import get_db, SessionLocal
from utils.auth import get_me

router = APIRouter()


@router.post('/users/personal-information', response_model=BasicResponse, status_code=status.HTTP_201_CREATED)
async def add_personal_information(data: PersonalInformationCreate, user: User = Depends(get_me), db: SessionLocal = Depends(get_db)) -> BasicResponse:
    personal_repo = PersonalInfoRepo(db)
    data.user_id = user.id
    personal_model = PersonalInformation(**data.dict())

    new_data = personal_repo.create(personal_model)

    return BasicResponse(ok=True, data=new_data)

@router.get('/users', status_code=status.HTTP_200_OK, response_model=List[User])
async def get_users(skip: int = 0, limit: int = 25, db: SessionLocal = Depends(get_db)) -> List[User]:
    user_repo = UserRepo(db)
    users: List[User] = []
    for user_model in user_repo.get(offset=skip, limit=limit):
        users.append(User.from_orm(user_model))
    return users

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: int, db: SessionLocal = Depends(get_db)) -> User:
    user_repo = UserRepo(db)
    user_mdl = user_repo.get_by_id(id=user_id)
    if not user_mdl:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")
    return User.from_orm(user_mdl)
