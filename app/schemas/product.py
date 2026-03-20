from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.schemas.category import CategoryResponse

class ProductBase(BaseModel):
    name: str
    category_id: int
    description: Optional[str] = None
    price: float = Field(..., gt=0)  # Price must be greater than 0

class ProductCreate(ProductBase):
    stock: Optional[int] = Field(0, ge=0)  # Stock must be greater than or equal to 0

class ProductResponse(ProductBase):
    id: int
    stock: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    #category: Optional["CategoryResponse"] = None

    class Config:
        from_attributes = True

from app.schemas.category import CategoryResponse
ProductResponse.model_rebuild() # This is necessary because we blocked the circular import with TYPE_CHECKİNG