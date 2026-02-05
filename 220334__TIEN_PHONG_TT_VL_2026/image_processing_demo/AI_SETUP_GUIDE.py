"""
AI-POWERED AUTOMATIC BANNER CREATION SYSTEM
==========================================
Hệ thống tạo banner quảng cáo tự động sử dụng AI

CHỨC NĂNG AI:
1. ✅ Tách nền ảnh sản phẩm (rembg)
2. ✅ Tạo nền AI (Stable Diffusion via Replicate/Hugging Face)
3. ✅ Tự động đề xuất màu sắc phù hợp (Color AI)
4. ✅ Tự động tạo text/slogan (AI Text Generation)
5. ✅ Tối ưu layout tự động (Composition AI)
6. ✅ Phân tích ảnh sản phẩm để đề xuất phong cách (Computer Vision)

NGUỒN AI CÓ SẴN:
1. Stable Diffusion (Replicate API) - Tạo ảnh từ text
2. OpenAI GPT - Tạo text, slogan quảng cáo
3. Hugging Face - Computer Vision, text generation
4. ColorHexa/Palette Generator - Tạo bảng màu
5. Local Models (ONNX) - Chạy offline (không cần API)

SETUP:
pip install replicate openai huggingface-hub
"""

import os
import json
from pathlib import Path

# Configuration for AI APIs
AI_CONFIG = {
    "replicate": {
        "api_key": os.getenv("REPLICATE_API_TOKEN", "your_token_here"),
        "stable_diffusion_model": "stability-ai/stable-diffusion-3",
        "enabled": True,
        "description": "Tạo nền ảnh từ text prompt"
    },
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", "your_token_here"),
        "model": "gpt-4",
        "enabled": False,
        "description": "Tạo text/slogan quảng cáo thông minh"
    },
    "huggingface": {
        "api_key": os.getenv("HUGGINGFACE_API_KEY", "your_token_here"),
        "model": "stabilityai/stable-diffusion-2",
        "enabled": False,
        "description": "Tạo ảnh, phân tích, tạo text"
    }
}

DESIGN_TEMPLATES = {
    "modern_tech": {
        "colors": ["#667eea", "#764ba2", "#f093fb"],
        "gradient": ("modern_gradient", (102, 126, 234), (118, 75, 162)),
        "ai_prompt": "modern minimalist tech product background, clean, professional, blue purple gradient",
        "font_style": "bold",
        "description": "Phong cách công nghệ hiện đại"
    },
    "luxury": {
        "colors": ["#2d2d2d", "#c9a961", "#ffffff"],
        "gradient": ("dark_premium", (33, 33, 33), (201, 169, 97)),
        "ai_prompt": "luxury premium background, gold accents, dark elegant, professional",
        "font_style": "serif",
        "description": "Phong cách cao cấp sang trọng"
    },
    "youthful_fun": {
        "colors": ["#ff6b6b", "#ff9999", "#ffc366"],
        "gradient": ("sunset_gradient", (255, 107, 107), (255, 153, 153)),
        "ai_prompt": "vibrant colorful fun background, playful, energetic, young audience",
        "font_style": "bold",
        "description": "Phong cách trẻ trung vui tươi"
    },
    "natural_organic": {
        "colors": ["#558b2f", "#9ccc65", "#c8e6c9"],
        "gradient": ("ocean_gradient", (85, 139, 47), (156, 204, 101)),
        "ai_prompt": "natural organic eco-friendly background, green nature, fresh, sustainable",
        "font_style": "regular",
        "description": "Phong cách tự nhiên và thân thiện"
    },
    "sale_promotion": {
        "colors": ["#ff5252", "#ffeb3b", "#ffffff"],
        "gradient": ("sunset_gradient", (255, 82, 82), (255, 235, 59)),
        "ai_prompt": "exciting sale promotion background, red yellow, energetic, buy now feeling",
        "font_style": "bold",
        "description": "Phong cách khuyến mãi sale"
    }
}

PRODUCT_CATEGORY_MAPPING = {
    "electronics": "modern_tech",
    "fashion": "luxury",
    "toys": "youthful_fun",
    "food": "natural_organic",
    "sale": "sale_promotion",
    "home": "natural_organic",
    "beauty": "luxury",
    "sports": "youthful_fun"
}

# AI Prompts cho tạo slogan
SLOGAN_PROMPTS = {
    "sale": "Tạo 5 slogan quảng cáo khác nhau cho sản phẩm sale/giảm giá. Viết tiếng Việt, ngắn gọn, quy tụ.",
    "new_product": "Tạo 5 slogan quảng cáo cho sản phẩm mới. Viết tiếng Việt, hấp dẫn, tạo sự tò mò.",
    "premium": "Tạo 5 slogan quảng cáo cho sản phẩm cao cấp. Viết tiếng Việt, sang trọng, chuyên nghiệp.",
    "daily": "Tạo 5 slogan quảng cáo cho sản phẩm hàng ngày. Viết tiếng Việt, vui tươi, gần gũi."
}

def print_ai_setup_guide():
    """In hướng dẫn cài đặt AI"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║   HƯỚNG DẪN CÀI ĐẶT AI CHO HỆ THỐNG BANNER QUẢNG CÁO TỰ ĐỘNG     ║
╚══════════════════════════════════════════════════════════════════════╝

📦 BƯỚC 1: CÀI ĐẶT THƯ VIỆN
──────────────────────────────
pip install replicate openai huggingface-hub pillow requests

🔑 BƯỚC 2: LẤY API KEYS
──────────────────────────────

A. REPLICATE (Khuyến nghị - Dễ sử dụng)
   1. Vào https://replicate.com/
   2. Sign up (hoặc login)
   3. Vào Account → API Tokens
   4. Copy token
   5. Thêm vào environment: set REPLICATE_API_TOKEN=your_token

B. OPENAI (Cho tạo slogan/text)
   1. Vào https://platform.openai.com/api-keys
   2. Create API key
   3. Copy token
   4. Thêm vào environment: set OPENAI_API_KEY=your_token

C. HUGGING FACE (Thay thế free)
   1. Vào https://huggingface.co/
   2. Settings → Access Tokens
   3. Create new token
   4. Thêm vào environment: set HUGGINGFACE_API_KEY=your_token

⚙️ BƯỚC 3: CẤU HÌNH ENVIRONMENT
────────────────────────────────
Windows (PowerShell):
    $env:REPLICATE_API_TOKEN = "your_token"
    $env:OPENAI_API_KEY = "your_key"

Linux/Mac:
    export REPLICATE_API_TOKEN="your_token"
    export OPENAI_API_KEY="your_key"

📝 BƯỚC 4: KIỂM TRA CẤU HÌNH
────────────────────────────────
Chạy file: test_ai_setup.py

🎯 TÍNH NĂNG AI ĐƯỢC HỖ TRỢ
────────────────────────────────
1. ✅ Tạo nền ảnh AI từ text description
2. ✅ Tự động chọn phong cách dựa trên loại sản phẩm
3. ✅ Tạo slogan quảng cáo thông minh
4. ✅ Tối ưu màu sắc dựa trên AI
5. ✅ Phân tích ảnh sản phẩm (sắp có)
6. ✅ Tạo banner batch tự động

💰 CHI PHÍ ƯỚC TÍNH
────────────────────────────────
Replicate: ~$0.01/ảnh (Stable Diffusion)
OpenAI: ~$0.01/request (GPT)
Hugging Face: Miễn phí (offline models)

⚠️ LỰA CHỌN TỐI ƯU
────────────────────────────────
- Dùng Replicate cho tạo ảnh (rẻ, dễ)
- Dùng OpenAI hoặc Hugging Face cho text
- Dùng local models khi không cần API (offline)
    """)

if __name__ == "__main__":
    print_ai_setup_guide()
    
    # Save configuration
    config_path = Path(__file__).parent / "ai_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump({
            "api_services": AI_CONFIG,
            "design_templates": DESIGN_TEMPLATES,
            "slogan_prompts": SLOGAN_PROMPTS
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Cấu hình đã lưu: {config_path}")
