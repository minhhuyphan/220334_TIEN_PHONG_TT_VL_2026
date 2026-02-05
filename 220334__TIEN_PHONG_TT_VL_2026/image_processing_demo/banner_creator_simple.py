"""
Simple Banner Creator GUI
========================
Giao diện đơn giản:
- Nút chọn ảnh
- Ô nhập chữ
- Nút tạo banner

Khi nhấn "Tạo Banner": tự động tách nền ảnh + thêm chữ + tạo banner
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import threading
from datetime import datetime

from background_removal import BackgroundRemover
from layer_compositing import LayerCompositor


class SimpleBannerCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Tạo Banner Đơn Giản")
        self.root.geometry("800x900")
        self.root.configure(bg="#f5f5f5")
        
        # Data
        self.image_path = None
        self.output_folder = Path("output")
        self.output_folder.mkdir(exist_ok=True)
        self.last_banner_path = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        
        # Header
        header = tk.Frame(self.root, bg="#667eea", height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🎨 Tạo Banner Nhanh",
            font=("Segoe UI", 20, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=10)
        
        # Main content with scrollbar
        main_frame = tk.Frame(self.root, bg="white", relief=tk.RAISED, bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create scrollable canvas
        canvas = tk.Canvas(main_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        content = tk.Frame(canvas, bg="white")
        
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Section 1: Chọn ảnh
        tk.Label(
            content,
            text="📸 Chọn ảnh",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(10, 5))
        
        button_frame1 = tk.Frame(content, bg="white")
        button_frame1.pack(fill=tk.X, pady=10)
        
        tk.Button(
            button_frame1,
            text="📁 Chọn ảnh từ máy",
            command=self.select_image,
            bg="#667eea",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#764ba2",
            width=25
        ).pack(side=tk.LEFT, padx=5)
        
        self.image_label = tk.Label(
            button_frame1,
            text="Chưa chọn ảnh",
            font=("Segoe UI", 10),
            fg="#999",
            bg="white"
        )
        self.image_label.pack(side=tk.LEFT, padx=10)
        
        # Section 2: Nhập chữ
        tk.Label(
            content,
            text="✍️ Nhập chữ",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(20, 5))
        
        self.text_input = tk.Entry(
            content,
            font=("Segoe UI", 14),
            width=40,
            relief=tk.FLAT,
            bd=2,
            bg="#f9f9f9"
        )
        self.text_input.insert(0, "🔥 SIÊU SALE 50%")
        self.text_input.pack(fill=tk.X, pady=10)
        
        # Section 3: Tạo banner button
        tk.Button(
            content,
            text="✨ TẠO BANNER",
            command=self.create_banner,
            bg="#ff6b6b",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            padx=30,
            pady=15,
            cursor="hand2",
            activebackground="#ff5252",
            width=30
        ).pack(pady=30)
        
        # Status
        self.status_label = tk.Label(
            content,
            text="Sẵn sàng ✓",
            font=("Segoe UI", 10),
            fg="green",
            bg="white"
        )
        self.status_label.pack(pady=10)
        
        # Section 4: Preview banner result
        tk.Label(
            content,
            text="👁️ Kết quả Banner",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(anchor=tk.W, pady=(20, 10))
        
        # Preview frame
        preview_frame = tk.Frame(content, bg="#f9f9f9", relief=tk.SUNKEN, bd=2)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = tk.Label(
            preview_frame,
            text="(Banner sẽ hiển thị ở đây)",
            font=("Segoe UI", 10),
            fg="#ccc",
            bg="#f9f9f9",
            height=15
        )
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def select_image(self):
        """Select image file"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif *.webp"), ("All files", "*.*")]
        )
        
        if file_path:
            self.image_path = file_path
            filename = Path(file_path).name
            self.image_label.config(text=f"✓ {filename}", fg="green")
            self.status_label.config(text="Ảnh đã chọn", fg="green")
    
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
        self.status_label.config(text="⏳ Đang xử lý...", fg="orange")
        self.root.update()
        
        # Run in thread to prevent freezing
        thread = threading.Thread(target=self._process_banner, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _process_banner(self, text):
        """Process banner creation (run in thread)"""
        try:
            # Step 1: Remove background
            self.status_label.config(text="⏳ Đang tách nền...", fg="orange")
            self.root.update()
            
            remover = BackgroundRemover()
            temp_no_bg = self.output_folder / f"temp_no_bg_{datetime.now().strftime('%H%M%S%f')}.png"
            remover.remove_background(self.image_path, str(temp_no_bg))
            
            # Step 2: Create banner with text
            self.status_label.config(text="⏳ Đang tạo banner...", fg="orange")
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
            
            self.status_label.config(text="✓ Tạo banner thành công!", fg="green")
            messagebox.showinfo("✓ Thành công", f"Banner đã lưu:\n{output_path.name}")
            
        except Exception as e:
            self.status_label.config(text=f"✗ Lỗi: {str(e)}", fg="red")
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
            
            # Resize for preview (max width 700, max height 400)
            img.thumbnail((700, 400), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Update label
            self.preview_label.config(image=photo, text="")
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            self.preview_label.config(text=f"Lỗi hiển thị: {str(e)}", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleBannerCreator(root)
    root.mainloop()
