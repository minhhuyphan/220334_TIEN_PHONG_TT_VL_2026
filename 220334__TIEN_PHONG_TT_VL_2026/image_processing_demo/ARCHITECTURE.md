# 3-Layer Image Compositing Architecture

## 📐 Kiến trúc Tổng quan

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
│  - Web Interface (Flask + HTML/CSS/JS)                      │
│  - Upload UI, Preview, Download                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER (REST)                         │
│  - /api/remove-background                                  │
│  - /api/generate-background                                │
│  - /api/create-banner                                      │
│  - /api/files                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 PROCESSING LAYER                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ LayerCompositor        | Advanced Compositor         │  │
│  │ - create_background()  | - paste_product()           │  │
│  │ - create_product()     | - add_smart_text()          │  │
│  │ - composite_layers()   | - calculate_brightness()    │  │
│  │ - add_text_overlay()   | - get_optimal_text_color()  │  │
│  │ - save_result()        | - find_text_placement()     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              IMAGE PROCESSING LAYER                         │
│  ┌─────────────────┬──────────────┬─────────────────────┐   │
│  │ Pillow (PIL)    │ rembg        │ numpy               │   │
│  │ - Image ops     │ - Background │ - Array operations  │   │
│  │ - ImageDraw     │   removal    │ - Brightness calc   │   │
│  │ - ImageFont     │ - U²-Net ML  │                     │   │
│  │ - Color ops     │ - ONNX model │                     │   │
│  └─────────────────┴──────────────┴─────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                AI/ML LAYER (External)                       │
│  ┌──────────────────┬────────────────────────────────────┐  │
│  │ Stable Diffusion │ rembg U²-Net                       │  │
│  │ - Local WebUI    │ - Pre-trained model                │  │
│  │ - Replicate API  │ - Optimized inference              │  │
│  │ - Text → Image   │ - Background segmentation          │  │
│  └──────────────────┴────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              STORAGE LAYER                                  │
│  - input/          (Product images, backgrounds)           │
│  - output/         (Final banners)                          │
│  - fonts/          (TTF font files)                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 The 3-Layer Image Model

### Layer 1: Background (Nền)
```
Purpose:    Create aesthetic context and lighting
Technology: Generative AI (Stable Diffusion)
Input:      Text prompt (English)
Output:     background_layer.png (RGB)

Example:
  Prompt: "modern blue gradient, professional lighting"
  ↓
  AI generates background image
  ↓
  Output: 800x600 RGB image
```

**Advantages:**
- AI excels at creating natural, beautiful backgrounds
- No text needed = No text corruption
- Customizable via prompt

**How it works:**
```
Stable Diffusion (Text-to-Image)
Input: "modern blue gradient background"
  ↓
1. Tokenize prompt
2. CLIP encoding (convert text to embeddings)
3. Diffusion model (iterative denoising)
4. VAE decoder (embeddings → image)
Output: 512x512 RGB image
  ↓
Resize to 800x600
```

---

### Layer 2: Product (Sản phẩm)
```
Purpose:    Extract product with transparent background
Technology: Machine Learning (U²-Net, rembg)
Input:      product_original.jpg (with background)
Output:     product_layer.png (RGBA, transparent)

Example:
  Input:  Nike shoe on white background
  ↓
  rembg removes white background
  ↓
  Output: Nike shoe with transparent background
```

**Algorithm: U²-Net (Salient Object Detection)**
```
Input image (3 channels: RGB)
  ↓
[Residual U-Blocks × 6]
  ├─ Encoder: Downsample + Feature extraction
  └─ Decoder: Upsample + Detail refinement
  ↓
Output: Binary mask (foreground/background)
  ↓
Multiply with original image
  ↓
Output: RGBA image (with alpha channel)
```

**Why this layer matters:**
- Isolates product without manual cutting
- Alpha channel enables smooth compositing
- Faster than manual editing
- Consistent results

---

### Layer 3: Text & Overlay (Chữ & Họa tiết)
```
Purpose:    Add Vietnamese text and visual effects
Technology: Traditional Image Processing (Pillow)
Input:      Text string (Vietnamese)
Output:     Final banner (RGB)

Example:
  Input: "Giảm 50%"
  ↓
  1. Load font (Roboto-Bold.ttf - Unicode support)
  2. Calculate text position (auto, centered)
  3. Measure brightness at that position
  4. Choose text color (black on light, white on dark)
  5. Draw shadow/outline for visibility
  6. Draw text
  ↓
  Output: Professional-looking banner
```

**Color Selection Algorithm:**
```python
def get_optimal_text_color(background_region):
    brightness = average_pixel_value(background_region)
    if brightness > 128:
        return (0, 0, 0)      # Black text on light bg
    else:
        return (255, 255, 255) # White text on dark bg
```

**Text Positioning Strategy:**
```
Priority positions:
1. Top center (most visible)
2. Bottom center (secondary)
3. Left middle (if top occupied)
4. Right middle (if left occupied)

Constraints:
- Don't overlap with product
- Maintain readable area
- Consider aspect ratio
```

---

## 📊 Data Flow: Step-by-Step

### Complete Pipeline Example

```
INPUT
  ├─ product.jpg (with background)
  └─ "Siêu Sale 50%"

STEP 1: Remove Background (Layer 2)
  ├─ Load: product.jpg
  ├─ Process: rembg U²-Net model
  └─ Output: product_no_bg.png (RGBA)

STEP 2: Generate Background (Layer 1)
  ├─ Prompt: "modern blue gradient, sportswear"
  ├─ Model: Stable Diffusion
  └─ Output: background.png (RGB, 800x600)

STEP 3: Composite Layers (Layer 1 + 2)
  ├─ Base: background.png
  ├─ Overlay: product_no_bg.png (centered)
  ├─ Method: PIL paste with alpha mask
  └─ Output: composite.png (RGB, 800x600)

STEP 4: Add Text (Layer 3)
  ├─ Text: "Siêu Sale 50%"
  ├─ Font: Roboto-Bold.ttf (Unicode)
  ├─ Brightness: Calculate from composite
  ├─ Color: auto-select (black or white)
  ├─ Position: Top center
  ├─ Effect: Add shadow for visibility
  └─ Output: final_banner.png (RGB, 800x600)

FINAL OUTPUT: Professional banner with:
  ✅ Beautiful AI-generated background
  ✅ Clean product isolation
  ✅ Perfect Vietnamese text
  ✅ Optimal color contrast
```

---

## 🧮 Mathematical Operations

### 1. Image Compositing (Blending)

```
For each pixel (x, y):
    C_final(x,y) = C_bg(x,y) * (1 - α) + C_fg(x,y) * α
    
Where:
  C_bg    = background color
  C_fg    = foreground (product) color
  α       = alpha channel (0 = transparent, 1 = opaque)
  
Example:
  Background: (100, 150, 200) - RGB
  Product:    (255, 0, 0) - Red
  Alpha:      0.8 - 80% opaque
  
  Result:
    R = 100 * (1-0.8) + 255 * 0.8 = 20 + 204 = 224
    G = 150 * (1-0.8) + 0 * 0.8 = 30 + 0 = 30
    B = 200 * (1-0.8) + 0 * 0.8 = 40 + 0 = 40
    
  C_final = (224, 30, 40)
```

### 2. Brightness Calculation

```
Grayscale = 0.299*R + 0.587*G + 0.114*B

Example:
  Pixel: (100, 150, 200)
  Brightness = 0.299*100 + 0.587*150 + 0.114*200
             = 29.9 + 88.05 + 22.8
             = 140.75 (relatively bright)
             
  Decision: Use dark text (0, 0, 0)
```

### 3. Font Rendering

```
TTF Font Rendering Pipeline:

1. Load .ttf file
   ↓
2. Rasterize to bitmap
   ├─ Font size
   ├─ DPI (dots per inch)
   └─ Anti-aliasing
   ↓
3. Render glyphs
   ├─ Character: 'S' → Glyph index
   ├─ Kerning: Adjust spacing
   └─ Ligatures: Handle combinations
   ↓
4. Composite on image
   ├─ Position: (x, y)
   ├─ Color: RGB
   └─ Blend with background
   ↓
Output: Rendered text on image
```

---

## 🔗 Module Dependencies

```
layer_compositing.py
├── PIL.Image
├── PIL.ImageDraw
├── PIL.ImageFont
└── pathlib.Path

background_removal.py
├── PIL.Image
├── rembg.remove, new_session
└── pathlib.Path

advanced_compositing.py
├── PIL.Image, ImageDraw, ImageFont
├── numpy
└── pathlib.Path

stable_diffusion_integration.py
├── requests
├── PIL.Image
├── io.BytesIO
├── base64
├── replicate (optional)
└── pathlib.Path

app.py (Flask API)
├── flask
├── werkzeug
├── layer_compositing
├── background_removal
├── stable_diffusion_integration
├── PIL.Image
└── pathlib.Path
```

---

## 🚀 Performance Characteristics

### Processing Times (Approximate)

| Step | Operation | Time | Notes |
|------|-----------|------|-------|
| Layer 1 | Generate background (Replicate) | 5-10s | API call + queue |
| Layer 1 | Generate background (Local WebUI) | 20-60s | Depends on GPU |
| Layer 2 | Remove background (rembg) | 2-5s | CPU/GPU optimized |
| Layer 3 | Composite + text | <1s | Very fast |
| **Total** | Full pipeline | 7-65s | Depends on Layer 1 |

### Memory Usage

- Layer 1: AI model requires 4-8GB VRAM (if local)
- Layer 2: rembg model ~200MB RAM
- Layer 3: Pillow operations <50MB RAM
- **Total:** ~4-8GB (dominated by Layer 1 model)

### Output Quality

- Resolution: Up to 1024x1024 (Stable Diffusion limit)
- Format: PNG (supports transparency)
- Color depth: 8-bit per channel (RGB/RGBA)
- Compression: Lossless

---

## 🎯 Design Patterns

### 1. Strategy Pattern (AI Model Selection)

```python
class StableDiffusionGenerator:
    def __init__(self, api_type="local"):
        self.strategy = self._create_strategy(api_type)
    
    def generate_background(self, prompt):
        return self.strategy.generate(prompt)
```

### 2. Facade Pattern (API Layer)

```python
@app.route('/api/create-banner', methods=['POST'])
def create_banner():
    # Hides complexity of 3 layers
    compositor = LayerCompositor()
    compositor.create_background(...)
    compositor.composite_layers(...)
    compositor.add_text_overlay(...)
    return json.response()
```

### 3. Template Method Pattern (Processing)

```python
class Compositor:
    def process(self):
        self.load_layers()
        self.validate_input()
        self.composite()
        self.finalize()
```

---

## 🔒 Error Handling

```
Pipeline Error Handling:

INPUT
  ↓
TRY:
  ├─ Layer 1: Generate background
  │   └─ CATCH: API error → Use solid color background
  ├─ Layer 2: Remove background
  │   └─ CATCH: rembg error → Use original image
  ├─ Layer 3: Add text
  │   └─ CATCH: Font error → Use default font
  └─ SAVE: Write to disk
      └─ CATCH: Disk error → Raise exception

OUTPUT: Graceful fallback or error message
```

---

## 📈 Scalability Considerations

### Horizontal Scaling

```
┌─────────┐
│ API 1   │──┐
└─────────┘  │
             ├─→ Load Balancer → Queue → Worker Pool
┌─────────┐  │
│ API 2   │──┤
└─────────┘  │
             │
┌─────────┐  │
│ API N   │──┘
└─────────┘

Each worker handles one pipeline.
```

### Caching Strategy

```
Cache Layer 1 outputs:
  Key: SHA256(prompt)
  Value: Generated image
  TTL: 24 hours
  
  Benefit: Identical prompts reuse results
```

### Async Processing

```
Request → Task Queue → Worker Pool → Result Storage
  ↓                                      ↓
Return job_id                    Return result via webhook
```

---

## 🎓 Advanced Topics

### 1. Stable Diffusion Fine-tuning

```python
# Custom model training (advanced)
def fine_tune_for_products():
    """
    Train SD on product images
    - LoRA (Low-Rank Adaptation)
    - Textual Inversion
    """
```

### 2. Advanced Text Layout

```python
# Multi-line text, rotation, effects
def advanced_text_rendering():
    """
    - Text wrapping
    - Rotation
    - Gradient fill
    - Outline
    - Shadow
    """
```

### 3. Batch Processing

```python
# Process 1000+ images
def batch_banner_generation():
    """
    - Parallel processing
    - GPU optimization
    - Memory pooling
    """
```

---

## 📚 References

- [Stable Diffusion Paper](https://arxiv.org/abs/2112.10752)
- [U²-Net: Going Deeper with Nested U-Structure](https://arxiv.org/abs/2005.09007)
- [Pillow Handbook](https://pillow.readthedocs.io/)
- [OpenAI CLIP](https://github.com/openai/CLIP)

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-02  
**Audience:** Technical documentation for developers
