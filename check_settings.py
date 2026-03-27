from app.config import settings
print(f"Cloud Name: {settings.CLOUDINARY_CLOUD_NAME}")
print(f"API Key: {settings.CLOUDINARY_API_KEY}")
print(f"API Secret: {'*' * len(settings.CLOUDINARY_API_SECRET) if settings.CLOUDINARY_API_SECRET else 'None'}")
