"""Module providing order routes."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.order import OrderResponse
from schemas.order import OrderUpdate
from services import order_service
from dependencies import get_db
from models import User
from auth.auth_handler import get_current_admin_user, get_current_user, verify_current_user_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user_order)):
    """Gets order"""
    return order_service.get_order(db, order_id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)):
    """Gets orders"""
    if user_data.is_admin:
        return order_service.get_orders(db, skip, limit)
    return order_service.get_orders(db, skip, limit, user_data.user_id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def create_order(db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    """Creates order"""
    return order_service.create_order(db, user_data.user_id)

@router.post("/{user_id}", status_code=status.HTTP_201_CREATED, response_model=OrderResponse)
def add_order(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Adds order"""
    return order_service.create_order(db, user_id)

@router.put("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderResponse)
def update_order(
    order_id: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Updates order"""
    return order_service.update_order(db, order_id, order)

@router.delete("/{order_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user_order)):
    """Deletes order"""
    return order_service.delete_order(db, order_id)
