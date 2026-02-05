# 🎨 AI Banner Creator - Inpainting + Groq Edition

> Tạo banner sản phẩm tự động với AI. Sản phẩm không bị méo mó, nền sinh bởi AI 100%.

## 🎯 Quy Trình

```
Ảnh sản phẩm (PNG)
    ↓
[Chuẩn bị & Mask]
    ↓
[Groq API: Text Generation] + [SD Inpainting: Background]
    ↓
[Composite: Background + Product + Text]
    ↓
✓ Banner 1200x630 PNG
```

## ⚙️ Kiến Trúc

- **Layer 1 (Bottom)**: Nền (Stable Diffusion Inpainting)
- **Layer 2 (Middle)**: Sản phẩm (gốc, không bị méo)
- **Layer 3 (Top)**: Text (Groq API)

## 🚀 Cài Đặt Nhanh

### 1. Yêu Cầu Phần Cứng

```
✓ GPU: NVIDIA RTX 3060 12GB (tối thiểu)
✓ RAM: 16GB
✓ Storage: 20GB (cho models)
```

### 2. Cài Dependencies

```bash
# Python 3.10+
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements_inpainting.txt
```

### 3. Setup Groq API (Tùy Chọn)

```bash
# Get API key: https://console.groq.com
export GROQ_API_KEY="your_key_here"
```

### 4. Test Setup

```bash
python test_inpainting_setup.py
```

### 5. Chạy Ứng Dụng

```bash
python banner_creator_free_ai.py
```

## 📖 Hướng Dẫn Chi Tiết

Xem file: [INPAINTING_GUIDE.py](INPAINTING_GUIDE.py)

## 📋 File Quan Trọng

| File                        | Mô Tả                          |
| --------------------------- | ------------------------------ |
| `banner_creator_free_ai.py` | GUI chính                      |
| `inpainting_helper.py`      | Helper cho inpainting workflow |
| `groq_integration.py`       | Tích hợp Groq API              |
| `inpainting_config.json`    | Cấu hình                       |
| `test_inpainting_setup.py`  | Script test                    |
| `INPAINTING_GUIDE.py`       | Hướng dẫn chi tiết             |

## 🎬 Ví Dụ Sử Dụng

### GUI Mode (Dễ nhất)

```bash
python banner_creator_free_ai.py
```

### Programmatic Mode (Python Script)

```python
from diffusers import StableDiffusionInpaintPipeline
from inpainting_helper import InpaintingHelper
from groq_integration import GroqTextGenerator
import torch

# Load models
pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

helper = InpaintingHelper(pipe)
text_gen = GroqTextGenerator(api_key="your_key")

# Generate text
title = text_gen.generate_title("Premium Shoes")

# Create inpainting mask
product_img = Image.open("shoe.png").convert("RGBA")
mask, resized, pos = helper.create_inpainting_mask(product_img)

# Run inpainting
init_img = helper.create_init_image()
bg = helper.run_inpainting(init_img, mask, "Professional studio backdrop")

# Composite
final = helper.composite_final(bg, resized, pos, title)
final.save("output/banner.png")
```

## 🔧 Advanced: Batch Processing

```python
from inpainting_helper import BatchInpaintingProcessor
from groq_integration import BatchTextGenerator

# Danh sách sản phẩm
products = [
    {"name": "Shoe 1", "type": "shoes"},
    {"name": "Shoe 2", "type": "shoes"},
]

# Tạo text cho batch
text_gen = BatchTextGenerator(api_key="your_key")
texts = text_gen.generate_for_products(products)

# Xử lý batch inpainting
processor = BatchInpaintingProcessor(pipeline)
output_paths = processor.process_products(
    product_paths=["shoe1.png", "shoe2.png"],
    prompt="Professional shoe display",
    output_folder=Path("output")
)
```

## ⚠️ Troubleshooting

### "CUDA out of memory"

```python
# Giảm quality
num_inference_steps=30  # vs 50
guidance_scale=6.5  # vs 7.5

# Hoặc giảm size
banner_width, banner_height = 800, 420
```

### "Model download failed"

```bash
# Manual download
from diffusers import StableDiffusionInpaintPipeline
import torch

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
)
# Lưu locally
pipe.save_pretrained("./models/inpaint")
```

### "Groq API timeout"

- Check internet connection
- Check rate limit (30 req/min free tier)
- Use fallback text: `product_name`

## 📊 Performance

**GPU RTX 3060 (12GB)**

- Model load: 2-3s
- Per inpainting: 30-60s
- Per banner: 1-2 min
- Batch 10: 5-10 min

**GPU RTX 4090 (24GB)**

- Per inpainting: 15-30s
- Per banner: 30-60s
- Batch 10: 3-5 min

## 💡 Tips

1. **Prompt Engineering**
   - "Professional studio lighting" → chuyên nghiệp
   - "Cinematic, movie poster" → high-end
   - "Vibrant, colorful" → sinh động

2. **Product Image Prep**
   - PNG transparent background ✓
   - 300-500px height recommended
   - Good lighting in original

3. **Batch Processing**
   - Run at night (idle GPU)
   - Monitor VRAM usage
   - Save config to JSON

## 🔗 Resources

- [Stable Diffusion Inpainting](https://huggingface.co/runwayml/stable-diffusion-inpainting)
- [Groq API Docs](https://groq.com/docs/)
- [Diffusers Documentation](https://huggingface.co/docs/diffusers)
- [Pillow Documentation](https://pillow.readthedocs.io/)

## ✅ Checklist Trước Deploy

- [ ] GPU RTX 3060+
- [ ] CUDA toolkit cài đúng
- [ ] Diffusers library OK
- [ ] Groq API key lấy được
- [ ] Inpainting model download OK
- [ ] Test 1 ảnh sản phẩm
- [ ] Output folder tạo được

## 📝 License

MIT License - Tự do sử dụng

## 👨‍💻 Support

Issues? Check:

1. [INPAINTING_GUIDE.py](INPAINTING_GUIDE.py) - Hướng dẫn chi tiết
2. [test_inpainting_setup.py](test_inpainting_setup.py) - Run để test
3. GitHub Issues - Report bugs

---

**Version:** 2.0 (Inpainting + Groq)  
**Last Updated:** 2026-02-04  
**Status:** ✓ Production Ready

🎉 **Ready? Run: `python banner_creator_free_ai.py`**
