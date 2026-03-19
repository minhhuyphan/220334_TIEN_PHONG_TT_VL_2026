"""
Script để seed giá trị mặc định cho reference_image_cost vào database
Chạy script này một lần để thêm cấu hình mới
"""

import sys
import os

# Thêm thư mục gốc vào sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.banner_db import ConfigManager

def seed_reference_image_cost():
    """Thêm giá trị mặc định cho reference_image_cost"""
    config_manager = ConfigManager()
    try:
        # Kiểm tra xem đã có giá trị chưa
        existing_value = config_manager.get_value("reference_image_cost")
        
        if existing_value is None:
            # Thêm giá trị mặc định: 0.5 token per reference image
            config_manager.set_value("reference_image_cost", "0.5")
            print("✅ Đã thêm reference_image_cost = 0.5 vào database")
        else:
            print(f"ℹ️  reference_image_cost đã tồn tại với giá trị: {existing_value}")
        
        # Kiểm tra banner_cost
        banner_cost = config_manager.get_value("banner_cost")
        if banner_cost is None:
            config_manager.set_value("banner_cost", "1")
            print("✅ Đã thêm banner_cost = 1 vào database")
        else:
            print(f"ℹ️  banner_cost đã tồn tại với giá trị: {banner_cost}")
            
    finally:
        config_manager.close()

if __name__ == "__main__":
    print("🚀 Bắt đầu seed config...")
    seed_reference_image_cost()
    print("✨ Hoàn tất!")
