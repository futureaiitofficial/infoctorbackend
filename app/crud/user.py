
from sqlalchemy.orm import Session
from app.models.user import User, Role
from app.schemas.user import UserCreate, UserUpdate, RoleCreate, RoleUpdate
from uuid import UUID
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# User CRUD operations
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(**user.dict(exclude={'password'}), password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: UUID):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: UUID, user: UserUpdate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        if 'password' in update_data:
            update_data['password_hash'] = get_password_hash(update_data['password'])
            del update_data['password']
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Role CRUD operations
def create_role(db: Session, role: RoleCreate):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_role(db: Session, role_id: UUID):
    return db.query(Role).filter(Role.role_id == role_id).first()

def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Role).offset(skip).limit(limit).all()

def update_role(db: Session, role_id: UUID, role: RoleUpdate):
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if db_role:
        for key, value in role.dict(exclude_unset=True).items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: UUID):
    db_role = db.query(Role).filter(Role.role_id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role
