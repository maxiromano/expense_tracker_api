### Crear modelo Usuario ###

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id:Optional[str]=None
    username:str
    email:str

class UserCreate(BaseModel):
    username:str
    email:str
    password:str






























