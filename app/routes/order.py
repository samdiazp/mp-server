from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.database import get_db, SessionLocal
from app.utils import auth
from app.models import order as order_model, user as user_model
from app.schemas import order, user, product 
from app.schemas.base import  BasicResponse
from app.repositories import orders

router = APIRouter()

@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(data: order.OrderCreate, db: SessionLocal = Depends(get_db), user: user.User = Depends(auth.get_me)) ->BasicResponse:
    order_repo = orders.OrderRepo(db)
    try:
        new_order = order_repo.create(order_model.Order(user_id=user.id, **data.dict()))
        return BasicResponse(ok=True, data=new_order)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creando al orden")

@router.put("/orders/products/{order_id}", status_code=status.HTTP_201_CREATED)
def add_products_to_order(order_id: int, data: order.AddProductOrder, db: SessionLocal = Depends(get_db)):
    try: 
        order_repo = orders.OrderRepo(db)
        order_repo.add_products_to_order(order_id=order_id, products_id=data.products_id)
        return BasicResponse(ok=True)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error agregando la orden")

@router.get("/orders/{order_id}", status_code=status.HTTP_200_OK)
def get_order_by_id(order_id:int, db: SessionLocal = Depends(get_db)) -> BasicResponse:
    try: 
        order_repo = orders.OrderRepo(db)
        order_founded = order_repo.get_by_id(order_id)
        if not order_founded:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La orden no existe")
        return BasicResponse(ok=True, data=order.Order.from_orm(order_founded))
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error obteniendo la orden")

@router.get("/orders", status_code=status.HTTP_200_OK)
def get_orders(skip: int = 0, limit: int = 25, db: SessionLocal = Depends(get_db)) ->  BasicResponse:
    try: 
        order_repo = orders.OrderRepo(db)
        orders_sch = []
        for order_mod in order_repo.get(offset=skip, limit=limit):
            orders_sch.append(order.Order.from_orm(order_mod))
        return BasicResponse(ok=True, data=orders_sch)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error obteniendo las ordenes")

@router.put("/orders/{order_id}", status_code=status.HTTP_201_CREATED, response_model=BasicResponse)
def update_order(order_id: int, data: order.OrderUpdate, db: SessionLocal = Depends(get_db)) -> BasicResponse:
    order_repo = orders.OrderRepo(db)
    founded = order_repo.get_by_id(order_id)
    try: 
        if not founded:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La orden no existe")

        updated = order_repo.update(founded, **data.dict(exclude_none=True))
        return BasicResponse(ok=True, data=updated)

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error actualizando la orden")