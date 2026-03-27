import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# Load .env
load_dotenv(override=True)

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")

print(f"Cloud Name: {cloud_name}")
print(f"API Key: {api_key}")
print(f"API Secret: {'*' * len(api_secret) if api_secret else 'None'}")

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True
)

def test_upload():
    # Create a dummy image or use an existing one
    dummy_path = "test_image.png"
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='red')
    img.save(dummy_path)
    
    try:
        print(f"Attempting to upload {dummy_path}...")
        response = cloudinary.uploader.upload(
            dummy_path,
            folder="test_folder",
            resource_type="image"
        )
        print("Upload successful!")
        print(f"URL: {response.get('secure_url')}")
    except Exception as e:
        print(f"Upload failed: {e}")
    finally:
        if os.path.exists(dummy_path):
            os.remove(dummy_path)

if __name__ == "__main__":
    test_upload()
