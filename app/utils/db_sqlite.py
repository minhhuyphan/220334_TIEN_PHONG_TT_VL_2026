import sqlite3
import os
from app.config import settings
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Xóa dư: Reset bảng để cập nhật schema mới (Google Auth)
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS packages")
    cursor.execute("DROP TABLE IF EXISTS payments")
    cursor.execute("DROP TABLE IF EXISTS banner_history")
    
    # Bảng Users (Google Login Only)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT,
        avatar_url TEXT,
        tokens REAL DEFAULT 5,
        is_admin BOOLEAN DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Bảng Packages (Các gói nạp token)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tokens INTEGER NOT NULL,
        amount_vnd INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1
    )
    ''')
    
    # Bảng Payments (Lịch sử nạp tiền)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        package_id INTEGER,
        amount_vnd INTEGER,
        tokens_received REAL,
        payment_code TEXT UNIQUE,
        sepay_transaction_id TEXT UNIQUE,
        status TEXT DEFAULT 'pending', -- pending, completed, failed
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        completed_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (package_id) REFERENCES packages (id)
    )
    ''')
    
    # Bảng Banner Details (Lịch sử sinh ảnh - chi tiết)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS banner_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        request_description TEXT,
        aspect_ratio TEXT,
        resolution TEXT,
        prompt_used TEXT,
        image_url TEXT,
        reference_images TEXT,  -- JSON string: [{"path": "...", "label": "..."}]
        token_cost REAL DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Thêm dữ liệu mẫu cho Packages
    cursor.execute("INSERT INTO packages (name, tokens, amount_vnd) VALUES (?, ?, ?)", ("Gói Khởi Đầu", 10, 20000))
    cursor.execute("INSERT INTO packages (name, tokens, amount_vnd) VALUES (?, ?, ?)", ("Gói Cơ Bản", 50, 100000))
    cursor.execute("INSERT INTO packages (name, tokens, amount_vnd) VALUES (?, ?, ?)", ("Gói Phổ Biến", 110, 200000))
    cursor.execute("INSERT INTO packages (name, tokens, amount_vnd) VALUES (?, ?, ?)", ("Gói Chuyên Nghiệp", 300, 500000))
    
    # Thêm tài khoản admin mẫu (Google ID giả lập cho local dev nếu cần)
    # cursor.execute("INSERT INTO users (email, full_name, tokens, is_admin) VALUES (?, ?, ?, ?)", 
    #                ('admin@example.com', 'Admin User', 999999, 1))

    conn.commit()
    conn.close()
    print("✅ Database re-initialized (Schema Updated for Google Login).")

def check_and_migrate_db():
    """
    Kiểm tra và cập nhật schema DB mà không làm mất dữ liệu.
    Chạy mỗi khi khởi động app.
    """
    print("🔄 Checking database schema...")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Đảm bảo các bảng tồn tại (Create if not exists)
    # Bảng Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT,
        avatar_url TEXT,
        tokens REAL DEFAULT 5,
        is_admin BOOLEAN DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Bảng Packages
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tokens INTEGER NOT NULL,
        amount_vnd INTEGER NOT NULL,
        is_active BOOLEAN DEFAULT 1
    )
    ''')
    
    # Bảng Payments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        package_id INTEGER,
        amount_vnd INTEGER,
        tokens_received REAL,
        payment_code TEXT UNIQUE,
        sepay_transaction_id TEXT UNIQUE,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        completed_at DATETIME,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (package_id) REFERENCES packages (id)
    )
    ''')
    
    # Bảng Banner Details
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS banner_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        request_description TEXT,
        aspect_ratio TEXT,
        resolution TEXT,
        prompt_used TEXT,
        image_url TEXT,
        token_cost REAL DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 2. Kiểm tra và thêm cột mới (Migration)
    # Check reference_images in banner_history
    cursor.execute("PRAGMA table_info(banner_history)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'reference_images' not in columns:
        print("⚠️ Missing column 'reference_images' in banner_history. Adding...")
        try:
            cursor.execute("ALTER TABLE banner_history ADD COLUMN reference_images TEXT")
            print("✅ Added column 'reference_images'")
        except Exception as e:
            print(f"❌ Error adding column reference_images: {e}")

    # Check description in packages
    cursor.execute("PRAGMA table_info(packages)")
    package_columns = [info[1] for info in cursor.fetchall()]
    if 'description' not in package_columns:
        print("⚠️ Missing column 'description' in packages. Adding...")
        try:
            cursor.execute("ALTER TABLE packages ADD COLUMN description TEXT DEFAULT ''")
            print("✅ Added column 'description'")
        except Exception as e:
            print(f"❌ Error adding column description: {e}")
            
    conn.commit()
    conn.close()
    print("✅ Database schema check completed.")

if __name__ == "__main__":
    # init_db() # DANGER: Only run this if you want to request DB
    check_and_migrate_db()
