"""Module providing category routes."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.category import CategoryCreate
from schemas.category import CategoryResponse
from services import category_service
from dependencies import get_db
from models import User
from auth.auth_handler import get_current_admin_user

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Gets category"""
    return category_service.get_category(db, category_id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Gets categories"""
    return category_service.get_categories(db, skip, limit)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Creates category"""
    return category_service.create_category(db, category)

@router.put("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Updates category"""
    return category_service.update_category(db, category_id, category)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Deletes category"""
    return category_service.delete_category(db, category_id)
