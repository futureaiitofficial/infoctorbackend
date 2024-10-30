
from sqlalchemy.orm import Session
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from uuid import UUID

def create_department(db: Session, department: DepartmentCreate):
    db_department = Department(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_department(db: Session, department_id: UUID):
    return db.query(Department).filter(Department.department_id == department_id).first()

def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Department).offset(skip).limit(limit).all()

def update_department(db: Session, department_id: UUID, department: DepartmentUpdate):
    db_department = db.query(Department).filter(Department.department_id == department_id).first()
    if db_department:
        for key, value in department.dict(exclude_unset=True).items():
            setattr(db_department, key, value)
        db.commit()
        db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: UUID):
    db_department = db.query(Department).filter(Department.department_id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
    return db_department
