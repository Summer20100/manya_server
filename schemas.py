from pydantic import BaseModel, field_validator, ValidationError, Field
from datetime import date
from datetime import datetime
from typing import Optional
import base64

# Клиент
 
class ClientBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=3, 
        max_length=25,
        title="Телефон клиента",
        description="Контактный номер клиента в международном формате (+7xxxxxxxxxx)."
    )
    phone: str = Field(
        ..., 
        min_length=12, 
        max_length=16,
        title="Имя клиента",
        description="Имя клиента (от 3 до 25 символов)."
    )

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
    """ client_id: int """
    client_phone: str = Field(
        ..., 
        min_length=12, 
        max_length=16,  # Ограничим длину номера телефона
        title="Телефон клиента",
        description="Контактный номер клиента в международном формате (+7xxxxxxxxxx)."
    )

    client_name: str = Field(
        ..., 
        min_length=3, 
        max_length=25,  # Ограничим длину имени
        title="Имя клиента",
        description="Имя клиента (от 3 до 25 символов)."
    )
    
    product_id: int
    
    quantity: Optional[int] = 1
    total_price: Optional[float] = 1
    total_weight: Optional[float] = 1
    
    adres: Optional[str] = Field(
        None,
        max_length=100,
        title="Адрес доставки",
        description="Укажите адрес, куда будет доставлен заказ (необязательно)."
    )

    comment: Optional[str] = Field(
        None,
        max_length=100,
        title="Комментарий к заказу",
        description="Дополнительная информация по заказу (необязательно)."
    )

    is_active: Optional[bool] = Field(
        True,
        description="Активность заказа"
    )
    date: date
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @field_validator("client_phone")
    @classmethod
    def validate_client_phone(cls, value: str) -> str:
        if len(value) < 12 or len(value) > 16:
            raise ValueError("Длина номера телефона должна быть от 12 до 16 цифр")      
        return value
    
    @field_validator("client_name")
    @classmethod
    def validate_client_name(cls, value: str) -> str:
        if len(value) < 3 or len(value) > 25:
            raise ValueError("Длина номера телефона должна быть от 3 до 25 символов")      
        return value
    

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
    title: str = Field(..., min_length=5, max_length=100, description="Название фото")
    filename: str = Field(..., description="Имя файла изображения")
    content_type: str = Field(..., description="Тип содержимого (например, image/png)")
    data: str = Field(..., description="Данные изображения в формате base64")

    class Config:
        from_attributes = True
        orm_mode = True

class Photo(PhotoBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True

class PhotoForUpdate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, description="Название фото")

    class Config:
        from_attributes = True
        orm_mode = True
    

# Пользователь

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=16, description="Имя пользователя")
    password: str = Field(..., min_length=6, max_length=16, description="Пароль пользователя")
    
    @field_validator("name")
    def validate_name_length(cls, value: str) -> str:
        if len(value) < 3 or len(value) > 16:
            raise ValueError("Имя пользователя не менее 3 и не более 16 символов")
        return value
    
    @field_validator("password")
    def validate_password_length(cls, value: str) -> str:
        if len(value) < 7 or len(value) > 16:
            raise ValueError("Пароль не менее 7 и не более 16 символов")
        return value

    class Config:
        orm_mode = True

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        
class UserRegister(BaseModel):
    name: str
    password: str

class UserLogin(BaseModel):
    name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None