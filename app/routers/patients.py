
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from app.crud import patient as crud_patient
from app.schemas.patient import Patient, PatientCreate, PatientUpdate
from app.database import get_db
from app.auth.utils import get_current_active_user
from app.auth.role_checker import role_required
from app.schemas.user import User
from app.interoperability import patient_to_fhir, fhir_to_patient, patient_to_hl7, hl7_to_patient, send_hl7_message
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=Patient)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def create_patient(patient: PatientCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud_patient.create_patient(db=db, patient=patient)

@router.get("/{patient_id}", response_model=Patient)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def read_patient(patient_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_patient = crud_patient.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.get("/", response_model=List[Patient])
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    patients = crud_patient.get_patients(db, skip=skip, limit=limit)
    return patients

@router.put("/{patient_id}", response_model=Patient)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def update_patient(patient_id: UUID, patient: PatientUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_patient = crud_patient.update_patient(db, patient_id=patient_id, patient=patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.delete("/{patient_id}", response_model=Patient)
@role_required(["System Administrator", "HIM Specialist"])
async def delete_patient(patient_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_patient = crud_patient.delete_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.get("/{patient_id}/fhir", response_model=dict)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def get_patient_fhir(patient_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_patient = crud_patient.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_to_fhir(db_patient)

@router.post("/fhir", response_model=Patient)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def create_patient_fhir(fhir_data: dict = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    patient_create = fhir_to_patient(fhir_data)
    return crud_patient.create_patient(db=db, patient=patient_create)

@router.get("/{patient_id}/hl7", response_model=str)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def get_patient_hl7(patient_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_patient = crud_patient.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_to_hl7(db_patient)

@router.post("/hl7", response_model=Patient)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def create_patient_hl7(hl7_message: str = Body(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    patient_create = hl7_to_patient(hl7_message)
    return crud_patient.create_patient(db=db, patient=patient_create)

@router.post("/send_hl7")
@role_required(["System Administrator", "HIM Specialist"])
async def send_hl7(patient_id: UUID, host: str, port: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_patient = crud_patient.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    hl7_message = patient_to_hl7(db_patient)
    response = await send_hl7_message(host, port, hl7_message)
    return {"message": "HL7 message sent successfully", "response": response}
