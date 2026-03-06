from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.product import ProductResponse

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    items: List["ProductResponse"] = []

    class Config:
        from_attributes = True

from app.schemas.product import ProductResponse 
CategoryResponse.model_rebuild()    # This is necessary because we blocked the circular import with TYPE_CHECKİNG