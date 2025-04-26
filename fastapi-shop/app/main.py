"""Main module."""

from fastapi import FastAPI
from routers.user import router as user_router
from routers.product import router as product_router
from routers.order import router as order_router
from routers.order_item import router as order_item_router
from routers.category import router as category_router
from routers.task import router as task_router
from routers.auth import router as auth_router

app = FastAPI(
    title="Интернет-магазин",
    description="Простейшая система управления онлайн-заказами "
    "в интернет-магазине мебели и бытовой техники, "
    "основанная на фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Васенина Елизавета Андреевна",
        "email": "vasenina.ea@phystech.edu",
    }
)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(order_item_router)
app.include_router(category_router)
app.include_router(task_router)
app.include_router(auth_router)
