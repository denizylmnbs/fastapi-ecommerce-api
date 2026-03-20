from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    name: str
    surname: str

class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True