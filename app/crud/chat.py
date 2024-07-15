from sqlalchemy.orm import Session
import app.models.chat as conv
from app.schemas import chat_schema
from fastapi import HTTPException, status

def create_chat(db: Session, chat: chat_schema.ChatBase):
        
        new_chat = conv.Chat(
            user_id=chat.user_id,
            topic=chat.topic
        )
    
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return new_chat

def get_history(db: Session, chat_id: int):

    chat = db.query(conv.Chat).filter(conv.Chat.chat_id == chat_id).first()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found")
    
    

