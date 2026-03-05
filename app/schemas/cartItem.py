from pydantic import BaseModel
from datetime import datetime

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    created_at: datetime

    class Config:
        from_attributes = True