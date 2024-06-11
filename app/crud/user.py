from sqlalchemy.orm import Session
import app.models.user as user
from app.schemas import user_schema
from fastapi import HTTPException, status
from app.utils import hashing

def create(request: user_schema.User, db: Session):
    new_user = user.User(
        name=request.name,
        email=request.email,
        password=hashing.Hash.bcrypt(request.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id: int, db: Session):
    user_found = db.query(user.User).filter(user.User.id == id).first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user_found

def show_by_email(email: str, db: Session):
    user_found = db.query(user.User).filter(user.User.email == email).first()
    if not user_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {email} not found")
    return user_found