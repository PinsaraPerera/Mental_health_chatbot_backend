from typing import List, Optional
from pydantic import BaseModel
from app.schemas.chat_schema import Chat
from app.schemas.user_schema import User


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

class LoginData(Token):
    id: int
    name: str
    email: str
    chats: List[Chat] = []