from app.models.banner_db import BannerHistoryManager
import json

def check_recent():
    manager = BannerHistoryManager()
    cursor = manager.cursor
    cursor.execute("SELECT id, image_url FROM banner_history ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID {row['id']} URL: {row['image_url']}")
    manager.close()

if __name__ == "__main__":
    check_recent()
