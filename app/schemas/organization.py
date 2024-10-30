
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class OrganizationBase(BaseModel):
    name: str
    subscription_plan: Optional[str] = None
    status: Optional[str] = "active"

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None
    subscription_plan: Optional[str] = None
    status: Optional[str] = None

class OrganizationInDB(OrganizationBase):
    organization_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Organization(OrganizationInDB):
    pass
