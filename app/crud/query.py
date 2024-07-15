from sqlalchemy.orm import Session
import app.models.query as query
from app.schemas import query_schema
from fastapi import HTTPException, status
from app.core.model import final_result
from datetime import datetime


def create_query(db: Session, chat: query_schema.QueryCreate):

    response = final_result(chat.message, chat.history)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found. Try again later.",
        )

    new_query = query.Query(
        user_id=chat.user_id,
        chat_id=chat.chat_id,
        message=chat.message,
        response=response,
    )

    db.add(new_query)
    db.commit()
    db.refresh(new_query)

    response = query_schema.QueryResponse(
        user_id=new_query.user_id,
        chat_id=new_query.chat_id,
        response=new_query.response,
        date_created=new_query.date_created,
    )

    return response


def get_history(db: Session, request: query_schema.QueryBase):
    history = (
        db.query(query.Query)
        .filter(query.Query.user_id == request.user_id, query.Query.chat_id == request.chat_id)
        .limit(request.limit)
        .all()
    )
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History for user with id {request.user_id} and chat id {request.chat_id} not found",
        )

    response = query_schema.QueryHistory(
        user_id=request.user_id,
        chat_id=request.chat_id,
        history=[
            query_schema.SingleQueryResponse(
                message=h.message,
                response=h.response,
                date_created=h.date_created
            ) for h in history
        ],
        date_created=datetime.now(),
    )

    return response
