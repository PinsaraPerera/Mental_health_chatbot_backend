from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import chat_schema, user_schema
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.utils import oauth2
import app.crud.chat as conversation

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post("/create", response_model=chat_schema.ChatCreate)
def create_chat(chat: chat_schema.ChatBase, db: Session = Depends(get_db)):
    return conversation.create_chat(db, chat)

@router.get("/get/{chat_id}", response_model=chat_schema.Chat)
def get_chat_history(chat_id: int, db: Session = Depends(get_db)):
    return conversation.get_history(db, chat_id)