# 🖥️ Giao Diện Sử Dụng (UI Guide)

## 3 Cách Sử Dụng

### 1️⃣ Desktop GUI (Dễ nhất)

**Tốt cho:** Người dùng thích click chuột, xem trước trực tiếp

```bash
python gui_desktop.py
```

**Tính năng:**

- ✅ Giao diện Windows-style
- ✅ Upload ảnh drag-drop
- ✅ Xem trước real-time
- ✅ Không cần cài thêm gì (tkinter tích hợp)
- ✅ Phù hợp cho cả máy Mac/Linux

**Hướng dẫn:**

1. **Upload ảnh sản phẩm** → Click "📂 Chọn ảnh sản phẩm"
2. **Tách nền** → Click "✂️ Tách nền" (optional)
3. **Chọn loại nền** → Click "🎯 Loại nền"
4. **Nhập chữ** → Ghi vào "Dòng chữ"
5. **Tạo banner** → Click "✨ TẠO BANNER"
6. **Lưu kết quả** → Click "💾 Lưu kết quả"

---

### 2️⃣ CLI Interface (Mạnh mẽ)

**Tốt cho:** Batch processing, automation, server

```bash
python cli_interface.py
```

**Menu:**

```
1. 🎯 Tạo Banner Nhanh
2. 📦 Tách nền sản phẩm
3. 🤖 Tạo nền AI
4. 🔧 Tùy chỉnh nâng cao
5. 📊 Chạy test toàn bộ
0. ❌ Thoát
```

**Ưu điểm:**

- ✅ Tất cả tính năng có sẵn
- ✅ Có thể scriptify dễ dàng
- ✅ Nhanh cho batch processing
- ✅ Hoạt động trên server (no GUI needed)

**Ví dụ sử dụng:**

```bash
# Chạy CLI
python cli_interface.py

# Chọn option 1 (Tạo Banner Nhanh)
# Nhập: "🔥 SIÊU SALE 50%"
# Nhập: 800 (width)
# Nhập: 600 (height)
# → Banner được tạo tại: output/quick_banner_*.png
```

---

### 3️⃣ Web Interface (Hiện đại)

**Tốt cho:** Browser, Mobile, Collaborative

```bash
python app.py
```

**Truy cập:** Open browser at `http://localhost:5000`

**Tính năng:**

- ✅ Responsive design (mobile-friendly)
- ✅ Xem trước trực tiếp
- ✅ REST API cho integration
- ✅ Modern UI/UX

---

## 📊 So sánh 3 Giao diện

| Tính năng            | Desktop GUI | CLI         | Web        |
| -------------------- | ----------- | ----------- | ---------- |
| **Dễ sử dụng**       | ⭐⭐⭐⭐⭐  | ⭐⭐⭐      | ⭐⭐⭐⭐   |
| **Xem trước**        | ⭐⭐⭐⭐⭐  | ❌          | ⭐⭐⭐⭐   |
| **Tốc độ**           | ⭐⭐⭐      | ⭐⭐⭐⭐⭐  | ⭐⭐⭐     |
| **Automation**       | ❌          | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐   |
| **API**              | ❌          | Python call | REST       |
| **Batch processing** | ❌          | ⭐⭐⭐⭐⭐  | ⭐⭐⭐     |
| **Mobile support**   | ❌          | ❌          | ⭐⭐⭐⭐⭐ |

---

## 🚀 Quick Start cho Mỗi Giao Diện

### Desktop GUI - 3 Bước

```bash
# 1. Chạy
python gui_desktop.py

# 2. Click buttons
# 3. Tải xuống
```

### CLI - 3 Bước

```bash
# 1. Chạy
python cli_interface.py

# 2. Chọn option 1
# 3. Nhập thông tin
```

### Web - 3 Bước

```bash
# 1. Chạy
python app.py

# 2. Mở http://localhost:5000
# 3. Upload và download
```

---

## 🎯 Trường hợp sử dụng

### Bạn muốn...

**Tạo nhanh một banner → Dùng Desktop GUI hoặc CLI**

```bash
python cli_interface.py
# Chọn option 1
```

**Xử lý 100 ảnh cùng lúc → Dùng CLI + Script**

```python
# batch_process.py
from cli_interface import quick_banner_mode

for i in range(100):
    quick_banner_mode()
```

**Chia sẻ với team → Dùng Web Interface**

```bash
python app.py
# Share: http://your-ip:5000
```

**Dùng lần đầu, thích click → Desktop GUI**

```bash
python gui_desktop.py
```

---

## 🔧 Desktop GUI - Chi Tiết

### Panel Trái (Controls)

**📦 Lớp 2: Sản phẩm**

- `📂 Chọn ảnh sản phẩm` - Chọn file ảnh
- `✂️ Tách nền` - Xóa nền cũ (dùng rembg)

**🎨 Lớp 1: Nền**

- `🎯 Loại nền` - Chọn gradient/solid/file
- `Màu nền` - RGB (100,150,200)
- `🤖 Tạo nền AI` - Dùng Stable Diffusion
- `Prompt AI` - Mô tả nền (tiếng Anh)

**✏️ Lớp 3: Chữ**

- `Dòng chữ` - Tiếng Việt hỗ trợ ✓
- `Kích thước chữ` - Slider 20-100px
- `Màu chữ` - RGB (255,255,0)
- `Kích thước` - W×H của banner

**Action Buttons**

- `✨ TẠO BANNER` - Generate (main button)
- `💾 Lưu kết quả` - Save to disk
- `📁 Mở thư mục output` - Browse results

### Panel Phải (Preview)

- **👁️ Xem trước** - Real-time preview
- **Info** - Kích thước ảnh

---

## 💻 CLI Interface - Menu Interaktif

```
Chọn chế độ:
1. 🎯 Tạo Banner Nhanh
   → Nhập text + kích thước
   → Output: quick_banner_*.png

2. 📦 Tách nền sản phẩm
   → Chọn ảnh từ input/
   → Output: *_no_bg.png

3. 🤖 Tạo nền AI
   → Nhập prompt
   → Chọn API (Replicate/Local)
   → Output: bg_ai_*.png

4. 🔧 Tùy chỉnh nâng cao
   → Chọn từng lớp
   → Tùy chỉnh đầy đủ
   → Output: custom_banner_*.png

5. 📊 Chạy test toàn bộ
   → Test các script
   → Output: test_*.png

0. ❌ Thoát
```

---

## 🌐 Web Interface - Endpoints

**Base URL:** `http://localhost:5000`

### Frontend

- `GET /` - Giao diện chính

### API Endpoints

```
POST /api/remove-background
  Body: file (multipart)
  Response: {success, filename, size, mode}

POST /api/generate-background
  Body: {prompt, width, height, api_type}
  Response: {success, filename, size}

POST /api/create-banner
  Body: {text, text_color, bg_color, ...}
  Response: {success, filename}

GET /api/files
  Response: {count, files}

GET /api/download/<filename>
  Response: Image file
```

---

## ⚙️ Configuration

### Desktop GUI Settings

Edit file `gui_desktop.py`:

```python
# Default values
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_TEXT = "🔥 SIÊU SALE 50%"
DEFAULT_TEXT_COLOR = (255, 255, 0)
DEFAULT_BG_COLOR = (100, 150, 200)
```

### CLI Settings

Edit file `cli_interface.py`:

```python
# Modify default values in functions
```

### Web Settings

Edit file `app.py`:

```python
UPLOAD_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

---

## 🐛 Troubleshooting

### Desktop GUI không chạy

```bash
# Check tkinter
python -c "import tkinter; print('OK')"

# If error, install:
# Windows: tkinter tích hợp sẵn
# Mac: brew install python-tk
# Linux: sudo apt install python3-tk
```

### CLI không hiển thị màu

```bash
# Đó là bình thường trên Windows CMD cũ
# Dùng PowerShell hoặc Windows Terminal
```

### Web không kết nối

```bash
# Check port 5000
# Hoặc dùng port khác:
python -c "from app import app; app.run(port=8000)"
```

---

## 📱 Mobile Access (Web)

```bash
# Lấy IP local
ipconfig  # Windows
ifconfig  # Mac/Linux

# Chia sẻ URL
http://<your-ip>:5000

# Team có thể access từ mobile
```

---

## 🎓 Cho Báo Cáo Thực Tập

### Screenshot cần lấy

**Desktop GUI:**

- Main window
- Panel controls
- Preview result

**CLI:**

- Menu screenshot
- Output messages

**Web:**

- Browser interface
- Upload form
- Result preview

### Mô tả

```
3.1 User Interface
  - Desktop GUI (tkinter): Giao diện dễ sử dụng
  - CLI Interface: Automation & batch processing
  - Web Interface: Browser-based, mobile-friendly
```

---

## 🎁 Bonus: Tạo Shortcut

### Windows Desktop Shortcut

```batch
@echo off
python gui_desktop.py
pause
```

Save as: `ImageCompositor.bat`

### Mac/Linux Desktop

```bash
#!/bin/bash
cd ~/path/to/image_processing_demo
python gui_desktop.py
```

Save as: `ImageCompositor.app` (Mac) or `.desktop` (Linux)

---

**Chọn giao diện phù hợp với nhu cầu của bạn!** 🚀
