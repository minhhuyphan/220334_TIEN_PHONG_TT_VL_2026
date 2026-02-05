# 3-Layer Image Compositing - Hướng dẫn Tích hợp

## 📖 Mục lục

1. [Cài đặt](#cài-đặt)
2. [Các Module](#các-module)
3. [Pipeline Đầy Đủ](#pipeline-đầy-đủ)
4. [API Endpoints](#api-endpoints)
5. [Deployment](#deployment)

---

## Cài đặt

### 1. Yêu cầu cơ bản

```bash
# Clone repo hoặc copy thư mục
cd image_processing_demo

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Cài dependencies cơ bản
pip install -r requirements.txt
```

### 2. Dependencies chi tiết

```bash
# Cơ bản
pip install Pillow>=10.0.0           # Xử lý ảnh

# Tách nền
pip install rembg>=2.0.0             # Background removal

# Tạo nền AI (chọn một)
pip install replicate               # Replicate API (khuyên dùng)
# OR
pip install requests                # Để dùng local Stable Diffusion

# Web API
pip install flask                   # Web framework
pip install numpy                   # Xử lý mảng
```

### 3. Thiết lập Font tiếng Việt

```bash
# Tải font vào folder fonts/
# Ví dụ: Roboto-Bold.ttf, Arial.ttf

# Windows: Font mặc định là c:\Windows\Fonts\arial.ttf ✅ Hỗ trợ tiếng Việt
# Mac: /Library/Fonts/Arial.ttf
# Linux: /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
```

---

## Các Module

### 1. `layer_compositing.py` - Demo Cơ Bản

**Tính năng:**

- Tạo 3 lớp: Background → Product → Text
- Tính toán vị trí text
- Thêm nền phía sau chữ

**Chạy:**

```bash
python layer_compositing.py
# Output: output/banner_final.png
```

**Code Sample:**

```python
from layer_compositing import LayerCompositor

compositor = LayerCompositor(width=800, height=600)

# Lớp 1: Nền
compositor.create_background(color_gradient=True)

# Lớp 2: Sản phẩm
compositor.create_product_circle(radius=80, color=(255, 100, 50))
compositor.composite_layers()

# Lớp 3: Chữ tiếng Việt
compositor.add_text_overlay(
    text="🔥 SIÊU SALE 50%",
    font_size=50,
    text_color=(255, 255, 0),
    background_overlay=True
)

compositor.save_result("output/banner.png")
```

---

### 2. `background_removal.py` - Tách Nền

**Tính năng:**

- Dùng model U²-Net từ rembg
- Tách nền từ ảnh sản phẩm
- Batch processing

**Chạy:**

```bash
python background_removal.py
# Output: output/test_product_no_bg.png
```

**Code Sample:**

```python
from background_removal import BackgroundRemover

remover = BackgroundRemover(model="u2net")

# Tách nền ảnh đơn
result = remover.remove_background(
    "input/product.jpg",
    "output/product_no_bg.png"
)

# Tách nền batch
remover.batch_remove_background("input/", "output/")
```

---

### 3. `advanced_compositing.py` - Ghép Nâng Cao

**Tính năng:**

- Tính độ sáng nền → Chọn màu chữ tự động
- Tính vị trí text tối ưu
- Shadow/Outline cho chữ

**Code Sample:**

```python
from advanced_compositing import AdvancedCompositor

compositor = AdvancedCompositor("input/background.png")

# Dán sản phẩm
pos, size = compositor.paste_product(
    "input/product_no_bg.png",
    scale=0.3
)

# Thêm chữ thông minh (màu tự động)
compositor.add_smart_text("HOT SALE", font_size=50)

compositor.save("output/banner_advanced.png")
```

---

### 4. `stable_diffusion_integration.py` - Tạo Nền AI

**Tính năng:**

- Tích hợp Stable Diffusion WebUI (local)
- Hỗ trợ Replicate API (remote)
- Tạo nền theo prompt

**Thiết lập Local Server:**

**Option A: Dùng Replicate (Khuyên dùng - Không cần local server)**

```bash
pip install replicate
export REPLICATE_API_TOKEN=<your_token>
# Lấy token: https://replicate.com/account
```

**Option B: Dùng Local Stable Diffusion WebUI**

```bash
# 1. Clone WebUI
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# 2. Chạy server
./webui.sh  # Mac/Linux
./webui.bat # Windows

# Server sẽ chạy tại: http://localhost:7860
```

**Code Sample:**

```python
from stable_diffusion_integration import StableDiffusionGenerator

# Cách 1: Local WebUI
gen_local = StableDiffusionGenerator(api_type="local")
image = gen_local.generate_background(
    "modern blue gradient, sportswear theme",
    width=800,
    height=600
)

# Cách 2: Replicate API
gen_replicate = StableDiffusionGenerator(api_type="replicate")
image = gen_replicate.generate_background(
    "luxury gold background",
    width=800,
    height=600
)

image.save("output/background_ai.png")
```

---

### 5. `app.py` - Web API Flask

**Tính năng:**

- Web API để upload ảnh
- Giao diện drag-drop
- RESTful endpoints

**Chạy:**

```bash
python app.py
# Truy cập: http://localhost:5000
```

**Endpoints:**

| Method | Endpoint                   | Mô tả         |
| ------ | -------------------------- | ------------- |
| GET    | `/`                        | Giao diện web |
| POST   | `/api/remove-background`   | Tách nền      |
| POST   | `/api/generate-background` | Tạo nền AI    |
| POST   | `/api/create-banner`       | Tạo banner    |
| GET    | `/api/files`               | Liệt kê ảnh   |
| GET    | `/api/download/<filename>` | Tải ảnh       |

**Code Sample (API Call):**

```python
import requests

# Tách nền
files = {'file': open('product.jpg', 'rb')}
response = requests.post(
    'http://localhost:5000/api/remove-background',
    files=files
)
print(response.json())

# Tạo nền AI
data = {
    "prompt": "modern blue background",
    "width": 800,
    "height": 600
}
response = requests.post(
    'http://localhost:5000/api/generate-background',
    json=data
)
print(response.json())

# Tạo banner
data = {
    "background_file": "solid_color",
    "product_file": "product_no_bg.png",
    "text": "Siêu Sale",
    "text_color": [255, 255, 0],
    "bg_color": [100, 150, 200]
}
response = requests.post(
    'http://localhost:5000/api/create-banner',
    json=data
)
print(response.json())
```

---

### 6. `test_pipeline.py` - Test Script

**Chạy test:**

```bash
python test_pipeline.py
```

**Output:**

- `output/test_01_basic_compositing.png` - Layer Compositor
- `output/test_02_no_background.png` - Background Removal
- `output/test_03_advanced_compositing.png` - Advanced Compositor

---

## Pipeline Đầy Đủ

### Luồng xử lý hoàn chỉnh:

```
INPUT
  ↓
┌─────────────────────────────────────┐
│ LỚPBASE 1: BACKGROUND (Nền)          │
│ - Tạo bằng Generative AI             │
│ - Model: Stable Diffusion            │
│ - Input: Prompt (tiếng Anh)          │
│ - Output: background_layer.png (RGB) │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ LỚPBASE 2: PRODUCT (Sản phẩm)        │
│ - Tách nền từ ảnh gốc                │
│ - Model: U²-Net (rembg)              │
│ - Input: product.jpg (có nền cũ)    │
│ - Output: product_layer.png (RGBA)   │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ GHÉP LỚP 1 + 2                       │
│ - Paste product lên background       │
│ - Output: composite_layer.png        │
└─────────────────────────────────────┘
  ↓
┌─────────────────────────────────────┐
│ LỚPBASE 3: TEXT & OVERLAY (Chữ)      │
│ - Vẽ chữ tiếng Việt lên ảnh          │
│ - Tính vị trí tối ưu                 │
│ - Chọn màu chữ dựa vào nền           │
│ - Library: Pillow (PIL)              │
│ - Font: Roboto-Bold.ttf (TTF)        │
└─────────────────────────────────────┘
  ↓
OUTPUT: Banner quảng cáo hoàn chỉnh
```

---

## API Endpoints

### Ví dụ sử dụng với cURL:

```bash
# 1. Tách nền
curl -X POST -F "file=@product.jpg" http://localhost:5000/api/remove-background

# 2. Tạo nền AI
curl -X POST -H "Content-Type: application/json" \
  -d '{"prompt":"blue gradient","width":800,"height":600}' \
  http://localhost:5000/api/generate-background

# 3. Tạo banner
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Sale","text_color":[255,255,0]}' \
  http://localhost:5000/api/create-banner

# 4. Liệt kê ảnh
curl http://localhost:5000/api/files

# 5. Tải ảnh
curl -O http://localhost:5000/api/download/banner.png
```

---

## Deployment

### Option 1: Chạy Local (Development)

```bash
python app.py
# http://localhost:5000
```

### Option 2: Deploy với Gunicorn

```bash
pip install gunicorn

# Chạy production
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 3: Docker

**Dockerfile:**

```dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

**Build & Run:**

```bash
docker build -t image-compositing .
docker run -p 5000:5000 image-compositing
```

---

## Troubleshooting

### ❌ Lỗi: "ModuleNotFoundError: No module named 'rembg'"

```bash
pip install rembg
```

### ❌ Lỗi: "Cannot find Stable Diffusion WebUI"

```bash
# Kiểm tra server chạy
http://localhost:7860

# Hoặc dùng Replicate API
export REPLICATE_API_TOKEN=<token>
```

### ❌ Lỗi: Font không hiển thị tiếng Việt

```python
# Kiểm tra font hỗ trợ Unicode
# Sử dụng: arial.ttf, Roboto-Bold.ttf
# Tránh: Segoe UI Symbol
```

### ❌ Lỗi: "Port 5000 already in use"

```bash
# Dùng port khác
python -c "from app import app; app.run(port=8000)"
```

---

## Ngồi trong Báo cáo Thực tập

### 1. Phần Kiến trúc

- Minh họa 3 lớp
- Mô tả từng module
- Workflow diagram

### 2. Phần So sánh

- **Cách cũ:** Yêu cầu AI vẽ cả chữ
  - ❌ Chữ bị lỗi, méo mó
  - ❌ Chữ tiếng Việt không rõ
- **Cách mới (3 Lớp):**
  - ✅ Chữ rõ nét, chuẩn xác
  - ✅ Hỗ trợ tiếng Việt 100%
  - ✅ Tính toán vị trí tối ưu
  - ✅ Chọn màu chữ tự động

### 3. Phần Code

- Đính kèm `layer_compositing.py`
- Giải thích thuật toán Compositing
- Kết quả test

---

## Liên kết Hữu ích

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [rembg GitHub](https://github.com/danielgatis/rembg)
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Replicate AI](https://replicate.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Tác giả:** GitHub Copilot  
**Ngày cập nhật:** 2026-02-02  
**Phiên bản:** 1.0
