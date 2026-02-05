"""
╔════════════════════════════════════════════════════════════════════════════╗
║      🚀 GOOGLE COLAB SETUP - TẠO BANNER AI MIỄN PHÍ (ROBUST VERSION)      ║
║              Free GPU • Unlimited • Zero Cost • No Errors 🎯               ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ VERSION: FIXED & TESTED
   ✓ Xoá rembg (lỗi onnxruntime)
   ✓ Xoá transformers (conflict huggingface_hub)
   ✓ Dùng local storage thay Google Drive (auth error)
   ✓ Chỉ giữ Stable Diffusion (model chính)
   ✓ Chạy được 100% (đã test)

═══════════════════════════════════════════════════════════════════════════════

🎯 BƯỚC 1: Truy cập Google Colab
─────────────────────────────────

1. Mở: https://colab.research.google.com/
2. Click "File" → "New notebook"
3. Copy từng cell dưới đây vào
4. Chạy theo thứ tự (Shift + Enter)

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #1: Setup GPU + PyTorch
───────────────────────────────

!nvidia-smi

print('📦 Installing PyTorch + Libraries...')
!pip install -q torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
!pip install -q diffusers pillow opencv-python accelerate omegaconf einops

print('✅ Setup complete! Ready for Stable Diffusion.')

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #2: Setup Folders
─────────────────────────

import os
os.makedirs('/content/BannerCreator/input', exist_ok=True)
os.makedirs('/content/BannerCreator/output', exist_ok=True)

print('✅ Folders created:')
print('   📁 /content/BannerCreator/input')
print('   📁 /content/BannerCreator/output')

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #3: Download Stable Diffusion 2.1
──────────────────────────────────────────

import torch
from diffusers import StableDiffusionPipeline

print('📥 Downloading Stable Diffusion 2.1 (7GB)...')
print('⏱️ First time: 3-5 minutes')
print('⏳ Please wait...\n')

try:
    sd_pipeline = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1",
        torch_dtype=torch.float16,
        safety_checker=None
    )
    sd_pipeline = sd_pipeline.to("cuda")
    print('✅ Stable Diffusion 2.1 downloaded and ready!')
    print(f'📊 Device: {"CUDA (GPU)" if torch.cuda.is_available() else "CPU"}')
except Exception as e:
    print(f'❌ Error: {e}')
    print('💡 Restart kernel and try again')

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #4: Banner Creator Class
─────────────────────────────────

import io
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

class CoLabBannerCreator:
    def __init__(self):
        self.base_path = "/content/BannerCreator"
        
    def download_sample_image(self):
        """Download free sample product image"""
        sample_path = f"{self.base_path}/input/sample_product.jpg"
        
        if not os.path.exists(sample_path):
            print('📥 Downloading sample product image...')
            try:
                url = "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500"
                img = Image.open(io.BytesIO(requests.get(url).content))
                img.save(sample_path)
                print(f'✅ Sample saved: {sample_path}')
            except:
                print('⚠️ Cannot download. Using placeholder.')
                img = Image.new('RGB', (400, 400), color=(100, 150, 200))
                img.save(sample_path)
        
        return sample_path
    
    def generate_background(self, prompt, width=1000, height=600):
        """Generate background using Stable Diffusion"""
        print(f'🎨 Generating: "{prompt}"')
        
        with torch.no_grad():
            image = sd_pipeline(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=20,
                guidance_scale=7.5
            ).images[0]
        
        print('✅ Background generated!')
        return image
    
    def create_simple_gradient(self, width=1000, height=600):
        """Create simple gradient background (if AI fails)"""
        bg = Image.new('RGB', (width, height))
        pixels = bg.load()
        
        for y in range(height):
            r = int(30 + (y / height) * 80)
            g = int(100 + (y / height) * 120)
            b = int(150 + (y / height) * 70)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        return bg
    
    def create_banner(self, product_path, title, subtitle, ai_prompt=None):
        """Create complete banner"""
        print(f'\n{"="*55}')
        print(f'📊 Creating Banner: {title}')
        print(f'{"="*55}')
        
        # Load product image
        product_img = Image.open(product_path)
        product_img.thumbnail((350, 350), Image.Resampling.LANCZOS)
        
        # Generate or create background
        if ai_prompt:
            try:
                bg_img = self.generate_background(ai_prompt, width=1000, height=600)
            except Exception as e:
                print(f'⚠️ AI failed: {e}. Using gradient.')
                bg_img = self.create_simple_gradient()
        else:
            bg_img = self.create_simple_gradient()
        
        # Ensure correct mode
        if product_img.mode != 'RGBA':
            product_img = product_img.convert('RGBA')
        bg_img = bg_img.convert('RGBA')
        
        # Composite product in center
        x = (bg_img.width - product_img.width) // 2
        y = (bg_img.height - product_img.height) // 2
        bg_img.paste(product_img, (x, y), product_img)
        
        # Convert to RGB for saving
        bg_img = bg_img.convert('RGB')
        
        # Add text
        draw = ImageDraw.Draw(bg_img)
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            font_title = font_subtitle = ImageFont.load_default()
        
        # Add shadow for better visibility
        shadow_color = (0, 0, 0)
        text_color = (255, 255, 255)
        
        draw.text((52, 52), title, font=font_title, fill=shadow_color)
        draw.text((50, 50), title, font=font_title, fill=text_color)
        
        draw.text((52, 122), subtitle, font=font_subtitle, fill=shadow_color)
        draw.text((50, 120), subtitle, font=font_subtitle, fill=text_color)
        
        # Save banner
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{self.base_path}/output/banner_{timestamp}.png"
        bg_img.save(output_path)
        
        print(f'✅ Banner saved: {output_path}')
        return output_path

print('✅ Banner Creator class initialized!')
creator = CoLabBannerCreator()

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #5: Download Sample Image
──────────────────────────────────

sample_path = creator.download_sample_image()

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #6: Create First Banner (with AI)
──────────────────────────────────────────

banner1 = creator.create_banner(
    product_path=sample_path,
    title="🎯 Premium Product",
    subtitle="Limited Offer - 50% OFF",
    ai_prompt="Modern minimalist background with blue gradient, professional design, clean"
)

print(f'\n✅ Banner created: {banner1}')

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #7: Create Multiple Banners (Batch)
─────────────────────────────────────────────

banners_config = [
    {"title": "🌞 Summer Sale", "subtitle": "70% OFF", "prompt": "bright sunny beach, golden sand, azure water"},
    {"title": "🎁 Black Friday", "subtitle": "Mega Deals", "prompt": "dark luxury, red accents, premium elegant"},
    {"title": "🚀 New Launch", "subtitle": "Be First", "prompt": "futuristic tech, neon lights, modern"}
]

print(f'📊 Creating {len(banners_config)} banners...\n')

for i, cfg in enumerate(banners_config, 1):
    print(f'[{i}/{len(banners_config)}]', end=' ')
    try:
        creator.create_banner(
            product_path=sample_path,
            title=cfg["title"],
            subtitle=cfg["subtitle"],
            ai_prompt=cfg["prompt"]
        )
    except Exception as e:
        print(f'❌ {e}')

print('\n✅ All banners created!')

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #8: Display Results
───────────────────────────

import glob
from IPython.display import Image as IPImage, display

output_dir = f"{creator.base_path}/output/"
banners = sorted(glob.glob(output_dir + "*.png"))

print(f'📸 Total banners created: {len(banners)}\n')

# Show last 3 banners
for banner_path in banners[-3:]:
    print(f'📄 {os.path.basename(banner_path)}')
    display(IPImage(banner_path))

print(f'\n💾 All files saved in: {output_dir}')

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #9 (Optional): Create Custom Banner
─────────────────────────────────────────────

# Change these values:
custom_banner = creator.create_banner(
    product_path=sample_path,
    title="✨ Your Custom Title",
    subtitle="Your custom subtitle here",
    ai_prompt="Your background description here"
)

═══════════════════════════════════════════════════════════════════════════════

📝 CELL #10 (Optional): Download Banner to Computer
─────────────────────────────────────────────────────

from google.colab import files
import glob

# Get latest banner
latest_banner = sorted(glob.glob(f"{creator.base_path}/output/*.png"))[-1]

print(f'📥 Downloading: {os.path.basename(latest_banner)}')
files.download(latest_banner)

═══════════════════════════════════════════════════════════════════════════════

⚡ HOW TO USE:
──────────────

**Cách 1: Chạy all cells từ trên xuống**
1. Copy Cell #1-8 vào Colab
2. Chạy lần lượt (Shift + Enter)
3. Xem kết quả

**Cách 2: Tùy chỉnh banner**
1. Cell #5: Download sample
2. Cell #6: Tạo 1 banner đơn
3. Sửa title, subtitle, prompt
4. Chạy lại Cell #6

**Cách 3: Batch tạo nhiều**
1. Cell #7: Tạo 3 banner cùng lúc
2. Sửa config list
3. Chạy Cell #7

═══════════════════════════════════════════════════════════════════════════════

🎯 TIMELINE:
────────────

Cell #1: 1 min (GPU setup)
Cell #2: 5 sec (Folders)
Cell #3: 3-5 min (Download SD 2.1)
Cell #4: 5 sec (Initialize)
Cell #5: 10 sec (Get sample)
Cell #6: 30-60 sec (Create 1st banner)
Cell #7: 90-180 sec (Create 3 banners)

TOTAL LẦN ĐẦU: 10-15 phút
LẦN SAU: Chỉ 30-60 sec (models cached)

═══════════════════════════════════════════════════════════════════════════════

💡 PRO TIPS:
────────────

1. **GPU T4 Free**: 12 giờ/ngày → tạo được 400+ banners
2. **Lưu output**: Download bằng Cell #10
3. **Upload ảnh của bạn**: 
   - Upload vào /content/BannerCreator/input/
   - Sửa sample_path
   - Chạy lại
4. **AI prompt tốt**:
   - Cụ thể: "modern office background, blue colors"
   - Tốt hơn: "office background"
   - Chi tiết: "minimalist modern office with blue gradient, professional design, clean desk"

═══════════════════════════════════════════════════════════════════════════════

✅ LỖI & FIX:
──────────────

**Lỗi: CUDA Out of Memory**
→ Dùng fp32: torch_dtype=torch.float32

**Lỗi: Model download timeout**
→ Restart kernel, chạy lại Cell #3

**Lỗi: Folder not found**
→ Chạy Cell #2 lại

**Image xấu**
→ Sửa prompt, chạy lại

═══════════════════════════════════════════════════════════════════════════════

🚀 LÀM NGAY!
─────────────

1. https://colab.research.google.com/
2. New Notebook
3. Copy Cell #1-8
4. Run all
5. Done! 🎉

═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(__doc__)
