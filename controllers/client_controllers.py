from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import ClientBase
from models import Client
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List
import logging
import config

class ClientControllers: 
    async def create_client(client: ClientBase, db: AsyncSession):
        try:
            new_client = Client(name=client.name, phone=client.phone)
            db.add(new_client)
            await db.commit()
            return { "message": "Клиент добавлен успешно" }
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Клиент с таким phone уже существует")        
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
            
    # async def get_users(key: str, db: AsyncSession):
    #     try:
    #         result = await db.execute(select(User).order_by(asc(User.id)))
    #         users = result.scalars().all()
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
    
    async def get_clients(db: AsyncSession):
        try:
            result = await db.execute(select(Client).order_by(asc(Client.id)))
            clients = result.scalars().all()
            return clients
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_client_by_id(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Client).filter(Client.id == id))
            client = result.scalars().first()
            if client:
                return client
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Клиент не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def update_client(id: int, client: ClientBase, db: AsyncSession):
        try:
            result = await db.execute(select(Client).filter(Client.id == id))
            existing_client = result.scalars().first()
            if existing_client:
                existing_client.name = client.name
                existing_client.phone = client.phone
                await db.commit()
                return {"message": "Данные клиента обновлены успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Клиент не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Клиент с таким phone уже существует")        
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
        
    
    async def del_client(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Client).filter(Client.id == id))
            client = result.scalars().first()
            if client:
                await db.delete(client)
                await db.commit()
                return {"message": "Клиент удален успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Клиент не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
