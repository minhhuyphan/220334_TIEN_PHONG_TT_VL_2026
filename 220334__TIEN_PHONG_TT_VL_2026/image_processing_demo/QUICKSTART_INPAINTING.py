"""
⚡ QUICK START - Inpainting + Groq Banner Creator

5 Phút Setup, Tạo Banner Banner Ngay!
"""

# STEP 1: CÀI ĐẶT (2 min)
# ========================
# 1. Run: pip install -r requirements_inpainting.txt
# 2. Get Groq API key: https://console.groq.com
# 3. Set: export GROQ_API_KEY="your_key"

# STEP 2: TEST (1 min)
# ========================
# Run: python test_inpainting_setup.py
# Kiểm tra mọi thứ OK

# STEP 3: CHUẨN BỊ ẢNH (1 min)
# ========================
# - Có 1 ảnh sản phẩm PNG (transparent background)
# - Hoặc dùng: python background_removal.py --input product.jpg

# STEP 4: CHẠY GUI (1 min)
# ========================
# Run: python banner_creator_free_ai.py

# STEP 5: TẠO BANNER (1-2 min)
# ========================
# 1. Click "Select Image" → chọn PNG sản phẩm
# 2. Điền:
#    - Product Name: "Tên sản phẩm"
#    - Groq API Key: "key_của_bạn"
#    - Background Prompt: "Mô tả nền"
# 3. Click "CREATE BANNER"
# 4. Chờ 1-2 phút
# 5. ✓ Banner ready!

print("""
╔════════════════════════════════════════════════╗
║   🎨 AI Banner Creator - Quick Start          ║
╚════════════════════════════════════════════════╝

Bước 1: Cài đặt
   $ pip install -r requirements_inpainting.txt

Bước 2: Setup Groq
   • Get key: https://console.groq.com
   • export GROQ_API_KEY="your_key"

Bước 3: Test
   $ python test_inpainting_setup.py

Bước 4: Chạy
   $ python banner_creator_free_ai.py

Bước 5: Tạo Banner
   • Select PNG product image
   • Fill info (name, API key, prompt)
   • Click CREATE
   • Wait 1-2 min
   • Done! 🎉

═══════════════════════════════════════════════

Chỉ cần:
✓ NVIDIA GPU (RTX 3060+)
✓ 20GB disk space
✓ Groq API key (free)

Kết quả:
✓ 1200x630 PNG banner
✓ Sản phẩm 100% gốc (không AI méo)
✓ Nền sinh bởi AI
✓ Text từ Groq API

═══════════════════════════════════════════════

Xem thêm:
• Chi tiết: INPAINTING_GUIDE.py
• Advanced: README_INPAINTING.md
• API: groq_integration.py

═══════════════════════════════════════════════
""")
