from fastapi import APIRouter, Depends, HTTPException, Request 
from utils.templating import templates
from database import SessionLocal, get_db
from .user import router as users_router

router = APIRouter()
router.include_router(users_router, prefix="/users", tags=["users"])

@router.get("/")
def dashboard(request: Request, db: SessionLocal = Depends(get_db)):
    return templates.TemplateResponse("dashboard-root.html", {"request": request, "user": {"name": "John Doe"}})
