from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Category
from schemas.category import CategoryCreate
from schemas.category import CategoryUpdate
from schemas.category import CategoryResponse
from typing import List

def get_category( db: Session, category_id: int) -> CategoryResponse:
    category_query = db.query(Category).filter(Category.category_id == category_id)
    db_category = category_query.first()

    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No category with this id: {category_id} found')
    
    return db_category

def get_categories(db: Session, skip: int, limit: int) -> List[CategoryResponse]:
    allCategories = db.query(Category).offset(skip).limit(limit).all()
    return allCategories

def create_category(db: Session, category: CategoryCreate) -> CategoryResponse:
    db_category = Category(category_name = category.category_name)
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: CategoryUpdate) -> CategoryResponse:
    db_category = get_category(db, category_id)

    db_category.category_name = category_update.category_name

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> dict:
    db_category = get_category(db, category_id)
    db.delete(db_category)
    db.commit()
    return {"message": f'Category with id {category_id} deleted successfully'}