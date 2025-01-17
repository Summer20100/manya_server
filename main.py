from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, Form, File
from pydantic import BaseModel, FieldValidationInfo, field_validator, ValidationError
import re
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from database import init_db, get_db, app
from schemas import Client, ClientBase, Category, CategoryBase, Product, ProductBase, OrderBase, Order, PhotoBase, Photo
from models import Client as ClientModel, Category as CategoryModel, Product as ProductModel
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from controllers.client_controllers import ClientControllers
from controllers.category_controllers import CategoryControllers
from controllers.product_controllers import ProductControllers
from controllers.order_controllers import OrderControllers
from controllers.photo_controllers import PhotoControllers
import os
import logging
import uvicorn

# Создание таблиц если их не существует

@app.on_event("startup")
async def on_startup():
    await init_db()

# Приветствие

@app.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    description="Приветствие",
    tags=["Default"]
)
async def say_hallo():
    return "HALOOOUUUU"

# Категории

@app.post(
    "/categories", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить новую категорию",
    tags=["Categories"]
    )
async def add_category(category: CategoryBase, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.create_category(category, db)

# @app.get("/{key}/categories", response_model=List[Category], status_code=status.HTTP_200_OK, description="Получить все категории")
# async def get_categories(key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
#     return await CategoryControllers.get_categories(key, db)

@app.get(
    "/categories", 
    response_model=List[Category], 
    status_code=status.HTTP_200_OK, 
    description="Получить все категории",
    tags=["Categories"]
)
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.get_categories(db)

@app.get(
    "/categories/{id}", 
    response_model=Category, 
    status_code=status.HTTP_200_OK, 
    description="Получить категорию по ID",
    tags=["Categories"]
)
async def get_category_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.get_category_by_id(id, db)

@app.put(
    "/categories/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить категорию по ID",
    tags=["Categories"]
)
async def update_category(id: int, category: CategoryBase, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.update_category(id, category, db)

@app.delete(
    "/categories/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Удалить категорию по ID",
    tags=["Categories"]
)
async def remove_category(id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.del_category(id, db)

# Продукты

# async def validate_product(product):
#     errors = []

#     # Проверка стоимости
#     if product.price_for_itm < 0:
#         errors.append("Стоимость не может быть меньше 0")
#     if not re.match(r'^(?!0\d)(\d+(\.\d{1,2})?)$', str(product.price_for_itm)):
#         errors.append("Стоимость должна быть в формате 00.00")

#     # Проверка веса
#     if product.weight_for_itm < 0:
#         errors.append("Вес не может быть меньше 0")
#     if not re.match(r'^(?!0\d)(\d+(\.\d{1,2})?)$', str(product.weight_for_itm)):
#         errors.append("Вес должен быть в формате 00.00")

#     if errors:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail={"kvflk.fl oioi,srti rosijv,ro"}
#         )

#     return "Проверка прошла успешно"

@app.post(
    "/products", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить новый продукт",
    tags=["Products"]
)
async def add_product(product: ProductBase, db: AsyncSession = Depends(get_db)):
    return await ProductControllers.create_product(product, db)

# @app.get("/{key}/categories", response_model=List[Category], status_code=status.HTTP_200_OK, description="Получить все категории")
# async def get_categories(key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
#     return await CategoryControllers.get_categories(key, db)

@app.get(
    "/products", 
    response_model=List[Product], 
    status_code=status.HTTP_200_OK, 
    description="Получить все продукты",
    tags=["Products"]
)
async def get_products(db: AsyncSession = Depends(get_db)):
    return await ProductControllers.get_products(db)

@app.get(
    "/products/{id}", 
    response_model=Product, 
    status_code=status.HTTP_200_OK, 
    description="Получить продукт по ID",
    tags=["Products"]
)
async def get_product_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await ProductControllers.get_product_by_id(id, db)

@app.put(
    "/products/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить продукт по ID",
    tags=["Products"]
)
async def update_product(id: int, product: ProductBase, db: AsyncSession = Depends(get_db)):
    return await ProductControllers.update_product(id, product, db)

@app.delete(
    "/products/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Удалить продукт по ID",
    tags=["Products"]    
)
async def remove_product(id: int, db: AsyncSession = Depends(get_db)):
    return await ProductControllers.del_product(id, db)

# Клиенты

@app.post(
    "/clients", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить нового клиента", 
    tags=["Clients"]
)
async def add_client(client: ClientBase, db: AsyncSession = Depends(get_db)):
    return await ClientControllers.create_client(client, db)

# @app.get("/{key}/users", response_model=List[User], status_code=status.HTTP_200_OK, description="Получить всех пользователей")
# async def get_users(key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
#     return await UserControllers.get_users(key, db)

@app.get(
    "/clients", 
    response_model=List[Client], 
    status_code=status.HTTP_200_OK, 
    description="Получить всех клиентов",
    tags=["Clients"]
)
async def get_clients(db: AsyncSession = Depends(get_db)):
    return await ClientControllers.get_clients(db)

@app.get(
    "/clients/{id}", 
    response_model=Client, 
    status_code=status.HTTP_200_OK, 
    description="Получить клиента по ID", 
    tags=["Clients"]
)
async def get_client_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await ClientControllers.get_client_by_id(id, db)

@app.put(
    "/clients/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить информацию клиента по ID", 
    tags=["Clients"]
)
async def update_client(id: int, client: ClientBase, db: AsyncSession = Depends(get_db)):
    return await ClientControllers.update_client(id, client, db)

@app.delete(
    "/clients/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Удалить клиента по ID", 
    tags=["Clients"]
)
async def remove_client(id: int, db: AsyncSession = Depends(get_db)):
    return await ClientControllers.del_client(id, db)

# Заказы

@app.post(
    "/orders", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить новый заказ",
    tags=["Orders"]
)
async def add_order(order: OrderBase, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.create_order(order, db)

@app.get(
    "/orders", 
    response_model=List[Order], 
    status_code=status.HTTP_200_OK, 
    description="Получить все заказы",
     tags=["Orders"]    
)
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await OrderControllers.get_orders(db)


@app.get(
    "/orders/{id}", 
    response_model=Order, 
    status_code=status.HTTP_200_OK, 
    description="Получить заказ по ID",
    tags=["Orders"]
)
async def get_order_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.get_order_by_id(id, db)

@app.put(
    "/orders/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить заказ по ID",
    tags=["Orders"]
)
async def update_order(id: int, order: OrderBase, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.update_order(id, order, db)

@app.delete(
    "/orders/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Удалить заказ по ID",
    tags=["Orders"]
)
async def remove_order(id: int, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.del_order(id, db)

# Фотографии

# @app.post(
#     "/photos", 
#     status_code=status.HTTP_201_CREATED, 
#     description="Добавить новое фото",
#     tags=["Photos"]
# )
# async def add_photo(
#     title: str = Form(...),  # Получаем текстовое поле через Form
#     file: UploadFile = Depends(),  # Получаем файл через UploadFile
#     db: AsyncSession = Depends(get_db)  # Получаем сессию базы данных
# ):
#     return await PhotoControllers.add_photo(title, file, db)


@app.post(
    "/photos", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить новое фото",
    tags=["Photos"]
)
async def upload_file(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await PhotoControllers.add_photo(title, file, db)

@app.get(
    "/photos", 
    response_model=List[Photo], 
    status_code=status.HTTP_200_OK, 
    description="Получить все фото",
    tags=["Photos"]
)
async def get_photos(db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.get_photos(db)

@app.get(
    "/photos/{id}", 
    response_model=Photo, 
    status_code=status.HTTP_200_OK, 
    description="Получить фото по ID",
    tags=["Photos"]
)
async def get_photo_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.get_photo_by_id(id, db)

# @app.put(
#     "/photos/{id}",
#     status_code=status.HTTP_200_OK, 
#     description="Обновить фото по ID",
#     tags=["Photos"]
# )
# async def update_order(id: int, photo: PhotoBase, db: AsyncSession = Depends(get_db)):
#     return await PhotoControllers.update_photo(id, photo, db)

@app.delete(
    "/photos/{id}",
    status_code=status.HTTP_200_OK, 
    description="Удалить фото по ID",
    tags=["Photos"]
)
async def remove_order(id: int, db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.del_photo(id, db)



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        error = exc.errors()[0] if exc.errors() else {}
        error_type = error.get("type", None)
        error_field = error.get("loc", [])[1] if len(error.get("loc", [])) > 1 else None
        error_msg = error.get("msg", "")
        error_ctx = error.get("ctx", {}).get("error", "")

        some_error = ""

        if error_ctx == "Expecting ',' delimiter":
            some_error = "Стоимость и/или вес продукта не должны начинаться с 0 если больше 0"
        elif error_ctx == "Expecting property name enclosed in double quotes":
            some_error = "Стоимость и/или вес продукта должны быть в формате 00.00"
        elif error_ctx == "Expecting value":
            some_error = "Ошибка типа данных при отправлении запроса"   
            
        elif error_type == "date_from_datetime_parsing" and error_field == "date" and error_msg == "Input should be a valid date or datetime, month value is outside expected range of 1-12":
            some_error = "Месяц находится вне диапазоне 1-12" 
        elif error_type == "date_from_datetime_parsing" and error_field == "date" and error_msg == "Input should be a valid date or datetime, day value is outside expected range":
            some_error = "День находится вне диапазона месяца"
        elif error_type == "string_too_short" and error_msg == "String should have at least 5 characters":
            some_error = f"Длина поля {error_field} должна быть более 5 символов"
        elif error_type == "value_error":
            some_error = str(error_ctx)
        else:
            some_error = error_msg

        print({
            "error_type": error_type, 
            "error_field": error_field,
            "error_msg": error_msg,
            "error_ctx": error_ctx
        })

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=some_error
        )
    except ValidationError as e:
        # Выводим все ошибки валидации
        print("Ошибка валидации:")
        for error in e.errors():
            print(f"Поле: {error['loc'][0]}, Ошибка: {error['msg']}")
    except ValidationError:
        raise
    except HTTPException as http_ex:
        raise http_ex
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex)
        )



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
