from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Product
from services.category_service import get_category
from schemas.product import ProductCreate
from schemas.product import ProductUpdate
from schemas.product import ProductResponse
from typing import List

def get_product(db: Session, product_id: int) -> ProductResponse:
    product_query = db.query(Product).filter(Product.product_id == product_id)
    db_product = product_query.first()

    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No product with this id: {product_id} found')
    
    return db_product

def get_products(db: Session, skip: int, limit: int) -> List[ProductResponse]:
    allProducts = db.query(Product).offset(skip).limit(limit).all()
    return allProducts

def create_product(db: Session, product: ProductCreate) -> ProductResponse:
    db_product = Product(product_name = product.product_name, 
                length = product.length, 
                width = product.width,
                height = product.height, 
                weight = product.weight, 
                price = product.price, 
                stock = product.stock, 
                category_id = product.category_id )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> ProductResponse:
    db_product = get_product(db, product_id)

    db_product.product_name = product_update.product_name
    db_product.length = product_update.length
    db_product.width = product_update.width
    db_product.height = product_update.height
    db_product.weight = product_update.weight
    db_product.price = product_update.price
    db_product.stock = product_update.stock
    
    db_category = get_category(db, product_update.category_id)
    db_product.category_id = db_category.category_id

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> dict:
    db_product = get_product(db, product_id)
    db.delete(db_product)
    db.commit()
    return {"message": f'Product with id {product_id} deleted successfully'}

def change_stock(db: Session, product_id: int, quantity: int) -> ProductResponse:
    db_product = get_product(db, product_id)
    result = db_product.stock + quantity
    
    if result < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Product stock cannot be less than 0: {result}')
    
    db_product.stock = result
    db.commit()
    db.refresh(db_product)
    return db_product