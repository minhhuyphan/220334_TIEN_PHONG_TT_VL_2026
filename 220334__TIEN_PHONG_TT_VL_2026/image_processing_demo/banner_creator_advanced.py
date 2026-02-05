"""
Advanced Banner Creator with Professional Design
================================================
Sử dụng các nguyên tắc thiết kế hiện đại:
- Gradient tốt, color contrast
- Typography hợp lý
- Layout chuẩn chuyên nghiệp
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageFilter, ImageEnhance
from pathlib import Path
import threading
from datetime import datetime

from background_removal import BackgroundRemover
from layer_compositing import LayerCompositor


class AdvancedBannerCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Banner Creator Pro - Advanced Design")
        self.root.geometry("1000x800")
        self.root.configure(bg="#0f1419")
        
        # Data
        self.image_path = None
        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)
        self.last_banner_path = None
        
        # Design options
        self.design_style = tk.StringVar(value="modern_gradient")
        self.text_position = tk.StringVar(value="bottom")
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI with design options"""
        
        # Header
        self.create_header()
        
        # Content
        content_area = tk.Frame(self.root, bg="#0f1419")
        content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left - Controls
        self.create_left_panel(content_area)
        
        # Right - Preview
        self.create_right_panel(content_area)
    
    def create_header(self):
        """Create header"""
        header = tk.Frame(self.root, bg="#1a1f2e", height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        inner = tk.Frame(header, bg="#667eea")
        inner.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        tk.Label(
            inner,
            text="✨ Advanced Banner Creator Pro",
            font=("Segoe UI", 26, "bold"),
            bg="#667eea",
            fg="white"
        ).pack(pady=15)
        
        tk.Label(
            inner,
            text="Thiết kế banner chuyên nghiệp theo chuẩn thiết kế hiện đại",
            font=("Segoe UI", 9),
            bg="#667eea",
            fg="#e0e0e0"
        ).pack()
    
    def create_left_panel(self, parent):
        """Create left control panel"""
        left = tk.Frame(parent, bg="#1a1f2e")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))
        
        # Canvas with scrollbar
        canvas = tk.Canvas(left, bg="#1a1f2e", highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(left, orient=tk.VERTICAL, command=canvas.yview)
        content = tk.Frame(canvas, bg="#1a1f2e")
        
        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Section 1: Upload
        self.create_card(content, "📸 Chọn Ảnh", self._create_upload_section)
        
        # Section 2: Text
        self.create_card(content, "✍️ Văn Bản", self._create_text_section)
        
        # Section 3: Design Style
        self.create_card(content, "🎨 Phong Cách Thiết Kế", self._create_style_section)
        
        # Section 4: Create
        self.create_card(content, "", self._create_button_section)
    
    def create_card(self, parent, title, content_func):
        """Create card UI"""
        card = tk.Frame(parent, bg="#252d3d", relief=tk.FLAT, bd=0)
        card.pack(fill=tk.X, pady=12)
        
        border = tk.Frame(card, bg="#667eea", height=3)
        border.pack(fill=tk.X)
        
        inner = tk.Frame(card, bg="#252d3d")
        inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        if title:
            tk.Label(
                inner,
                text=title,
                font=("Segoe UI", 11, "bold"),
                bg="#252d3d",
                fg="#667eea"
            ).pack(anchor=tk.W, pady=(0, 10))
        
        content_func(inner)
    
    def _create_upload_section(self, parent):
        """Upload section"""
        tk.Button(
            parent,
            text="🗂️  Chọn ảnh sản phẩm",
            command=self.select_image,
            bg="#667eea",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=10,
            cursor="hand2",
            activebackground="#764ba2",
            relief=tk.FLAT,
            bd=0
        ).pack(fill=tk.X, pady=5)
        
        self.image_label = tk.Label(
            parent,
            text="Chưa chọn ảnh",
            font=("Segoe UI", 9),
            fg="#888",
            bg="#252d3d"
        )
        self.image_label.pack(anchor=tk.W, pady=8)
    
    def _create_text_section(self, parent):
        """Text section"""
        tk.Label(parent, text="Tiêu đề:", font=("Segoe UI", 9), bg="#252d3d", fg="#aaa").pack(anchor=tk.W, pady=(0, 3))
        self.text_title = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg="#1a1f2e",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#667eea",
            highlightcolor="#667eea"
        )
        self.text_title.insert(0, "🔥 SIÊU SALE 50%")
        self.text_title.pack(fill=tk.X, pady=(0, 10), ipady=8)
        
        tk.Label(parent, text="Phụ đề (tùy chọn):", font=("Segoe UI", 9), bg="#252d3d", fg="#aaa").pack(anchor=tk.W, pady=(0, 3))
        self.text_subtitle = tk.Entry(
            parent,
            font=("Segoe UI", 9),
            bg="#1a1f2e",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground="#667eea",
            highlightcolor="#667eea"
        )
        self.text_subtitle.insert(0, "Mua ngay để nhận quà")
        self.text_subtitle.pack(fill=tk.X, ipady=6)
    
    def _create_style_section(self, parent):
        """Design style options"""
        styles = [
            ("modern_gradient", "🎨 Modern Gradient (Xanh tím)"),
            ("sunset_gradient", "🌅 Sunset Gradient (Cam-Đỏ)"),
            ("ocean_gradient", "🌊 Ocean Gradient (Xanh biển)"),
            ("dark_premium", "⬛ Dark Premium (Đen-Gold)"),
        ]
        
        for value, label in styles:
            tk.Radiobutton(
                parent,
                text=label,
                variable=self.design_style,
                value=value,
                bg="#252d3d",
                fg="#ddd",
                activebackground="#252d3d",
                activeforeground="#667eea",
                selectcolor="#252d3d",
                highlightthickness=0
            ).pack(anchor=tk.W, pady=4)
        
        # Text position
        tk.Label(parent, text="Vị trí chữ:", font=("Segoe UI", 9), bg="#252d3d", fg="#aaa").pack(anchor=tk.W, pady=(10, 5))
        
        for value, label in [("top", "Trên cùng"), ("center", "Giữa"), ("bottom", "Dưới cùng")]:
            tk.Radiobutton(
                parent,
                text=label,
                variable=self.text_position,
                value=value,
                bg="#252d3d",
                fg="#ddd",
                activebackground="#252d3d",
                activeforeground="#667eea",
                selectcolor="#252d3d",
                highlightthickness=0
            ).pack(anchor=tk.W, pady=3)
    
    def _create_button_section(self, parent):
        """Create button"""
        tk.Button(
            parent,
            text="⚡ TẠO BANNER NGAY",
            command=self.create_banner,
            bg="#ff6b6b",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            padx=20,
            pady=14,
            cursor="hand2",
            activebackground="#ff5252",
            relief=tk.FLAT,
            bd=0
        ).pack(fill=tk.X, pady=8)
        
        self.status_label = tk.Label(
            parent,
            text="✓ Sẵn sàng",
            font=("Segoe UI", 9),
            fg="#4caf50",
            bg="#252d3d"
        )
        self.status_label.pack(anchor=tk.W, pady=8)
    
    def create_right_panel(self, parent):
        """Right preview panel"""
        right = tk.Frame(parent, bg="#252d3d")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            right,
            text="👁️ Xem Trước Kết Quả",
            font=("Segoe UI", 11, "bold"),
            bg="#252d3d",
            fg="#667eea"
        ).pack(anchor=tk.W, padx=15, pady=15)
        
        preview_frame = tk.Frame(right, bg="#1a1f2e", relief=tk.FLAT, bd=1)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.preview_label = tk.Label(
            preview_frame,
            text="Banner sẽ hiển thị ở đây",
            font=("Segoe UI", 10),
            fg="#555",
            bg="#1a1f2e"
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
    
    def select_image(self):
        """Select image"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.webp"), ("All", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            filename = Path(file_path).name
            self.image_label.config(text=f"✓ {filename}", fg="#4caf50")
            self.status_label.config(text="✓ Ảnh đã chọn", fg="#4caf50")
    
    def create_banner(self):
        """Create banner"""
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Chọn ảnh trước!")
            return
        
        title_text = self.text_title.get().strip()
        if not title_text:
            messagebox.showwarning("Cảnh báo", "Nhập tiêu đề!")
            return
        
        self.status_label.config(text="⏳ Đang xử lý...", fg="#ff9800")
        self.root.update()
        
        thread = threading.Thread(target=self._process, args=(title_text,))
        thread.daemon = True
        thread.start()
    
    def _process(self, title_text):
        """Process banner"""
        try:
            self.status_label.config(text="⏳ Tách nền...", fg="#ff9800")
            self.root.update()
            
            remover = BackgroundRemover()
            temp_path = self.output_folder / f"temp_{datetime.now().strftime('%H%M%S%f')}.png"
            remover.remove_background(self.image_path, str(temp_path))
            
            self.status_label.config(text="⏳ Tạo banner...", fg="#ff9800")
            self.root.update()
            
            # Create banner
            product_img = Image.open(temp_path).convert("RGBA")
            bg_img = self._create_background_with_style()
            
            # Resize product
            product_img.thumbnail((500, 350), Image.Resampling.LANCZOS)
            bg_img = bg_img.convert("RGBA")
            
            # Position product
            product_x = 50
            product_y = (bg_img.height - product_img.height) // 2
            bg_img.paste(product_img, (product_x, product_y), product_img)
            
            # Add text
            subtitle = self.text_subtitle.get().strip()
            bg_img = self._add_professional_text(bg_img, title_text, subtitle)
            
            # Save
            output_path = self.output_folder / f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            bg_img.convert("RGB").save(output_path)
            
            temp_path.unlink()
            
            self._show_preview(output_path)
            self.status_label.config(text="✓ Hoàn tất!", fg="#4caf50")
            messagebox.showinfo("✓ Thành công", f"Banner: {output_path.name}\nLưu tại: output/")
            
        except Exception as e:
            self.status_label.config(text="✗ Lỗi!", fg="#ff5252")
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")
    
    def _create_background_with_style(self):
        """Create background based on style"""
        width, height = 1000, 600
        style = self.design_style.get()
        
        if style == "modern_gradient":
            return self._gradient_background(width, height, (102, 126, 234), (118, 75, 162))
        elif style == "sunset_gradient":
            return self._gradient_background(width, height, (255, 154, 77), (255, 87, 34))
        elif style == "ocean_gradient":
            return self._gradient_background(width, height, (26, 188, 156), (52, 211, 153))
        elif style == "dark_premium":
            return self._gradient_background(width, height, (33, 33, 33), (76, 175, 80))
        
        return self._gradient_background(width, height, (102, 126, 234), (118, 75, 162))
    
    def _gradient_background(self, width, height, color1, color2):
        """Create gradient background"""
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            for x in range(width):
                pixels[x, y] = (r, g, b)
        
        return img
    
    def _add_professional_text(self, image, title, subtitle):
        """Add professional text"""
        draw = ImageDraw.Draw(image)
        
        # Get position
        text_pos = self.text_position.get()
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 72)
            font_subtitle = ImageFont.truetype("arial.ttf", 32)
        except:
            try:
                font_title = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 72)
                font_subtitle = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 32)
            except:
                font_title = font_subtitle = ImageFont.load_default()
        
        # Calculate positions
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = image.width - title_width - 80
        
        if text_pos == "top":
            title_y = 50
        elif text_pos == "center":
            title_y = (image.height - (title_bbox[3] - title_bbox[1])) // 2
        else:  # bottom
            title_y = image.height - 150
        
        # Draw title with shadow
        for offset in range(3, 0, -1):
            alpha = 50
            shadow = Image.new('RGBA', image.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow)
            shadow_draw.text((title_x + offset, title_y + offset), title, font=font_title, fill=(0, 0, 0, alpha))
            image = Image.alpha_composite(image.convert('RGBA'), shadow).convert('RGB')
        
        # Draw title
        draw = ImageDraw.Draw(image)
        draw.text((title_x, title_y), title, font=font_title, fill=(255, 255, 255))
        
        # Draw subtitle
        if subtitle:
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = image.width - subtitle_width - 80
            subtitle_y = title_y + (title_bbox[3] - title_bbox[1]) + 20
            
            draw.text((subtitle_x, subtitle_y), subtitle, font=font_subtitle, fill=(255, 200, 0))
        
        return image
    
    def _show_preview(self, path):
        """Show preview"""
        try:
            img = Image.open(path)
            img.thumbnail((700, 420), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            self.preview_label.config(text=f"Lỗi: {str(e)}", fg="#ff5252")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedBannerCreator(root)
    root.mainloop()
