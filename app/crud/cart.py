from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.schemas.cart import CartCreate, CartResponse

def create_cart(db: Session, cart: CartCreate, user_id: int):
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).first()