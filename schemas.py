from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError
from fastapi import HTTPException, status
from typing import Optional
import logging

# Пользователь
 
class UserBase(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str
    
# Категория

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = ""

class Category(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    
# Продукт

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = ""
    price_for_itm:  Optional[float] = 0
    weight_for_itm: Optional[float] = 0
    
    is_active: Optional[bool] = False
    category_id: Optional[int] = None

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
        
        
class Product(BaseModel):
    id: int
    title: str
    description: Optional[str] = ""
    price_for_itm: float
    weight_for_itm: float
    
    is_active: bool
    category_id: Optional[int] = None
    
    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True
