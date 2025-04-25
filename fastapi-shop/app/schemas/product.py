from pydantic import BaseModel

class Product(BaseModel):
    product_name: str
    length: int
    width: int
    height: int
    weight: float
    price: float
    stock: int
    category_id: int

class ProductRecord(Product):
    product_id: int

class ProductCreate(Product):
    pass

class ProductUpdate(Product):
    pass

class ProductResponse(ProductRecord):
    pass