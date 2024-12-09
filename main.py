from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config import create_model_from_data
from typing import List, Dict
from schemas import User, UserBase
from controllers.user_controllers import UserControllers

# Инициализация приложения FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup():
    UserControllers.create_table()

@app.post("/users", status_code=201)
async def add_user(user: UserBase):
    try:
        UserControllers.insert_user(user.name, user.email)
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=List[User])
async def get_users():
    try:
        users = UserControllers.get_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{id}")
async def get_user(id: int):
    try:
        user = UserControllers.get_user(id)
        if user:
            return user
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": "User not found", 
                    "status_code": status.HTTP_404_NOT_FOUND
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
