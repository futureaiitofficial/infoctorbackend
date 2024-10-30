
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from uuid import UUID

def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def get_patient(db: Session, patient_id: UUID):
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient_id: UUID, patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if db_patient:
        for key, value in patient.dict(exclude_unset=True).items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: UUID):
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
    return db_patient
