from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db, app
from schemas import User, UserBase, Category, CategoryBase
from models import User as UserModel, Category as CategoryModel
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from controllers.user_controllers import UserControllers
from controllers.category_controllers import CategoryControllers
import os
import uvicorn

# Создание таблиц если их не существует

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/", status_code=status.HTTP_200_OK, description="Приветствие")
async def say_hallo():
    return "HALOOOUUUU"

# Пользователи

@app.post("/users", status_code=status.HTTP_201_CREATED, description="Добавить нового пользователя")
async def add_user(user: UserBase, db: AsyncSession = Depends(get_db)):
    return await UserControllers.create_user(user, db)

# @app.get("/{key}/users", response_model=List[User], status_code=status.HTTP_200_OK, description="Получить всех пользователей")
# async def get_users(key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
#     return await UserControllers.get_users(key, db)

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, description="Получить всех пользователей")
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserControllers.get_users(db)

@app.get("/users/{id}", response_model=User, status_code=status.HTTP_200_OK, description="Получить пользователя по ID")
async def get_user_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await UserControllers.get_user_by_id(id, db)

@app.put("/users/{id}", status_code=status.HTTP_200_OK, description="Обновить пользователя по ID")
async def update_user(id: int, user: UserBase, db: AsyncSession = Depends(get_db)):
    return await UserControllers.update_user(id, user, db)

@app.delete("/users/{id}", status_code=status.HTTP_200_OK, description="Удалить пользователя по ID")
async def remove_user(id: int, db: AsyncSession = Depends(get_db)):
    return await UserControllers.del_user(id, db)

# Категории

@app.post("/categories", status_code=status.HTTP_201_CREATED, description="Добавить новую категорию")
async def add_category(category: CategoryBase, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.create_category(category, db)

# @app.get("/{key}/categories", response_model=List[Category], status_code=status.HTTP_200_OK, description="Получить все категории")
# async def get_categories(key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
#     return await CategoryControllers.get_categories(key, db)

@app.get("/categories", response_model=List[Category], status_code=status.HTTP_200_OK, description="Получить все категории")
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.get_categories(db)

@app.get("/categories/{id}", response_model=Category, status_code=status.HTTP_200_OK, description="Получить категорию по ID")
async def get_category_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.get_category_by_id(id, db)

@app.put("/categories/{id}", status_code=status.HTTP_200_OK, description="Обновить категорию по ID")
async def update_category(id: int, category: CategoryBase, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.update_category(id, category, db)

@app.delete("/categories/{id}", status_code=status.HTTP_200_OK, description="Удалить категорию по ID")
async def remove_category(id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.del_category(id, db)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
