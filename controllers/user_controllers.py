from typing import Any
from db_connect import get_connection, execute_query
from queries.user_queries import UserQueries
from config import create_model_from_data
from schemas import User

class UserControllers:
    def create_table():
        execute_query(UserQueries.create_table)

    def insert_user(name: str, email: str):
        execute_query(UserQueries.insert_user, params=(name, email, ))

    def get_users():
        result = execute_query(UserQueries.get_users, fetch_all=True)
        users = create_model_from_data(result, User)
        return users
    
    def get_user(id: int):
        result = execute_query(UserQueries.get_user, params=(id,), fetch_all=True)
        user = create_model_from_data(result, User)
        return user

    def update_user(name: str, email: str, id: int):
        execute_query(UserQueries.update_user, params=(name, email, id, ))
    
    def del_user(id: int):
        execute_query(UserQueries.del_user, params=(id,))

