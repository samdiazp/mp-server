from typing import List
from fastapi import APIRouter, status, Depends
from app.schemas.user import PersonalInformationCreate
from app.schemas.base import BasicResponse
from app.models.user import PersonalInformation
from app.repositories.users import PersonalInfoRepo, UserRepo
from app.schemas.user import User, PersonalInformation as PersonalInformationSCH
from app.database import get_db, SessionLocal
from app.utils.auth import get_me

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
        user_dict = user_model.as_dict()
        users.append(User(**user_dict, user_data=user_model.user_data) if user_model.user_data else User(**user_dict))
    return users

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=User)
async def get_user(user_id: int, db: SessionLocal = Depends(get_db)) -> User:
    user_repo = UserRepo(db)
    user_mdl = user_repo.get_by_id(id=user_id)

    user_dict = user_mdl.as_dict()
    
    user = User(**user_dict) if user_mdl.user_data is None else User(**user_dict, user_data=user_mdl.user_data)

    return user
