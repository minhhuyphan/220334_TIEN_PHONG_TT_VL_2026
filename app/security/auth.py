from fastapi import Depends, HTTPException
from app.security.jwt import get_current_user

def get_admin_user(user: dict = Depends(get_current_user)):
    """Verify that the current user is an admin"""
    if not user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
