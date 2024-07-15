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

    


