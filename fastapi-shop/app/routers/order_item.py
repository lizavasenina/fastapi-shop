"""Module providing order item routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.order_item import OrderItemCreate
from schemas.order_item import OrderItemResponse
from services import order_item_service
from services import order_service
from models import User
from auth.auth_handler import get_current_user, verify_current_user_order_item
from dependencies import get_db

router = APIRouter(prefix="/order_items", tags=["order_items"])

@router.get("/{order_item_id}", status_code=status.HTTP_200_OK, response_model=OrderItemResponse)
def get_order_item(
    order_item_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user_order_item)):
    """Gets order item"""
    return order_item_service.get_order_item(db, order_item_id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[OrderItemResponse])
def get_order_items(db: Session = Depends(get_db), user_data: User = Depends(get_current_user)):
    """Gets order items"""
    if user_data.is_admin:
        return order_item_service.get_order_items(db)
    return order_item_service.get_order_items(db, user_data.user_id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderItemResponse)
def create_order_item(
    order_item: OrderItemCreate,
    db: Session = Depends(get_db),
    user_data: User = Depends(get_current_user)):
    """Creates order item"""
    user_id = order_service.get_user_id(db, order_item.order_id)
    if user_data.is_admin or user_data.user_id == user_id:
        return order_item_service.create_order_item(db, order_item)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access')

@router.put("/{order_item_id}", status_code=status.HTTP_200_OK, response_model=OrderItemResponse)
def update_order_item(
    order_item_id: int,
    order_item: OrderItemCreate,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user_order_item)):
    """Updates order item"""
    return order_item_service.update_order_item(db, order_item_id, order_item)

@router.delete("/{order_item_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_order_item(
    order_item_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user_order_item)):
    """Deletes order item"""
    return order_item_service.delete_order_item(db, order_item_id)
