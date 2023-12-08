from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from repositories import users
from schemas import user as user_sch, base
from database import SessionLocal, get_db
from models import user
from utils import auth

router = APIRouter()


@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)
) -> Dict[str, str]:
    user_repo = users.UserRepo(db)
    # username is the email
    founded = user_repo.get_by_email(form.username)
    if not founded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas"
        )

    if not auth.verify_password(form.password, founded.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas"
        )

    return {
        "access_token": auth.create_access_token(form.username),
        "refresh_token": auth.create_refresh_token(form.username),
        "token_type": "bearer",
    }


@router.get("/auth/me", status_code=status.HTTP_200_OK, response_model=user_sch.User)
async def get_me(user: user_sch.User = Depends(auth.get_me)) -> user_sch.User:
    return user


@router.post(
    "/auth/signup", status_code=status.HTTP_201_CREATED, response_model=user_sch.User
)
async def signup(
    form: user_sch.UserCreate, db: SessionLocal = Depends(get_db)
) -> user_sch.User:
    user_repo = users.UserRepo(db)
    founded = user_repo.get_by_email(form.email)
    if founded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe"
        )

    hashed_password: str = auth.get_hashed_password(form.password)
    new_user_model = user.User(
        email=form.email, hashed_password=hashed_password, role="USER"
    )
    new_user = user_repo.create(new_user_model)
    return user_sch.User.from_orm(new_user)
