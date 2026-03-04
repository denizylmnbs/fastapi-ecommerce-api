from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_all_categories(db: Session):
    return db.query(Category).all()

def update_category(db: Session, category_id: int, category: CategoryCreate):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        return None
    
    db_category.name = category.name
    db_category.description = category.description
    
    db.commit()
    db.refresh(db_category)
    
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id=category_id)
    if db_category is None:
        return None
    
    db.delete(db_category)
    db.commit()
    
    return db_category