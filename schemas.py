from pydantic import BaseModel, field_validator, ValidationError, Field
from datetime import date
from datetime import datetime
from typing import Optional
import base64

# Клиент
 
class ClientBase(BaseModel):
    name: str
    phone: str

class Client(ClientBase):
    id: int
        
    class Config:
        orm_mode = True
    
# Категория

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = ""
    img_URL: Optional[str] = ""
    img_title: Optional[str] = ""

class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True
    
# Продукт

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = ""
    img_URL: Optional[str] = ""
    img_title: Optional[str] = ""
    price_for_itm:  Optional[float] = 0
    weight_for_itm: Optional[float] = 0
    
    is_active: Optional[bool] = False
    category_id: Optional[int] = None

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True

    @field_validator("price_for_itm")
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            price_str = f"{v:.2f}"
            if price_str.startswith('0') and len(price_str) > 1 and price_str[1].isdigit():
                raise ValueError("Стоимость не может начинаться с '0' или быть в формате '00,00'")
        return v
    
    @field_validator("weight_for_itm")
    def validate_weight(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            weight_str = f"{v:.2f}"
            if weight_str.startswith('0') and len(weight_str) > 1 and weight_str[1].isdigit():
                raise ValueError("Вес не может начинаться с '0' или быть в формате '00,00'")
        return v
             
class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
        
# Заказ

class OrderBase(BaseModel):
    client_id: int
    product_id: int
    
    quantity: Optional[int] = 1
    total_price: Optional[float] = 1
    total_weight: Optional[float] = 1
    
    adres: str = Field(..., min_length=5, max_length=100, description="Адрес доставки")
    comment: Optional[str] = Field(
        None, 
        min_length=5, 
        max_length=100,
        description="Комментарии к заказу"
    )
    is_active: Optional[bool] = Field(
        True,
        description="Активность заказа"
    )
    date: date
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    

    @field_validator("date")
    def validate_date(cls, value):
        if value < date.today():
            raise ValueError("Заказ не может быть заказан раньше даты, чем сегодя")
        return value
    
    @field_validator("is_active")
    def validate_is_active(cls, value):
        if value not in [True, False]:
            raise ValueError("Поле is_active должно быть булевым значением (True или False)")
        return value
    
    @field_validator("total_price")
    def validate_price(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            price_str = f"{v:.2f}"
            if price_str.startswith('0') and len(price_str) > 1 and price_str[1].isdigit():
                raise ValueError("Стоимость не может начинаться с '0' или быть в формате '00,00'")
        return v
    
    @field_validator("total_weight")
    def validate_weight(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            weight_str = f"{v:.2f}"
            if weight_str.startswith('0') and len(weight_str) > 1 and weight_str[1].isdigit():
                raise ValueError("Вес не может начинаться с '0' или быть в формате '00,00'")
        return v

class Order(OrderBase):
    id: int
    
    class Config:
        orm_mode = True
        
# Фото
    
class PhotoBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, description="Описание фото")
    filename: str
    content_type: str
    data: str

    class Config:
        from_attributes = True
        orm_mode = True

class Photo(PhotoBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
