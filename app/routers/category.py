from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import category as category_schema
from app.crud import category as category_crud, user
from app.schemas import user as user_schema

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.post("/", response_model=category_schema.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Yönetici yetkisi gereklidir")
    
    return category_crud.create_category(db=db, category=category)

@router.get("/{category_id}", response_model=category_schema.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    return db_category

@router.get("/", response_model=list[category_schema.CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return category_crud.get_all_categories(db=db)

@router.put("/{category_id}", response_model=category_schema.CategoryResponse)
def update_category(category_id: int, category: category_schema.CategoryCreate, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Yönetici yetkisi gereklidir")
    
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    db_category.name = category.name
    
    db.commit()
    db.refresh(db_category)
    
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Yönetici yetkisi gereklidir")
    
    db_category = category_crud.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    category_crud.delete_category(db=db, category_id=category_id)