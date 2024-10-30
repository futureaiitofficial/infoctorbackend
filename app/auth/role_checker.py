from fastapi import HTTPException, Depends
from app.auth.utils import get_current_active_user
from app.schemas.user import User
from functools import wraps

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_active_user), **kwargs):
            if current_user.role.name not in allowed_roles:
                raise HTTPException(status_code=403, detail="Not enough permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
