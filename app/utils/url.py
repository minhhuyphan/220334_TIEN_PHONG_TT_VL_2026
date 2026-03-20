from app.config import settings
from fastapi import Request
import os

def fix_banner_url(url: str, request: Request = None):
    """
    Chuyển đổi URL ảnh từ DB sang URL xem ảnh thông qua route /view.
    Đảm bảo URL luôn dùng đúng domain/ip hiện tại của backend.
    """
    if not url: return url
    
    # Lấy tên file từ URL hoặc đường dẫn
    # Ví dụ: http://localhost:55002/api/v1/generate/view/abc.png -> abc.png
    filename = url.split("/")[-1]
    
    # Ưu tiên lấy base URL từ request (để khớp với port/domain người dùng đang truy cập)
    if request:
        base = str(request.base_url).rstrip('/')
        
        # Xử lý Mixed Content: Nếu chạy sau Nginx/Proxy có SSL
        forwarded_proto = request.headers.get("x-forwarded-proto")
        if forwarded_proto == "https" and base.startswith("http://"):
            base = base.replace("http://", "https://", 1)
            
        return f"{base}/api/v1/generate/view/{filename}"
    
    # Fallback dùng API_URL từ cấu hình
    base = settings.API_URL.rstrip('/')
    return f"{base}/api/v1/generate/view/{filename}"
