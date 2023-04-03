from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db, SessionLocal
from utils import auth
from models import order as order_model, user as user_model
from schemas import order, user, product 
from schemas.base import  BasicResponse
from repositories import orders, products

router = APIRouter()


@router.post("/products", response_model=product.Product, status_code=status.HTTP_201_CREATED)
def create_product(data: product.ProductCreate, db: SessionLocal = Depends(get_db), user: user.User = Depends(auth.get_me)):
    product_repo = products.ProductRepo(db)
    new_product = product_repo.create(order_model.Product(**data.dict()))

    return product.Product.from_orm(new_product)

@router.get("/products", response_model=BasicResponse, status_code=status.HTTP_200_OK)
def get_products(limit: int = 25, skip: int = 0, db: SessionLocal = Depends(get_db), user: user.User = Depends(auth.get_me)):
    product_repo = products.ProductRepo(db)

    products_schm = []
    try:

        for prod_mod in product_repo.get(offset=skip, limit=limit):
            products_schm.append(product.Product.from_orm(prod_mod))
    except:
        raise HTTPException(status_code=400, detail="no se pudo obtener los productos")

    return BasicResponse(ok=True, data=products_schm)