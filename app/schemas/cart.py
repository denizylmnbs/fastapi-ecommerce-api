from pydantic import BaseModel
from datetime import datetime

class CartBase(BaseModel):
    pass

class CartCreate(CartBase):
    pass

class CartResponse(CartBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True