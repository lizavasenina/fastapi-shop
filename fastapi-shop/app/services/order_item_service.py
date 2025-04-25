from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import OrderItem
from models import Order
from services import product_service
from services import order_service
from schemas.order_item import OrderItemCreate
from schemas.order_item import OrderItemUpdate
from schemas.order_item import OrderItemResponse
from typing import List

def get_order_item( db: Session, order_item_id: int) -> OrderItemResponse:
    order_item_query = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id)
    db_order_item = order_item_query.first()

    if not db_order_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No order item with this id: {order_item_id} found')
    
    return db_order_item

def get_order_items(db: Session, user_id: int | None = None) -> List[OrderItemResponse]:
    if user_id:
        return db.execute(select(OrderItem).join(Order, Order.order_id == OrderItem.order_id).where(Order.user_id == user_id).order_by(OrderItem.order_id)).scalars().all()
    return db.query(OrderItem).order_by(OrderItem.order_id).all()

def create_order_item(db: Session, order_item: OrderItemCreate) -> OrderItemResponse:
    product = product_service.get_product(db, order_item.product_id)
    check_product_stock(product.stock, order_item.products_count)
    
    db_order_item = OrderItem(products_count = order_item.products_count, 
                order_id = order_item.order_id, 
                product_id = order_item.product_id)
    
    db.add(db_order_item)
    db.commit()
    db.refresh(db_order_item)

    product.stock -= db_order_item.products_count
    product_service.update_product(db, product.product_id, product)

    return db_order_item

def check_product_stock(stock, count) -> None:
    if (stock < count):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'The count of products in the order is more than the stock (stock: {stock}, count: {count})')

def update_order_item(db: Session, order_item_id: int, order_item_update: OrderItemUpdate) -> OrderItemResponse:
    db_order_item = get_order_item(db, order_item_id)

    db_product = product_service.get_product(db, order_item_update.product_id)
    db_order_item.product_id = db_product.product_id
    
    check_product_stock(db_product.stock + db_order_item.products_count, order_item_update.products_count)
    db_product.stock += db_order_item.products_count - order_item_update.products_count
    db_order_item.products_count = order_item_update.products_count
    
    db_order = order_service.get_order(db, order_item_update.order_id)
    db_order_item.order_id = db_order.order_id

    db.commit()
    db.refresh(db_order_item)
    return db_order_item

def delete_order_item(db: Session, order_item_id: int) -> dict:
    db_order_item = get_order_item(db, order_item_id)
    db_order = order_service.get_order(db, db_order_item.order_id)
    
    if db_order.status:
        return {"message": f'Order with id {db_order.order_id} is already completed, impossible to delete order item'}
    
    db_product = product_service.get_product(db, db_order_item.product_id)
    db_product.stock += db_order_item.products_count
    
    db.delete(db_order_item)
    db.commit()
    return {"message": f'OrderItem with id {order_item_id} deleted successfully'}

def get_user_id(db: Session, order_item_id: int) -> int:
    db_order_item = get_order_item(db, order_item_id)
    return order_service.get_user_id(db, db_order_item.order_id)