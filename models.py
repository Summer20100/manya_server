from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

# Модель клиента
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)

    # Связь с заказами, при удалении Client, удаляется Order
    orders = relationship("Order", back_populates="client", cascade="all, delete")


# Модель заказа
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    adres = Column(String, nullable=False)
    comment = Column(String, default="")
    is_active = Column(Boolean, default=True)
    date = Column(Date, nullable=False)
    

    # Связи
    client = relationship("Client", back_populates="orders")
    product = relationship("Product", back_populates="orders")


# Модель категории
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, default="")

    # Связь с продуктами, при удалении Category обновляются поля в Product
    products = relationship("Product", back_populates="category", cascade="all", passive_deletes=True)


# Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    price_for_itm = Column(Numeric(10, 2), default=0)
    weight_for_itm = Column(Numeric(10, 2), default=0)

    is_active = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Связи
    category = relationship("Category", back_populates="products")
    orders = relationship("Order", back_populates="product", cascade="all, delete")


