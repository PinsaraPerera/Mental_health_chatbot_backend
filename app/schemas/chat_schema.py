from typing import List, Optional
from pydantic import BaseModel

class ChatBase(BaseModel):
    user_id: int
    topic: str

class ChatCreate(ChatBase):
    chat_id: int

class Chat(BaseModel):
    chat_id: int
    topic: str

    class Config:
        from_attributes=True

class ChatUpdate(BaseModel):
    topic: str


