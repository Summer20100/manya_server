from pydantic import BaseModel

# Пользователь
 
class UserBase(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str
    
# Категории

class CategoryBase(BaseModel):
    title: str
    description: str

class Category(BaseModel):
    id: int
    title: str
    description: str
