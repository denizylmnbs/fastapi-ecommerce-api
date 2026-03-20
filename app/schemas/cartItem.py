from pydantic import BaseModel, Field
from app.schemas.product import ProductResponse

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = Field(1, ge=1)

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    product: ProductResponse
    item_total_price: float

    class Config:
        from_attributes = True