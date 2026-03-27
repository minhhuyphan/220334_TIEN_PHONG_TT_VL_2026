import os
import json
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

def update_db_with_cloudinary():
    conn = get_db_connection()
    db_type = getattr(settings, "DB_TYPE", "sqlite").lower()
    p = "%s" if db_type == "mysql" else "?"
    
    if db_type == "mysql":
        cursor = conn.cursor(dictionary=True)
    else:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row if db_type == "sqlite" else None # Handled in get_db_connection usually

    # 1. Update banner_history
    print("Updating banner_history...")
    cursor.execute("SELECT id, image_url, reference_images FROM banner_history")
    rows = cursor.fetchall()
    
    banner_dir = os.path.join(os.getcwd(), "banners")
    ref_dir = os.path.join(os.getcwd(), "uploads", "references")

    for row in rows:
        row_id = row['id']
        image_url = row['image_url']
        reference_images_json = row['reference_images']
        
        # Check if banner image needs upload (is local)
        if image_url and ("/view/" in image_url or not image_url.startswith("http")):
            filename = image_url.split("/")[-1]
            path = os.path.join(banner_dir, filename)
            if os.path.exists(path):
                try:
                    print(f"Uploading banner for history ID {row_id} ({filename})...")
                    res = cloudinary.uploader.upload(path, folder="banners", resource_type="image")
                    new_url = res.get('secure_url')
                    if new_url:
                        cursor.execute(f"UPDATE banner_history SET image_url = {p} WHERE id = {p}", (new_url, row_id))
                        print(f"  Updated URL to: {new_url}")
                except Exception as e:
                    print(f"  Failed to upload banner {filename}: {e}")
            else:
                print(f"  Local file {path} not found for banner {row_id}")

        # Check if reference images need update
        if reference_images_json:
            try:
                refs = json.loads(reference_images_json)
                updated_refs = []
                changed = False
                for ref in refs:
                    if 'url' not in ref or not ref['url'].startswith("http"):
                        ref_path = os.path.join(ref_dir, ref['path'])
                        if os.path.exists(ref_path):
                            try:
                                print(f"  Uploading reference {ref['path']} for history ID {row_id}...")
                                res = cloudinary.uploader.upload(ref_path, folder="references", resource_type="image")
                                ref['url'] = res.get('secure_url')
                                changed = True
                            except Exception as e:
                                print(f"    Failed to upload reference: {e}")
                    updated_refs.append(ref)
                
                if changed:
                    cursor.execute(f"UPDATE banner_history SET reference_images = {p} WHERE id = {p}", (json.dumps(updated_refs), row_id))
                    print(f"  Updated reference_images for ID {row_id}")
            except Exception as e:
                print(f"  Error processing reference_images for ID {row_id}: {e}")

    conn.commit()
    conn.close()
    print("DB Update finished.")

if __name__ == "__main__":
    import sqlite3 # Import specifically for Row access in case
    update_db_with_cloudinary()
