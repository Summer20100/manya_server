from fastapi import FastAPI, HTTPException, Depends, status, Body
from fastapi.responses import JSONResponse
from typing import List
from schemas import User, UserBase
from controllers.user_controllers import UserControllers
import logging
from psycopg2.errors import UniqueViolation

app = FastAPI()

# EVENTS

@app.on_event("startup")
async def startup():
    UserControllers.create_table()
    
# USER

@app.get("/", status_code=status.HTTP_200_OK, description="Say HallOOOOO")
async def say_hallo():
    return "HALOOOUUUU"

@app.post("/users", status_code=status.HTTP_201_CREATED, description="Add a new user")
async def add_user(user: UserBase):
    try:
        UserControllers.insert_user(user.name, user.email)
        return {"message": "User added successfully"}
    except UniqueViolation as e:
        conflict_detail = getattr(e.diag, 'message_detail')
        raise HTTPException(
            status_code=400,
            detail=conflict_detail
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK, description="Get all users")
async def get_users():
    try:
        users = UserControllers.get_users()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.get("/users/{id}", status_code=status.HTTP_200_OK, description="Get user by ID")
async def get_user(id: int):
    try:
        user = UserControllers.get_user(id)
        if user:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.put("/users/{id}", status_code=status.HTTP_200_OK, description="Update user by ID")
async def update_user(
    id: int,
    name: str = Body(..., embed=True), 
    email: str = Body(..., embed=True)
):
    try:
        user = UserControllers.get_user(id)
        if user:
            UserControllers.update_user(name, email, id)
            return {"message": "User updated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except UniqueViolation as e:
        conflict_detail = getattr(e.diag, 'message_detail')
        raise HTTPException(
            status_code=400,
            detail=conflict_detail
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@app.delete("/users/{id}", status_code=status.HTTP_200_OK, description="Remove user by ID")
async def remove_user(id: int):
    try:
        user = UserControllers.get_user(id)
        if user:
            UserControllers.del_user(id)
            return {"message": "User removed successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )
