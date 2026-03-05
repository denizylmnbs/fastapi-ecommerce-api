from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import order as crud_order
from app.schemas.order import OrderCreate, OrderResponse
from app.database import get_db

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = crud_order.create_order(db, order)
    return db_order

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.get_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.get("/user/{user_id}", response_model=list[OrderResponse])
def read_orders_by_user(user_id: int, db: Session = Depends(get_db)):
    return crud_order.get_orders_by_user(db, user_id)

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    db_order = crud_order.update_order_status(db, order_id, status)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.delete("/{order_id}", response_model=OrderResponse)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud_order.delete_order(db, order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order