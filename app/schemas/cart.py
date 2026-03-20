from pydantic import BaseModel
from typing import List
from app.schemas.cartItem import CartItemResponse

class CartBase(BaseModel):
    pass

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    id: int
    user_id: int    
    items: List[CartItemResponse]
    total_price: float

    class Config:
        from_attributes = True