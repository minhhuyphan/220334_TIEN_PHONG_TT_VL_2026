import os
import traceback
import sys
from app.utils.database import get_db_connection
from app.config import settings

# Define packages
packages = [
    {
        "name": "Gói Khởi Đầu",
        "description": "Best for personal use",
        "amount_vnd": 20000,
        "tokens": 10,
        "is_active": 1
    },
    {
        "name": "Gói Cơ Bản",
        "description": "Best for personal use",
        "amount_vnd": 100000,
        "tokens": 50,
        "is_active": 1
    },
    {
        "name": "Gói Phổ Biến",
        "description": "Best for personal use",
        "amount_vnd": 200000,
        "tokens": 110,
        "is_active": 1
    },
    {
        "name": "Gói Chuyên Nghiệp",
        "description": "Best for personal use",
        "amount_vnd": 500000,
        "tokens": 300,
        "is_active": 1
    }
]

def seed_packages():
    print(f"Connecting to database type: {settings.DB_TYPE}...")
    
    conn = None
    try:
        conn = get_db_connection()
        db_type = getattr(settings, "DB_TYPE", "sqlite").lower()
        cursor = conn.cursor()

        # Check existing columns
        try:
            cursor.execute("SELECT * FROM packages LIMIT 1")
            col_names = [description[0] for description in cursor.description]
            print(f"Current columns: {col_names}")
            
            # Handle migration from price_vnd to amount_vnd
            if 'price_vnd' in col_names and 'amount_vnd' not in col_names:
                print("Renaming column price_vnd to amount_vnd...")
                cursor.execute("ALTER TABLE packages RENAME COLUMN price_vnd TO amount_vnd")
                print("Renamed successfully.")
                col_names = [c if c != 'price_vnd' else 'amount_vnd' for c in col_names]
        except:
            print("Table packages might not exist. Creating...")

        # Create table with correct syntax for DB type
        auto_inc = "AUTO_INCREMENT" if db_type == "mysql" else "AUTOINCREMENT"
        pk_type = "INT" if db_type == "mysql" else "INTEGER"
        text_type = "LONGTEXT" if db_type == "mysql" else "TEXT"
        
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS packages (
            id {pk_type} PRIMARY KEY {auto_inc},
            name VARCHAR(255) NOT NULL,
            description {text_type},
            amount_vnd INTEGER NOT NULL,
            tokens INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Determine placeholder based on DB type
        p = "%s" if db_type == "mysql" else "?"

        # Check/Insert
        print("Seeding packages...")
        for pkg in packages:
            # Check if exists by name to avoid duplicates
            cursor.execute(f"SELECT id FROM packages WHERE name = {p}", (pkg['name'],))
            existing = cursor.fetchone()
            
            # For MySQL cursor(dictionary=True), existing is a dict
            if isinstance(existing, dict):
                pkg_id = existing['id']
            elif existing:
                pkg_id = existing[0]
            else:
                pkg_id = None
            
            if pkg_id:
                print(f"Update package: {pkg['name']}")
                cursor.execute(f"""
                    UPDATE packages 
                    SET description = {p}, amount_vnd = {p}, tokens = {p}, is_active = {p}, updated_at = CURRENT_TIMESTAMP
                    WHERE id = {p}
                """, (pkg['description'], pkg['amount_vnd'], pkg['tokens'], pkg['is_active'], pkg_id))
            else:
                print(f"Insert package: {pkg['name']}")
                cursor.execute(f"""
                    INSERT INTO packages (name, description, amount_vnd, tokens, is_active)
                    VALUES ({p}, {p}, {p}, {p}, {p})
                """, (pkg['name'], pkg['description'], pkg['amount_vnd'], pkg['tokens'], pkg['is_active']))

        conn.commit()
        print("Done successfully.")
        
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
        sys.exit(1)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    seed_packages()
