from typing import List, Optional
from pydantic import BaseModel
from app.schemas.chat_schema import Chat

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class User(BaseModel):
    id: int
    name: str
    email: str
    chats: List[Chat] = []
