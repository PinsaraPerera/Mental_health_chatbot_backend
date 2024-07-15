from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class QueryBase(BaseModel):
    user_id: int
    chat_id: int
    limit: int

class QueryCreate(BaseModel):
    user_id: int
    chat_id: int
    message: str
    history: Optional[str] = None

class QueryResponse(BaseModel):
    user_id: int
    chat_id: int
    response: str
    date_created: datetime

class SingleQueryResponse(BaseModel):
    message: str
    response: str
    date_created: datetime

class QueryHistory(BaseModel):
    user_id: int
    chat_id: int
    history: List[SingleQueryResponse] = []
    date_created: datetime