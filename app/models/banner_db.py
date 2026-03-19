import sqlite3
import os
from datetime import datetime
from app.config import settings
from app.utils.db_sqlite import get_db_connection

class SQLiteConnection:
    def __init__(self):
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

class ConfigManager(SQLiteConnection):
    def __init__(self):
        super().__init__()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_configs (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def get_value(self, key, default=None):
        self.cursor.execute("SELECT value FROM system_configs WHERE key = ?", (key,))
        row = self.cursor.fetchone()
        return row['value'] if row else default

    def set_value(self, key, value):
        self.cursor.execute("""
            INSERT INTO system_configs (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (key, str(value)))
        self.conn.commit()
        return self.cursor.rowcount

class BannerHistoryManager(SQLiteConnection):
    def get_all(self, user_id=None):
        if user_id:
            sql = "SELECT * FROM banner_history WHERE user_id = ? ORDER BY created_at DESC"
            self.cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT * FROM banner_history ORDER BY created_at DESC"
            self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_recent_by_user(self, user_id, limit=4):
        sql = "SELECT * FROM banner_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?"
        self.cursor.execute(sql, (user_id, limit))
        return [dict(row) for row in self.cursor.fetchall()]

    def count_by_user(self, user_id):
        sql = "SELECT COUNT(*) as count FROM banner_history WHERE user_id = ?"
        self.cursor.execute(sql, (user_id,))
        row = self.cursor.fetchone()
        return row['count'] if row else 0

    def create(self, user_id, description, aspect_ratio, resolution, prompt, image_url, token_cost=1, reference_images=None):
        sql = """
            INSERT INTO banner_history
            (user_id, request_description, aspect_ratio, resolution, prompt_used, image_url, reference_images, token_cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (user_id, description, aspect_ratio, resolution, prompt, image_url, reference_images, token_cost))
        self.conn.commit()
        return self.cursor.lastrowid

    def delete(self, banner_id, user_id):
        sql = "DELETE FROM banner_history WHERE id = ? AND user_id = ?"
        self.cursor.execute(sql, (banner_id, user_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete_all(self, user_id):
        sql = "DELETE FROM banner_history WHERE user_id = ?"
        self.cursor.execute(sql, (user_id,))
        self.conn.commit()
        return self.cursor.rowcount

class TasksManager(SQLiteConnection):
    def __init__(self):
        super().__init__()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL, -- pending, processing, completed, failed
                result TEXT, -- json string of results (e.g. image urls)
                request_data TEXT, -- json string of request params
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def create_task(self, task_id, user_id, request_data):
        self.cursor.execute("""
            INSERT INTO tasks (id, user_id, status, request_data)
            VALUES (?, ?, 'pending', ?)
        """, (task_id, user_id, request_data))
        self.conn.commit()
        return task_id

    def get_task(self, task_id):
        self.cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def update_task(self, task_id, status, result=None, error_message=None):
        sql = """
            UPDATE tasks 
            SET status = ?, result = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.cursor.execute(sql, (status, result, error_message, task_id))
        self.conn.commit()
        return self.cursor.rowcount

class PackageManager(SQLiteConnection):
    def get_all(self, include_inactive=True):
        if include_inactive:
            sql = "SELECT * FROM packages ORDER BY amount_vnd ASC"
        else:
            sql = "SELECT * FROM packages WHERE is_active = 1 ORDER BY amount_vnd ASC"
        self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_by_id(self, package_id):
        self.cursor.execute("SELECT * FROM packages WHERE id = ?", (package_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create(self, name, description, amount_vnd, tokens, is_active=1):
        sql = """
            INSERT INTO packages (name, description, amount_vnd, tokens, is_active)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (name, description, amount_vnd, tokens, is_active))
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, package_id, name, description, amount_vnd, tokens, is_active):
        sql = """
            UPDATE packages 
            SET name = ?, description = ?, amount_vnd = ?, tokens = ?, is_active = ?
            WHERE id = ?
        """
        self.cursor.execute(sql, (name, description, amount_vnd, tokens, is_active, package_id))
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self, package_id):
        # Instead of hard delete, we might want to check for dependencies, but for now simple delete
        # Or better, just soft delete by setting is_active=0, but the user asked for configuration.
        # Let's support delete but usually soft delete is safer. 
        # Given this is SQLite and simple app, I'll allow delete but it might fail if FK constraints exist (which they do in payments).
        # So actually, we should probably only allow deactivating.
        # But if no payments exist, we can delete.
        try:
            self.cursor.execute("DELETE FROM packages WHERE id = ?", (package_id,))
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.IntegrityError:
            # If used in payments, fall back to soft delete (deactivate)
            # But the 'update' method can handle deactivation.
            # Let's just catch the error and return False or raise
            raise Exception("Cannot delete package because it has related payments. Deactivate it instead.")

class PaymentManager(SQLiteConnection):
    def get_packages(self):
        self.cursor.execute("SELECT * FROM packages WHERE is_active = 1")
        return [dict(row) for row in self.cursor.fetchall()]

    def create_payment(self, user_id, package_id, amount_vnd, tokens, payment_code):
        sql = """
            INSERT INTO payments (user_id, package_id, amount_vnd, tokens_received, payment_code)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (user_id, package_id, amount_vnd, tokens, payment_code))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_payment(self, payment_id, status, transaction_id=None):
        sql = "UPDATE payments SET status = ?, sepay_transaction_id = ?, completed_at = ? WHERE id = ?"
        completed_at = datetime.now() if status == 'completed' else None
        self.cursor.execute(sql, (status, transaction_id, completed_at, payment_id))
        self.conn.commit()
        return self.cursor.rowcount

    def get_user_payments(self, user_id):
        sql = "SELECT p.*, pk.name as package_name FROM payments p LEFT JOIN packages pk ON p.package_id = pk.id WHERE p.user_id = ? ORDER BY p.created_at DESC"
        self.cursor.execute(sql, (user_id,))
        return [dict(row) for row in self.cursor.fetchall()]

class UserManager(SQLiteConnection):
    def get_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
        
    def get_by_google_id(self, google_id):
        self.cursor.execute("SELECT * FROM users WHERE google_id = ?", (google_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create(self, email, full_name, google_id=None, avatar_url=None):
        sql = "INSERT INTO users (email, full_name, google_id, avatar_url, tokens) VALUES (?, ?, ?, ?, 5)"
        self.cursor.execute(sql, (email, full_name, google_id, avatar_url))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_token(self, user_id, tokens_to_add):
        # tokens_to_add có thể âm nếu là trừ token
        sql = "UPDATE users SET tokens = tokens + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        self.cursor.execute(sql, (tokens_to_add, user_id))
        self.conn.commit()
        return self.cursor.rowcount
    
    def set_admin(self, email):
        """Set user làm admin thông qua email"""
        sql = "UPDATE users SET is_admin = 1, updated_at = CURRENT_TIMESTAMP WHERE email = ?"
        self.cursor.execute(sql, (email,))
        self.conn.commit()
        return self.cursor.rowcount
    
    def remove_admin(self, email):
        """Gỡ quyền admin của user thông qua email"""
        sql = "UPDATE users SET is_admin = 0, updated_at = CURRENT_TIMESTAMP WHERE email = ?"
        self.cursor.execute(sql, (email,))
        self.conn.commit()
        return self.cursor.rowcount
