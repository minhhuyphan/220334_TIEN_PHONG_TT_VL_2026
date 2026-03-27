import os
import sqlite3
import cloudinary
import cloudinary.uploader
from app.config import settings
from app.utils.database import get_db_connection

# Load keys
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

def sync_banners():
    print("Syncing banners...")
    banner_dir = os.path.join(os.getcwd(), "banners")
    if not os.path.exists(banner_dir):
        print("No banners directory found.")
        return

    for filename in os.listdir(banner_dir):
        if filename.endswith(".png"):
            path = os.path.join(banner_dir, filename)
            try:
                print(f"Uploading banner {filename}...")
                res = cloudinary.uploader.upload(path, folder="banners", resource_type="image")
                print(f"Uploaded: {res.get('secure_url')}")
            except Exception as e:
                print(f"Failed {filename}: {e}")

def sync_references():
    print("\nSyncing references...")
    ref_dir = os.path.join(os.getcwd(), "uploads", "references")
    if not os.path.exists(ref_dir):
        print("No references directory found.")
        return

    for filename in os.listdir(ref_dir):
        if any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            path = os.path.join(ref_dir, filename)
            try:
                print(f"Uploading reference {filename}...")
                res = cloudinary.uploader.upload(path, folder="references", resource_type="image")
                print(f"Uploaded: {res.get('secure_url')}")
            except Exception as e:
                print(f"Failed {filename}: {e}")

if __name__ == "__main__":
    sync_banners()
    sync_references()
