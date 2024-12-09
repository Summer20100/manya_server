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

def create_model_from_data(data: List[List[Any]], model_class: BaseModel):
    field_names = model_class.__annotations__.keys()
    result = []
    
    for item in data:
        if len(item) == len(field_names):
            result.append(model_class(**{field: value.strip() if isinstance(value, str) else value
                                          for field, value in zip(field_names, item)}))
    return result