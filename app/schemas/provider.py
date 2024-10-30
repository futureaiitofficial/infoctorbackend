
from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional
from datetime import datetime

class ProviderBase(BaseModel):
    first_name: str
    last_name: str
    speciality: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    status: Optional[str] = "active"

class ProviderCreate(ProviderBase):
    hospital_id: UUID4

class ProviderUpdate(ProviderBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hospital_id: Optional[UUID4] = None

class ProviderInDB(ProviderBase):
    provider_id: UUID4
    hospital_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Provider(ProviderInDB):
    pass
