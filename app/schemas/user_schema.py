from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    name: str
    email: str
