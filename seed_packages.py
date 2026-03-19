import sqlite3
import os
import traceback
import sys
import datetime

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

DB_PATH = "banner_ai.db"

def seed_packages():
    # If using absolute path for safety in agent env
    db_abs_path = os.path.join(os.getcwd(), DB_PATH)
    
    print(f"Connecting to {db_abs_path}")
    
    conn = None
    try:
        conn = sqlite3.connect(db_abs_path)
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
            
            # Add missing columns safely ONE BY ONE
            if 'description' not in col_names:
                print("Adding missing column: description")
                try:
                    cursor.execute("ALTER TABLE packages ADD COLUMN description TEXT")
                except Exception as e:
                    print(f"Error adding description: {e}")
                
            if 'created_at' not in col_names:
                print("Adding missing column: created_at")
                try:
                    # Try without default first if default fails
                    cursor.execute("ALTER TABLE packages ADD COLUMN created_at TIMESTAMP")
                    cursor.execute("UPDATE packages SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
                except Exception as e:
                    print(f"Error adding created_at: {e}")
                
            if 'updated_at' not in col_names:
                print("Adding missing column: updated_at")
                try:
                    cursor.execute("ALTER TABLE packages ADD COLUMN updated_at TIMESTAMP")
                    cursor.execute("UPDATE packages SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")
                except Exception as e:
                    print(f"Error adding updated_at: {e}")

        except sqlite3.OperationalError as e:
            print(f"OperationalError checking columns: {e}")
            print("Table packages might not exist. Creating...")

        # Create table if it really doesn't exist (this block is safe to run even if table exists safely ignored)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            amount_vnd INTEGER NOT NULL,
            tokens INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Check/Insert
        print("Seeding packages...")
        for pkg in packages:
            # Check if exists by name to avoid duplicates
            cursor.execute("SELECT id FROM packages WHERE name = ?", (pkg['name'],))
            existing = cursor.fetchone()
            
            if existing:
                print(f"Update package: {pkg['name']}")
                cursor.execute("""
                    UPDATE packages 
                    SET description = ?, amount_vnd = ?, tokens = ?, is_active = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (pkg['description'], pkg['amount_vnd'], pkg['tokens'], pkg['is_active'], existing[0]))
            else:
                print(f"Insert package: {pkg['name']}")
                cursor.execute("""
                    INSERT INTO packages (name, description, amount_vnd, tokens, is_active)
                    VALUES (?, ?, ?, ?, ?)
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
