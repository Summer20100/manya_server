from fastapi import APIRouter, FastAPI, Response, HTTPException, Depends, status, UploadFile, Form, File, WebSocket
from pydantic import ValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException
from asyncpg.exceptions import UniqueViolationError

from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import init_db, get_db, app
from schemas import User, UserBase, UserLogin, UserRegister, Client, ClientBase, Category, CategoryBase, Product, ProductBase, OrderBase, Order, PhotoBase, Photo, PhotoForUpdate
from models import Client as ClientModel, Category as CategoryModel, Product as ProductModel
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Union
from controllers.client_controllers import ClientControllers
from controllers.category_controllers import CategoryControllers
from controllers.product_controllers import ProductControllers
from controllers.order_controllers import OrderControllers
from controllers.photo_controllers import PhotoControllers
from controllers.user_controllers import UserControllers
from WebSocket.ws import websocket_manager, logger
import os
import config
import logging
import uvicorn
from auth.access_token import verify_jwt_token

# Создание роута

router = APIRouter(prefix="/api/v1")
verify = APIRouter(dependencies=[Depends(verify_jwt_token)])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Создание таблиц если их не существует

@app.on_event("startup")
async def on_startup():
    await init_db()
    
# Приветствие

""" @router.get( """
@app.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    description="Приветствие",
    tags=["Default"]
)
async def say_hallo():
    return "HALOOOUUUU"

# Категории

@verify.post(
    "/categories", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить новую категорию",
    tags=["Categories"]
    )
async def add_category(
    category: CategoryBase, 
    db: AsyncSession = Depends(get_db)
):
    return await CategoryControllers.create_category(category, db)

# @app.get("/{key}/categories", response_model=List[Category], status_code=status.HTTP_200_OK, description="Получить все категории")
# async def get_categories(key: Optional[str] = None, db: AsyncSession = Depends(get_db)):
#     return await CategoryControllers.get_categories(key, db)

""" @app.get(
    "/categories", 
    response_model=List[Category], 
    status_code=status.HTTP_200_OK, 
    description="Получить все категории",
    tags=["Categories"]
)
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    return await CategoryControllers.get_categories(db) """

@app.get(
    "/categories", 
    response_model=List[Category], 
    status_code=status.HTTP_200_OK, 
    description="Получить все категории",
    tags=["Categories"]
)
async def get_categories(
    # username: str = Depends(verify_jwt_token),
    db: AsyncSession = Depends(get_db)
):
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

@verify.put(
    "/categories/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить категорию по ID",
    tags=["Categories"]
)
async def update_category(id: int, category: CategoryBase, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.update_category(id, category, db)

@verify.delete(
    "/categories/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Удалить категорию по ID",
    tags=["Categories"]
)
async def remove_category(id: int, db: AsyncSession = Depends(get_db)):
    return await CategoryControllers.del_category(id, db)

@verify.post(
    "/products", 
    status_code=status.HTTP_201_CREATED, 
    description="Добавить новый продукт",
    tags=["Products"]
)
async def add_product(product: ProductBase, db: AsyncSession = Depends(get_db)):
    return await ProductControllers.create_product(product, db)

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

@verify.put(
    "/products/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить продукт по ID",
    tags=["Products"]
)
async def update_product(id: int, product: ProductBase, db: AsyncSession = Depends(get_db)):
    return await ProductControllers.update_product(id, product, db)

@verify.delete(
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

@verify.get(
    "/clients", 
    response_model=List[Client], 
    status_code=status.HTTP_200_OK, 
    description="Получить всех клиентов",
    tags=["Clients"]
)
async def get_clients(db: AsyncSession = Depends(get_db)):
    return await ClientControllers.get_clients(db)

@verify.get(
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
async def add_order(order: Union[OrderBase, List[OrderBase]], db: AsyncSession = Depends(get_db)):
    return await OrderControllers.create_order(order, db)

@verify.get(
    "/orders", 
    response_model=List[Order], 
    status_code=status.HTTP_200_OK, 
    description="Получить все заказы",
     tags=["Orders"]
)
async def get_orders(db: AsyncSession = Depends(get_db)):
    return await OrderControllers.get_orders(db)


@verify.get(
    "/orders/{id}", 
    response_model=Order, 
    status_code=status.HTTP_200_OK, 
    description="Получить заказ по ID",
    tags=["Orders"]
)
async def get_order_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.get_order_by_id(id, db)

@verify.put(
    "/orders/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Обновить заказ по ID",
    tags=["Orders"]
)
async def update_order(id: int, order: OrderBase, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.update_order(id, order, db)

@verify.delete(
    "/orders/{id}", 
    status_code=status.HTTP_200_OK, 
    description="Удалить заказ по ID",
    tags=["Orders"]
)
async def remove_order(id: int, db: AsyncSession = Depends(get_db)):
    return await OrderControllers.del_order(id, db)

# Фотографии

@verify.post(
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

@verify.get(
    "/photos", 
    response_model=List[Photo], 
    status_code=status.HTTP_200_OK, 
    description="Получить все фото",
    tags=["Photos"]
)
async def get_photos(db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.get_photos(db)

@verify.get(
    "/photos/{id}", 
    response_model=Photo, 
    status_code=status.HTTP_200_OK, 
    description="Получить фото по ID",
    tags=["Photos"]
)
async def get_photo_by_ID(id: int, db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.get_photo_by_id(id, db)

@verify.put(
    "/photos/{id}",
    status_code=status.HTTP_200_OK, 
    description="Обновить фото по ID",
    tags=["Photos"]
)
async def update_order(id: int, photo_update: PhotoForUpdate, db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.update_photo(id, photo_update, db)

@verify.delete(
    "/photos/{id}",
    status_code=status.HTTP_200_OK, 
    description="Удалить фото по ID",
    tags=["Photos"]
)
async def remove_order(id: int, db: AsyncSession = Depends(get_db)):
    return await PhotoControllers.del_photo(id, db)


# Доступ к приложению

@app.post(
    "/{reg_key}/register",
    status_code=status.HTTP_201_CREATED, 
    description="Добавить нового пользователя с reg_key",
    tags=["Access"]
)
async def create_user(
    reg_key: str,
    user: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    if reg_key != config.regKey:
        raise HTTPException(status_code=400, detail="Неверный регистрационный ключ")
    
    return await UserControllers.create_user(user, db)
    
@app.post(
    "/login",
    status_code=status.HTTP_200_OK, 
    description="Войти в систему",
    tags=["Access"]
)
async def login(
    response: Response, 
    user: UserLogin, 
    db: AsyncSession = Depends(get_db)
):
    return await UserControllers.login(response, user, db)


""" @app.get(
    "/auth/validate",
    status_code=status.HTTP_200_OK, 
    description="Проверка валидности токена",
    tags=["Access"]
)
async def validate_token(request: Request):
    token = request.cookies.get("access_token")
    if not token or not verify_jwt_token(token):
        raise HTTPException(status_code=401, detail="Токен недействителен")
    return {"valid": True} """

@app.get(
    "/auth/validate",
    status_code=status.HTTP_200_OK,
    description="Проверка валидности токена",
    tags=["Access"]
)
async def validate_token(request: Request, token: str = Depends(oauth2_scheme)):
    token_from_cookie = request.cookies.get("access_token")
    final_token = token_from_cookie or token  # Берём токен из cookies или Authorization
    if not final_token:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    username = verify_jwt_token(final_token)
    return {"valid": True, "username": username}


@verify.get(
    "/protected",
    status_code=status.HTTP_200_OK,
    description="Войти в систему с авторизацией",
    tags=["Access"]
    )
async def protected_route(username: str = Depends(verify_jwt_token)):
    return {"message": f"Hello {username}, you are authorized!"}

@verify.get(
    "/users",
    status_code=status.HTTP_200_OK,
    description="Получить всех пользователей",
    tags=["Access"]
)
async def get_users(db: AsyncSession = Depends(get_db)):   
    return await UserControllers.get_users(db)

@verify.get(
    "/users/{id}",
    response_model=UserLogin,
    status_code=status.HTTP_200_OK, 
    description="Получить пользователя по ID",
    tags=["Access"]
)
async def get_user_by_ID(
    id: int, 
    db: AsyncSession = Depends(get_db)
):   
    return await UserControllers.get_user_by_id(id, db)

@app.delete(
    "/{del_key}/users/{id}",
    status_code=status.HTTP_200_OK, 
    description="Удалить пользователя по ID",
    tags=["Access"]
)
async def remove_user(
    del_key: str,
    id: int, 
    db: AsyncSession = Depends(get_db)
):
    if del_key != config.delKey:
        raise HTTPException(
            status_code=400, 
            detail="Неверный ключ для удаления"
        )

    return await UserControllers.del_user(id, db)

# WebSocket

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message from client: {data}")
            # Здесь можно добавить обработку входящих сообщений, если нужно
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        websocket_manager.disconnect(websocket)

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
        elif error_ctx == "String should have at most 16 characters":
            some_error = "Длина номера телефона должен быть не более 16 цифр"
            
        elif error_type == "date_from_datetime_parsing" and error_field == "date" and error_msg == "Input should be a valid date or datetime, month value is outside expected range of 1-12":
            some_error = "Месяц находится вне диапазоне 1-12" 
        elif error_type == "date_from_datetime_parsing" and error_field == "date" and error_msg == "Input should be a valid date or datetime, day value is outside expected range":
            some_error = "День находится вне диапазона месяца"
        elif error_type == "string_too_short" and error_msg == "String should have at least 5 characters":
            some_error = f"Длина поля {error_field} должна быть более 5 символов"
        elif error_type == "string_too_long" and error_msg == "String should have at most 16 characters":
            some_error = f"Длина поля {error_field} должна быть менее 17 символов"
        elif error_type == "string_too_short" and error_msg == "String should have at least 12 characters":
            some_error = f"Длина поля {error_field} должна быть более 12 символов"
            
        elif error_type == "string_too_long" and error_msg == "String should have at most 100 characters":
            some_error = f"Длина поля {error_field} должна быть менее 100 символов"
        elif error_type == "string_too_long" and error_msg == "String should have at most 25 characters":
            some_error = f"Длина поля {error_field} должна быть менее 25 символов"
        elif error_type == "string_too_short" and error_msg == "String should have at least 3 characters":
            some_error = f"Длина поля {error_field} должна быть более 3 символов"
            
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
        
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Вы не авторизованы для доступа к этому ресурсу"}
        )
    # Возвращаем стандартный обработчик для других ошибок
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(UniqueViolationError)
async def handle_unique_violation_error(request, exc: UniqueViolationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Клиент с таким номером телефона уже существует"}
    )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
        
        
app.include_router(router)
app.include_router(verify, prefix="")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
