
from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from uuid import UUID

def create_organization(db: Session, organization: OrganizationCreate):
    db_organization = Organization(**organization.dict())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

def get_organization(db: Session, organization_id: UUID):
    return db.query(Organization).filter(Organization.organization_id == organization_id).first()

def get_organizations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organization).offset(skip).limit(limit).all()

def update_organization(db: Session, organization_id: UUID, organization: OrganizationUpdate):
    db_organization = db.query(Organization).filter(Organization.organization_id == organization_id).first()
    if db_organization:
        for key, value in organization.dict(exclude_unset=True).items():
            setattr(db_organization, key, value)
        db.commit()
        db.refresh(db_organization)
    return db_organization

def delete_organization(db: Session, organization_id: UUID):
    db_organization = db.query(Organization).filter(Organization.organization_id == organization_id).first()
    if db_organization:
        db.delete(db_organization)
        db.commit()
    return db_organization
