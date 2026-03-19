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
    
    # Drop tables for re-init (be careful with production!)
    tables = ["users", "packages", "payments", "banner_history", "system_configs", "tasks"]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
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
    
    # Thêm dữ liệu mẫu cho Packages
    placeholder = "%s" if db_type == "mysql" else "?"
    cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Khởi Đầu", 10, 20000))
    cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Cơ Bản", 50, 100000))
    cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Phổ Biến", 110, 200000))
    cursor.execute(f"INSERT INTO packages (name, tokens, amount_vnd) VALUES ({placeholder}, {placeholder}, {placeholder})", ("Gói Chuyên Nghiệp", 300, 500000))
    
    conn.commit()
    conn.close()
    print(f"✅ Database re-initialized ({db_type.upper()}).")

def check_and_migrate_db():
    # Simplification: For now, if MySQL, just ensure tables exist. 
    # Migration is complex across different DBs.
    init_db()

if __name__ == "__main__":
    check_and_migrate_db()
