from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.product import ProductResponse

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    items = List[ProductResponse] = []
    

    class Config:
        from_attributes = True