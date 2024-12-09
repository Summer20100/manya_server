from pydantic import BaseModel
 
class UserBase(BaseModel):
    name: str
    email: str

class User(UserBase):
    id: int
    name: str
    email: str