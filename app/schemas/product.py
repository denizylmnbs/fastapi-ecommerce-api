from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None
    price: int

class ProductCreate(ProductBase):
    stock: Optional[int] = 0

class ProductResponse(ProductBase):
    id: int
    stock: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True