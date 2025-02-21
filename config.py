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
key = os.getenv('KEY_SERVER')
sectetKey = os.getenv('SECRET_KEY')
regKey = os.getenv('REGISTER_KEY')
delKey = os.getenv('DELETE_KEY')


cookie_max_age = (12*60*60)               #  секунды
token_timedelta_sec_val = (12*60*60)        # секунды