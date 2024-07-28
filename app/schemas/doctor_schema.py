from typing import List, Optional
from pydantic import BaseModel

class DoctorBase(BaseModel):
    name: str
    address: str
    specialty: str
    contact: str

class DoctorResponse(DoctorBase):
    doctor_id: int

    