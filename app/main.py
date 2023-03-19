from fastapi import FastAPI
from typing import Union
from app.routes import auth, order, user

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(order.router)

@app.get("/")
async def root():
    return {"Hello": "World"}
