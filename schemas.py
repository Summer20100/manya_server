from pydantic import BaseModel

# USER
 
class UserBase(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str
