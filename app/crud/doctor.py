from sqlalchemy.orm import Session
import app.models.doctor as doctor_model
from app.schemas import user_schema
from fastapi import HTTPException, status

def create(request: doctor_model.Doctor, db: Session):
    existing_doctor = db.query(doctor_model.Doctor).filter(doctor_model.Doctor.name == request.name).first()
    
    if existing_doctor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor already registered")

    new_doctor = doctor_model.Doctor(
        name=request.name,
        address=request.address,
        specialty=request.specialty,
        contact=request.contact,
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

def show(id: int, db: Session):
    doctor_found = db.query(doctor_model.Doctor).filter(doctor_model.Doctor.doctor_id == id).first()
    if not doctor_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with id {id} not found")
    return doctor_found

def show_all(start: int, limit: int, db: Session):
    doctors = db.query(doctor_model.Doctor).offset(start).limit(limit).all()
    return doctors

def update(id: int, request: doctor_model.Doctor, db: Session):
    doctor_found = db.query(doctor_model.Doctor).filter(doctor_model.Doctor.doctor_id == id).first()
    if not doctor_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with id {id} not found")
    
    doctor_found.name = request.name
    doctor_found.address = request.address
    doctor_found.specialty = request.specialty
    doctor_found.contact = request.contact

    db.commit()
    db.refresh(doctor_found)
    return doctor_found
