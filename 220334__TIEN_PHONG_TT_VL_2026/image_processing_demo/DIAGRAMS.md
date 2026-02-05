# 📊 DIAGRAMS - Visualizations

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│  ┌─────────────┬──────────────┬──────────────────────────┐ │
│  │ Desktop GUI │  CLI Menu    │  Web Interface           │ │
│  │ (tkinter)   │ (Terminal)   │  (Flask + HTML/CSS/JS)   │ │
│  └─────┬───────┴──────┬───────┴──────────┬───────────────┘ │
│        │               │                  │                 │
└────────┼───────────────┼──────────────────┼─────────────────┘
         │               │                  │
┌────────▼───────────────▼──────────────────▼─────────────────┐
│                    API LAYER                                 │
│  - /api/create-banner                                       │
│  - /api/remove-background                                   │
│  - /api/generate-background                                 │
└────────┬──────────────────────────────────────────────────────┘
         │
┌────────▼──────────────────────────────────────────────────────┐
│              PROCESSING LAYER                                 │
│  ┌──────────────────┬────────────────┬──────────────────┐    │
│  │ LayerCompositor  │ AdvancedComp   │ BackgroundRem.   │    │
│  ├──────────────────┼────────────────┼──────────────────┤    │
│  │ - create_bg()    │ - paste_prod() │ - remove_bg()    │    │
│  │ - composite()    │ - smart_text() │ - batch_remove() │    │
│  │ - add_text()     │ - calc_bright()│                  │    │
│  │ - save()         │                │                  │    │
│  └──────────────────┴────────────────┴──────────────────┘    │
└────────┬──────────────────────────────────────────────────────┘
         │
┌────────▼──────────────────────────────────────────────────────┐
│           IMAGE PROCESSING LAYER                              │
│  ┌──────────────┬─────────────┬────────────────────────┐     │
│  │ Pillow (PIL) │ rembg       │ numpy                  │     │
│  │ - Image ops  │ - U²-Net ML │ - Array operations     │     │
│  │ - ImageDraw  │ - ONNX      │ - Brightness calc      │     │
│  │ - ImageFont  │ - Remove BG │                        │     │
│  └──────────────┴─────────────┴────────────────────────┘     │
└────────┬──────────────────────────────────────────────────────┘
         │
┌────────▼──────────────────────────────────────────────────────┐
│              AI/ML LAYER (External Services)                  │
│  ┌──────────────────────┬────────────────────────────────┐   │
│  │ Stable Diffusion     │ U²-Net (via rembg)            │   │
│  │ - Local WebUI        │ - Pre-trained model           │   │
│  │ - Replicate API      │ - Background segmentation     │   │
│  │ - Text to Image      │                               │   │
│  └──────────────────────┴────────────────────────────────┘   │
└────────┬──────────────────────────────────────────────────────┘
         │
┌────────▼──────────────────────────────────────────────────────┐
│                  OUTPUT / STORAGE                              │
│  ├─ output/banner_*.png                                       │
│  ├─ output/*_no_bg.png                                        │
│  └─ output/bg_*.png                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. 3-Layer Stacking Model

```
FINAL OUTPUT (Banner 800×600)
┌──────────────────────────────────────┐
│                                      │
│  ┌────────────────────────────────┐ │
│  │  LAYER 3: TEXT                 │ │──► Vẽ chữ tiếng Việt
│  │  🔥 SIÊU SALE 50%              │ │    (Pillow, TTF Font)
│  │  ┌──────────────────────────┐  │ │
│  │  │ LAYER 2: PRODUCT        │  │ │──► Product (Transparent)
│  │  │ (Isolated with alpha)   │  │ │    (rembg U²-Net)
│  │  │    ┌──────────────┐     │  │ │
│  │  │    │ LAYER 1:     │     │  │ │
│  │  │    │ BACKGROUND   │     │  │ │──► Nền đẹp
│  │  │    │ (Gradient)   │     │  │ │    (Stable Diffusion)
│  │  │    └──────────────┘     │  │ │
│  │  └──────────────────────────┘  │ │
│  └────────────────────────────────┘ │
│                                      │
└──────────────────────────────────────┘

Stacking Order (Z-depth):
  3 (Top)    ← TEXT & OVERLAY (Lớp 3)
  2 (Middle) ← PRODUCT (Lớp 2)
  1 (Bottom) ← BACKGROUND (Lớp 1)
```

---

## 3. Data Flow Pipeline

```
┌──────────────┐
│ USER INPUT   │
│ - Image      │
│ - Text       │
└────────┬─────┘
         │
         ▼
┌────────────────────────────────────┐
│ LỚPBASE 1: BACKGROUND (Nền)        │
│ ────────────────────────────────── │
│ Input:  Text prompt (English)      │
│ Model:  Stable Diffusion           │
│ Output: background_layer.png (RGB) │
│ Time:   5-60s (API dependent)      │
└────────┬─────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ LỚPBASE 2: PRODUCT (Sản phẩm)      │
│ ────────────────────────────────── │
│ Input:  product.jpg (with BG)      │
│ Model:  U²-Net (rembg)             │
│ Output: product_layer.png (RGBA)   │
│ Time:   2-5s                       │
└────────┬─────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ COMPOSITE LAYERS (1 + 2)           │
│ ────────────────────────────────── │
│ Method: PIL Image.paste()          │
│ Output: composite_layer.png        │
│ Time:   <1s                        │
└────────┬─────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ LỚPBASE 3: TEXT & OVERLAY (Chữ)    │
│ ────────────────────────────────── │
│ Input:  Vietnamese text string     │
│ Font:   Roboto-Bold.ttf (Unicode)  │
│ Process:                           │
│  - Calculate brightness at pos     │
│  - Choose color (black/white)      │
│  - Draw text with shadow           │
│  - Optimize position               │
│ Output: final_banner.png (RGB)     │
│ Time:   <1s                        │
└────────┬─────────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│ FINAL OUTPUT                       │
│ - Professional Banner (800×600)    │
│ - High Quality (PNG)               │
│ - Vietnamese Text Support ✓        │
│ - Ready for Publishing             │
└────────────────────────────────────┘
```

---

## 4. GUI Layout

```
╔════════════════════════════════════════════════════════════════╗
║                   3-Layer Image Compositing Tool               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ┌──────────────────────┐  ┌──────────────────────────────┐   ║
║  │   LEFT PANEL         │  │    RIGHT PANEL               │   ║
║  │   (Controls)         │  │    (Preview)                 │   ║
║  │                      │  │                              │   ║
║  │ 📦 LỚPBASE 2         │  │  ┌──────────────────────────┐│   ║
║  │ [📂 Chọn ảnh]        │  │  │  Banner Preview          ││   ║
║  │ [✂️ Tách nền]        │  │  │  (Live update)           ││   ║
║  │ ✓ product.png       │  │  │                          ││   ║
║  │                      │  │  │  Size: 800×600           ││   ║
║  │ 🎨 LỚPBASE 1         │  │  │                          ││   ║
║  │ [🎯 Loại nền]        │  │  └──────────────────────────┘│   ║
║  │ Màu: 100,150,200    │  │                              │   ║
║  │ [🤖 Tạo nền AI]      │  │  ┌──────────────────────────┐│   ║
║  │ Prompt: [........]  │  │  │  Image info              ││   ║
║  │                      │  │  │  800 × 600 px           ││   ║
║  │ ✏️ LỚPBASE 3          │  │  └──────────────────────────┘│   ║
║  │ Text: [🔥 SALE]     │  │                              │   ║
║  │ Size: |---|---|--   │  │                              │   ║
║  │ Color: 255,255,0   │  │                              │   ║
║  │ W×H: 800 × 600      │  │                              │   ║
║  │                      │  │                              │   ║
║  │ [✨ TẠO BANNER]      │  │                              │   ║
║  │ [💾 LƯU KẾT QUẢ]     │  │                              │   ║
║  │ [📁 MỞ THƯ MỤC]     │  │                              │   ║
║  │ ✓ Ready             │  │                              │   ║
║  │                      │  │                              │   ║
║  └──────────────────────┘  └──────────────────────────────┘   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 5. CLI Menu Tree

```
MAIN MENU
  │
  ├─ 1️⃣ Tạo Banner Nhanh
  │   ├─ Input: Text
  │   ├─ Input: Width×Height
  │   └─ Output: quick_banner_*.png
  │
  ├─ 2️⃣ Tách nền sản phẩm
  │   ├─ List: input/ files
  │   ├─ Select: Image
  │   ├─ Process: rembg
  │   └─ Output: *_no_bg.png
  │
  ├─ 3️⃣ Tạo nền AI
  │   ├─ Input: Prompt
  │   ├─ Select: API (Replicate/Local)
  │   ├─ Process: Stable Diffusion
  │   └─ Output: bg_ai_*.png
  │
  ├─ 4️⃣ Tùy chỉnh nâng cao
  │   ├─ Layer 1: bg_type, path
  │   ├─ Layer 2: product_path
  │   ├─ Layer 3: text, color, size
  │   └─ Output: custom_banner_*.png
  │
  ├─ 5️⃣ Chạy test toàn bộ
  │   ├─ Test: test_01_basic.png
  │   ├─ Test: test_02_removal.png
  │   ├─ Test: test_03_advanced.png
  │   └─ Output: test_*.png
  │
  └─ 0️⃣ Thoát
```

---

## 6. Technology Stack

```
┌────────────────────────────────────────────┐
│         3-Layer Image Compositing          │
├────────────────────────────────────────────┤
│                                            │
│  Frontend Layer                            │
│  ├─ Tkinter (Desktop GUI)                 │
│  ├─ HTML/CSS/JS (Web UI)                  │
│  └─ Terminal (CLI)                        │
│                                            │
│  Backend Layer                             │
│  ├─ Flask (Web framework)                 │
│  ├─ Python 3.8+ (Core)                    │
│  └─ Custom modules                        │
│                                            │
│  Image Processing                          │
│  ├─ Pillow (PIL)                          │
│  ├─ NumPy (array operations)              │
│  ├─ rembg (background removal)            │
│  └─ OpenCV (optional)                     │
│                                            │
│  AI/ML Integration                         │
│  ├─ Stable Diffusion                      │
│  │  ├─ Local WebUI API                    │
│  │  └─ Replicate API                      │
│  │                                         │
│  └─ U²-Net (via rembg)                    │
│     ├─ ONNX runtime                       │
│     └─ Pre-trained models                 │
│                                            │
│  Deployment                                │
│  ├─ Docker                                │
│  ├─ Docker Compose                        │
│  └─ Gunicorn (production)                 │
│                                            │
└────────────────────────────────────────────┘
```

---

## 7. Workflow Comparison

```
Traditional Approach (AI only)
  ┌─────────────────────────────┐
  │ AI Model                    │
  │ ├─ Generate background      │
  │ ├─ Add product              │
  │ ├─ Write text (FAILS!)      │◄─ Problem!
  │ └─ Output: Broken result    │
  └─────────────────────────────┘
  ❌ Text corrupted, Vietnamese fails


Our Approach (3-Layer)
  ┌─────────────────┐
  │ Layer 1: AI     │ ◄─ Generate background
  └────────┬────────┘
           │
  ┌────────▼────────┐
  │ Layer 2: ML     │ ◄─ Remove background
  └────────┬────────┘
           │
  ┌────────▼────────┐
  │ Layer 3: Code   │ ◄─ Write Vietnamese text
  │ (Pillow)        │    (Perfect quality!)
  └────────┬────────┘
           │
  ┌────────▼──────────────┐
  │ Output: Perfect Banner │
  └───────────────────────┘
  ✅ Clean, professional, Vietnamese support
```

---

## 8. Performance Metrics

```
┌──────────────────────────────────────────┐
│         Processing Time (seconds)         │
├──────────────────────────────────────────┤
│                                          │
│  Layer 1 - Background Generation        │
│  ├─ Local WebUI:     ████████ 20-60s    │
│  └─ Replicate API:   ███ 5-10s          │
│                                          │
│  Layer 2 - Background Removal            │
│  └─ rembg (U²-Net):  ███ 2-5s           │
│                                          │
│  Layer 3 - Text & Compositing            │
│  └─ Pillow + Fonts:  █ <1s              │
│                                          │
│  Total Time:         ███████ 7-65s      │
│  (Dominated by Layer 1)                  │
│                                          │
└──────────────────────────────────────────┘

Memory Usage:
├─ Layer 1 (AI):    4-8 GB (GPU VRAM)
├─ Layer 2 (ML):    200-500 MB
└─ Layer 3 (PIL):   <50 MB
├─ TOTAL:           4-8 GB (GPU-dependent)

Output Quality:
├─ Resolution:      Up to 1024×1024
├─ Format:          PNG (lossless)
├─ Color depth:     8-bit per channel
└─ Compression:     No quality loss
```

---

**Created with ❤️ for your project**
