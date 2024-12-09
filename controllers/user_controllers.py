from typing import Any
from db_connect import get_connection, execute_query
from queries.user_queries import UserQueries
from config import create_model_from_data
from schemas import User

class UserControllers:
    def create_table():
        execute_query(UserQueries.create_table)

    def insert_user(name: str, email: str):
        execute_query(UserQueries.insert_user, params=(name, email))

    def get_users():
        result = execute_query(UserQueries.get_users, fetch_all=True)
        users = create_model_from_data(result, User)
        print(f"Query result for user: {users}")
        return users
        
        # return execute_query(UserQueries.get_users, fetch_all=True)
    
    def get_user(id):
        result = execute_query(UserQueries.get_user, params=(id,), fetch_all=True)
        user = create_model_from_data(result, User)
        return user
