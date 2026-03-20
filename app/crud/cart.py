from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.user import User
from app.schemas.cart import CartCreate, CartResponse

def create_cart(db: Session, user: User):
    db_cart = Cart(user_id=user.id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart(db: Session, user: User):
    return db.query(Cart).filter(Cart.user_id == user.id).first()

def delete_cart(db: Session, user: User):
    db_cart = get_cart(db, user)
    if db_cart:
        db.delete(db_cart)
        db.commit()
        return True
    return False