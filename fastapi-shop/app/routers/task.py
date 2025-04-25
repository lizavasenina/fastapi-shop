"""Module providing task routes."""

from typing import List, Union
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services import task_service
from models import User
from dependencies import get_db
from auth.auth_handler import get_current_admin_user

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=Union[List[int], dict])
def get_solution(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin_user)):
    """Gets task solution"""
    return task_service.task(db)
