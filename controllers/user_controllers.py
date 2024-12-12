from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import UserBase
from models import User
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List
import logging

class UserControllers: 
    async def create_user(user: UserBase, db: AsyncSession):
        try:
            new_user = User(name=user.name, email=user.email)
            db.add(new_user)
            await db.commit()
            return { "message": "Пользователь добавлен успешно" }
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Пользователь с таким email уже существует")        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=conflict_detail
            )
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_users(db: AsyncSession):
        try:
            result = await db.execute(select(User).order_by(asc(User.id)))
            users = result.scalars().all()
            return users
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_users_by_id(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(User).filter(User.id == id))
            user = result.scalars().first()
            if user:
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def update_user(id: int, user: UserBase, db: AsyncSession):
        try:
            result = await db.execute(select(User).filter(User.id == id))
            existing_user = result.scalars().first()
            if existing_user:
                existing_user.name = user.name
                existing_user.email = user.email
                await db.commit()
                return {"message": "Пользователь обновлен успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Пользователь с таким email уже существует")        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=conflict_detail
            )
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
        
    
    async def del_user(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(User).filter(User.id == id))
            user = result.scalars().first()
            if user:
                await db.delete(user)
                await db.commit()
                return {"message": "Пользователь удален успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Пользователь не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
