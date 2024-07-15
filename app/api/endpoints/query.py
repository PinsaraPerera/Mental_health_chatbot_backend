from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import query_schema, user_schema
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.utils import oauth2
import app.crud.query as query

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


@router.post("/message", response_model=query_schema.QueryResponse)
def chat(chat: query_schema.QueryCreate, db: Session = Depends(get_db)):
    return query.create_query(db, chat)

@router.post("/history", response_model=query_schema.QueryHistory)
def get_history(request: query_schema.QueryBase, db: Session = Depends(get_db)):
    return query.get_history(db, request)
