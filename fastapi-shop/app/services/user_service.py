from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
from models import Order
from models import OrderItem
from services import product_service
from schemas.user import UserUpdate
from schemas.user import UserResponse
from typing import List

def get_user(db: Session, user_id: int) -> UserResponse:
    user_query = db.query(User).filter(User.user_id == user_id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {user_id} found')
    
    return db_user

def get_user_by_email(db: Session, email: str) -> (User | None):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int, limit: int) -> List[UserResponse]:
    allUsers = db.query(User).offset(skip).limit(limit).all()
    return allUsers

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> UserResponse:
    db_user = get_user(db, user_id)

    db_user.user_name = user_update.user_name
    db_user.birth_date = user_update.birth_date
    db_user.sex = user_update.sex

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> dict:
    db_user = get_user(db, user_id)
    unfinished_orders = db.query(Order).filter(Order.user_id == db_user.user_id and not Order.status).all()
    
    for order in unfinished_orders:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order.order_id).all()
        for item in order_items:
            db_product = product_service.get_product(db, item.product_id)
            db_product.stock += item.products_count
    
    db.delete(db_user)
    db.commit()
    return {"message": f'User with id {user_id} deleted successfully'}