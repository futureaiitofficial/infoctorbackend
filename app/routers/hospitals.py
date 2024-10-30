
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import hospital as crud_hospital
from app.schemas.hospital import Hospital, HospitalCreate, HospitalUpdate
from app.database import get_db
from app.auth.utils import get_current_active_user
from app.auth.role_checker import role_required
from app.schemas.user import User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=Hospital)
@role_required(["System Administrator", "HIM Specialist"])
async def create_hospital(hospital: HospitalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud_hospital.create_hospital(db=db, hospital=hospital)

@router.get("/{hospital_id}", response_model=Hospital)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse"])
async def read_hospital(hospital_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_hospital = crud_hospital.get_hospital(db, hospital_id=hospital_id)
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_hospital

@router.get("/", response_model=List[Hospital])
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse"])
async def read_hospitals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    hospitals = crud_hospital.get_hospitals(db, skip=skip, limit=limit)
    return hospitals

@router.put("/{hospital_id}", response_model=Hospital)
@role_required(["System Administrator", "HIM Specialist"])
async def update_hospital(hospital_id: UUID, hospital: HospitalUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_hospital = crud_hospital.update_hospital(db, hospital_id=hospital_id, hospital=hospital)
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_hospital

@router.delete("/{hospital_id}", response_model=Hospital)
@role_required(["System Administrator"])
async def delete_hospital(hospital_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_hospital = crud_hospital.delete_hospital(db, hospital_id=hospital_id)
    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return db_hospital
