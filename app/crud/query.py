from sqlalchemy.orm import Session
import app.models.query as query
from app.schemas import query_schema
from fastapi import HTTPException, status

def create_query(db: Session, chat: query_schema.QueryCreate):
    new_query = query.Query(
        user_id=chat.user_id,
        message=chat.message,
        response="testing",
    )

    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query

def get_history(db: Session, user_id: int, limit: int):
    history = db.query(query.Query).filter(query.Query.user_id == user_id).limit(limit).all()
    if not history:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"History for user with id {user_id} not found")
    return history