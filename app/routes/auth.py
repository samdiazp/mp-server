from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext

ALGORITHM="HS256"
ACCESS_TOKEN_DURATION=1
SECRET="asfasfasfasfaAFASFA"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])


@router.post("/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(oauth2)):
    pass

@router.post("/auth/signup")
def signup():
    pass