from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

# Модель пользователя

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    
# Модель категории

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, index=True)
