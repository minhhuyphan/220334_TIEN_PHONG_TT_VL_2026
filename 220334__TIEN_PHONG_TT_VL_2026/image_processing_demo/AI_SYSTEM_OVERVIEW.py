"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     HỆ THỐNG TẠO BANNER QUẢNG CÁO TỰ ĐỘNG SỬ DỤNG TRÍ TUỆ NHÂN TẠO (AI)    ║
║              AUTOMATIC BANNER CREATION SYSTEM WITH AI                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

TỔNG QUAN
=========
Một hệ thống hoàn chỉnh để tạo banner quảng cáo chuyên nghiệp tự động bằng cách:
1. Tách nền ảnh sản phẩm (Background Removal)
2. Tạo nền backdrop từ AI (Stable Diffusion)
3. Tự động chọn phong cách thiết kế (Design AI)
4. Tạo slogan quảng cáo (Text Generation)
5. Tối ưu layout và màu sắc (Composition AI)

KIẾN TRÚC HỆ THỐNG
==================

┌─────────────────────────────────────────────────────────────┐
│                     GUI Interface (Tkinter)                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Simple Mode  │  │  AI Mode     │  │ Batch Mode   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
           ↓              ↓              ↓
┌─────────────────────────────────────────────────────────────┐
│              Core Processing Engine                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │Background Remove │  │AI Background Gen │ (Replicate)    │
│  └──────────────────┘  └──────────────────┘                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Design AI        │  │ Text Generation  │ (OpenAI)       │
│  └──────────────────┘  └──────────────────┘                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │Image Compositing │  │Color Optimization│                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
           ↓              ↓              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Output (Banner PNG)                      │
└─────────────────────────────────────────────────────────────┘

CÁC TỆP CHÍNH
=============

📁 banner_creator_ai.py
   - Giao diện chính với 4 tabs
   - Simple Mode, AI Mode, Batch Mode, Setup Tab
   - Hỗ trợ các phong cách thiết kế khác nhau

📁 AI_SETUP_GUIDE.py
   - Hướng dẫn chi tiết cải đặt các API
   - Danh sách các mô hình AI và chi phí
   - Cấu hình environment variables

📁 test_ai_setup.py
   - Kiểm tra cấu hình AI
   - Xác nhận các thư viện được cài đặt
   - Xác nhận API keys hợp lệ

📁 banner_creator_advanced.py (cũ)
   - Phiên bản nâng cao với 4 gradient styles
   - Chế độ chuyên nghiệp cho thiết kế

📁 BANNER_DESIGN_GUIDE.py
   - Nguồn tham khảo thiết kế
   - Nguyên tắc màu sắc, typography, layout
   - Các style trending 2025-2026

📁 background_removal.py
   - Tách nền ảnh sử dụng rembg
   - Xử lý ảnh sản phẩm

📁 layer_compositing.py
   - Ghép lớp ảnh
   - Tạo background gradient

CÀI ĐẶT
=======

1. CÀI ĐẶT THƯ VIỆN CĂN BẢN:
   pip install pillow rembg requests

2. CÀI ĐẶT AI MODULES (TUỲ CHỌN):
   pip install replicate openai huggingface-hub

3. LẤY API KEYS:
   
   a) Replicate (khuyến nghị):
      - Vào https://replicate.com/
      - Sign up
      - Account → API Tokens
      - Copy token
      - set REPLICATE_API_TOKEN=your_token
   
   b) OpenAI (tuỳ chọn):
      - Vào https://platform.openai.com/api-keys
      - Create API key
      - set OPENAI_API_KEY=your_key
   
   c) Hugging Face (tuỳ chọn):
      - Vào https://huggingface.co/
      - Settings → Access Tokens
      - set HUGGINGFACE_API_KEY=your_token

4. KIỂM TRA CẤU HÌNH:
   python test_ai_setup.py

CHẠY HỆ THỐNG
=============

# Giao diện chính:
python run_banner_creator.py

# Xem hướng dẫn AI:
python AI_SETUP_GUIDE.py

# Kiểm tra AI setup:
python test_ai_setup.py

TÍNH NĂNG AI
============

1. ✅ BACKGROUND REMOVAL
   - Tách nền ảnh sản phẩm sạch sẽ
   - Hỗ trợ PNG transparent
   - Sử dụng: rembg

2. ✅ AI BACKGROUND GENERATION
   - Tạo nền backdrop từ text description
   - Model: Stable Diffusion 3 via Replicate
   - Hoặc: DALL-E via OpenAI
   - Chi phí: ~$0.01/ảnh

3. ✅ DESIGN AI
   - Tự động chọn phong cách dựa loại sản phẩm
   - 5 template: Modern Tech, Luxury, Youth, Natural, Sale
   - Tùy chỉnh gradient colors

4. ✅ TEXT GENERATION
   - Tạo slogan quảng cáo tự động
   - Tạo mô tả sản phẩm
   - Sử dụng: GPT-4 hoặc Hugging Face Models

5. ✅ COLOR OPTIMIZATION
   - Chọn màu phù hợp với sản phẩm
   - Tối ưu contrast cho readability
   - Trending colors 2025-2026

6. ⏳ PRODUCT ANALYSIS (Sắp có)
   - Phân tích hình ảnh sản phẩm
   - Đề xuất layout tối ưu
   - Computer Vision + AI

CHI PHÍ ƯỚC TÍNH
================

PER BANNER COST:
- Replicate (Stable Diffusion): ~$0.01
- OpenAI (GPT-4): ~$0.01-0.05
- Hugging Face: Miễn phí (chạy local)
- Total: ~$0.01-0.06 per banner

BULK DISCOUNT:
- 1,000 banners: ~$10-60
- 10,000 banners: ~$100-600

CÓ THỂ GIẢM CHI PHÍ BẰNG:
- Sử dụng local models (offline)
- Batch processing để discount
- Cache kết quả đã tạo

WORKFLOW ÚY TIÊN
================

Mode 1: SIMPLE (Nhanh, không cần AI)
├─ Upload ảnh sản phẩm
├─ Nhập tiêu đề
├─ Chọn phong cách (gradient)
└─ Tạo banner (2-3 giây)

Mode 2: AI ASSISTED (Thông minh)
├─ Upload ảnh sản phẩm
├─ Chọn loại sản phẩm
├─ AI tạo nền
├─ AI tạo slogan
└─ Tạo banner (10-20 giây)

Mode 3: BATCH (Hàng loạt)
├─ Upload CSV danh sách sản phẩm
├─ Chọn template
├─ Cấu hình AI settings
└─ Tạo 100+ banner cùng lúc (5-10 phút)

EXAMPLES
========

Example 1 - Simple Mode:
   Input: ảnh phone.jpg, "🔥 iPhone 15 Sale 30%"
   Output: banner_20260202_120000.png

Example 2 - AI Mode:
   Input: ảnh watch.jpg, category="fashion"
   AI tạo: nền luxury, slogan "Đồng hồ cao cấp"
   Output: banner_luxury_watch.png

Example 3 - Batch Mode:
   Input: products.csv (100 sản phẩm)
   Output: 100 banner tự động trong folder output/

TROUBLESHOOTING
===============

❌ Lỗi: "No module named 'replicate'"
✓ Giải pháp: pip install replicate

❌ Lỗi: "API token not found"
✓ Giải pháp: set REPLICATE_API_TOKEN=your_token

❌ Lỗi: "Failed to remove background"
✓ Giải pháp: Thử ảnh khác, chất lượng cao hơn

❌ Lỗi: "Connection timeout"
✓ Giải pháp: Kiểm tra internet, thử lại sau

NEXT STEPS
==========

1. ✅ Cài đặt thư viện cơ bản
2. ✅ Thử Simple Mode
3. ✅ Lấy API keys (Replicate)
4. ✅ Cấu hình environment
5. ✅ Thử AI Mode
6. ⏳ Test Batch Processing (sắp có)
7. ⏳ Tối ưu hóa chi phí

TÀI LIỆU THAM KHẢO
==================

- Replicate: https://replicate.com/
- OpenAI: https://platform.openai.com/
- Hugging Face: https://huggingface.co/
- Stable Diffusion: https://www.youtube.com/watch?v=...
- Banner Design: BANNER_DESIGN_GUIDE.py
- Setup Guide: AI_SETUP_GUIDE.py

SUPPORT
=======

For issues:
1. Chạy: python test_ai_setup.py
2. Kiểm tra logs
3. Xem AI_SETUP_GUIDE.py
4. Thử lại từ đầu

GIẤY PHÉP
=========

Dự án: Hệ thống tạo banner quảng cáo AI
Thời gian: Tháng 2 năm 2026
Chủ đề: Thực tập sinh

════════════════════════════════════════════════════════════════════════════════
"""

def main():
    print(__doc__)

if __name__ == "__main__":
    main()
