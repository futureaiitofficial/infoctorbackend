
from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional
from datetime import date, datetime

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = "active"

class PatientCreate(PatientBase):
    organization_id: UUID4

class PatientUpdate(PatientBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None

class PatientInDB(PatientBase):
    patient_id: UUID4
    organization_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Patient(PatientInDB):
    pass
