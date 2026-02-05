"""
Modern Banner Creator GUI
========================
Giao diện hiện đại với thiết kế tương tự ứng dụng cao cấp
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import threading
from datetime import datetime

from background_removal import BackgroundRemover
from layer_compositing import LayerCompositor


class ModernBannerCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Banner Creator Pro")
        self.root.geometry("1000x800")
        self.root.configure(bg="#0f1419")
        
        # Data
        self.image_path = None
        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)
        self.last_banner_path = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup modern user interface"""
        
        # Main container
        main_container = tk.Frame(self.root, bg="#0f1419")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header with gradient effect
        self.create_header(main_container)
        
        # Content area - split into left and right
        content_area = tk.Frame(main_container, bg="#0f1419")
        content_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Controls
        self.create_left_panel(content_area)
        
        # Right panel - Preview
        self.create_right_panel(content_area)
    
    def create_header(self, parent):
        """Create modern header"""
        header = tk.Frame(parent, bg="#1a1f2e", height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Gradient-like effect using frame colors
        inner_header = tk.Frame(header, bg="#667eea")
        inner_header.pack(fill=tk.X, padx=1, pady=1)
        inner_header.pack_propagate(False)
        inner_header.config(height=98)
        
        title_frame = tk.Frame(inner_header, bg="#667eea")
        title_frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(
            title_frame,
            text="✨ Banner Creator Pro",
            font=("Segoe UI", 28, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=20)
        
        subtitle = tk.Label(
            title_frame,
            text="Tạo banner chuyên nghiệp trong vài giây",
            font=("Segoe UI", 10),
            bg="#667eea",
            fg="#e0e0e0"
        )
        subtitle.pack()
    
    def create_left_panel(self, parent):
        """Create left control panel"""
        left_panel = tk.Frame(parent, bg="#1a1f2e", relief=tk.FLAT, bd=0)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))
        
        # Scrollable area
        canvas = tk.Canvas(left_panel, bg="#1a1f2e", highlightthickness=0, bd=0)
        scrollbar = tk.Scrollbar(left_panel, orient=tk.VERTICAL, command=canvas.yview)
        content = tk.Frame(canvas, bg="#1a1f2e")
        
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ===== Section 1: Upload Image =====
        self.create_card(content, "📸 Chọn Ảnh Sản Phẩm", self.create_upload_section)
        
        # ===== Section 2: Text Input =====
        self.create_card(content, "✍️ Nhập Văn Bản", self.create_text_section)
        
        # ===== Section 3: Create Button =====
        self.create_card(content, "", self.create_button_section)
    
    def create_card(self, parent, title, content_creator):
        """Create modern card UI"""
        card = tk.Frame(parent, bg="#252d3d", relief=tk.FLAT, bd=0)
        card.pack(fill=tk.X, pady=12)
        
        # Add slight border effect
        border = tk.Frame(card, bg="#667eea", height=3)
        border.pack(fill=tk.X)
        
        # Card content
        inner = tk.Frame(card, bg="#252d3d")
        inner.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        if title:
            title_label = tk.Label(
                inner,
                text=title,
                font=("Segoe UI", 12, "bold"),
                bg="#252d3d",
                fg="#667eea"
            )
            title_label.pack(anchor=tk.W, pady=(0, 12))
        
        content_creator(inner)
    
    def create_upload_section(self, parent):
        """Create upload image section"""
        button = tk.Button(
            parent,
            text="🗂️  Chọn ảnh từ máy",
            command=self.select_image,
            bg="#667eea",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=12,
            cursor="hand2",
            activebackground="#764ba2",
            relief=tk.FLAT,
            bd=0
        )
        button.pack(fill=tk.X, pady=5)
        
        self.image_label = tk.Label(
            parent,
            text="Chưa chọn ảnh",
            font=("Segoe UI", 9),
            fg="#888",
            bg="#252d3d"
        )
        self.image_label.pack(anchor=tk.W, pady=8)
    
    def create_text_section(self, parent):
        """Create text input section"""
        self.text_input = tk.Entry(
            parent,
            font=("Segoe UI", 12),
            width=30,
            relief=tk.FLAT,
            bd=0,
            bg="#1a1f2e",
            fg="white",
            insertbackground="white",
            highlightthickness=1,
            highlightbackground="#667eea",
            highlightcolor="#667eea"
        )
        self.text_input.insert(0, "🔥 SIÊU SALE 50%")
        self.text_input.pack(fill=tk.X, pady=8, ipady=10)
    
    def create_button_section(self, parent):
        """Create main action button"""
        button = tk.Button(
            parent,
            text="⚡ TẠO BANNER NGAY",
            command=self.create_banner,
            bg="#ff6b6b",
            fg="white",
            font=("Segoe UI", 13, "bold"),
            padx=20,
            pady=16,
            cursor="hand2",
            activebackground="#ff5252",
            relief=tk.FLAT,
            bd=0
        )
        button.pack(fill=tk.X, pady=10)
        
        # Status
        self.status_label = tk.Label(
            parent,
            text="✓ Sẵn sàng",
            font=("Segoe UI", 9),
            fg="#4caf50",
            bg="#252d3d"
        )
        self.status_label.pack(anchor=tk.W, pady=8)
    
    def create_right_panel(self, parent):
        """Create right preview panel"""
        right_panel = tk.Frame(parent, bg="#252d3d", relief=tk.FLAT, bd=0)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            right_panel,
            text="👁️ Xem Trước Kết Quả",
            font=("Segoe UI", 12, "bold"),
            bg="#252d3d",
            fg="#667eea"
        )
        title.pack(anchor=tk.W, padx=15, pady=15)
        
        # Preview area
        preview_frame = tk.Frame(right_panel, bg="#1a1f2e", relief=tk.FLAT, bd=1)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.preview_label = tk.Label(
            preview_frame,
            text="Banner sẽ hiển thị ở đây",
            font=("Segoe UI", 11),
            fg="#555",
            bg="#1a1f2e"
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def select_image(self):
        """Select image file"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.webp"), ("All files", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            filename = Path(file_path).name
            self.image_label.config(text=f"✓ {filename}", fg="#4caf50")
            self.status_label.config(text="✓ Ảnh đã chọn", fg="#4caf50")
    
    def create_banner(self):
        """Create banner: remove background + add text"""
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước!")
            return
        
        text = self.text_input.get().strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập chữ!")
            return
        
        # Show processing status
        self.status_label.config(text="⏳ Đang xử lý...", fg="#ff9800")
        self.root.update()
        
        # Run in thread to prevent freezing
        thread = threading.Thread(target=self._process_banner, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _process_banner(self, text):
        """Process banner creation (run in thread)"""
        try:
            # Step 1: Remove background
            self.status_label.config(text="⏳ Đang tách nền...", fg="#ff9800")
            self.root.update()
            
            remover = BackgroundRemover()
            temp_no_bg = self.output_folder / f"temp_no_bg_{datetime.now().strftime('%H%M%S%f')}.png"
            remover.remove_background(self.image_path, str(temp_no_bg))
            
            # Step 2: Create banner with text
            self.status_label.config(text="⏳ Đang tạo banner...", fg="#ff9800")
            self.root.update()
            
            compositor = LayerCompositor(width=800, height=600)
            
            # Load product image (no background)
            product_img = Image.open(temp_no_bg).convert("RGBA")
            
            # Create background (blue gradient)
            bg_img = compositor.create_background(color_gradient=True)
            
            # Resize and center product on background
            product_img.thumbnail((600, 400), Image.Resampling.LANCZOS)
            bg_img = bg_img.convert("RGBA")
            
            # Calculate position to center product
            x = (bg_img.width - product_img.width) // 2
            y = (bg_img.height - product_img.height) // 3
            
            # Paste product
            bg_img.paste(product_img, (x, y), product_img)
            
            # Add text
            bg_img = self._add_text_to_image(bg_img, text)
            
            # Save result
            output_path = self.output_folder / f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            bg_img.convert("RGB").save(output_path)
            
            # Clean up temp file
            temp_no_bg.unlink()
            
            # Display preview
            self.last_banner_path = output_path
            self._show_preview(output_path)
            
            self.status_label.config(text="✓ Tạo banner thành công!", fg="#4caf50")
            messagebox.showinfo("✓ Thành công", f"Banner đã lưu:\n{output_path.name}\n\nTại: output/")
            
        except Exception as e:
            self.status_label.config(text=f"✗ Lỗi!", fg="#ff5252")
            messagebox.showerror("Lỗi", f"Lỗi tạo banner:\n{str(e)}")
    
    def _add_text_to_image(self, image, text):
        """Add text to image"""
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font (Windows)
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 60)
            except:
                font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center text horizontally, place near bottom
        x = (image.width - text_width) // 2
        y = image.height - text_height - 50
        
        # Draw text with yellow color and black outline
        outline_width = 3
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                draw.text((x + adj_x, y + adj_y), text, font=font, fill="black")
        
        draw.text((x, y), text, font=font, fill=(255, 255, 0))  # Yellow
        
        return image
    
    def _show_preview(self, image_path):
        """Display preview of created banner"""
        try:
            # Load image
            img = Image.open(image_path)
            
            # Resize for preview
            img.thumbnail((700, 450), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Update label
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            self.preview_label.config(text=f"Lỗi: {str(e)}", fg="#ff5252")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBannerCreator(root)
    root.mainloop()
