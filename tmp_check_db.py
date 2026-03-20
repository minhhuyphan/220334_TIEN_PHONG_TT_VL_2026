from app.models.banner_db import BannerHistoryManager
import json

def check_one():
    manager = BannerHistoryManager()
    cursor = manager.cursor
    # For MySQL
    cursor.execute("SELECT * FROM banner_history WHERE id = 1")
    row = cursor.fetchone()
    print("Record #1:", row)
    manager.close()

if __name__ == "__main__":
    check_one()
