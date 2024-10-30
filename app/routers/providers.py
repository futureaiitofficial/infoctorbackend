
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.crud import provider as crud_provider
from app.schemas.provider import Provider, ProviderCreate, ProviderUpdate
from app.database import get_db
from app.auth.utils import get_current_active_user
from app.auth.role_checker import role_required
from app.schemas.user import User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=Provider)
@role_required(["System Administrator", "HIM Specialist"])
async def create_provider(provider: ProviderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return crud_provider.create_provider(db=db, provider=provider)

@router.get("/{provider_id}", response_model=Provider)
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def read_provider(provider_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_provider = crud_provider.get_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

@router.get("/", response_model=List[Provider])
@role_required(["System Administrator", "HIM Specialist", "Physician", "Nurse", "Medical Assistant"])
async def read_providers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    providers = crud_provider.get_providers(db, skip=skip, limit=limit)
    return providers

@router.put("/{provider_id}", response_model=Provider)
@role_required(["System Administrator", "HIM Specialist"])
async def update_provider(provider_id: UUID, provider: ProviderUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_provider = crud_provider.update_provider(db, provider_id=provider_id, provider=provider)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider

@router.delete("/{provider_id}", response_model=Provider)
@role_required(["System Administrator"])
async def delete_provider(provider_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_provider = crud_provider.delete_provider(db, provider_id=provider_id)
    if db_provider is None:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_provider
