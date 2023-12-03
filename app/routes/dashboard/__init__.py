from fastapi import APIRouter, Depends, HTTPException, Request 
from utils.templating import templates
from database import SessionLocal, get_db

router = APIRouter()

@router.get("/")
def dashboard(request: Request, db: SessionLocal = Depends(get_db)):
    return templates.TemplateResponse("dashboard-root.html", {"request": request})