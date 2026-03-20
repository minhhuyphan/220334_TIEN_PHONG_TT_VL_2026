import cloudinary
import cloudinary.uploader
from app.config import settings
import os

# Cấu hình Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def upload_to_cloudinary(file_path: str, folder: str = "banners") -> str:
    """
    Tải ảnh lên Cloudinary và trả về URL ổn định.
    """
    if not settings.CLOUDINARY_API_KEY or not settings.CLOUDINARY_API_SECRET:
        return None
        
    try:
        if not os.path.exists(file_path):
            return None
            
        response = cloudinary.uploader.upload(
            file_path, 
            folder=folder,
            resource_type="image"
        )
        return response.get("secure_url")
    except Exception as e:
        print(f"Cloudinary Error: {e}")
        return None
