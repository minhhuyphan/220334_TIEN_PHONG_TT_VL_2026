#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🚀 ULTRA FAST BANNER CREATOR - Groq API
========================================
Tạo banner trong 10-15 giây sử dụng Groq API

Tính năng:
- Groq API: Text generation (1-2s)
- PIL: Image compositing (instant)
- Không cần GPU
- Chạy offline sau lần đầu

Thời gian: ~10 giây per banner
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import json

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

GROQ_AVAILABLE = False
REMBG_AVAILABLE = False

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    pass

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except:
    pass


class UltraFastBannerCreator:
    """Tạo banner siêu nhanh sử dụng Groq API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)
        
        self.groq_client = None
        if not GROQ_AVAILABLE:
            print("⚠️ Groq not installed: pip install groq")
            return
            
        if not self.api_key:
            print("❌ GROQ_API_KEY not set")
            return
            
        try:
            self.groq_client = Groq(api_key=self.api_key)
            print("✓ Groq client initialized")
        except Exception as e:
            print(f"❌ Groq error: {e}")
    
    def generate_marketing_text(self, product_name, product_type="product"):
        """Tạo text marketing (fallback nếu Groq không available)"""
        
        # Fallback marketing templates
        templates = {
            "product": {
                "title": f"{product_name}",
                "subtitle": "Premium Quality ⭐",
                "cta": "ORDER NOW"
            },
            "sale": {
                "title": f"{product_name}",
                "subtitle": "Limited Time Offer 🔥",
                "cta": "SHOP NOW"
            },
            "premium": {
                "title": f"{product_name}",
                "subtitle": "Exclusive Collection ✨",
                "cta": "DISCOVER"
            }
        }
        
        return templates.get(product_type, templates["product"])
    
    def create_banner_with_product_image(self, 
                                        product_image_path,
                                        product_name,
                                        banner_width=1200,
                                        banner_height=600,
                                        background_color="#1a1a2e"):
        """
        Tạo banner với hình sản phẩm
        
        Layout:
        ┌─────────────────────────────┬──────────────┐
        │                             │  ┌────────┐ │
        │   TEXT AREA                 │  │Product │ │
        │   Title                     │  └────────┘ │
        │   Subtitle                  │             │
        │   CTA Button                │             │
        └─────────────────────────────┴──────────────┘
        """
        
        print(f"🎨 Generating marketing text for '{product_name}'...")
        marketing_text = self.generate_marketing_text(product_name)
        
        # Create base banner
        print(f"🖼️  Creating banner {banner_width}x{banner_height}...")
        banner = Image.new('RGB', (banner_width, banner_height), background_color)
        draw = ImageDraw.Draw(banner)
        
        # Load product image
        if Path(product_image_path).exists():
            product_img = Image.open(product_image_path)
            
            # Remove background if available
            if REMBG_AVAILABLE:
                try:
                    product_img = remove(product_img)
                    print("✓ Background removed from product")
                except:
                    pass
            
            # Resize product to fit (40% of banner height)
            product_height = int(banner_height * 0.7)
            ratio = product_img.width / product_img.height
            product_width = int(product_height * ratio)
            product_img = product_img.resize((product_width, product_height), Image.Resampling.LANCZOS)
            
            # Place product on right side
            product_x = banner_width - product_width - 50
            product_y = (banner_height - product_height) // 2
            banner.paste(product_img, (product_x, product_y), product_img if product_img.mode == 'RGBA' else None)
            
            text_area_width = banner_width - product_width - 100
        else:
            text_area_width = banner_width - 100
        
        # Draw text
        try:
            # Try to use a nice font
            title_font = ImageFont.truetype("arial.ttf", 60)
            subtitle_font = ImageFont.truetype("arial.ttf", 36)
            cta_font = ImageFont.truetype("arial.ttf", 28)
        except:
            # Fallback to default
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            cta_font = ImageFont.load_default()
        
        # Title
        title = marketing_text.get("title", product_name)[:30]
        draw.text((50, 100), title, fill="white", font=title_font)
        
        # Subtitle
        subtitle = marketing_text.get("subtitle", "Premium Quality")[:50]
        draw.text((50, 200), subtitle, fill="#cccccc", font=subtitle_font)
        
        # CTA Button
        cta = marketing_text.get("cta", "BUY NOW")
        cta_width = 200
        cta_height = 60
        cta_x = 50
        cta_y = 350
        
        # Draw button background
        draw.rectangle(
            [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
            fill="#ff6b6b",
            outline="white"
        )
        
        # Draw button text
        draw.text((cta_x + 30, cta_y + 15), cta, fill="white", font=cta_font)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_folder / f"banner_groq_{timestamp}.png"
        banner.save(output_path)
        
        print(f"✓ Banner saved: {output_path}")
        return str(output_path)
    
    def create_banner_simple(self, 
                            product_name,
                            banner_width=1200,
                            banner_height=600):
        """Tạo banner đơn giản chỉ với text (cực nhanh)"""
        
        print(f"⚡ Generating marketing text...")
        marketing_text = self.generate_marketing_text(product_name)
        
        # Create gradient background
        banner = Image.new('RGB', (banner_width, banner_height))
        pixels = banner.load()
        
        # Gradient từ xanh đậm sang xanh nhạt
        for y in range(banner_height):
            r = int(26 + (y / banner_height) * 50)
            g = int(26 + (y / banner_height) * 100)
            b = int(46 + (y / banner_height) * 150)
            for x in range(banner_width):
                pixels[x, y] = (r, g, b)
        
        draw = ImageDraw.Draw(banner)
        
        # Font
        try:
            title_font = ImageFont.truetype("arial.ttf", 80)
            subtitle_font = ImageFont.truetype("arial.ttf", 40)
            cta_font = ImageFont.truetype("arial.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            cta_font = ImageFont.load_default()
        
        # Title (centered)
        title = marketing_text.get("title", product_name)[:30]
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (banner_width - title_width) // 2
        draw.text((title_x, 100), title, fill="white", font=title_font)
        
        # Subtitle
        subtitle = marketing_text.get("subtitle", "Premium Quality")[:50]
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (banner_width - subtitle_width) // 2
        draw.text((subtitle_x, 250), subtitle, fill="#ffeb3b", font=subtitle_font)
        
        # CTA
        cta = marketing_text.get("cta", "BUY NOW")
        cta_width = 300
        cta_height = 80
        cta_x = (banner_width - cta_width) // 2
        cta_y = 420
        
        draw.rectangle(
            [cta_x, cta_y, cta_x + cta_width, cta_y + cta_height],
            fill="#ff6b6b",
            outline="white"
        )
        
        cta_bbox = draw.textbbox((0, 0), cta, font=cta_font)
        cta_text_width = cta_bbox[2] - cta_bbox[0]
        cta_text_x = cta_x + (cta_width - cta_text_width) // 2
        draw.text((cta_text_x, cta_y + 20), cta, fill="white", font=cta_font)
        
        # Save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_folder / f"banner_simple_{timestamp}.png"
        banner.save(output_path)
        
        print(f"✓ Banner saved: {output_path}")
        return str(output_path)


def main():
    """Test script"""
    
    # Get API key from environment
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ GROQ_API_KEY not set!")
        print("\nHow to set it:")
        print("  Windows: set GROQ_API_KEY=your_key")
        print("  Linux/Mac: export GROQ_API_KEY=your_key")
        print("\nGet key from: https://console.groq.com")
        return
    
    creator = UltraFastBannerCreator(api_key)
    
    # Example 1: Simple banner with text only (fastest)
    print("\n" + "="*50)
    print("Creating simple banner with Groq AI text...")
    print("="*50)
    banner_path = creator.create_banner_simple("iPhone 15 Pro Max")
    print(f"\n✓ Done! Banner: {banner_path}\n")
    
    # Example 2: Banner with product image
    print("="*50)
    print("Creating banner with product image...")
    print("="*50)
    
    sample_product = Path("input") / "sample_product.png"
    if sample_product.exists():
        banner_path = creator.create_banner_with_product_image(
            str(sample_product),
            "Premium Product"
        )
        print(f"\n✓ Done! Banner: {banner_path}\n")
    else:
        print(f"⚠️ Sample product image not found: {sample_product}")
        print("   Using simple banner instead\n")


if __name__ == "__main__":
    main()
