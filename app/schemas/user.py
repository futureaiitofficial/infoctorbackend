
from pydantic import BaseModel, UUID4, EmailStr
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    name: Optional[str] = None

class RoleInDB(RoleBase):
    role_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Role(RoleInDB):
    pass

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    status: Optional[str] = "active"

class UserCreate(UserBase):
    password: str
    organization_id: UUID4
    role_id: UUID4

class UserUpdate(UserBase):
    password: Optional[str] = None
    organization_id: Optional[UUID4] = None
    role_id: Optional[UUID4] = None

class UserInDB(UserBase):
    user_id: UUID4
    organization_id: UUID4
    role_id: UUID4
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserInDB):
    role: Role
