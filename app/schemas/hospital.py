
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class HospitalBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = "active"

class HospitalCreate(HospitalBase):
    organization_id: UUID4

class HospitalUpdate(HospitalBase):
    name: Optional[str] = None
    organization_id: Optional[UUID4] = None

class HospitalInDB(HospitalBase):
    hospital_id: UUID4
    organization_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Hospital(HospitalInDB):
    pass
