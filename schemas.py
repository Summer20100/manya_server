from pydantic import BaseModel, Field
from typing import Annotated

# User Models
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    age: int = Field(..., ge=0, le=120, description="Возраст пользователя (0-120 лет)")

class UserCreate(UserBase):
    """Модель для создания нового пользователя"""
    pass

class User(UserBase):
    id: int = Field(..., description="Идентификатор пользователя")
    
    class Config:
        orm_mode = True

# Post Models
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Заголовок поста")
    body: str = Field(..., min_length=1, description="Содержимое поста")
    author_id: int = Field(..., ge=1, description="ID автора поста")

class PostCreate(PostBase):
    """Модель для создания нового поста"""
    pass

class PostResponse(PostBase):
    id: int = Field(..., description="Идентификатор поста")
    author: User
    
    class Config:
        orm_mode = True
