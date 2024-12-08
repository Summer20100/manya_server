import psycopg2
from psycopg2.extensions import connection as Connection
from psycopg2 import DatabaseError

# Параметры подключения
DB_CONFIG = {
    "dbname": "mariadmitr",  # Имя базы данных
    "user": "mariadmitr",        # Имя пользователя
    "password": "Masha_hrenova_1996",    # Пароль
    "host": "pg3.sweb.ru",            # Хост
    "port": 5432                    # Порт (по умолчанию 5432)
}

# Функция для получения соединения
def get_connection() -> Connection:
    try:
        return psycopg2.connect(**DB_CONFIG)
    except DatabaseError as error:
        print(f"Database connection error: {error}")
        raise
