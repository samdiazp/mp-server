from fastapi import FastAPI
from typing import Union
from app.routes import auth

app = FastAPI()
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"Hello": "World"}
