from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse

def create_order(db: Session, order: OrderCreate):
    db_order = Order(
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()

def update_order_status(db: Session, order_id: int, status: str):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        return None
    
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        return None
    
    db.delete(db_order)
    db.commit()
    
    return db_order