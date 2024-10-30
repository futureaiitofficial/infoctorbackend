
from sqlalchemy.orm import Session
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from uuid import UUID

def create_hospital(db: Session, hospital: HospitalCreate):
    db_hospital = Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def get_hospital(db: Session, hospital_id: UUID):
    return db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()

def get_hospitals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Hospital).offset(skip).limit(limit).all()

def update_hospital(db: Session, hospital_id: UUID, hospital: HospitalUpdate):
    db_hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if db_hospital:
        for key, value in hospital.dict(exclude_unset=True).items():
            setattr(db_hospital, key, value)
        db.commit()
        db.refresh(db_hospital)
    return db_hospital

def delete_hospital(db: Session, hospital_id: UUID):
    db_hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if db_hospital:
        db.delete(db_hospital)
        db.commit()
    return db_hospital
