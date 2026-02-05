# 3-Layer Image Compositing Project Summary

## 📊 Project Overview

Đây là dự án **xử lý ảnh + AI** theo kiến trúc **"Divide and Conquer"** (Chia để trị) để tạo banner quảng cáo tự động.

### Vấn đề

AI hiện nay (Stable Diffusion, Midjourney) không biết viết chữ tiếng Việt một cách chính xác.

### Giải pháp

Chia bài toán thành **3 lớp độc lập**:

1. **Lớp 1 (Background):** AI tạo nền đẹp
2. **Lớp 2 (Product):** Thuật toán tách nền sản phẩm
3. **Lớp 3 (Text):** Vẽ chữ tiếng Việt bằng code

---

## 🗂️ Cấu trúc Project

```
image_processing_demo/
│
├── 📄 Startup Scripts
│   ├── run.bat                    # Windows startup
│   └── run.sh                     # Mac/Linux startup
│
├── 🔧 Core Modules
│   ├── layer_compositing.py       # ⭐ Demo cơ bản (START HERE)
│   ├── advanced_compositing.py    # Ghép nâng cao (tính toán thông minh)
│   ├── background_removal.py      # Tách nền (sử dụng rembg)
│   └── stable_diffusion_integration.py  # Tạo nền AI
│
├── 🌐 Web API
│   └── app.py                     # Flask API + Frontend
│
├── 🧪 Testing & Deployment
│   ├── test_pipeline.py           # Test toàn bộ pipeline
│   ├── requirements.txt           # Dependencies
│   ├── Dockerfile                 # Docker deployment
│   └── docker-compose.yml         # Docker orchestration
│
└── 📚 Documentation
    ├── README.md                  # Hướng dẫn cơ bản
    ├── INTEGRATION_GUIDE.md       # Hướng dẫn tích hợp chi tiết
    ├── PROJECT_SUMMARY.md         # File này
    └── ARCHITECTURE.md            # Chi tiết kiến trúc (optional)
```

---

## 🎯 Bắt đầu nhanh

### Windows

```bash
cd image_processing_demo
double-click run.bat
# Hoặc
run.bat
```

### Mac/Linux

```bash
cd image_processing_demo
chmod +x run.sh
./run.sh
```

### Manual

```bash
# 1. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Chạy một trong các script:
python layer_compositing.py        # Demo cơ bản
python test_pipeline.py             # Test đầy đủ
python app.py                       # Web API
```

---

## 📌 Các Script Chính

### 1️⃣ `layer_compositing.py` - **START HERE**

Demo cơ bản về ghép 3 lớp.

**Chạy:**

```bash
python layer_compositing.py
```

**Output:** `output/banner_final.png`

**Code:**

```python
from layer_compositing import LayerCompositor

compositor = LayerCompositor(width=800, height=600)

# Lớp 1
compositor.create_background(color_gradient=True)

# Lớp 2
compositor.create_product_circle(radius=80, color=(255, 100, 50))
compositor.composite_layers()

# Lớp 3
compositor.add_text_overlay(
    text="🔥 SIÊU SALE",
    font_size=50,
    text_color=(255, 255, 0)
)

compositor.save_result("output/banner.png")
```

---

### 2️⃣ `background_removal.py` - Tách Nền

Dùng model U²-Net (rembg) để tách nền sản phẩm.

**Yêu cầu:**

```bash
pip install rembg
```

**Chạy:**

```bash
python background_removal.py
```

**Code:**

```python
from background_removal import BackgroundRemover

remover = BackgroundRemover(model="u2net")
remover.remove_background("input/product.jpg", "output/product_no_bg.png")

# Batch
remover.batch_remove_background("input/", "output/")
```

---

### 3️⃣ `stable_diffusion_integration.py` - Tạo Nền AI

Tạo nền bằng Stable Diffusion (Local hoặc Replicate API).

**Setup Replicate (Khuyên dùng):**

```bash
pip install replicate
export REPLICATE_API_TOKEN=<your_token>
```

**Setup Local WebUI:**

```bash
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
./webui.sh  # Mac/Linux
# Server chạy tại http://localhost:7860
```

**Code:**

```python
from stable_diffusion_integration import StableDiffusionGenerator

# Replicate
gen = StableDiffusionGenerator(api_type="replicate")
image = gen.generate_background("blue gradient, modern style", 800, 600)

# Local WebUI
gen = StableDiffusionGenerator(api_type="local")
image = gen.generate_background("blue gradient", 800, 600)

image.save("output/background.png")
```

---

### 4️⃣ `advanced_compositing.py` - Ghép Nâng Cao

Tính toán thông minh: chọn màu chữ dựa vào nền.

**Code:**

```python
from advanced_compositing import AdvancedCompositor

compositor = AdvancedCompositor("input/bg.png")
compositor.paste_product("input/product_no_bg.png", scale=0.3)
compositor.add_smart_text("HOT SALE", font_size=50)  # Màu tự động
compositor.save("output/banner.png")
```

---

### 5️⃣ `app.py` - Web API

Chạy web server với giao diện drag-drop.

**Chạy:**

```bash
python app.py
# Mở: http://localhost:5000
```

**Endpoints:**

```
GET  /               - Giao diện web
POST /api/remove-background      - Tách nền
POST /api/generate-background    - Tạo nền AI
POST /api/create-banner          - Tạo banner
GET  /api/files                  - Liệt kê ảnh
GET  /api/download/<filename>    - Tải ảnh
```

---

### 6️⃣ `test_pipeline.py` - Test Đầy Đủ

Test toàn bộ pipeline từ đầu đến cuối.

**Chạy:**

```bash
python test_pipeline.py
```

**Output:**

```
output/test_01_basic_compositing.png      # Layer Compositor
output/test_02_no_background.png          # Background Removal
output/test_03_advanced_compositing.png   # Advanced Compositor
```

---

## 📊 Pipeline Workflow

```
INPUT (Ảnh sản phẩm + Chữ)
    ↓
┌──────────────────────────────┐
│ LỚPBASE 1: BACKGROUND        │
│ Stable Diffusion + Text Prompt
└──────────────────────────────┘
    ↓
┌──────────────────────────────┐
│ LỚPBASE 2: PRODUCT           │
│ rembg (U²-Net Model)         │
│ Output: PNG transparent      │
└──────────────────────────────┘
    ↓
┌──────────────────────────────┐
│ GHÉP LỚP 1 + 2               │
│ Composite (Paste)            │
└──────────────────────────────┘
    ↓
┌──────────────────────────────┐
│ LỚPBASE 3: TEXT              │
│ Pillow + TTF Font            │
│ Tính vị trí + Chọn màu       │
└──────────────────────────────┘
    ↓
OUTPUT (Banner hoàn chỉnh)
```

---

## 🔌 Tích hợp các API

### Replicate (Stable Diffusion)

```bash
pip install replicate
export REPLICATE_API_TOKEN=<token>
```

### Local Stable Diffusion WebUI

```bash
# Chạy server
python -m venv sd_env
sd_env\Scripts\activate
pip install -r requirements.txt
# Server: http://localhost:7860
```

### rembg (Background Removal)

```bash
pip install rembg
# Hoặc: pip install rembg[gpu] (CUDA support)
```

---

## 💾 Dependencies

**Bắt buộc:**

- Pillow >= 10.0.0
- numpy >= 1.24.0

**Tách nền:**

- rembg >= 2.0.0
- onnxruntime >= 1.14.0

**Web API:**

- flask >= 2.3.0

**AI:**

- replicate >= 0.9.0 (cho Replicate API)
- requests >= 2.31.0 (cho Local WebUI)

---

## 🎓 Ứng dụng trong Báo cáo Thực tập

### 1. Phần Kiến trúc

- Vẽ diagram 3 lớp
- Minh họa workflow
- Giải thích từng bước

### 2. Phần So sánh

| Phương pháp     | Ưu điểm      | Nhược điểm            |
| --------------- | ------------ | --------------------- |
| AI vẽ toàn bộ   | Đơn giản     | Chữ tiếng Việt lỗi ❌ |
| 3-Lớp (Đề xuất) | Chữ chuẩn ✅ | Phức tạp hơn          |

### 3. Phần Code

- Đính kèm `layer_compositing.py`
- Giải thích thuật toán Compositing
- Kết quả test images

### 4. Kết luận

- Giải quyết được vấn đề AI viết chữ
- Kiến trúc modular, dễ mở rộng
- Hiệu suất cao

---

## 🐳 Docker Deployment

```bash
# Build image
docker build -t image-compositing .

# Run container
docker run -p 5000:5000 image-compositing

# Docker compose
docker-compose up
```

---

## 🔍 Troubleshooting

### Font tiếng Việt không hiển thị

```python
# Sử dụng font đúng
font_path = "fonts/Roboto-Bold.ttf"  # Hỗ trợ Unicode
```

### Stable Diffusion không kết nối

```bash
# Kiểm tra server
curl http://localhost:7860/api/sd-models

# Hoặc dùng Replicate API
export REPLICATE_API_TOKEN=<token>
```

### Lỗi "Port 5000 already in use"

```bash
# Sử dụng port khác
python -c "from app import app; app.run(port=8000)"
```

---

## 📚 Tài liệu Tham khảo

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [rembg GitHub](https://github.com/danielgatis/rembg)
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Replicate AI API](https://replicate.com/docs)
- [Flask Framework](https://flask.palletsprojects.com/)

---

## 📝 Ghi chú

- **Phiên bản:** 1.0
- **Ngày tạo:** 2026-02-02
- **Python:** 3.8+
- **OS:** Windows, Mac, Linux

---

## 🎉 Tiếp theo

1. ✅ Chạy `layer_compositing.py` để hiểu cơ bản
2. ✅ Chạy `test_pipeline.py` để test đầy đủ
3. ✅ Thiết lập Stable Diffusion (Local hoặc Replicate)
4. ✅ Chạy `app.py` để sử dụng web interface
5. ✅ Tích hợp vào project của bạn

**Good luck! 🚀**
