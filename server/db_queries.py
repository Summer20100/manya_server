from typing import Any
from db_connection import get_connection

# Универсальная функция для выполнения запросов
def execute_query(query: str, params: tuple = (), fetch_one: bool = False, fetch_all: bool = False) -> Any:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if fetch_one:
                    return cur.fetchone()
                if fetch_all:
                    return cur.fetchall()
                conn.commit()
    except Exception as error:
        print(f"Query execution error: {error}")
        raise

# Пример функции для создания таблицы
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """
    execute_query(query)

# Пример функции для вставки данных
def insert_user(name: str, email: str):
    query = "INSERT INTO users (name, email) VALUES (%s, %s);"
    execute_query(query, params=(name, email))

# Пример функции для получения всех пользователей
def get_all_users():
    query = "SELECT * FROM users;"
    return execute_query(query, fetch_all=True)
