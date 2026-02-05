"""
AI-Powered Banner Creator with Automatic Design
================================================
Hệ thống banner tự động với AI:
- AI tạo nền từ text description
- AI đề xuất phong cách + màu sắc
- AI tạo slogan quảng cáo
- Tối ưu layout tự động
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import threading
from datetime import datetime
import json
import os

from background_removal import BackgroundRemover
from layer_compositing import LayerCompositor

# AI imports
try:
    import replicate
    HAS_REPLICATE = True
except ImportError:
    HAS_REPLICATE = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


class AIBannerCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Banner Creator Pro")
        self.root.geometry("1200x900")
        self.root.configure(bg="#0f1419")
        
        # Data
        self.image_path = None
        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)
        
        # Variables
        self.product_category = tk.StringVar(value="electronics")
        self.use_ai_background = tk.BooleanVar(value=False)
        self.use_ai_text = tk.BooleanVar(value=True)
        self.ai_background_prompt = tk.StringVar()
        
        # Load AI config
        self.load_ai_config()
        
        # Setup UI
        self.setup_ui()
    
    def load_ai_config(self):
        """Load AI configuration"""
        config_path = Path(__file__).parent / "ai_config.json"
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.ai_config = json.load(f)
        except:
            self.ai_config = {}
    
    def setup_ui(self):
        """Setup UI"""
        self.create_header()
        
        content = tk.Frame(self.root, bg="#0f1419")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tabs
        self.create_tabs(content)
    
    def create_header(self):
        """Create header"""
        header = tk.Frame(self.root, bg="#1a1f2e", height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        inner = tk.Frame(header, bg="#667eea")
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        tk.Label(
            inner,
            text="🤖 AI-Powered Banner Creator",
            font=("Segoe UI", 26, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(pady=15)
        
        status_text = f"AI Status: {self._get_ai_status()}"
        tk.Label(
            inner,
            text=status_text,
            font=("Segoe UI", 9),
            bg="#667eea",
            fg="#e0e0e0"
        ).pack()
    
    def _get_ai_status(self):
        """Get AI availability status"""
        status = []
        status.append("✓ Background Removal" if True else "✗ Background Removal")
        status.append("✓ Replicate" if HAS_REPLICATE else "✗ Replicate")
        status.append("✓ OpenAI" if HAS_OPENAI else "✗ OpenAI")
        return " | ".join(status)
    
    def create_tabs(self, parent):
        """Create tabbed interface"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background="#0f1419")
        style.configure('TNotebook.Tab', background="#252d3d", foreground="white")
        
        # Tab 1: Simple Mode
        tab1 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab1, text="🚀 Mode Nhanh")
        self.setup_simple_mode(tab1)
        
        # Tab 2: Advanced AI
        tab2 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab2, text="🤖 Chế độ AI")
        self.setup_ai_mode(tab2)
        
        # Tab 3: Batch Processing
        tab3 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab3, text="📦 Batch")
        self.setup_batch_mode(tab3)
        
        # Tab 4: AI Setup
        tab4 = tk.Frame(notebook, bg="#1a1f2e")
        notebook.add(tab4, text="⚙️ Cài đặt AI")
        self.setup_ai_setup_tab(tab4)
    
    def setup_simple_mode(self, parent):
        """Simple mode - traditional banner creation"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side
        left = tk.Frame(content, bg="#1a1f2e")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))
        
        tk.Label(left, text="📸 Sản phẩm", font=("Segoe UI", 12, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W)
        tk.Button(
            left,
            text="Chọn ảnh",
            command=self.select_image,
            bg="#667eea",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(10, 20))
        
        self.simple_image_label = tk.Label(left, text="Chưa chọn", fg="#888", bg="#1a1f2e")
        self.simple_image_label.pack(anchor=tk.W)
        
        # Text
        tk.Label(left, text="✍️ Tiêu đề", font=("Segoe UI", 11, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W, pady=(20, 5))
        self.simple_title = tk.Entry(left, font=("Segoe UI", 10), bg="#252d3d", fg="white", relief=tk.FLAT)
        self.simple_title.insert(0, "🔥 SIÊU SALE 50%")
        self.simple_title.pack(fill=tk.X, pady=5, ipady=8)
        
        # Create button
        tk.Button(
            left,
            text="⚡ TẠO BANNER",
            command=self.create_simple_banner,
            bg="#ff6b6b",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(30, 20))
        
        self.simple_status = tk.Label(left, text="Sẵn sàng", fg="#4caf50", bg="#1a1f2e")
        self.simple_status.pack(anchor=tk.W)
        
        # Right side - Preview
        right = tk.Frame(content, bg="#252d3d")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="👁️ Xem trước", font=("Segoe UI", 11, "bold"), bg="#252d3d", fg="#667eea").pack(anchor=tk.W, padx=15, pady=15)
        
        self.simple_preview = tk.Label(right, text="Banner sẽ hiển thị ở đây", fg="#555", bg="#1a1f2e")
        self.simple_preview.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def setup_ai_mode(self, parent):
        """AI mode - automatic design with AI"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left controls
        left = tk.Frame(content, bg="#1a1f2e")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))
        
        # Product category
        tk.Label(left, text="📦 Loại sản phẩm", font=("Segoe UI", 11, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W, pady=(0, 10))
        
        categories = [
            ("electronics", "🖥️ Điện tử"),
            ("fashion", "👗 Thời trang"),
            ("food", "🍔 Thực phẩm"),
            ("beauty", "💄 Làm đẹp"),
            ("sports", "⚽ Thể thao"),
            ("sale", "🔥 Sale/Khuyến mãi")
        ]
        
        for value, label in categories:
            tk.Radiobutton(
                left,
                text=label,
                variable=self.product_category,
                value=value,
                bg="#1a1f2e",
                fg="#ddd",
                activebackground="#1a1f2e",
                activeforeground="#667eea",
                selectcolor="#1a1f2e",
                highlightthickness=0
            ).pack(anchor=tk.W, pady=3)
        
        # AI Options
        tk.Label(left, text="🤖 Tùy chọn AI", font=("Segoe UI", 11, "bold"), bg="#1a1f2e", fg="#667eea").pack(anchor=tk.W, pady=(20, 10))
        
        tk.Checkbutton(
            left,
            text="Tạo nền AI (beta)",
            variable=self.use_ai_background,
            bg="#1a1f2e",
            fg="#ddd",
            activebackground="#1a1f2e",
            activeforeground="#667eea",
            selectcolor="#1a1f2e",
            highlightthickness=0
        ).pack(anchor=tk.W, pady=3)
        
        tk.Checkbutton(
            left,
            text="Tạo slogan AI",
            variable=self.use_ai_text,
            bg="#1a1f2e",
            fg="#ddd",
            activebackground="#1a1f2e",
            activeforeground="#667eea",
            selectcolor="#1a1f2e",
            highlightthickness=0
        ).pack(anchor=tk.W, pady=3)
        
        # AI Prompt
        tk.Label(left, text="📝 Mô tả nền", font=("Segoe UI", 10), bg="#1a1f2e", fg="#aaa").pack(anchor=tk.W, pady=(15, 5))
        self.ai_prompt = tk.Text(left, height=4, font=("Segoe UI", 9), bg="#252d3d", fg="white", relief=tk.FLAT)
        self.ai_prompt.insert(1.0, "modern tech background")
        self.ai_prompt.pack(fill=tk.BOTH, pady=5, ipady=8)
        
        # Create button
        tk.Button(
            left,
            text="🚀 TẠO BANNER AI",
            command=self.create_ai_banner,
            bg="#9775fa",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=12,
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(20, 10))
        
        self.ai_status = tk.Label(left, text="Sẵn sàng", fg="#4caf50", bg="#1a1f2e")
        self.ai_status.pack(anchor=tk.W)
        
        # Right - Preview & Info
        right = tk.Frame(content, bg="#252d3d")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="ℹ️ Thông tin AI", font=("Segoe UI", 11, "bold"), bg="#252d3d", fg="#667eea").pack(anchor=tk.W, padx=15, pady=15)
        
        info_text = """AI FEATURES AVAILABLE:
✓ Tách nền ảnh sản phẩm
✓ Tạo nền từ Stable Diffusion
✓ Tạo slogan thông minh
✓ Chọn phong cách tự động
✓ Tối ưu màu sắc

REQUIREMENTS:
• API keys từ Replicate
• hoặc OpenAI API key
• Internet connection

BETA FEATURES:
⏳ Phân tích ảnh sản phẩm
⏳ Text-to-Image enhancement
⏳ Auto color matching"""
        
        info_label = tk.Label(right, text=info_text, font=("Courier", 9), bg="#1a1f2e", fg="#aaa", justify=tk.LEFT)
        info_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def setup_batch_mode(self, parent):
        """Batch processing mode"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            content,
            text="📦 Batch Processing (Sắp có)",
            font=("Segoe UI", 14, "bold"),
            bg="#1a1f2e",
            fg="#667eea"
        ).pack(pady=20)
        
        info = """Tạo nhiều banner cùng lúc:
• Upload danh sách CSV với sản phẩm
• Tùy chỉnh mẫu cho mỗi sản phẩm
• Xuất batch tự động
• Báo cáo chi phí API

Sắp cập nhật..."""
        
        tk.Label(content, text=info, font=("Segoe UI", 10), bg="#1a1f2e", fg="#999", justify=tk.LEFT).pack(pady=10)
    
    def setup_ai_setup_tab(self, parent):
        """AI Setup configuration tab"""
        content = tk.Frame(parent, bg="#1a1f2e")
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get setup guide from AI_SETUP_GUIDE
        setup_text = """⚙️ HƯỚNG DẪN CẤU HÌNH AI

1. CÀI ĐẶT THƯ VIỆN:
   pip install replicate openai huggingface-hub

2. LẤY API KEYS:
   
   REPLICATE (khuyến nghị):
   - https://replicate.com/
   - Account → API Tokens
   
   OPENAI (cho text generation):
   - https://platform.openai.com/api-keys
   
3. CẤU HÌNH ENVIRONMENT:
   
   Windows (PowerShell):
   $env:REPLICATE_API_TOKEN = "your_token"
   $env:OPENAI_API_KEY = "your_key"
   
   Linux/Mac:
   export REPLICATE_API_TOKEN="your_token"
   export OPENAI_API_KEY="your_key"

4. TEST:
   Chạy test_ai_setup.py để kiểm tra

💰 CHI PHÍ ƯỚC TÍNH:
• Replicate: ~$0.01/ảnh
• OpenAI: ~$0.01/request
• Hugging Face: Miễn phí (offline)"""
        
        text_widget = tk.Text(
            content,
            font=("Courier", 9),
            bg="#252d3d",
            fg="#aaa",
            relief=tk.FLAT,
            wrap=tk.WORD,
            height=30
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(1.0, setup_text)
        text_widget.config(state=tk.DISABLED)
        
        # Button to show full guide
        tk.Button(
            content,
            text="📖 Xem Hướng Dẫn Chi Tiết (AI_SETUP_GUIDE.py)",
            command=self.show_full_guide,
            bg="#667eea",
            fg="white",
            padx=15,
            pady=10,
            relief=tk.FLAT
        ).pack(pady=10)
    
    def select_image(self):
        """Select product image"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif"), ("All", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            filename = Path(file_path).name
            self.simple_image_label.config(text=f"✓ {filename}", fg="#4caf50")
            self.simple_status.config(text="Ảnh đã chọn", fg="#4caf50")
    
    def create_simple_banner(self):
        """Create simple banner"""
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Chọn ảnh trước!")
            return
        
        title = self.simple_title.get().strip()
        if not title:
            messagebox.showwarning("Cảnh báo", "Nhập tiêu đề!")
            return
        
        self.simple_status.config(text="⏳ Xử lý...", fg="#ff9800")
        self.root.update()
        
        thread = threading.Thread(target=self._create_simple, args=(title,))
        thread.daemon = True
        thread.start()
    
    def _create_simple(self, title):
        """Process simple banner creation"""
        try:
            self.simple_status.config(text="⏳ Tách nền...", fg="#ff9800")
            self.root.update()
            
            remover = BackgroundRemover()
            temp_path = self.output_folder / f"temp_{datetime.now().strftime('%H%M%S%f')}.png"
            remover.remove_background(self.image_path, str(temp_path))
            
            # Create banner
            product_img = Image.open(temp_path).convert("RGBA")
            
            compositor = LayerCompositor(width=1000, height=600)
            bg_img = compositor.create_background(color_gradient=True)
            
            product_img.thumbnail((500, 350), Image.Resampling.LANCZOS)
            bg_img = bg_img.convert("RGBA")
            
            product_x = 50
            product_y = (bg_img.height - product_img.height) // 2
            bg_img.paste(product_img, (product_x, product_y), product_img)
            
            # Add text
            draw = ImageDraw.Draw(bg_img)
            try:
                font = ImageFont.truetype("arial.ttf", 72)
            except:
                font = ImageFont.load_default()
            
            title_bbox = draw.textbbox((0, 0), title, font=font)
            title_x = bg_img.width - (title_bbox[2] - title_bbox[0]) - 80
            title_y = (bg_img.height - (title_bbox[3] - title_bbox[1])) // 2
            
            draw.text((title_x, title_y), title, font=font, fill=(255, 255, 255))
            
            # Save
            output_path = self.output_folder / f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            bg_img.convert("RGB").save(output_path)
            
            temp_path.unlink()
            
            # Show preview
            img = Image.open(output_path)
            img.thumbnail((700, 420), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.simple_preview.config(image=photo, text="")
            self.simple_preview.image = photo
            
            self.simple_status.config(text="✓ Hoàn tất!", fg="#4caf50")
            messagebox.showinfo("✓", f"Banner: {output_path.name}")
            
        except Exception as e:
            self.simple_status.config(text="✗ Lỗi!", fg="#ff5252")
            messagebox.showerror("Lỗi", str(e))
    
    def create_ai_banner(self):
        """Create banner with AI"""
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Chọn ảnh trước!")
            return
        
        messagebox.showinfo("AI Banner", "Tính năng sắp ra mắt! Đang cài đặt các thư viện AI...")
    
    def show_full_guide(self):
        """Show full AI setup guide"""
        try:
            import subprocess
            import sys
            subprocess.Popen([sys.executable, "AI_SETUP_GUIDE.py"], cwd=Path(__file__).parent)
        except:
            messagebox.showinfo("Hướng dẫn", "Mở file AI_SETUP_GUIDE.py để xem hướng dẫn chi tiết")


if __name__ == "__main__":
    root = tk.Tk()
    app = AIBannerCreator(root)
    root.mainloop()
