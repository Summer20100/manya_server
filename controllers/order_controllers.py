from fastapi import HTTPException, status
from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
import re
from datetime import date
from sqlalchemy.exc import IntegrityError, OperationalError
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import OrderBase
from models import Order
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List, Union
import logging
import config

class OrderControllers: 
    async def create_order(order: OrderBase, db: AsyncSession):
        async def each_order(eachOrder: OrderBase):
            try:
                new_order = Order(
                    client_phone=eachOrder.client_phone,
                    client_name=eachOrder.client_name,
                    product_id=eachOrder.product_id,
                    quantity=eachOrder.quantity,
                    total_price=eachOrder.total_price,
                    total_weight=eachOrder.total_weight,
                    adres=eachOrder.adres,
                    comment=eachOrder.comment,
                    is_active=eachOrder.is_active,
                    date=eachOrder.date
                )
                db.add(new_order)
                await db.commit()  # обязательно добавляем await
                return {"message": "Заказ добавлен успешно"}
            except IntegrityError as e:
                error_code = getattr(e.orig, 'pgcode', None)
                error_message = e.args[0]
                
                match = re.search(r"Key \((.*?)\)=\((.*?)\)", error_message)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                else:
                    print("Не удалось извлечь данные из сообщения об ошибке.")
                
                if error_code == "23503":
                    detail = f"'{key}' с значением '{value}' не найдено"
                elif error_code == "23505":
                    detail = "Заказ с таким названием уже существует"
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

        # Если пришел одиночный заказ
        if isinstance(order, OrderBase):
            await each_order(order)
            return {"message": "Заказ добавлен успешно"}

        # Если пришел список заказов
        elif isinstance(order, list):
            for ord in order:
                await each_order(ord)
            return {"message": "Заказы добавлены успешно"}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат данных"
        )

        
    
    async def get_orders(db: AsyncSession):
        try:
            current_date = date.today()
            result = await db.execute(
                select(Order)
                .where(Order.date >= current_date)
                .order_by(asc(Order.id))
            )
            orders = result.scalars().all()
            return orders
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_order_by_id(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Order).filter(Order.id == id))
            order = result.scalars().first()
            if order:
                return order
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заказ не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def update_order(id: int, order:OrderBase, db: AsyncSession):
        try:
            result = await db.execute(select(Order).filter(Order.id == id))
            existing_order = result.scalars().first()

            if not existing_order:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заказ не найден"
                )
            existing_order.client_phone = order.client_phone
            existing_order.client_name = order.client_name
            existing_order.product_id = order.product_id
            existing_order.quantity = order.quantity
            existing_order.total_price = order.total_price
            existing_order.total_weight = order.total_weight
            existing_order.adres = order.adres
            existing_order.comment = order.comment
            existing_order.is_active = order.is_active
            existing_order.date = order.date

            await db.commit()
            return {"message": "Заказ обновлен успешно"}

        except IntegrityError as e:
            error_code = getattr(e.orig, 'pgcode', None)
            if error_code == "23503":
                detail = "Заказ ID не найдено"
            elif error_code == "23505":
                detail = "Заказ с таким названием уже существует"
            else:
                detail = "Произошла непредвиденная ошибка"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= detail
            )
        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def del_order(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Order).filter(Order.id == id))
            order = result.scalars().first()
            if order:
                await db.delete(order)
                await db.commit()
                return {"message": "Заказ удален успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Заказ не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
