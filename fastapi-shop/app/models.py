"""Module providing database models."""

from datetime import datetime
from db.database import Base, pk
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql.expression import text

class Category(Base):
    """Class providing a category model."""
    __tablename__ = "categories"

    category_id: Mapped[pk]
    category_name: Mapped[str]

    products: Mapped[list["Product"]] = relationship(
        "Product",
        back_populates="category",
        cascade="all, delete-orphan",
        passive_deletes=True)

class OrderItem(Base):
    """Class providing a order item model."""
    __tablename__ = "order_items"

    order_item_id: Mapped[pk]
    products_count: Mapped[int]

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.order_id", ondelete="CASCADE"),
        nullable=False)
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="order_items")

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.product_id", ondelete="CASCADE"),
        nullable=False)
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="order_items")

class Order(Base):
    """Class providing a order model."""
    __tablename__ = "orders"

    order_id: Mapped[pk]
    order_date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    status: Mapped[bool] = mapped_column(server_default="false")
    priority: Mapped[int] = mapped_column(server_default="1")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="orders")

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True)

class Product(Base):
    """Class providing a product model."""
    __tablename__ = "products"

    product_id: Mapped[pk]
    product_name: Mapped[str]
    length: Mapped[int]
    width: Mapped[int]
    height: Mapped[int]
    weight: Mapped[float]
    price: Mapped[float]
    stock: Mapped[int]

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.category_id", ondelete="CASCADE"),
        nullable=False)
    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="products")

    order_items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True)

class User(Base):
    """Class providing a user model."""
    __tablename__ = "users"

    user_id: Mapped[pk]
    email: Mapped[str]
    password: Mapped[str]
    user_name: Mapped[str]
    birth_date: Mapped[datetime]
    sex: Mapped[bool]

    is_admin: Mapped[bool] = mapped_column(
        default=False,
        server_default=text('false'),
        nullable=False)

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True)
