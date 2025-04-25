"""Module providing product routes."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.product import ProductCreate
from schemas.product import ProductResponse
from services import product_service
from dependencies import get_db
from models import User
from auth.auth_handler import get_current_admin_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Gets product"""
    return product_service.get_product(db, product_id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Gets products"""
    return product_service.get_products(db, skip, limit)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Creates product"""
    return product_service.create_product(db, product)

@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Updates product"""
    return product_service.update_product(db, product_id, product)

@router.delete("/{product_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Deletes product"""
    return product_service.delete_product(db, product_id)

@router.patch("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
def change_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Changes product stock"""
    return product_service.change_stock(db, product_id, quantity)
