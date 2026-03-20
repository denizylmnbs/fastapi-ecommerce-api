from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import cartItem as cart_item_schema
from app.crud import cartItem as cart_item_crud
from app.crud import cart as cart_crud
from app.models.cartItem import CartItem
from app.dependencies import get_current_user
from app.schemas import user as user_schema

router = APIRouter(
    prefix="/cart/items",
    tags=["cart items"]
)

@router.post("/", response_model=cart_item_schema.CartItemResponse)
def add_cart_item(cart_item: cart_item_schema.CartItemCreate, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    user_cart = cart_crud.get_cart(db, user=current_user)
    if user_cart is None:
        raise HTTPException(status_code=404, detail="Kullanıcının sepeti bulunamadı")
    
    if cart_item_crud.check_stock_availability(db, product_id=cart_item.product_id, quantity=cart_item.quantity) == False:
        raise HTTPException(status_code=400, detail="Yeterli stok bulunmamaktadır")

    for item in user_cart.items:
        if item.product_id == cart_item.product_id:
            return cart_item_crud.increase_cart_item_quantity(db=db, cart_item_id=item.id)
        
    return cart_item_crud.create_cart_item(db=db, cart_item=cart_item, user=current_user)

@router.get("/", response_model=list[cart_item_schema.CartItemResponse])
def get_cart_items(db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")

    return cart_item_crud.get_cart_items(db=db, user=current_user)

@router.put("/{cart_item_id}", response_model=cart_item_schema.CartItemResponse)
def update_cart_item_quantity(cart_item_id: int, quantity: int, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if cart_item_crud.check_stock_availability(db, product_id=cart_item.product_id, quantity=quantity) == False:
        raise HTTPException(status_code=400, detail="Yeterli stok bulunmamaktadır")

    updated_cart_item = cart_item_crud.update_cart_item_quantity(db=db, cart_item_id=cart_item_id, quantity=quantity)
    if updated_cart_item is None:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    
    return updated_cart_item

@router.delete("/{cart_item_id}")
def delete_cart_item(cart_item_id: int, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")

    success = cart_item_crud.delete_cart_item(db=db, cart_item_id=cart_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    
    return {"detail": "Sepet öğesi başarıyla silindi"}

@router.patch("/{cart_item_id}/increase", response_model=cart_item_schema.CartItemResponse)
def increase_cart_item_quantity(cart_item_id: int, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if cart_item_crud.check_stock_availability(db, product_id=cart_item.product_id, quantity=(cart_item.quantity + 1)) == False:
        raise HTTPException(status_code=400, detail="Yeterli stok bulunmamaktadır")

    updated_cart_item = cart_item_crud.increase_cart_item_quantity(db=db, cart_item_id=cart_item_id)
    if updated_cart_item is None:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    
    return updated_cart_item

@router.patch("/{cart_item_id}/decrease", response_model=cart_item_schema.CartItemResponse)
def decrease_cart_item_quantity(cart_item_id: int, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if cart_item_crud.check_stock_availability(db, product_id=cart_item.product_id, quantity=(cart_item.quantity - 1)) == False:
        raise HTTPException(status_code=400, detail="Yeterli stok bulunmamaktadır")

    updated_cart_item = cart_item_crud.decrease_cart_item_quantity(db=db, cart_item_id=cart_item_id)
    if updated_cart_item is None:
        raise HTTPException(status_code=404, detail="Sepet öğesi bulunamadı")
    
    return updated_cart_item