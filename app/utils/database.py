import sqlite3
import mysql.connector
import os
import json
from app.config import settings
from datetime import datetime

def get_db_connection():
    db_type = getattr(settings, "DB_TYPE", "sqlite").lower()
    
    if db_type == "mysql":
        config = {
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD,
            'database': settings.DB_DATABASE,
            'autocommit': True,
            'connect_timeout': 10 # Giới hạn 10 giây để tránh Render bị timeout
        }
        
        # TiDB Cloud requires TLS (SSL)
        if hasattr(settings, "DB_SSL") and settings.DB_SSL:
            ssl_val = settings.DB_SSL
            if isinstance(ssl_val, str) and ssl_val.startswith('{'):
                try:
                    ssl_dict = json.loads(ssl_val)
                    if 'ca' in ssl_dict:
                        config['ssl_ca'] = ssl_dict['ca']
                except:
                    pass
            elif isinstance(ssl_val, str) and ssl_val:
                # If it's a raw string, use as CA path
                config['ssl_ca'] = ssl_val
            
            # Ensure SSL is NOT disabled
            config['ssl_disabled'] = False
            
        conn = mysql.connector.connect(**config)
        return conn
    else:
        # Default to SQLite
        conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    db_type = getattr(settings, "DB_TYPE", "sqlite").lower()
    
    # [FIXED] NEVER DROP TABLES ON STARTUP!
    # tables = ["users", "packages", "payments", "banner_history", "system_configs", "tasks"]
    # for table in tables:
    #     cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    # Auto-increment syntax differs
    auto_inc = "AUTO_INCREMENT" if db_type == "mysql" else "AUTOINCREMENT"
    pk_type = "INT" if db_type == "mysql" else "INTEGER"
    text_type = "LONGTEXT" if db_type == "mysql" else "TEXT"
    bool_type = "BOOLEAN" if db_type == "mysql" else "BOOLEAN"
    ts_default = "CURRENT_TIMESTAMP"
    
    # Bảng Users
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS users (
        id {pk_type} PRIMARY KEY {auto_inc},
        google_id VARCHAR(255) UNIQUE,
        email VARCHAR(255) UNIQUE NOT NULL,
        full_name VARCHAR(255),
        avatar_url {text_type},
        tokens REAL DEFAULT 5,
        is_admin {bool_type} DEFAULT 0,
        created_at DATETIME DEFAULT {ts_default},
        updated_at DATETIME DEFAULT {ts_default}
    )
    ''')
    
    # Bảng Packages
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS packages (
        id {pk_type} PRIMARY KEY {auto_inc},
        name VARCHAR(255) NOT NULL,
        tokens INTEGER NOT NULL,
        amount_vnd INTEGER NOT NULL,
        description {text_type},
        is_active {bool_type} DEFAULT 1
    )
    ''')
    
    # Bảng Payments
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS payments (
        id {pk_type} PRIMARY KEY {auto_inc},
        user_id {pk_type},
        package_id {pk_type},
        amount_vnd INTEGER,
        tokens_received REAL,
        payment_code VARCHAR(255) UNIQUE,
        sepay_transaction_id VARCHAR(255) UNIQUE,
        status VARCHAR(50) DEFAULT 'pending',
        created_at DATETIME DEFAULT {ts_default},
        completed_at DATETIME
    )
    ''')
    
    # Bảng Banner Details
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS banner_history (
        id {pk_type} PRIMARY KEY {auto_inc},
        user_id {pk_type},
        request_description {text_type},
        aspect_ratio VARCHAR(50),
        resolution VARCHAR(50),
        prompt_used {text_type},
        image_url {text_type},
        reference_images {text_type},
        token_cost REAL DEFAULT 1,
        is_public {bool_type} DEFAULT 1,
        created_at DATETIME DEFAULT {ts_default}
    )
    ''')
    
    # Bảng Configs
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS system_configs (
        `key` VARCHAR(255) PRIMARY KEY,
        `value` {text_type} NOT NULL
    )
    ''')

    # Bảng Tasks
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS tasks (
        id VARCHAR(255) PRIMARY KEY,
        user_id {pk_type} NOT NULL,
        status VARCHAR(50) NOT NULL,
        result {text_type},
        request_data {text_type},
        error_message {text_type},
        created_at DATETIME DEFAULT {ts_default},
        updated_at DATETIME DEFAULT {ts_default}
    )
    ''')
    
    # Thêm dữ liệu mẫu cho Packages (Chỉ thêm nếu bảng trống)
    cursor.execute("SELECT COUNT(*) as count FROM packages")
    row = cursor.fetchone()
    count = row[0] if isinstance(row, tuple) else row['count']
    
    if count == 0:
        placeholder = "%s" if db_type == "mysql" else "?"
        cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Khởi Đầu", 10, 20000))
        cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Cơ Bản", 50, 100000))
        cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Phổ Biến", 110, 200000))
        cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Chuyên Nghiệp", 300, 500000))
        print("✅ Added default packages.")
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized ({db_type.upper()}). Persistence is now active.")

def check_and_migrate_db():
    """Kiểm tra và migrate DB an toàn — thêm cột mới nếu chưa tồn tại."""
    init_db()
    
    conn = get_db_connection()
    db_type = getattr(settings, "DB_TYPE", "sqlite").lower()
    cursor = conn.cursor(dictionary=True) if db_type == "mysql" else conn.cursor()
    
    try:
        # Migration: Thêm cột is_public vào banner_history nếu chưa có
        if db_type == "mysql":
            cursor.execute("""
                SELECT COUNT(*) as cnt FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                  AND TABLE_NAME = 'banner_history'
                  AND COLUMN_NAME = 'is_public'
            """)
            row = cursor.fetchone()
            col_exists = (row['cnt'] if isinstance(row, dict) else row[0]) > 0
        else:
            cursor.execute("PRAGMA table_info(banner_history)")
            cols = [r[1] for r in cursor.fetchall()]
            col_exists = 'is_public' in cols
        
        if not col_exists:
            cursor.execute("ALTER TABLE banner_history ADD COLUMN is_public BOOLEAN DEFAULT 1")
            # Đặt tất cả banner cũ là public
            cursor.execute("UPDATE banner_history SET is_public = 1 WHERE is_public IS NULL")
            if db_type != "mysql":
                conn.commit()
            print("✅ Migration: Đã thêm cột 'is_public' vào banner_history")
        else:
            print("✅ Migration: Cột 'is_public' đã tồn tại")
    except Exception as e:
        print(f"⚠️ Migration warning: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_and_migrate_db()
