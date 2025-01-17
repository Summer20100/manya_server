from fastapi import HTTPException, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import PhotoBase
from models import Photo
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List
import logging
import base64
import config

from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from models import Photo  # Это SQLAlchemy модель
from schemas import Photo as PhotoSchema  # Это Pydantic модель

class PhotoControllers:
    async def add_photo(title: str, file: UploadFile, db: AsyncSession):
        try:
            # Считываем файл в бинарный формат
            file_data = await file.read()

            # Создаем новый объект Photo
            new_photo = Photo(
                title=title,
                filename=file.filename,
                content_type=file.content_type,
                data=file_data
            )

            # Сохраняем в базу данных
            db.add(new_photo)
            await db.commit()
            return {"message": "Фото добавлено успешно"}
        except IntegrityError as e:
            # Проверка на уникальность
            error_message = str(e.orig) if hasattr(e, 'orig') else "Произошла ошибка базы данных"
            if "unique constraint" in error_message.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Фото с таким названием уже существует"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка при добавлении фото"
            )
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )

    async def get_photos(db: AsyncSession):
        try:
            # Получаем все фотографии из базы данных
            result = await db.execute(select(Photo).order_by(Photo.id))
            photos = result.scalars().all()

            # Преобразуем объекты SQLAlchemy Photo в Pydantic модели
            photo_schemas = []
            for photo in photos:
                photo_dict = photo.__dict__  # Получаем словарь атрибутов объекта
                if "data" in photo_dict:
                    # Преобразуем бинарные данные в строку base64
                    photo_dict["data"] = base64.b64encode(photo_dict["data"]).decode("utf-8")
                photo_schema = PhotoSchema(**photo_dict)  # Преобразуем в Pydantic модель
                photo_schemas.append(photo_schema)
            return photo_schemas
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_photo_by_id(id: int, db: AsyncSession):
        try:
            # Получаем фотографию из базы данных
            result = await db.execute(select(Photo).filter(Photo.id == id))
            photo = result.scalars().one_or_none()  # Получаем единственный объект или None

            if photo:
                # Преобразуем объект SQLAlchemy в Pydantic модель
                photo_dict = photo.__dict__.copy()
                photo_dict.pop('_sa_instance_state', None)  # Убираем служебные атрибуты SQLAlchemy

                # Преобразуем бинарные данные в строку base64
                if "data" in photo_dict:
                    photo_dict["data"] = base64.b64encode(photo_dict["data"]).decode("utf-8")

                # Возвращаем Pydantic модель
                photo_schema = PhotoSchema(**photo_dict)

                # Возвращаем одну модель, а не список
                return photo_schema
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Фото не найдено"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
    
    # async def update_photo(id: int, client: PhotoBase, db: AsyncSession):
    #     try:
    #         result = await db.execute(select(Client).filter(Client.id == id))
    #         existing_client = result.scalars().first()
    #         if existing_client:
    #             existing_client.name = client.name
    #             existing_client.phone = client.phone
    #             await db.commit()
    #             return {"message": "Данные клиента обновлены успешно"}
    #         else:
    #             raise HTTPException(
    #                 status_code=status.HTTP_404_NOT_FOUND,
    #                 detail="Клиент не найден"
    #             )
    #     except HTTPException as http_ex:
    #         raise http_ex
    #     except IntegrityError as e:
    #         conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Клиент с таким phone уже существует")        
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=conflict_detail
    #         )
    #     except Exception as e:
    #         logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Произошла непредвиденная ошибка"
    #         )
        
    async def del_photo(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Photo).filter(Photo.id == id))
            photo = result.scalars().first()
            if photo:
                await db.delete(photo)
                await db.commit()
                return {"message": "Фото удалено успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Фото не найдено"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
