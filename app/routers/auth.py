from fastapi import APIRouter, HTTPException, Depends, Body
from app.models.banner_db import UserManager
from app.config import settings
from app.security.jwt import create_access_token, get_current_user
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter(prefix="/auth", tags=["auth"])

def get_user_manager():
    manager = UserManager()
    try:
        yield manager
    finally:
        manager.close()

@router.post("/google")
async def google_login(
    token: str = Body(..., embed=True), 
    user_manager: UserManager = Depends(get_user_manager)
):
    try:
        # Xác thực Google Token thật
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        # Lấy thông tin user từ token thật
        google_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', 'Unknown User')
        picture = idinfo.get('picture', '')

        # Kiểm tra user trong DB
        user = user_manager.get_by_google_id(google_id)
        
        if not user:
            # Nếu chưa có, tạo mới
            user_id = user_manager.create(
                email=email, 
                full_name=name, 
                google_id=google_id, 
                avatar_url=picture
            )
            user = user_manager.get_by_id(user_id)
        
        # Tạo JWT Token
        access_token = create_access_token(data={"sub": str(user['id']), "email": user['email']})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user['id'],
                "email": user['email'],
                "full_name": user['full_name'],
                "tokens": user['tokens'],
                "avatar": user['avatar_url'],
                "is_admin": user['is_admin'] == 1
            }
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Token")
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(status_code=500, detail="Authentication Failed")

@router.get("/me")
async def get_current_user_profile(user: dict = Depends(get_current_user)):
    return {
        "id": user['id'],
        "email": user['email'],
        "full_name": user['full_name'],
        "tokens": user['tokens'],
        "avatar": user['avatar_url'],
        "is_admin": user['is_admin'] == 1,
        "created_at": user['created_at']
    }
