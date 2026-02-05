#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Free AI Banner Creator - Advanced Mode with Inpainting
=======================================================
Sử dụng Stable Diffusion (Inpainting) + Groq API (Text Generation)

Quy trình:
1. User tải ảnh sản phẩm đã tách nền
2. Ghép sản phẩm vào giữa khung hình
3. AI tạo nền (Inpainting) xung quanh sản phẩm
4. Groq API viết nội dung (tiêu đề, mô tả)
5. Kết quả: Banner hoàn chỉnh
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import threading
from datetime import datetime
import json
import numpy as np

from background_removal import BackgroundRemover
from layer_compositing import LayerCompositor

# Import AI libraries
try:
    from diffusers import StableDiffusionInpaintPipeline, StableDiffusionControlNetPipeline, ControlNetModel
    import torch
    HAS_INPAINTING = True
except:
    HAS_INPAINTING = False

try:
    from groq import Groq
    HAS_GROQ = True
except:
    HAS_GROQ = False


class FreeAIBannerCreator:
    """Banner creator với Inpainting + Groq API"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 AI Banner Creator (Inpainting + Groq)")
        self.root.geometry("1300x950")
        self.root.configure(bg="#0f1419")
        
        # Data
        self.image_path = None
        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)
        
        # AI Models
        self.inpaint_pipeline = None
        self.groq_client = None
        
        # Config
        self.groq_api_key = None
        self.product_width_percent = 0.35  # Sản phẩm chiếm 35% chiều rộng
        
        # UI Variables
        self.use_inpaint = tk.BooleanVar(value=True)
        self.use_groq = tk.BooleanVar(value=False)
        self.inpaint_prompt = tk.StringVar(value="Professional product backdrop, modern lighting, studio quality")
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        self.create_header()
        
        content = tk.Frame(self.root, bg="#0f1419")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create tabs
        notebook = ttk.Notebook(content)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Simple Mode
        tab1 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab1, text="🚀 Quick Mode")
        self.setup_quick_mode(tab1)
        
        # Tab 2: AI Models
        tab2 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab2, text="🤖 Load Models")
        self.setup_models_tab(tab2)
        
        # Tab 3: Info
        tab3 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab3, text="ℹ️ Info & Setup")
        self.setup_info_tab(tab3)
    
    def create_header(self):
        """Create header"""
        header = tk.Frame(self.root, bg="#1a1f2e", height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        inner = tk.Frame(header, bg="#667eea")
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        tk.Label(
            inner,
            text="🎨 AI Banner Creator (Inpainting + Groq)",
            font=("Segoe UI", 24, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(pady=15)
        
        status = f"Inpainting: {'✓' if HAS_INPAINTING else '✗'} | Groq: {'✓' if HAS_GROQ else '✗'}"
        tk.Label(
            inner,
            text=status,
            font=("Segoe UI", 9),
            bg="#667eea",
            fg="#e0e0e0"
        ).pack()
    
    def setup_quick_mode(self, parent):
        """Inpainting mode - Product + AI Background"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Input
        left = tk.Frame(content, bg="#1a1f2e", width=350)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))
        left.pack_propagate(False)
        
        # Section 1: Product Image
        tk.Label(left, text="📸 PRODUCT IMAGE", font=("Segoe UI", 12, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W)
        tk.Button(
            left,
            text="Select Image (PNG with transparent bg)",
            command=self.select_image,
            bg="#667eea",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(10, 10))
        
        self.image_label = tk.Label(left, text="Not selected", fg="#888", bg="#1a1f2e", wraplength=300)
        self.image_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Section 2: Groq Text Generation
        tk.Label(left, text="📝 TEXT GENERATION (Groq)", font=("Segoe UI", 11, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W, pady=(10, 5))
        
        tk.Checkbutton(
            left,
            text="Use Groq API for title",
            variable=self.use_groq,
            bg="#1a1f2e",
            fg="#ddd",
            activebackground="#1a1f2e",
            activeforeground="#667eea",
            selectcolor="#1a1f2e",
            highlightthickness=0
        ).pack(anchor=tk.W, pady=3)
        
        tk.Label(left, text="Product Name", font=("Segoe UI", 10, "bold"), bg="#1a1f2e", fg="#aaa").pack(anchor=tk.W, pady=(10, 3))
        self.product_name_input = tk.Entry(left, font=("Segoe UI", 9), bg="#252d3d", fg="white", relief=tk.FLAT)
        self.product_name_input.insert(0, "Premium Sneakers")
        self.product_name_input.pack(fill=tk.X, pady=(0, 8), ipady=6)
        
        tk.Label(left, text="Prompt for Groq", font=("Segoe UI", 10), bg="#1a1f2e", fg="#aaa").pack(anchor=tk.W, pady=(5, 3))
        self.groq_prompt_input = tk.Entry(left, font=("Segoe UI", 9), bg="#252d3d", fg="white", relief=tk.FLAT)
        self.groq_prompt_input.insert(0, "Create marketing slogan for a trendy shoe")
        self.groq_prompt_input.pack(fill=tk.X, pady=(0, 15), ipady=6)
        
        # Section 3: Inpainting Settings
        tk.Label(left, text="🎨 INPAINTING SETTINGS", font=("Segoe UI", 11, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W, pady=(5, 5))
        
        tk.Checkbutton(
            left,
            text="Use Inpainting for background",
            variable=self.use_inpaint,
            bg="#1a1f2e",
            fg="#ddd",
            activebackground="#1a1f2e",
            activeforeground="#667eea",
            selectcolor="#1a1f2e",
            highlightthickness=0
        ).pack(anchor=tk.W, pady=3)
        
        tk.Label(left, text="Background Prompt", font=("Segoe UI", 9), bg="#1a1f2e", fg="#aaa").pack(anchor=tk.W, pady=(8, 3))
        self.inpaint_prompt_input = tk.Entry(left, font=("Segoe UI", 9), bg="#252d3d", fg="white", relief=tk.FLAT)
        self.inpaint_prompt_input.insert(0, "Professional studio backdrop, modern lighting, minimalist aesthetic")
        self.inpaint_prompt_input.pack(fill=tk.X, pady=(0, 15), ipady=6)
        
        # API Key (if Groq needed)
        tk.Label(left, text="Groq API Key (Optional)", font=("Segoe UI", 9), bg="#1a1f2e", fg="#aaa").pack(anchor=tk.W, pady=(5, 3))
        self.groq_key_input = tk.Entry(left, font=("Segoe UI", 9), bg="#252d3d", fg="white", relief=tk.FLAT, show="*")
        self.groq_key_input.pack(fill=tk.X, pady=(0, 15), ipady=6)
        
        # Create button
        tk.Button(
            left,
            text="⚡ CREATE BANNER",
            command=self.create_advanced_banner,
            bg="#ff6b6b",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(20, 10))
        
        self.status_label = tk.Label(left, text="Ready", fg="#667eea", bg="#1a1f2e", wraplength=300, justify=tk.LEFT)
        self.status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Right side - Preview
        right = tk.Frame(content, bg="#252d3d")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="👁️ PREVIEW", font=("Segoe UI", 11, "bold"), bg="#252d3d", fg="#667eea").pack(anchor=tk.W, padx=15, pady=15)
        
        self.preview_label = tk.Label(right, text="Banner will show here", fg="#555", bg="#1a1f2e")
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def setup_models_tab(self, parent):
        """Setup AI models"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Info
        info_text = """🤖 SETUP GUIDE - Inpainting + Groq

ARCHITECTURE:
1. Stable Diffusion Inpainting (~7GB)
   - Giữ nguyên sản phẩm, vẽ nền xung quanh
   - Speed: 30-60s per image
   - GPU: NVIDIA RTX 3060+

2. Groq API (Free Tier Available)
   - Text generation cho tiêu đề/mô tả
   - Speed: Real-time
   - No GPU needed

SETUP STEPS:

1️⃣ Install PyTorch (GPU):
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

2️⃣ Install Diffusers:
   pip install diffusers transformers accelerate opencv-python

3️⃣ Setup Groq (Optional):
   pip install groq
   • Get API key from: https://console.groq.com
   • Free tier: 30 requests/min

4️⃣ Download Inpainting Model:
   Click "Download Inpainting" button (first time: 10-30 mins)

WORKFLOW:
┌─────────────┬──────────────┬──────────────┐
│   Product   │ Inpainting   │     Text     │
│   (PNG)     │ (AI Nền)     │   (Groq)     │
└─────────────┴──────────────┴──────────────┘
         ↓
    ✓ Final Banner

REQUIREMENTS:
• GPU: RTX 3060 12GB (min)
• RAM: 16GB
• Disk: 20GB (models)

COST:
• One-time: GPU or cloud credit
• Per banner: ~0.0001$ (electricity)
• Groq API: FREE for first 10k requests/month"""
        
        text_widget = tk.Text(
            content,
            font=("Courier", 9),
            bg="#252d3d",
            fg="#aaa",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=25
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 20), ipady=10)
        text_widget.insert(1.0, info_text)
        text_widget.config(state=tk.DISABLED)
        
        # Model load buttons
        button_frame = tk.Frame(content, bg="#1a1f2e")
        button_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(
            button_frame,
            text="📥 Download Inpainting Model",
            command=self.download_inpainting,
            bg="#667eea",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=5)
    
    def download_inpainting(self):
        """Download Inpainting Model"""
        if not HAS_INPAINTING:
            messagebox.showwarning("Warning", "Install diffusers first:\npip install diffusers transformers")
            return
        
        messagebox.showinfo("Info", 
            "Downloading Inpainting Model (~7GB)...\n\n"
            "This may take 10-30 minutes.\n"
            "You need GPU with 12GB+ VRAM.\n\n"
            "Model will be saved in: ~/.cache/huggingface/")
        
        thread = threading.Thread(target=self._load_inpainting)
        thread.daemon = True
        thread.start()
    
    def setup_info_tab(self, parent):
        """Info and setup guide"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        info_text = """📖 ADVANCED WORKFLOW - Inpainting + Groq

═══════════════════════════════════════════════

Qgains HỮU THỰC TẾ:

1. User Upload → PNG (Transparent Background)
   ✓ Sản phẩm đã tách nền sạch
   ✓ Kích thước tùy ý

2. Vị Trí Sản Phẩm → Xác Định Tọa Độ
   • Lớp 2 (Middle): Sản phẩm (giữa khung)
   • Thường: 35% chiều rộng, căn giữa

3. Tạo Inpainting Mask → AI Tô Nền
   • Mask = Vùng cần vẽ (không phải sản phẩm)
   • Prompt: "Chuyên nghiệp backdrop, ánh sáng..."
   • Result: Nền hoàn toàn mới

4. Groq → Text Generation
   • Input: Tên sản phẩm
   • Prompt: "Tạo slogan marketing"
   • Output: Tiêu đề, mô tả

5. Compose Cuối Cùng
   • Layer 1: Nền (Inpainting)
   • Layer 2: Sản phẩm (gốc)
   • Layer 3: Text (Groq)

═══════════════════════════════════════════════

LỢI ÍCH:

✓ Sản phẩm KHÔNG BỊ MÉO MÓ (dùng gốc)
✓ Nền hoàn toàn do AI tạo (Inpainting)
✓ Text thông minh (Groq)
✓ Tự động hóa 100%
✓ Miễn phí (nếu có GPU)

═══════════════════════════════════════════════

YÊUWẦU PHẦN CỨNG:

GPU: NVIDIA RTX 3060 12GB (minimum)
RAM: 16GB
Disk: 20GB (models)

═══════════════════════════════════════════════

LỖI THƯỜNG GẶP:

❌ "CUDA out of memory"
   → Giảm batch size hoặc dùng CPU

❌ "Inpainting mask lỗi"
   → Kiểm tra PNG format (RGBA)

❌ "Groq timeout"
   → Check internet, rate limit

═══════════════════════════════════════════════"""
        
        text_widget = scrolledtext.ScrolledText(
            content,
            font=("Courier", 9),
            bg="#252d3d",
            fg="#aaa",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=30
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=0, pady=0, ipady=10)
        text_widget.insert(1.0, info_text)
        text_widget.config(state=tk.DISABLED)
    
    def select_image(self):
        """Select image"""
        file_path = filedialog.askopenfilename(
            title="Select product image",
            filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All", "*.*")]
        )
        
        if file_path:
            self.image_label.config(text="🔄 Removing background...", fg="#ff9800")
            self.root.update()
            
            try:
                # Load image
                from PIL import Image
                img = Image.open(file_path).convert("RGBA")
                
                # Auto remove background
                try:
                    from rembg import remove
                    print("Removing background...")
                    img = remove(img)
                    print("Background removed!")
                except Exception as e:
                    print(f"Background removal failed: {e}, using original")
                
                # Save temp file with removed background (force PNG format)
                temp_filename = f"temp_no_bg_{Path(file_path).stem}.png"
                temp_path = Path(file_path).parent / temp_filename
                img.save(temp_path, "PNG")
                
                self.image_path = str(temp_path)
                filename = Path(file_path).name
                self.image_label.config(text=f"✓ {filename} (bg removed)", fg="#4caf50")
                self.status_label.config(text="Image selected & background removed!", fg="#4caf50")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process image:\n{str(e)}")
                self.image_label.config(text="Error loading image", fg="#ff5252")
    
    def create_simple_banner(self):
        """Create advanced banner with inpainting"""
        if not self.image_path:
            messagebox.showwarning("Warning", "Select image first!")
            return
        
        product_name = self.product_name_input.get().strip()
        if not product_name:
            messagebox.showwarning("Warning", "Enter product name!")
            return
        
        self.status_label.config(text="⏳ Starting...", fg="#ff9800")
        self.root.update()
        
        thread = threading.Thread(target=self._create_advanced_banner_worker)
        thread.daemon = True
        thread.start()
    
    def create_advanced_banner(self):
        """Create advanced banner with inpainting"""
        if not self.image_path:
            messagebox.showwarning("⚠️ Warning", "Select image first!")
            return
        
        self.status_label.config(text="⏳ Starting workflow...", fg="#ff9800")
        self.root.update()
        
        thread = threading.Thread(target=self._create_advanced_banner_worker)
        thread.daemon = True
        thread.start()
    
    def _create_advanced_banner_worker(self):
        """Worker thread for banner creation"""
        try:
            product_name = self.product_name_input.get().strip()
            groq_prompt = self.groq_prompt_input.get().strip()
            inpaint_prompt = self.inpaint_prompt_input.get().strip()
            groq_key = self.groq_key_input.get().strip()
            
            # Step 1: Load and prepare product image
            self.status_label.config(text="📸 Loading product image...", fg="#ff9800")
            self.root.update()
            
            product_img = Image.open(self.image_path).convert("RGBA")
            
            # Ensure product has transparent background
            if product_img.mode != "RGBA":
                product_img = product_img.convert("RGBA")
            
            # Step 2: Generate text using Groq if enabled
            generated_title = product_name
            if self.use_groq.get() and groq_key:
                self.status_label.config(text="🤖 Generating title with Groq...", fg="#ff9800")
                self.root.update()
                
                try:
                    from groq import Groq
                    client = Groq(api_key=groq_key)
                    
                    message = client.messages.create(
                        model="mixtral-8x7b-32768",
                        max_tokens=100,
                        messages=[
                            {"role": "user", "content": f"{groq_prompt}\nProduct: {product_name}"}
                        ]
                    )
                    
                    generated_title = message.content[0].text.strip()[:50]
                    # Ensure UTF-8 encoding
                    if isinstance(generated_title, bytes):
                        generated_title = generated_title.decode('utf-8')
                    else:
                        generated_title = str(generated_title).encode('utf-8', errors='replace').decode('utf-8')
                except Exception as e:
                    print(f"Groq error: {e}")
                    generated_title = product_name
            
            # Step 3: Create banner canvas
            banner_width, banner_height = 1200, 640
            
            # Step 4: Create mask for inpainting
            if self.use_inpaint.get():
                self.status_label.config(text="🎨 Preparing inpainting mask...", fg="#ff9800")
                self.root.update()
                
                # Resize product to fit
                max_product_width = int(banner_width * self.product_width_percent)
                product_img.thumbnail((max_product_width, banner_height - 100), Image.Resampling.LANCZOS)
                
                # Create mask (where AI will paint)
                mask = Image.new("L", (banner_width, banner_height), 255)
                product_x = (banner_width - product_img.width) // 2
                product_y = (banner_height - product_img.height) // 2
                
                # Black region = keep, white = paint
                mask_draw = Image.new("L", (banner_width, banner_height), 255)
                mask_draw.paste(0, (product_x - 20, product_y - 20, 
                                     product_x + product_img.width + 20,
                                     product_y + product_img.height + 20))
                
                # Step 5: Run inpainting
                self.status_label.config(text="✨ Generating background with AI...", fg="#ff9800")
                self.root.update()
                
                if HAS_INPAINTING and self.inpaint_pipeline:
                    self._run_inpainting(banner_width, banner_height, mask_draw, inpaint_prompt, product_img, product_x, product_y, generated_title)
                else:
                    self._create_fallback_banner(banner_width, banner_height, product_img, product_x, product_y, generated_title)
            else:
                self._create_fallback_banner(banner_width, banner_height, product_img, (banner_width - product_img.width) // 2, (banner_height - product_img.height) // 2, generated_title)
            
            self.status_label.config(text="✓ Done!", fg="#4caf50")
            messagebox.showinfo("✓ Success", "Banner created successfully!")
            
        except Exception as e:
            self.status_label.config(text=f"✗ Error!", fg="#ff5252")
            messagebox.showerror("Error", str(e))
    
    def _run_inpainting(self, width, height, mask, prompt, product_img, prod_x, prod_y, title):
        """Run inpainting pipeline"""
        try:
            if not self.inpaint_pipeline:
                raise Exception("Inpainting model not loaded. Click 'Download Inpainting' first.")
            
            # Create initial image (white canvas)
            init_img = Image.new("RGB", (width, height), "white")
            
            # Convert mask to PIL format
            mask_pil = mask.convert("L")
            
            # Run inpainting
            with torch.no_grad():
                result = self.inpaint_pipeline(
                    prompt=prompt,
                    image=init_img,
                    mask_image=mask_pil,
                    num_inference_steps=50,
                    guidance_scale=7.5,
                    height=height,
                    width=width
                ).images[0]
            
            # Composite: Background + Product + Text
            result = result.convert("RGBA")
            result.paste(product_img, (prod_x, prod_y), product_img)
            
            # Add title
            draw = ImageDraw.Draw(result)
            try:
                font = ImageFont.truetype("fonts/arial.ttf" if Path("fonts/arial.ttf").exists() else "", 72)
            except:
                font = ImageFont.load_default()
            
            # Draw title
            title_bbox = draw.textbbox((0, 0), title, font=font)
            title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
            title_y = 50
            draw.text((title_x, title_y), title, font=font, fill=(255, 255, 255))
            
            # Save
            output_path = self.output_folder / f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            result.convert("RGB").save(output_path)
            
            # Preview
            preview_img = Image.open(output_path)
            preview_img.thumbnail((700, 370), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(preview_img)
            
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo
            
        except Exception as e:
            raise Exception(f"Inpainting error: {str(e)}")
    
    def _create_fallback_banner(self, width, height, product_img, prod_x, prod_y, title):
        """Create simple banner without inpainting"""
        # Create gradient background
        bg = Image.new("RGB", (width, height), (100, 150, 200))
        pixels = bg.load()
        
        for y in range(height):
            r = int(100 + (80 * y / height))
            g = int(150 + (60 * y / height))
            b = int(200 - (100 * y / height))
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        bg = bg.convert("RGBA")
        bg.paste(product_img, (prod_x, prod_y), product_img)
        
        # Add text
        draw = ImageDraw.Draw(bg)
        try:
            font = ImageFont.truetype("", 72)
        except:
            font = ImageFont.load_default()
        
        title_bbox = draw.textbbox((0, 0), title, font=font)
        title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
        title_y = 50
        draw.text((title_x, title_y), title, font=font, fill=(255, 255, 255))
        
        # Save
        output_path = self.output_folder / f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        bg.convert("RGB").save(output_path)
        
        # Preview
        preview_img = Image.open(output_path)
        preview_img.thumbnail((700, 370), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(preview_img)
        
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo
    
    def download_stable_diffusion(self):
        """Download Stable Diffusion model"""
        if not HAS_INPAINTING:
            messagebox.showwarning("Warning", "Install diffusers first:\npip install diffusers transformers")
            return
        
        messagebox.showinfo("Info", 
            "Downloading Inpainting Model (~7GB)...\n\n"
            "This may take 10-30 minutes.\n"
            "You need GPU with 12GB+ VRAM.\n\n"
            "Model will be saved in: ~/.cache/huggingface/")
        
        thread = threading.Thread(target=self._load_inpainting)
        thread.daemon = True
        thread.start()
    
    def _load_inpainting(self):
        """Load inpainting model"""
        try:
            from diffusers import StableDiffusionInpaintPipeline
            import torch
            
            print("Loading Stable Diffusion Inpainting...")
            self.status_label.config(text="📥 Loading inpainting model...", fg="#ff9800")
            self.root.update()
            
            # Use CPU with float32 safe loading
            device = "cpu"
            dtype = torch.float32
            
            pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                torch_dtype=dtype,
                safety_checker=None,
                load_connected_pipe=False
            )
            pipe = pipe.to(device)
            pipe.enable_attention_slicing()  # Reduce memory usage
            self.inpaint_pipeline = pipe
            
            self.status_label.config(text="✓ Model loaded!", fg="#4caf50")
            messagebox.showinfo("✓ Success", "Inpainting model loaded!\nYou can now use it to generate backgrounds.")
        except Exception as e:
            self.status_label.config(text="⚠ Fallback mode (gradient)", fg="#ff9800")
            messagebox.showwarning("Warning", f"Could not load inpainting model.\nUsing fallback gradient mode.\n\nError: {str(e)[:100]}")
            self.inpaint_pipeline = None
    
    def download_mistral(self):
        """Not used in new workflow"""
        messagebox.showinfo("Info", "Use Groq API instead!\nIt's faster and doesn't need GPU.\n\nGet API key: https://console.groq.com")


if __name__ == "__main__":
    root = tk.Tk()
    app = FreeAIBannerCreator(root)
    root.mainloop()
