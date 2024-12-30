from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import CategoryBase
from models import Category
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List
import logging
import config

class CategoryControllers: 
    async def create_category(category: CategoryBase, db: AsyncSession):
        try:
            new_category = Category(
                title=category.title,
                description=category.description,
                img_URL=category.img_URL,
                img_title=category.img_title
            )
            db.add(new_category)
            await db.commit()
            return { "message": "Категория добавлена успешно" }
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Категория с таким названием уже существует")        
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
            
    # async def get_categories(key: str, db: AsyncSession):
    #     try:
    #         result = await db.execute(select(Category).order_by(asc(Category.id)))
    #         categories = result.scalars().all()
    #         if key != config.key:
    #             raise HTTPException(
    #                 status_code=status.HTTP_403_FORBIDDEN,
    #                 detail="Доступ запрещён. Введён неправильный код"
    #             )
    #         return users
    #     except HTTPException as http_ex:
    #         raise http_ex
    #     except Exception as e:
    #         logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Произошла непредвиденная ошибка"
    #         )
    
    async def get_categories(db: AsyncSession):
        try:
            result = await db.execute(select(Category).order_by(asc(Category.id)))
            categories = result.scalars().all()
            return categories
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_category_by_id(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Category).filter(Category.id == id))
            user = result.scalars().first()
            if user:
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категория не найдена"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def update_category(id: int, category: CategoryBase, db: AsyncSession):
        try:
            result = await db.execute(select(Category).filter(Category.id == id))
            existing_category = result.scalars().first()
            if existing_category:
                existing_category.title = category.title
                existing_category.description = category.description
                existing_category.img_URL=category.img_URL
                existing_category.img_title=category.img_title
                await db.commit()
                return {"message": "Категория обновлена успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категория не найдена"
                )
        except HTTPException as http_ex:
            raise http_ex
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Категория с таким названием уже существует")        
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
        
    async def del_category(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Category).filter(Category.id == id))
            category = result.scalars().first()
            if category:
                await db.delete(category)
                await db.commit()
                return {"message": "Категория удалена успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Категория не найдена"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
