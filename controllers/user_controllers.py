from fastapi import HTTPException, status, Response
from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import re
from datetime import date
from sqlalchemy.exc import IntegrityError, OperationalError
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import UserBase, UserLogin, UserRegister
from models import User
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List
import bcrypt
import logging
import config
from auth.access_token import create_jwt_token

logger = logging.getLogger(__name__)

class UserControllers: 
    async def create_user(user: UserRegister, db: AsyncSession):
        try:
            existing_user = await db.execute(select(User).filter(User.name == user.name))
            existing_user = existing_user.scalar_one_or_none()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Пользователь с таким именем уже существует"
                )

            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(5))

            new_user = User(
                name=user.name,
                password=hashed_password.decode('utf-8')
            )

            db.add(new_user)
            await db.commit()

            return {"message": "Пользователь добавлен успешно"}

        except IntegrityError as e:
            error_code = getattr(e.orig, 'pgcode', None)
            error_message = e.args[0]
            match = re.search(r"Key \((.*?)\)=\((.*?)\)", error_message)

            if match:
                key = match.group(1)
                value = match.group(2)
            else:
                key, value = None, None

            if error_code == "23503":
                detail = f"'{key}' с значением '{value}' не найдено"
            elif error_code == "23505":
                detail = "Пользователь с таким именем уже существует"
            else:
                detail = "Произошла непредвиденная ошибка"

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def login(response: Response, user: UserLogin, db: AsyncSession):
        try:
            existing_user = await db.execute(select(User).filter(User.name == user.name))
            existing_user = existing_user.scalar_one_or_none()

            if not existing_user:
                logger.warning(f"Попытка войти провалена: Пользователь {user.name} не найден")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверное имя или пароль пользователя"
                )
            

            if not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
                logger.warning(f"Попытка войти провалена: Неверный пароль для пользователя {user.name}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверное имя или пароль пользователя"
                )
                
            
            token = create_jwt_token(user.name)
            
            response.set_cookie(
                key="access_token",                     # Имя cookie
                value=token,                            # Значение cookie (JWT токен)
                httponly=True,                          # Cookie недоступно через JavaScript
                secure=True,                            # Cookie передается только по HTTPS
                samesite="lax",                         # Защита от CSRF
                #samesite="None",                        # Для работы в браузерах
                max_age=config.cookie_max_age           # Время жизни cookie (в секундах)
            )

            logger.info(f"Пользователь {user.name} вошёл успешно")
            logger.info(f"Cookie установлено: {response.headers}")
            return {"message": "Успешный вход", "access_token": token}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_users(db: AsyncSession):
        try:
            result = await db.execute(select(User).order_by(asc(User.name)))
            users = result.scalars().all()
            return users
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_user_by_id(id: int, db: AsyncSession):
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