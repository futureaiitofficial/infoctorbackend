
from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    status: Optional[str] = "active"

class DepartmentCreate(DepartmentBase):
    hospital_id: UUID4

class DepartmentUpdate(DepartmentBase):
    name: Optional[str] = None
    hospital_id: Optional[UUID4] = None

class DepartmentInDB(DepartmentBase):
    department_id: UUID4
    hospital_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Department(DepartmentInDB):
    pass
