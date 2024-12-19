from fastapi import HTTPException, status
from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError
from contextlib import asynccontextmanager
from database import init_db, get_db
from schemas import ProductBase
from models import Product
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import asc
from typing import List
import logging
import config

def validate_product_data(product):
    errors = []

    if product.price_for_itm < 0:
        errors.append("Стоимость продукта меньше 0")
    if product.weight_for_itm < 0:
        errors.append("Вес продукта меньше 0")

    price_str = str(product.price_for_itm).replace(',', '.')
    weight_str = str(product.weight_for_itm).replace(',', '.')

    if price_str.startswith('0') and len(price_str) > 1 and price_str[1].isdigit():
        errors.append("Стоимость продукта не может начинаться с 0 если она больше 0")
    if weight_str.startswith('0') and len(weight_str) > 1 and weight_str[1].isdigit():
        errors.append("Вес продукта не может начинаться с 0 если она больше 0")
    try:
        product.price_for_itm = float(price_str)
    except ValueError:
        errors.append("Стоимость продукта должна быть числом формата 0.00")

    try:
        product.weight_for_itm = float(weight_str)
    except ValueError:
        errors.append("Вес продукта должна быть числом формата 0.00")

    if errors:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors
        )


class ProductControllers: 
    async def create_product(product: ProductBase, db: AsyncSession):
        try:
            validate_product_data(product)
            
            new_product = Product(
                title = product.title, 
                description = product.description,
                price_for_itm = product.price_for_itm,
                weight_for_itm = product.weight_for_itm,
                is_active = product.is_active,
                category_id = product.category_id,
            )
            db.add(new_product)
            await db.commit()
            return { "message": "Продукт добавлен успешно" }
        except IntegrityError as e:
            conflict_detail = getattr(e.orig, 'diag', {}).get('message_detail', "Продукт с таким названием уже существует")        
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=conflict_detail
            )
        except HTTPException as http_ex:
            raise http_ex
        except ValidationError as e:
            print("ValidationError:", e)
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
    
    async def get_products(db: AsyncSession):
        try:
            result = await db.execute(select(Product).order_by(asc(Product.id)))
            products = result.scalars().all()
            return products
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def get_product_by_id(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Product).filter(Product.id == id))
            product = result.scalars().first()
            if product:
                return product
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Продукт не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
            
    async def update_product(id: int, product:ProductBase, db: AsyncSession):
        try:
            validate_product_data(product)

            result = await db.execute(select(Product).filter(Product.id == id))
            existing_product = result.scalars().first()

            if not existing_product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Продукт не найден"
                )
            existing_product.title = product.title
            existing_product.description = product.description
            existing_product.price_for_itm = product.price_for_itm
            existing_product.weight_for_itm = product.weight_for_itm
            existing_product.is_active = product.is_active
            existing_product.category_id = product.category_id

            await db.commit()
            return {"message": "Продукт обновлен успешно"}

        except IntegrityError as e:
            error_code = getattr(e.orig, 'pgcode', None)
            if error_code == "23503":
                detail = "Категории ID не найдено"
            elif error_code == "23505":
                detail = "Продукт с таким названием уже существует"
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

    async def del_product(id: int, db: AsyncSession):
        try:
            result = await db.execute(select(Product).filter(Product.id == id))
            product = result.scalars().first()
            if product:
                await db.delete(product)
                await db.commit()
                return {"message": "Продукт удален успешно"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Продукт не найден"
                )
        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logging.error(f"Произошла непредвиденная ошибка: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Произошла непредвиденная ошибка"
            )
