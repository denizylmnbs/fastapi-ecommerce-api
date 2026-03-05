from sqlalchemy.orm import Session
from app.models.orderItem import OrderItem
from app.schemas.orderItem import OrderItemCreate, OrderItemResponse

def create_order_item(db: Session, order_item: OrderItemCreate):
    db_order_item = OrderItem(
        order_id=order_item.order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price_at_purchase=0.0  # This should be set to the actual product price at purchase time
    )
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def get_order_item(db: Session, order_item_id: int):
    return db.query(OrderItem).filter(OrderItem.id == order_item_id).first()

def get_order_items_by_order(db: Session, order_id: int):
    return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()

def delete_order_item(db: Session, order_item_id: int):
    db_order_item = get_order_item(db, order_item_id=order_item_id)
    if db_order_item is None:
        return None
    
    db.delete(db_order_item)
    db.commit()
    
    return db_order_item