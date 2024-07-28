from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import doctor_schema
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.crud import doctor

router = APIRouter(
    prefix="/doctor",
    tags=["Doctors"],
)

@router.post("/add", status_code=status.HTTP_201_CREATED)
def create_doctor(request: doctor_schema.DoctorBase, db: Session = Depends(get_db)):
    return doctor.create(request, db)

@router.get("/{id}", response_model=doctor_schema.DoctorResponse)
def get_doctor(id: int, db: Session = Depends(get_db)):
    return doctor.show(id, db)

@router.get("/get/{start}/{limit}", response_model=List[doctor_schema.DoctorResponse])
def get_doctors(start: int, limit: int, db: Session = Depends(get_db)):
    return doctor.show_all(start, limit, db)

@router.put("/update/{id}", response_model=doctor_schema.DoctorResponse)
def update_doctor(id: int, request: doctor_schema.DoctorBase, db: Session = Depends(get_db)):
    return doctor.update(id, request, db)
