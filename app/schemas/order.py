from pydantic import BaseModel

class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True