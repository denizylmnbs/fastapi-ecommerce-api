from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.models.cartItem import CartItem
from app.schemas.cartItem import CartItemCreate, CartItemResponse

def create_cart_item(db: Session, cart_item: CartItemCreate, user_id: int):
    is_existence = db.query(CartItem)\
    .join(Cart)\
    .filter(Cart.user_id == user_id, CartItem.product_id == cart_item.product_id)\
    .first()
    
    cart_id = db.query(Cart.id).filter(Cart.user_id == user_id).first()
    if not cart_id:
        return None

    if is_existence: # If the same product already exists in the cart, just update the quantity
        is_existence.quantity += cart_item.quantity
        db.commit()
        db.refresh(is_existence)
        return is_existence

    db_cart_item = CartItem(
        cart_id=cart_id.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def get_cart_items(db: Session, user_id: int):
    cart_id = db.query(Cart.id).filter(Cart.user_id == user_id).first().id
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