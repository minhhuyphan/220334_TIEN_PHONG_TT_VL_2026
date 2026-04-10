from fastapi import APIRouter, HTTPException, Depends, Body
from app.models.banner_db import UserManager
from app.config import settings
from app.security.jwt import create_access_token, get_current_user
from app.security.password import get_password_hash, verify_password
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

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

    except ValueError as ve:
        print(f"Google Token Validation Error: {ve}")
        raise HTTPException(status_code=401, detail=f"Invalid Google Token: {ve}")
    except Exception as e:
        print(f"AUTHENTICATION SYSTEM ERROR: {type(e).__name__} - {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Authentication Failed. Please check server logs.")

@router.get("/me")
async def get_current_user_profile(user: dict = Depends(get_current_user)):
    return {
        "id": user['id'],
        "email": user['email'],
        "username": user.get('username'),
        "full_name": user['full_name'],
        "tokens": user['tokens'],
        "avatar": user['avatar_url'],
        "is_admin": user['is_admin'] == 1,
        "created_at": user['created_at']
    }

class LoginRequest(BaseModel):
    account: str # username or email
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

@router.post("/register")
async def register(
    data: RegisterRequest,
    user_manager: UserManager = Depends(get_user_manager)
):
    # Check duplicate username
    if user_manager.get_by_username(data.username):
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")
    
    # Check duplicate email
    if user_manager.get_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email đã được sử dụng")
    
    try:
        pw_hash = get_password_hash(data.password)
        user_id = user_manager.create_with_password(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            password_hash=pw_hash
        )
        return {"success": True, "message": "Đăng ký thành công", "user_id": user_id}
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Lỗi đăng ký hệ thống")

@router.post("/login")
async def login(
    data: LoginRequest,
    user_manager: UserManager = Depends(get_user_manager)
):
    # Try find by username first
    user = user_manager.get_by_username(data.account)
    if not user:
        # Then try by email
        user = user_manager.get_by_email(data.account)
    
    if not user or not user.get('password_hash'):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác")
    
    if not verify_password(data.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác")
    
    # Create Token
    access_token = create_access_token(data={"sub": str(user['id']), "email": user['email']})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "email": user['email'],
            "username": user.get('username'),
            "full_name": user['full_name'],
            "tokens": user['tokens'],
            "avatar": user['avatar_url'],
            "is_admin": user['is_admin'] == 1
        }
    }

class ForgotPasswordRequest(BaseModel):
    account: str # username or email

@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    user_manager: UserManager = Depends(get_user_manager)
):
    user = user_manager.get_by_username(data.account)
    if not user:
        user = user_manager.get_by_email(data.account)
        
    if not user:
        # For security, don't reveal if user exists. 
        # But for this app, we'll return error for easier debugging if user wants.
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản")

    # Check daily limit (2 times)
    now = datetime.now()
    last_at = user.get('last_forgot_password_at')
    count = user.get('forgot_password_count', 0)
    
    if last_at:
        # SQLite/MySQL might return a string or object
        if isinstance(last_at, str):
            try:
                # Common formats: '2023-10-27 10:00:00' or ISO
                last_at_dt = datetime.fromisoformat(last_at.replace(' ', 'T'))
            except:
                last_at_dt = now # fallback
        else:
            last_at_dt = last_at
            
        if last_at_dt.date() == now.date():
            if count >= 2:
                raise HTTPException(status_code=429, detail="Bạn đã vượt quá giới hạn 2 lần quên mật khẩu trong ngày.")
            count += 1
        else:
            count = 1
    else:
        count = 1
        
    user_manager.update_forgot_password_stats(user['id'], count, now.isoformat())
    
    # Generate a temporary token or simple mock link
    reset_token = create_access_token(data={"sub": str(user['id']), "purpose": "reset_password"}, expires_delta=timedelta(minutes=15))
    
    # [THỰC TẾ] Gửi email chứa link reset
    from app.utils.email_utils import send_reset_email
    email_sent = send_reset_email(user['email'], reset_token)
    
    return {
        "message": "Link khôi phục mật khẩu đã được gửi tới email của bạn.",
        "email_sent": email_sent,
        "mock_link": f"http://localhost:3000/reset-password?token={reset_token}" if not email_sent else None
    }

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordRequest,
    user_manager: UserManager = Depends(get_user_manager)
):
    from jose import jwt, JWTError
    
    try:
        payload = jwt.decode(data.token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        purpose = payload.get("purpose")
        
        if not user_id or purpose != "reset_password":
            raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc đã hết hạn")
            
        pw_hash = get_password_hash(data.new_password)
        user_manager.reset_password(int(user_id), pw_hash)
        
        return {"success": True, "message": "Đổi mật khẩu thành công. Vui lòng đăng nhập lại."}
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc đã hết hạn")
