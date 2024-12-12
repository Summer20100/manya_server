from typing import List, Any
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

dbname = os.getenv('DB_NAME')
user = os.getenv('USER_NAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')