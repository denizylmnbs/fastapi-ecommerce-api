from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import user as user_schema
from app.crud import user as user_crud

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email zaten kayıtlı")
    return user_crud.create_user(db=db, user=user)

@router.get("/me", response_model=user_schema.UserResponse)
def get_my_profile(current_user: user_schema.UserResponse = Depends(get_current_user)):
    return current_user