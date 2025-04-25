from datetime import datetime
from pydantic import BaseModel

class Order(BaseModel):
    user_id: int
    order_date: datetime
    status: bool
    priority: int

class OrderRecord(Order):
    order_id: int

class OrderUpdate(Order):
    pass

class OrderResponse(OrderRecord):
    pass