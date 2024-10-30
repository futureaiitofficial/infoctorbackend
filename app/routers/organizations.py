
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import organization as crud_organization
from app.schemas.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.database import get_db
from app.auth.utils import get_current_active_user
from app.auth.role_checker import role_required
from app.schemas.user import User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=Organization)
@role_required(["System Administrator"])
async def create_organization(organization: OrganizationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud_organization.create_organization(db=db, organization=organization)

@router.get("/{organization_id}", response_model=Organization)
@role_required(["System Administrator", "HIM Specialist", "Compliance Officer"])
async def read_organization(organization_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_organization = crud_organization.get_organization(db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization

@router.get("/", response_model=List[Organization])
@role_required(["System Administrator", "HIM Specialist", "Compliance Officer"])
async def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    organizations = crud_organization.get_organizations(db, skip=skip, limit=limit)
    return organizations

@router.put("/{organization_id}", response_model=Organization)
@role_required(["System Administrator"])
async def update_organization(organization_id: UUID, organization: OrganizationUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_organization = crud_organization.update_organization(db, organization_id=organization_id, organization=organization)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization

@router.delete("/{organization_id}", response_model=Organization)
@role_required(["System Administrator"])
async def delete_organization(organization_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_organization = crud_organization.delete_organization(db, organization_id=organization_id)
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return db_organization
