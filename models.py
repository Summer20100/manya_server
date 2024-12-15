from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from database import Base

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

# Модель категории
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, default="")

# Модель продукта
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    description = Column(String, default="")
    price_for_itm = Column(Numeric(10, 2), default=0)
    weight_for_itm = Column(Numeric(10, 2), default=0)

    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, nullable=True)

    # __table_args__ = (
    #     CheckConstraint(price_for_itm >= 0, name="Стоимость не может быть меньше 0"),
    #     CheckConstraint(weight_for_itm >= 0, name="Вес не может быть меньше 0"),
    #     CheckConstraint("price_for_itm ~ '^(?!0\\d)(\\d+(\\.\\d{1,2})?)$'", name="Стоимость должна быть в формате 00.00"),
    #     CheckConstraint("weight_for_itm ~ '^(?!0\\d)(\\d+(\\.\\d{1,2})?)$'", name="Вес должн быть в формате 00.00"),
    # )
