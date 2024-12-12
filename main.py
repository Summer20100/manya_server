from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db, app
from schemas import User, UserBase
from models import User as UserModel
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from controllers.user_controllers import UserControllers
import os
import uvicorn

@app.get("/", status_code=status.HTTP_200_OK, description="Приветствие")
async def say_hallo():
    return "HALOOOUUUU"

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
    return await UserControllers.get_users_by_id(id, db)

@app.put("/users/{id}", status_code=status.HTTP_200_OK, description="Обновить пользователя по ID")
async def update_user(id: int, user: UserBase, db: AsyncSession = Depends(get_db)):
    return await UserControllers.update_user(id, user, db)

@app.delete("/users/{id}", status_code=status.HTTP_200_OK, description="Удалить пользователя по ID")
async def remove_user(id: int, db: AsyncSession = Depends(get_db)):
    return await UserControllers.del_user(id, db)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
