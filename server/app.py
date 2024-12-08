from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from db_queries import create_table, insert_user, get_all_users

# Инициализация приложения FastAPI
app = FastAPI()

# Создание таблицы при старте приложения
@app.on_event("startup")
def startup():
    create_table()

# Модель для данных пользователя
class User(BaseModel):
    name: str
    email: str

# Роут для добавления пользователя
@app.post("/users", status_code=201)
def add_user(user: User):
    try:
        insert_user(user.name, user.email)
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Роут для получения всех пользователей
@app.get("/users")
def list_users():
    try:
        users = get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
