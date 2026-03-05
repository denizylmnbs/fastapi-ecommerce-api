from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import cart as cart_schema
from app.crud import cart as cart_crud
from app.dependencies import get_current_user
from app.schemas import user as user_schema

router = APIRouter(
    prefix="/cart",
    tags=["cart"]
)

@router.post("/", response_model=cart_schema.CartResponse)
def create_cart(cart: cart_schema.CartCreate, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    existing_cart = cart_crud.get_cart(db, user_id=current_user.id)
    if existing_cart:
        raise HTTPException(status_code=400, detail="Kullanıcının zaten bir sepeti var")
    
    return cart_crud.create_cart(db=db, cart=cart, user_id=current_user.id)

@router.get("/", response_model=cart_schema.CartResponse)
def get_cart(db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    db_cart = cart_crud.get_cart(db, user_id=current_user.id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Sepet bulunamadı")
    
    return db_cart