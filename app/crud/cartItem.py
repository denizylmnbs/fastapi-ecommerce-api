from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.user import User
from app.models.cartItem import CartItem
from app.schemas.cartItem import CartItemCreate, CartItemResponse

def create_cart_item(db: Session, cart_item: CartItemCreate, user: User):
    cart_id = db.query(User).filter(User.id == user.id).first().cart.id
    if not cart_id:
        return None

    db_cart_item = CartItem(
        cart_id=cart_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def get_cart_items(db: Session, user: User):
    cart_id = db.query(User).filter(User.id == user.id).first().cart.id
    return db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

def delete_cart_item(db: Session, cart_item_id: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return True
    return False

def update_cart_item_quantity(db: Session, cart_item_id: int, quantity: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.commit()
        db.refresh(cart_item)
        return cart_item
    return None

def increase_cart_item_quantity(db: Session, cart_item_id: int):
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    if cart_item:
        cart_item.quantity += 1
        db.commit()
        db.refresh(cart_item)
        return cart_item
    return None