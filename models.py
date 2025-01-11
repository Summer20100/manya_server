from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Модель клиента
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    # Связь с заказами
    orders = relationship("Order", back_populates="client", cascade="all, delete")


# Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    total_price = Column(Numeric(10, 2), nullable=False, default=1)
    total_weight = Column(Numeric(10, 2), nullable=False, default=1)
    adres = Column(String, nullable=False)
    comment = Column(String, default="")
    is_active = Column(Boolean, default=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Связи
    client = relationship("Client", back_populates="orders")
    product = relationship("Product", back_populates="orders")

# Модель категории
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    img_URL = Column(String, default="")
    img_title = Column(String, default="")

    # Связь с продуктами, при удалении Category обновляется поле category_id в Product
    products = relationship(
        "Product", 
        back_populates="category", 
        passive_deletes=True
    )


# Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    img_URL = Column(String, default="")
    img_title = Column(String, default="")
    price_for_itm = Column(Numeric(10, 2), default=0)
    weight_for_itm = Column(Numeric(10, 2), default=0)

    is_active = Column(Boolean, default=False)
    category_id = Column(
        Integer, 
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )

    # Связи
    category = relationship("Category", back_populates="products")
    orders = relationship("Order", back_populates="product", cascade="all, delete")
