"""
HƯỚNG DẪN CHI TIẾT - Inpainting + Groq Banner Creator
======================================================

🎯 LỤC TIÊU:
Tạo banner sản phẩm tự động sử dụng AI:
- Giữ nguyên sản phẩm 100% (không bị méo mó)
- AI vẽ nền thông minh xung quanh (Inpainting)
- Text tự động sinh bởi Groq API

═════════════════════════════════════════════════════

📋 KIẾN TRÚC GIẢI PHÁP:

Input:
  └─ ảnh sản phẩm (PNG, transparent background)
     ↓
Step 1: Chuẩn bị (Preparation)
  └─ Load ảnh
  └─ Resize phù hợp (35% chiều rộng banner)
  └─ Định vị (center)
     ↓
Step 2: Tạo Mask (Masking)
  └─ Mask = vùng cần vẽ (không phải sản phẩm)
  └─ Format: PIL Image (L mode)
  └─ Trắng (255) = vẽ
  └─ Đen (0) = giữ nguyên
     ↓
Step 3: Groq - Text Generation
  └─ Input: Tên sản phẩm
  └─ Output: Title, Description, Slogan
     ↓
Step 4: Stable Diffusion - Inpainting
  └─ Model: runwayml/stable-diffusion-inpainting
  └─ Input: Init image (white canvas) + Mask + Prompt
  └─ Output: Nền mới được vẽ bởi AI
     ↓
Step 5: Composite (Ghép)
  └─ Layer 1: Nền (từ inpainting)
  └─ Layer 2: Sản phẩm gốc (RGBA)
  └─ Layer 3: Text (từ Groq)
     ↓
Output:
  └─ Banner 1200x630 PNG

═════════════════════════════════════════════════════

🛠️ CÀI ĐẶT (INSTALLATION):

1️⃣ Clone/Download project

2️⃣ Tạo virtual environment:
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate

3️⃣ Cài dependencies:
   pip install -r requirements.txt
   
   Nếu không có requirements.txt:
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   pip install diffusers transformers accelerate opencv-python pillow groq

4️⃣ Cài Groq (cho text generation):
   pip install groq
   
   Lấy API key:
   • Truy cập: https://console.groq.com
   • Đăng ký miễn phí
   • Tạo API key
   • Copy key

5️⃣ Download model (lần đầu tiên):
   • Chạy: python banner_creator_free_ai.py
   • Click "Download Inpainting Model"
   • Chờ 10-30 phút (tùy tốc độ internet)
   • Model lưu tại: ~/.cache/huggingface/

═════════════════════════════════════════════════════

🚀 CHẠY CHƯƠNG TRÌNH:

python banner_creator_free_ai.py

GUI sẽ mở:
  ├─ Tab 1: Quick Mode (Tạo banner)
  ├─ Tab 2: Load Models (Download model)
  └─ Tab 3: Info & Setup (Hướng dẫn)

═════════════════════════════════════════════════════

📝 HƯỚNG DẪN TỪNG BƯỚC (STEP-BY-STEP):

STEP 1: Chuẩn bị ảnh sản phẩm
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Ảnh phải là PNG (có độ trong suốt)
✓ Nền phải trong suốt (sử dụng BackgroundRemover hoặc Photoshop)
✓ Sản phẩm chiếm khoảng 300-500px chiều cao
✓ Nên có padding xung quanh sản phẩm

Cách tách nền:
  Option 1: BackgroundRemover (tự động)
    python background_removal.py --input product.jpg --output product.png
  
  Option 2: Photoshop/GIMP (thủ công, chính xác)
  
  Option 3: Remove.bg API (online)

STEP 2: Chuẩn bị API key Groq
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Truy cập https://console.groq.com
✓ Tạo tài khoản (free)
✓ Tạo API key
✓ Copy key

STEP 3: Chạy chương trình
━━━━━━━━━━━━━━━━━━━━━━━━
1. Mở GUI: python banner_creator_free_ai.py

2. Tab "Load Models":
   • Click "Download Inpainting Model"
   • Chờ download (~7GB, 10-30 min)
   • Thông báo "✓ Inpainting model loaded!"

3. Tab "Quick Mode":
   • Click "Select Image"
   • Chọn file product.png (transparent)
   • Điền thông tin:
     - Product Name: tên sản phẩm
     - Groq API Key: paste key từ bước 2
     - Background Prompt: mô tả nền muốn vẽ
     
   • Examples background prompt:
     "Professional studio lighting, marble backdrop, luxury"
     "Outdoor beach scene, golden hour, tropical"
     "Modern minimalist office, clean white walls"
   
   • Click "CREATE BANNER"
   • Chờ xử lý (1-3 phút tùy GPU)
   • Kết quả hiển thị preview
   • Banner lưu tại: output/banner_YYYYMMDD_HHMMSS.png

STEP 4: Sử dụng banner
━━━━━━━━━━━━━━━━━━
✓ Banner ready to use
✓ Tối ưu cho social media (1200x630px)
✓ PNG format, trong suốt được giữ

═════════════════════════════════════════════════════

⚙️ TUỲ CHỈNH SETTINGS:

Trong code (banner_creator_free_ai.py):

1. Kích thước banner:
   banner_width, banner_height = 1200, 630  # Thay đổi
   
2. % chiều rộng sản phẩm:
   self.product_width_percent = 0.35  # 35% chiều rộng
   
3. Quality inpainting (num_steps):
   num_inference_steps=50  # Tăng = chất lượng cao, chậm
   # 20-30 = nhanh, 50 = cân bằng, 75+ = quality cao
   
4. Guidance scale:
   guidance_scale=7.5  # 7-8 = cân bằng, 5-6 = tự do hơn

═════════════════════════════════════════════════════

🔧 ADVANCED - BATCH PROCESSING:

Xử lý nhiều sản phẩm cùng lúc:

```python
from inpainting_helper import BatchInpaintingProcessor
from groq_integration import BatchTextGenerator

# Danh sách sản phẩm
products = [
    {"name": "Shoe 1", "type": "shoes", "features": ["leather", "comfortable"]},
    {"name": "Shoe 2", "type": "shoes", "features": ["canvas", "casual"]},
]

# Tạo text
text_gen = BatchTextGenerator(api_key="your_key")
texts = text_gen.generate_for_products(products)

# Tạo banner batch
from diffusers import StableDiffusionInpaintPipeline
import torch

pipeline = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

processor = BatchInpaintingProcessor(pipeline)
output_paths = processor.process_products(
    product_paths=["shoe1.png", "shoe2.png"],
    prompt="Professional shoe display, studio lighting",
    output_folder=Path("output")
)
```

═════════════════════════════════════════════════════

⚠️ TROUBLESHOOTING:

❌ "CUDA out of memory"
✓ Giảm num_inference_steps (50 → 30)
✓ Giảm banner size (1200x630 → 800x420)
✓ Dùng CPU (chậm hơn)

❌ "Model download failed"
✓ Check internet connection
✓ Thử lại download
✓ Kiểm tra disk space (20GB free)

❌ "Groq timeout/API error"
✓ Check API key
✓ Check internet
✓ Check rate limit (30 req/min free)

❌ "Inpainting mask error"
✓ Kiểm tra PNG format (RGBA)
✓ Test mask: helper.create_inpainting_mask()

❌ "Sản phẩm bị méo"
✓ Tăng product_width_percent nhỏ hơn
✓ Dùng ảnh product lớn hơn
✓ Adjust canvas size

═════════════════════════════════════════════════════

📊 PERFORMANCE METRICS:

GPU RTX 3060 (12GB VRAM):
- Model load: ~2-3 giây
- Single inpainting: 30-60 giây (50 steps)
- Batch 10 images: 5-10 phút
- Groq API: ~1 giây (text generation)
- Total per banner: 1-2 phút

GPU RTX 4090 (24GB VRAM):
- Single inpainting: 15-30 giây
- Batch 10 images: 3-5 phút

CPU mode (no GPU):
- Single inpainting: 5-10 phút (❌ not recommended)

═════════════════════════════════════════════════════

💡 TIPS & TRICKS:

1. Mask tuning:
   - Nếu sản phẩm bị vẽ lên: tăng padding (prod_x - 20 → prod_x - 30)
   - Nếu nền không vẽ hết: giảm padding

2. Prompt engineering:
   - "Professional studio lighting" → chuyên nghiệp
   - "Cinematic, movie poster quality" → high-end
   - "Minimalist modern" → sạch sẽ
   - "Vibrant, colorful" → sinh động

3. Batch processing:
   - Xử lý ban đêm để tận dụng idle GPU
   - Lưu batch setting vào JSON
   - Tự động upload kết quả

4. Cost optimization:
   - Groq free tier: 30 requests/min
   - Nếu vượt: dùng fallback text
   - SD inpainting: cost electricity (~0.0001$/image)

═════════════════════════════════════════════════════

🔗 REFERENCES:

- Stable Diffusion Inpainting:
  https://huggingface.co/runwayml/stable-diffusion-inpainting

- Groq API:
  https://console.groq.com
  https://groq.com/docs/

- Diffusers Library:
  https://huggingface.co/docs/diffusers

- PIL/Pillow:
  https://pillow.readthedocs.io/

═════════════════════════════════════════════════════

✅ CHECKLIST TRƯỚC KHI DEPLOY:

□ GPU RTX 3060+ có sẵn
□ CUDA toolkit cài đúng
□ PyTorch GPU cài thành công
□ Diffusers library cài được
□ Groq API key lấy được
□ Inpainting model download thành công
□ Test 1 ảnh sản phẩm
□ Preview kết quả OK
□ Output folder tạo được
□ Backup code trước khi scale

═════════════════════════════════════════════════════

📞 SUPPORT:

Issues:
  - GitHub: [your_repo]/issues
  - Email: [your_email]

Resources:
  - Hugging Face: huggingface.co/
  - Groq: groq.com/
  - Discord communities

═════════════════════════════════════════════════════

VERSION: 2.0 (Inpainting + Groq)
LAST UPDATED: 2026-02-04
AUTHOR: [Your Name]
"""

print(__doc__)
