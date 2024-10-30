
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import department as crud_department
from app.schemas.department import Department, DepartmentCreate, DepartmentUpdate
from app.database import get_db
from app.auth.utils import get_current_active_user
from app.auth.role_checker import role_required
from app.schemas.user import User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=Department)
@role_required(["System Administrator", "HIM Specialist"])
async def create_department(department: DepartmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud_department.create_department(db=db, department=department)

@router.get("/{department_id}", response_model=Department)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def read_department(department_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_department = crud_department.get_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.get("/", response_model=List[Department])
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    departments = crud_department.get_departments(db, skip=skip, limit=limit)
    return departments

@router.put("/{department_id}", response_model=Department)
@role_required(["System Administrator", "HIM Specialist"])
async def update_department(department_id: UUID, department: DepartmentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_department = crud_department.update_department(db, department_id=department_id, department=department)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department

@router.delete("/{department_id}", response_model=Department)
@role_required(["System Administrator"])
async def delete_department(department_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_department = crud_department.delete_department(db, department_id=department_id)
    if db_department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return db_department
