"""Module providing user routes."""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.user import UserResponse
from schemas.user import UserUpdate
from services import user_service
from dependencies import get_db
from models import User
from auth.auth_handler import get_current_admin_user, verify_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(verify_current_user)):
    """Gets user"""
    return user_service.get_user(db, user_id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Gets users"""
    return user_service.get_users(db, skip, limit)

@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse,)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user)):
    """Updates user"""
    return user_service.update_user(db, user_id, user)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=dict)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(verify_current_user)):
    """Deletes user"""
    return user_service.delete_user(db, user_id)
