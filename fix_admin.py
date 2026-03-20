import os
import mysql.connector
from app.config import settings
import json

def fix_admin():
    config = {
        'host': settings.DB_HOST,
        'port': settings.DB_PORT,
        'user': settings.DB_USER,
        'password': settings.DB_PASSWORD,
        'database': settings.DB_DATABASE,
        'autocommit': True
    }
    
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
            config['ssl_ca'] = ssl_val
        config['ssl_disabled'] = False
        
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    
    email = "phanminhhuycm@gmail.com"
    cursor.execute("SELECT id, email, full_name, is_admin FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    
    if not user:
        print(f"User {email} not found")
        return
        
    print(f"Found user: {user}")
    
    if user['is_admin'] == 1:
        print("User is already admin")
    else:
        cursor.execute("UPDATE users SET is_admin = 1 WHERE email = %s", (email,))
        print(f"Updated user {email} to admin")
        
    conn.close()

if __name__ == "__main__":
    fix_admin()
