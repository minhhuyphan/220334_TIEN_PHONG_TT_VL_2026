"""
Script để set admin cho user thông qua email
Usage: python set_admin.py <email>
"""
import sys
import sqlite3
from app.config import settings
from app.utils.db_sqlite import get_db_connection


def set_admin_by_email(email: str) -> bool:
    """
    Set user làm admin thông qua email
    
    Args:
        email: Email của user cần set admin
        
    Returns:
        True nếu thành công, False nếu không tìm thấy user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Kiểm tra user có tồn tại không
        cursor.execute("SELECT id, email, full_name, is_admin FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Không tìm thấy user với email: {email}")
            conn.close()
            return False
        
        user_dict = dict(user)
        
        # Kiểm tra user đã là admin chưa
        if user_dict['is_admin'] == 1:
            print(f"ℹ️  User '{user_dict['full_name']}' ({email}) đã là admin rồi!")
            conn.close()
            return True
        
        # Set user làm admin
        cursor.execute("UPDATE users SET is_admin = 1, updated_at = CURRENT_TIMESTAMP WHERE email = ?", (email,))
        conn.commit()
        
        print(f"✅ Đã set user '{user_dict['full_name']}' ({email}) làm admin thành công!")
        print(f"   User ID: {user_dict['id']}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi set admin: {e}")
        return False


def remove_admin_by_email(email: str) -> bool:
    """
    Gỡ quyền admin của user thông qua email
    
    Args:
        email: Email của user cần gỡ quyền admin
        
    Returns:
        True nếu thành công, False nếu không tìm thấy user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Kiểm tra user có tồn tại không
        cursor.execute("SELECT id, email, full_name, is_admin FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Không tìm thấy user với email: {email}")
            conn.close()
            return False
        
        user_dict = dict(user)
        
        # Kiểm tra user có phải admin không
        if user_dict['is_admin'] == 0:
            print(f"ℹ️  User '{user_dict['full_name']}' ({email}) không phải là admin!")
            conn.close()
            return True
        
        # Gỡ quyền admin
        cursor.execute("UPDATE users SET is_admin = 0, updated_at = CURRENT_TIMESTAMP WHERE email = ?", (email,))
        conn.commit()
        
        print(f"✅ Đã gỡ quyền admin của user '{user_dict['full_name']}' ({email})!")
        print(f"   User ID: {user_dict['id']}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi gỡ quyền admin: {e}")
        return False


def list_all_admins():
    """
    Liệt kê tất cả admin trong hệ thống
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, full_name, created_at FROM users WHERE is_admin = 1")
        admins = cursor.fetchall()
        
        if not admins:
            print("ℹ️  Chưa có admin nào trong hệ thống!")
        else:
            print(f"\n📋 Danh sách Admin ({len(admins)} người):")
            print("-" * 80)
            for admin in admins:
                admin_dict = dict(admin)
                print(f"  • ID: {admin_dict['id']}")
                print(f"    Tên: {admin_dict['full_name']}")
                print(f"    Email: {admin_dict['email']}")
                print(f"    Tạo lúc: {admin_dict['created_at']}")
                print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Lỗi khi liệt kê admin: {e}")


def list_all_users():
    """
    Liệt kê tất cả user trong hệ thống
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, full_name, is_admin, tokens, created_at FROM users ORDER BY created_at DESC")
        users = cursor.fetchall()
        
        if not users:
            print("ℹ️  Chưa có user nào trong hệ thống!")
        else:
            print(f"\n📋 Danh sách Users ({len(users)} người):")
            print("-" * 80)
            for user in users:
                user_dict = dict(user)
                admin_badge = "👑 ADMIN" if user_dict['is_admin'] == 1 else "👤 User"
                print(f"  {admin_badge}")
                print(f"    ID: {user_dict['id']}")
                print(f"    Tên: {user_dict['full_name']}")
                print(f"    Email: {user_dict['email']}")
                print(f"    Tokens: {user_dict['tokens']}")
                print(f"    Tạo lúc: {user_dict['created_at']}")
                print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Lỗi khi liệt kê users: {e}")


def print_usage():
    """In hướng dẫn sử dụng"""
    print("""
📖 Hướng dẫn sử dụng:

1. Set user làm admin:
   python set_admin.py set <email>
   Ví dụ: python set_admin.py set user@example.com

2. Gỡ quyền admin:
   python set_admin.py remove <email>
   Ví dụ: python set_admin.py remove user@example.com

3. Liệt kê tất cả admin:
   python set_admin.py list-admins

4. Liệt kê tất cả users:
   python set_admin.py list-users

5. Hiển thị hướng dẫn:
   python set_admin.py help
    """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Thiếu tham số!")
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "set":
        if len(sys.argv) < 3:
            print("❌ Thiếu email!")
            print("Usage: python set_admin.py set <email>")
            sys.exit(1)
        email = sys.argv[2]
        success = set_admin_by_email(email)
        sys.exit(0 if success else 1)
        
    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Thiếu email!")
            print("Usage: python set_admin.py remove <email>")
            sys.exit(1)
        email = sys.argv[2]
        success = remove_admin_by_email(email)
        sys.exit(0 if success else 1)
        
    elif command == "list-admins":
        list_all_admins()
        sys.exit(0)
        
    elif command == "list-users":
        list_all_users()
        sys.exit(0)
        
    elif command == "help":
        print_usage()
        sys.exit(0)
        
    else:
        print(f"❌ Lệnh không hợp lệ: {command}")
        print_usage()
        sys.exit(1)
