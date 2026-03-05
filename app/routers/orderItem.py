from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import orderItem as crud_order_item
from app.schemas.orderItem import OrderItemCreate, OrderItemResponse
from app.database import get_db

router = APIRouter(prefix="/order-items", tags=["order-items"])
@router.post("/", response_model=OrderItemResponse)
def create_order_item(order_item: OrderItemCreate, db: Session = Depends(get_db)):
    db_order_item = crud_order_item.create_order_item(db, order_item)
    return db_order_item

@router.get("/{order_item_id}", response_model=OrderItemResponse)
def read_order_item(order_item_id: int, db: Session = Depends(get_db)):
    db_order_item = crud_order_item.get_order_item(db, order_item_id)
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_order_item

@router.get("/order/{order_id}", response_model=list[OrderItemResponse])
def read_order_items_by_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order_item.get_order_items_by_order(db, order_id)

@router.delete("/{order_item_id}", response_model=OrderItemResponse)
def delete_order_item(order_item_id: int, db: Session = Depends(get_db)):
    db_order_item = crud_order_item.delete_order_item(db, order_item_id)
    if db_order_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_order_item

