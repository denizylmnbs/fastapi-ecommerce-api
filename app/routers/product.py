from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import product as product_schema
from app.crud import product as product_crud
from app.crud import category as category_crud
from app.dependencies import get_current_user
from app.schemas import user as user_schema

router = APIRouter(
    prefix="/products",
    tags=["products"]
)

@router.post("/", response_model=product_schema.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Yönetici yetkisi gereklidir")
    
    if product.category_id is not None:
        db_category = category_crud.get_category(db, category_id=product.category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail="Kategori bulunamadı")
    
    return product_crud.create_product(db=db, product=product)

@router.get("/{product_id}", response_model=product_schema.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return db_product

@router.get("/", response_model=list[product_schema.ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return product_crud.get_all_products(db=db)

@router.put("/{product_id}", response_model=product_schema.ProductResponse)
def update_product(product_id: int, product: product_schema.ProductCreate, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Yönetici yetkisi gereklidir")
    
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    db_product.name = product.name
    db_product.category = product.category_id
    db_product.description = product.description
    db_product.price = product.price
    db_product.stock = product.stock
    
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: user_schema.UserResponse = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")
    
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Yönetici yetkisi gereklidir")
    
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    db.delete(db_product)
    db.commit()