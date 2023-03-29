import uvicorn
from fastapi import FastAPI
from .routes import auth, order, user, products

app = FastAPI()
app.include_router(auth.router, tags=['auth'])
app.include_router(user.router, tags=['users'])
app.include_router(order.router, tags=['orders'])
app.include_router(products.router, tags=['products'])

@app.get("/")
async def root():
    return {"Hello": "World"}


if __name__ == "main":
    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True, debug=True)
