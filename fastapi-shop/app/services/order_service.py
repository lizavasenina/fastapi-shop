from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Order
from models import OrderItem
from services import product_service
from schemas.order import OrderUpdate
from schemas.order import OrderResponse
from services.user_service import get_user
from typing import List

def get_order( db: Session, order_id: int) -> OrderResponse:
    order_query = db.query(Order).filter(Order.order_id == order_id)
    db_order = order_query.first()

    if not db_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No order with this id: {order_id} found')
    
    return db_order

def get_orders(db: Session, skip: int, limit: int, user_id: int | None = None) -> List[OrderResponse]:
    query = db.query(Order)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    return query.offset(skip).limit(limit)

def create_order(db: Session, user_id: int) -> OrderResponse:
    db_user = get_user(db, user_id)
    db_order = Order(user_id = db_user.user_id)
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> OrderResponse:
    db_order = get_order(db, order_id)

    db_order.order_date = order_update.order_date
    
    db_user = get_user(db, order_update.user_id)
    db_order.user_id = db_user.user_id
    
    db_order.priority = order_update.priority
    db_order.status = order_update.status

    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int) -> dict:
    db_order = get_order(db, order_id)
    
    if not db_order.status:
        order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        for item in order_items:
            db_product = product_service.get_product(db, item.product_id)
            db_product.stock += item.products_count
        
    db.delete(db_order)
    db.commit()
    return {"message": f'Order with id {order_id} deleted successfully'}

def get_user_id(db: Session, order_id: int) -> int:
    db_order = get_order(db, order_id)
    return db_order.user_id
