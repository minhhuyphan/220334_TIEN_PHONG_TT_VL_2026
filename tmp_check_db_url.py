from app.models.banner_db import BannerHistoryManager
import json

def check_one():
    manager = BannerHistoryManager()
    cursor = manager.cursor
    cursor.execute("SELECT id, image_url FROM banner_history WHERE id = 1")
    row = cursor.fetchone()
    print("Record #1 URL:", row['image_url'] if row else "NOT FOUND")
    manager.close()

if __name__ == "__main__":
    check_one()
