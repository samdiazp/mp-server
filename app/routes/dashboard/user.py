from fastapi import Request, APIRouter, Depends
from utils.templating import templates
from utils import auth
from schemas.user import User

router = APIRouter()

@router.get("/")
async def users_page(request: Request, user: User = Depends(auth.get_active_user)):
    return templates.TemplateResponse("users.html", {"request": request, "title": "Usuarios", "user": user})