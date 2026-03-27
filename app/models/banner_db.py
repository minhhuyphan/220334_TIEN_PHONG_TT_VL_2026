import sqlite3
import os
from datetime import datetime
from app.config import settings
from app.utils.database import get_db_connection

class DBConnection:
    def __init__(self):
        self.conn = get_db_connection()
        db_type = getattr(settings, "DB_TYPE", "sqlite").lower()
        self.db_type = db_type
        
        # Determine placeholder based on DB type
        self.p = "%s" if db_type == "mysql" else "?"
        
        if db_type == "mysql":
            # MySQL connector uses dictionary=True for dict-like rows
            self.cursor = self.conn.cursor(dictionary=True)
        else:
            # SQLite uses row_factory (already set in get_db_connection)
            self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

class ConfigManager(DBConnection):
    def __init__(self):
        super().__init__()
        # Table creation is now handled in init_db utility, but keep for safety if needed
        pass

    def get_value(self, key, default=None):
        self.cursor.execute(f"SELECT value FROM system_configs WHERE `key` = {self.p}", (key,))
        row = self.cursor.fetchone()
        return row['value'] if row else default

    def set_value(self, key, value):
        if self.db_type == "mysql":
            sql = f"INSERT INTO system_configs (`key`, `value`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `value` = VALUES(`value`)"
        else:
            sql = f"INSERT INTO system_configs (`key`, `value`) VALUES (?, ?) ON CONFLICT(`key`) DO UPDATE SET `value` = excluded.value"
        self.cursor.execute(sql, (key, str(value)))
        self.commit()
        return self.cursor.rowcount

class BannerHistoryManager(DBConnection):
    def get_all(self, user_id=None):
        if user_id:
            sql = f"SELECT * FROM banner_history WHERE user_id = {self.p} ORDER BY created_at DESC"
            self.cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT * FROM banner_history ORDER BY created_at DESC"
            self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_recent_by_user(self, user_id, limit=4):
        sql = f"SELECT * FROM banner_history WHERE user_id = {self.p} ORDER BY created_at DESC LIMIT {self.p}"
        self.cursor.execute(sql, (user_id, limit))
        return [dict(row) for row in self.cursor.fetchall()]

    def count_by_user(self, user_id):
        sql = f"SELECT COUNT(*) as count FROM banner_history WHERE user_id = {self.p}"
        self.cursor.execute(sql, (user_id,))
        row = self.cursor.fetchone()
        return row['count'] if row else 0

    def get_public_banners(self, limit=20):
        """Lấy banner cho gallery trang chủ — hiển thị tất cả banner có ảnh hợp lệ."""
        sql = f"""SELECT bh.id, bh.image_url, bh.request_description, bh.aspect_ratio,
                         bh.created_at, u.full_name, u.avatar_url
                  FROM banner_history bh
                  LEFT JOIN users u ON bh.user_id = u.id
                  WHERE bh.image_url IS NOT NULL AND bh.image_url != ''
                  ORDER BY bh.created_at DESC
                  LIMIT {self.p}"""
        self.cursor.execute(sql, (limit,))
        return [dict(row) for row in self.cursor.fetchall()]

    def set_public(self, banner_id, user_id, is_public: bool):
        """Toggle is_public cho banner của user."""
        sql = f"UPDATE banner_history SET is_public = {self.p} WHERE id = {self.p} AND user_id = {self.p}"
        self.cursor.execute(sql, (1 if is_public else 0, banner_id, user_id))
        self.commit()
        return self.cursor.rowcount

    def create(self, user_id, description, aspect_ratio, resolution, prompt, image_url, token_cost=1, reference_images=None, is_public=True):
        sql = f"""
            INSERT INTO banner_history
            (user_id, request_description, aspect_ratio, resolution, prompt_used, image_url, reference_images, token_cost, is_public)
            VALUES ({self.p}, {self.p}, {self.p}, {self.p}, {self.p}, {self.p}, {self.p}, {self.p}, {self.p})
        """
        self.cursor.execute(sql, (user_id, description, aspect_ratio, resolution, prompt, image_url, reference_images, token_cost, 1 if is_public else 0))
        self.commit()
        return self.cursor.lastrowid

    def delete(self, banner_id, user_id):
        sql = f"DELETE FROM banner_history WHERE id = {self.p} AND user_id = {self.p}"
        self.cursor.execute(sql, (banner_id, user_id))
        self.commit()
        return self.cursor.rowcount

    def delete_all(self, user_id):
        sql = f"DELETE FROM banner_history WHERE user_id = {self.p}"
        self.cursor.execute(sql, (user_id,))
        self.commit()
        return self.cursor.rowcount

class TasksManager(DBConnection):
    def create_task(self, task_id, user_id, request_data):
        self.cursor.execute(f"""
            INSERT INTO tasks (id, user_id, status, request_data)
            VALUES ({self.p}, {self.p}, 'pending', {self.p})
        """, (task_id, user_id, request_data))
        self.commit()
        return task_id

    def get_task(self, task_id):
        self.cursor.execute(f"SELECT * FROM tasks WHERE id = {self.p}", (task_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def update_task(self, task_id, status, result=None, error_message=None):
        sql = f"""
            UPDATE tasks 
            SET status = {self.p}, result = {self.p}, error_message = {self.p}, updated_at = CURRENT_TIMESTAMP
            WHERE id = {self.p}
        """
        self.cursor.execute(sql, (status, result, error_message, task_id))
        self.commit()
        return self.cursor.rowcount

class PackageManager(DBConnection):
    def get_all(self, include_inactive=True):
        if include_inactive:
            sql = "SELECT * FROM packages ORDER BY amount_vnd ASC"
        else:
            sql = f"SELECT * FROM packages WHERE is_active = {self.p} ORDER BY amount_vnd ASC"
            self.cursor.execute(sql, (1,))
            return [dict(row) for row in self.cursor.fetchall()]
        self.cursor.execute(sql)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_by_id(self, package_id):
        self.cursor.execute(f"SELECT * FROM packages WHERE id = {self.p}", (package_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create(self, name, description, amount_vnd, tokens, is_active=1):
        sql = f"""
            INSERT INTO packages (name, description, amount_vnd, tokens, is_active)
            VALUES ({self.p}, {self.p}, {self.p}, {self.p}, {self.p})
        """
        self.cursor.execute(sql, (name, description, amount_vnd, tokens, is_active))
        self.commit()
        return self.cursor.lastrowid

    def update(self, package_id, name, description, amount_vnd, tokens, is_active):
        sql = f"""
            UPDATE packages 
            SET name = {self.p}, description = {self.p}, amount_vnd = {self.p}, tokens = {self.p}, is_active = {self.p}
            WHERE id = {self.p}
        """
        self.cursor.execute(sql, (name, description, amount_vnd, tokens, is_active, package_id))
        self.commit()
        return self.cursor.rowcount

    def delete(self, package_id):
        try:
            self.cursor.execute(f"DELETE FROM packages WHERE id = {self.p}", (package_id,))
            self.commit()
            return self.cursor.rowcount
        except Exception:
            raise Exception("Cannot delete package because it has related payments. Deactivate it instead.")

class PaymentManager(DBConnection):
    def get_packages(self):
        self.cursor.execute(f"SELECT * FROM packages WHERE is_active = {self.p}", (1,))
        return [dict(row) for row in self.cursor.fetchall()]

    def create_payment(self, user_id, package_id, amount_vnd, tokens, payment_code):
        sql = f"""
            INSERT INTO payments (user_id, package_id, amount_vnd, tokens_received, payment_code)
            VALUES ({self.p}, {self.p}, {self.p}, {self.p}, {self.p})
        """
        self.cursor.execute(sql, (user_id, package_id, amount_vnd, tokens, payment_code))
        self.commit()
        return self.cursor.lastrowid

    def update_payment(self, payment_id, status, transaction_id=None):
        sql = f"UPDATE payments SET status = {self.p}, sepay_transaction_id = {self.p}, completed_at = {self.p} WHERE id = {self.p}"
        completed_at = datetime.now() if status == 'completed' else None
        self.cursor.execute(sql, (status, transaction_id, completed_at, payment_id))
        self.commit()
        return self.cursor.rowcount

    def get_user_payments(self, user_id):
        sql = f"SELECT p.*, pk.name as package_name FROM payments p LEFT JOIN packages pk ON p.package_id = pk.id WHERE p.user_id = {self.p} ORDER BY p.created_at DESC"
        self.cursor.execute(sql, (user_id,))
        return [dict(row) for row in self.cursor.fetchall()]

class UserManager(DBConnection):
    def get_by_id(self, user_id):
        self.cursor.execute(f"SELECT * FROM users WHERE id = {self.p}", (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_by_email(self, email):
        self.cursor.execute(f"SELECT * FROM users WHERE email = {self.p}", (email,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
        
    def get_by_google_id(self, google_id):
        self.cursor.execute(f"SELECT * FROM users WHERE google_id = {self.p}", (google_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create(self, email, full_name, google_id=None, avatar_url=None):
        sql = f"INSERT INTO users (email, full_name, google_id, avatar_url, tokens) VALUES ({self.p}, {self.p}, {self.p}, {self.p}, 5)"
        self.cursor.execute(sql, (email, full_name, google_id, avatar_url))
        self.commit()
        return self.cursor.lastrowid

    def update_token(self, user_id, tokens_to_add):
        sql = f"UPDATE users SET tokens = tokens + {self.p}, updated_at = CURRENT_TIMESTAMP WHERE id = {self.p}"
        self.cursor.execute(sql, (tokens_to_add, user_id))
        self.commit()
        return self.cursor.rowcount
    
    def set_admin(self, email):
        sql = f"UPDATE users SET is_admin = 1, updated_at = CURRENT_TIMESTAMP WHERE email = {self.p}"
        self.cursor.execute(sql, (email,))
        self.commit()
        return self.cursor.rowcount
    
    def remove_admin(self, email):
        sql = f"UPDATE users SET is_admin = 0, updated_at = CURRENT_TIMESTAMP WHERE email = {self.p}"
        self.cursor.execute(sql, (email,))
        self.commit()
        return self.cursor.rowcount

class BannerDetails(DBConnection):
    def get_pending(self):
        sql = "SELECT * FROM banner_history WHERE status = 0 LIMIT 1"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def update_status(self, banner_id, status):
        sql = f"UPDATE banner_history SET status = {self.p}, updated_at = CURRENT_TIMESTAMP WHERE id = {self.p}"
        self.cursor.execute(sql, (status, banner_id))
        self.commit()
        return self.cursor.rowcount

class Banners(DBConnection):
    def create(self, banner_details_id, image_url, is_selected=False, score=0):
        sql = f"""
            INSERT INTO banners (banner_details_id, image_url, is_selected, score)
            VALUES ({self.p}, {self.p}, {self.p}, {self.p})
        """
        self.cursor.execute(sql, (banner_details_id, image_url, 1 if is_selected else 0, score))
        self.commit()
        return self.cursor.lastrowid

# Legacy aliases
Users = UserManager
