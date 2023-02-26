
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from app.repositories.users import UserRepo
from app.schemas.user import User as UserSCH
from datetime import datetime
from pydantic import ValidationError, BaseModel
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db, SessionLocal

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'secret')     # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY', 'secret_refresh')      # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT"
)

class TokenPayload(BaseModel):
    exp: int
    sub: str

def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def get_me(token: str = Depends(reuseable_oauth), db: SessionLocal = Depends(get_db)) -> UserSCH:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_payload = TokenPayload(**payload)

        if datetime.fromtimestamp(token_payload.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_repo = UserRepo(db)
    user = user_repo.get_by_email(token_payload.sub)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no existe",
        )
    
    return UserSCH(**user.as_dict())

    
