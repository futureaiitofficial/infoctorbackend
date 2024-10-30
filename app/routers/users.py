
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from app.crud import user as crud_user
from app.schemas.user import User, UserCreate, UserUpdate, Role, RoleCreate, RoleUpdate, Token
from app.database import get_db
from app.auth.utils import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.role_checker import role_required
from uuid import UUID

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=User)
@role_required(["System Administrator"])
async def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)

@router.get("/users/", response_model=List[User])
@role_required(["System Administrator", "HIM Specialist"])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/{user_id}", response_model=User)
@role_required(["System Administrator", "HIM Specialist"])
async def read_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=User)
@role_required(["System Administrator"])
async def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud_user.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=User)
@role_required(["System Administrator"])
async def delete_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_user = crud_user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Role routes
@router.post("/roles/", response_model=Role)
@role_required(["System Administrator"])
async def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_role = crud_user.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud_user.create_role(db=db, role=role)

@router.get("/roles/", response_model=List[Role])
@role_required(["System Administrator", "HIM Specialist"])
async def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    roles = crud_user.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/roles/{role_id}", response_model=Role)
@role_required(["System Administrator", "HIM Specialist"])
async def read_role(role_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_role = crud_user.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/roles/{role_id}", response_model=Role)
@role_required(["System Administrator"])
async def update_role(role_id: UUID, role: RoleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_role = crud_user.update_role(db, role_id=role_id, role=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.delete("/roles/{role_id}", response_model=Role)
@role_required(["System Administrator"])
async def delete_role(role_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_role = crud_user.delete_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role
