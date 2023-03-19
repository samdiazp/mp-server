from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db, SessionLocal
from app.utils import auth
from app.models import order as order_model, user as user_model
from app.schemas import order, user, product 
from app.schemas.base import  BasicResponse
from app.repositories import orders

router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(data: order.OrderCreate, db: SessionLocal = Depends(get_db)):
    order_repo = orders.OrderRepo(db)
    try:
        new_order = order_repo.create(order_model.Order(**data.dict()))
        return BasicResponse(ok=True, data=new_order)
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating the order")

@router.put("/orders/products/{order_id}", status_code=status.HTTP_201_CREATED)
def add_products_to_order(order_id: int, data: order.AddProductOrder, db: SessionLocal = Depends(get_db)):
    try: 
        order_repo = orders.OrderRepo(db)
        order_repo.add_products_to_order(order_id=order_id, products_id=data.products_id)
        return BasicResponse(ok=True, data=None)
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error adding the products to order")

@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order_by_id(order_id:int, db: SessionLocal = Depends(get_db)):
    try: 
        order_repo = orders.OrderRepo(db)
        order_founded = order_repo.get_by_id(order_id)
        return BasicResponse(ok=True, data=order.Order(**order_founded.as_dict()))
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error getting the orders")

@router.get("/orders", status_code=status.HTTP_200_OK)
def get_orders(skip: int = 0, limit: int = 25, db: SessionLocal = Depends(get_db)):
    try: 
        order_repo = orders.OrderRepo(db)
        orders_sch = []
        for order_mod in order_repo.get(offset=skip, limit=limit):
            orders_sch.append(order.Order(**order_mod.as_dict(), user=order_mod.user))
        return BasicResponse(ok=True, data=orders_sch)
    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error getting the order")
