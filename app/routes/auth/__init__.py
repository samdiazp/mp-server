from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import RedirectResponse, PlainTextResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from repositories import users
from utils.templating import templates
from database import SessionLocal, get_db
from utils import auth
from models import user

router = APIRouter()


@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "title": "Registro"})

@router.get("/signin")
def login_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "title": "Iniciar sesión"})

@router.post("/signin", status_code=status.HTTP_201_CREATED)
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user_repo = users.UserRepo(db)
    # username is the email
    founded = user_repo.get_by_email(form.username)
    if not founded:
        return PlainTextResponse(content="Credenciales incorrectas")

    if not auth.verify_password(form.password, founded.hashed_password):
        return PlainTextResponse(content="Credenciales incorrectas")
    token = auth.create_access_token(founded.email)
    response = Response(status_code=status.HTTP_303_SEE_OTHER, headers={"HX-Redirect": "/dashboard"})
    response.set_cookie(key="token", value=token)
    return response


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user_repo = users.UserRepo(db)
    founded = user_repo.get_by_email(form.username)
    if founded:
        return PlainTextResponse(content="Usuario ya existe")

    hashed_password: str = auth.get_hashed_password(form.password)
    new_user_model = user.User(
        email=form.username, hashed_password=hashed_password, role="USER"
    )
    user_repo.create(new_user_model)
    token = auth.create_access_token(new_user_model.email)
    response = Response(status_code=status.HTTP_303_SEE_OTHER, headers={"HX-Redirect": "/dashboard"})
    response.set_cookie(key="token", value=token)
    return response


@router.get("/logout")
def logout(request: Request):
    response = Response(status_code=status.HTTP_303_SEE_OTHER, headers={"HX-Redirect": "/"})
    response.delete_cookie(key="token")
    return  response