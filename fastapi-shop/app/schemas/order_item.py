from pydantic import BaseModel, field_validator

class OrderItem(BaseModel):
    products_count: int
    order_id: int
    product_id: int
    
    @field_validator("products_count")
    def validate_products_count(cls, value):
        if value <= 0:
            raise ValueError("Products count must be greater than 0")
        return value

class OrderItemRecord(OrderItem):
    order_item_id: int

class OrderItemCreate(OrderItem):
    pass

class OrderItemUpdate(OrderItem):
    pass

class OrderItemResponse(OrderItemRecord):
    pass