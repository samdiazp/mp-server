import uvicorn
from fastapi import FastAPI, Request
from routes import auth, order, user, products, dashboard
from fastapi.staticfiles import StaticFiles
from utils.templating import templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
ACTUAL_VERSION_API = "1"
PREFIX_API = f"/api/v{ACTUAL_VERSION_API}"

app.include_router(auth.router, tags=['auth'], prefix=PREFIX_API)
app.include_router(user.router, tags=['users'], prefix=PREFIX_API)
app.include_router(order.router, tags=['orders'], prefix=PREFIX_API)
app.include_router(products.router, tags=['products'], prefix=PREFIX_API)
app.include_router(dashboard.router, tags=['dashboard'], prefix='/dashboard')

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
