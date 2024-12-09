import psycopg2
from typing import Any
from psycopg2.extensions import connection as Connection
from psycopg2 import DatabaseError
from config import dbname, user, password, host, port

DB_CONFIG = {
    "dbname": dbname,
    "user": user,
    "password": password,
    "host": host,
    "port": port
}

def get_connection() -> Connection:
    try:
        return psycopg2.connect(**DB_CONFIG)
    except DatabaseError as error:
        print(f"Database connection error: {error}")
        raise
    
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
