"""
Desktop GUI: 3-Layer Image Compositing Tool
=============================================
Giao diện desktop dễ sử dụng với tkinter
- Upload ảnh sản phẩm
- Tạo nền AI
- Ghép lớp + thêm chữ tiếng Việt
- Xem trước và tải xuống

Không cần cài thêm gì - tkinter tích hợp sẵn Python
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from pathlib import Path
import threading
from datetime import datetime
import json

# Import các module của chúng ta
from layer_compositing import LayerCompositor
from background_removal import BackgroundRemover
from stable_diffusion_integration import StableDiffusionGenerator


class ImageCompositorGUI:
    """Desktop GUI for 3-Layer Image Compositing"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 3-Layer Image Compositing Tool")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Data
        self.product_image_path = None
        self.background_image_path = None
        self.current_preview = None
        self.output_folders = Path("output")
        self.output_folders.mkdir(exist_ok=True)
        
        # Create UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main UI layout"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#667eea", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🎨 3-Layer Image Compositing Tool",
            font=("Segoe UI", 24, "bold"),
            bg="#667eea",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main content
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel: Controls
        left_panel = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        self.setup_control_panel(left_panel)
        
        # Right panel: Preview
        right_panel = tk.Frame(content_frame, bg="white", relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_preview_panel(right_panel)
    
    def setup_control_panel(self, parent):
        """Setup left control panel"""
        
        # Scrollable frame
        canvas = tk.Canvas(parent, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ============ SECTION 1: Product Image ============
        section1 = tk.LabelFrame(scrollable_frame, text="📦 Lớp 2: Sản phẩm", 
                                 font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15)
        section1.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(section1, text="📂 Chọn ảnh sản phẩm", 
                 command=self.select_product_image,
                 bg="#667eea", fg="white", font=("Segoe UI", 10),
                 padx=10, pady=8, cursor="hand2",
                 activebackground="#764ba2").pack(fill=tk.X, pady=5)
        
        self.product_label = tk.Label(section1, text="Chưa chọn ảnh", 
                                     fg="#999", font=("Segoe UI", 9))
        self.product_label.pack(fill=tk.X, pady=5)
        
        tk.Button(section1, text="✂️ Tách nền", 
                 command=self.remove_background,
                 bg="#ff6b6b", fg="white", font=("Segoe UI", 10),
                 padx=10, pady=8, cursor="hand2",
                 activebackground="#ff5252").pack(fill=tk.X, pady=5)
        
        # ============ SECTION 2: Background ============
        section2 = tk.LabelFrame(scrollable_frame, text="🎨 Lớp 1: Nền", 
                                 font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15)
        section2.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(section2, text="🎯 Loại nền", 
                 command=self.choose_background_type,
                 bg="#ffa94d", fg="white", font=("Segoe UI", 10),
                 padx=10, pady=8, cursor="hand2",
                 activebackground="#ff8c42").pack(fill=tk.X, pady=5)
        
        self.bg_type_label = tk.Label(section2, text="Nền gradient", 
                                     fg="#667eea", font=("Segoe UI", 9, "bold"))
        self.bg_type_label.pack(fill=tk.X, pady=5)
        
        # Background color selector
        tk.Label(section2, text="Màu nền:", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=5)
        
        color_frame = tk.Frame(section2, bg="white")
        color_frame.pack(fill=tk.X, pady=5)
        
        self.bg_color = tk.StringVar(value="100,150,200")
        tk.Entry(color_frame, textvariable=self.bg_color, width=15, 
                font=("Segoe UI", 9)).pack(side=tk.LEFT)
        tk.Label(color_frame, text="(R,G,B)", font=("Segoe UI", 8), fg="#999").pack(side=tk.LEFT, padx=5)
        
        # AI Background button
        tk.Button(section2, text="🤖 Tạo nền AI (Replicate)", 
                 command=self.generate_ai_background,
                 bg="#51cf66", fg="white", font=("Segoe UI", 10),
                 padx=10, pady=8, cursor="hand2",
                 activebackground="#40c057").pack(fill=tk.X, pady=5)
        
        # AI Prompt
        tk.Label(section2, text="Prompt AI (tiếng Anh):", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=5)
        self.ai_prompt = tk.Text(section2, height=3, width=25, font=("Courier", 8))
        self.ai_prompt.insert(1.0, "modern blue gradient, professional background")
        self.ai_prompt.pack(fill=tk.X, pady=5)
        
        # ============ SECTION 3: Text ============
        section3 = tk.LabelFrame(scrollable_frame, text="✏️ Lớp 3: Chữ", 
                                 font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15)
        section3.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(section3, text="Dòng chữ:", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=5)
        self.text_input = tk.Entry(section3, font=("Segoe UI", 10), width=25)
        self.text_input.insert(0, "🔥 SIÊU SALE 50%")
        self.text_input.pack(fill=tk.X, pady=5)
        
        tk.Label(section3, text="Kích thước chữ:", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=5)
        self.font_size = tk.Scale(section3, from_=20, to=100, orient=tk.HORIZONTAL, bg="white")
        self.font_size.set(50)
        self.font_size.pack(fill=tk.X, pady=5)
        
        tk.Label(section3, text="Màu chữ:", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=5)
        self.text_color = tk.StringVar(value="255,255,0")
        tk.Entry(section3, textvariable=self.text_color, width=15, 
                font=("Segoe UI", 9)).pack(fill=tk.X, pady=5)
        
        # Canvas size
        tk.Label(section3, text="Kích thước (W×H):", font=("Segoe UI", 9)).pack(anchor=tk.W, pady=5)
        size_frame = tk.Frame(section3, bg="white")
        size_frame.pack(fill=tk.X, pady=5)
        
        self.width = tk.StringVar(value="800")
        self.height = tk.StringVar(value="600")
        tk.Entry(size_frame, textvariable=self.width, width=8, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        tk.Label(size_frame, text="×", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=5)
        tk.Entry(size_frame, textvariable=self.height, width=8, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        
        # ============ ACTION BUTTONS ============
        section4 = tk.Frame(scrollable_frame, bg="white")
        section4.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(section4, text="✨ TẠO BANNER", 
                 command=self.create_banner,
                 bg="#9775fa", fg="white", font=("Segoe UI", 12, "bold"),
                 padx=20, pady=12, cursor="hand2",
                 activebackground="#7c3aed").pack(fill=tk.X, pady=5)
        
        tk.Button(section4, text="💾 Lưu kết quả", 
                 command=self.save_result,
                 bg="#339af0", fg="white", font=("Segoe UI", 10),
                 padx=10, pady=8, cursor="hand2",
                 activebackground="#1971c2").pack(fill=tk.X, pady=5)
        
        tk.Button(section4, text="📁 Mở thư mục output", 
                 command=self.open_output_folder,
                 bg="#748ffc", fg="white", font=("Segoe UI", 10),
                 padx=10, pady=8, cursor="hand2",
                 activebackground="#5c7cfa").pack(fill=tk.X, pady=5)
        
        # Status
        self.status_label = tk.Label(section4, text="Ready ✓", 
                                    fg="green", font=("Segoe UI", 9))
        self.status_label.pack(pady=10)
    
    def setup_preview_panel(self, parent):
        """Setup right preview panel"""
        
        title = tk.Label(parent, text="👁️ Xem trước", 
                        font=("Segoe UI", 12, "bold"), bg="white")
        title.pack(pady=10)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(parent, bg="#f9f9f9", width=450, height=550)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info label
        self.info_label = tk.Label(parent, text="Chưa tạo banner", 
                                  font=("Segoe UI", 9), fg="#999", bg="white")
        self.info_label.pack(pady=5)
    
    def select_product_image(self):
        """Select product image"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image files", "*.jpg *.png *.jpeg"), ("All files", "*.*")]
        )
        
        if file_path:
            self.product_image_path = file_path
            filename = Path(file_path).name
            self.product_label.config(text=f"✓ {filename}", fg="green")
            self.status_label.config(text="Ảnh sản phẩm đã chọn", fg="green")
    
    def remove_background(self):
        """Remove background from product"""
        if not self.product_image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh sản phẩm trước!")
            return
        
        self.status_label.config(text="⏳ Đang tách nền...", fg="orange")
        self.root.update()
        
        try:
            remover = BackgroundRemover()
            output_path = self.output_folders / f"product_no_bg_{datetime.now().strftime('%H%M%S')}.png"
            
            remover.remove_background(self.product_image_path, str(output_path))
            
            self.product_image_path = str(output_path)
            messagebox.showinfo("Thành công", f"Đã tách nền!\nFile: {output_path.name}")
            self.status_label.config(text="Tách nền thành công!", fg="green")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tách nền: {e}")
            self.status_label.config(text="Lỗi!", fg="red")
    
    def choose_background_type(self):
        """Choose background type"""
        # Simple dialog
        window = tk.Toplevel(self.root)
        window.title("Chọn loại nền")
        window.geometry("300x150")
        window.resizable(False, False)
        
        tk.Label(window, text="Chọn loại nền:", font=("Segoe UI", 11)).pack(pady=10)
        
        def set_gradient():
            self.bg_type_label.config(text="Nền gradient")
            window.destroy()
        
        def set_solid():
            self.bg_type_label.config(text="Nền màu đơn")
            window.destroy()
        
        tk.Button(window, text="Gradient", command=set_gradient, width=20).pack(pady=5)
        tk.Button(window, text="Màu đơn", command=set_solid, width=20).pack(pady=5)
    
    def generate_ai_background(self):
        """Generate background using Stable Diffusion"""
        prompt = self.ai_prompt.get(1.0, tk.END).strip()
        
        if not prompt:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập prompt AI!")
            return
        
        self.status_label.config(text="⏳ Đang tạo nền AI (có thể mất 1-2 phút)...", fg="orange")
        self.root.update()
        
        # Run in thread to prevent UI freezing
        def generate():
            try:
                gen = StableDiffusionGenerator(api_type="replicate")
                image = gen.generate_background(
                    prompt,
                    int(self.width.get()),
                    int(self.height.get())
                )
                
                if image:
                    output_path = self.output_folders / f"bg_ai_{datetime.now().strftime('%H%M%S')}.png"
                    image.save(output_path)
                    self.background_image_path = str(output_path)
                    
                    self.root.after(0, lambda: messagebox.showinfo("Thành công", "Nền AI đã tạo!"))
                    self.status_label.config(text="Nền AI tạo thành công!", fg="green")
                    self.bg_type_label.config(text="Nền AI (Stable Diffusion)")
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi: {e}"))
                self.status_label.config(text="Lỗi tạo nền AI!", fg="red")
        
        thread = threading.Thread(target=generate, daemon=True)
        thread.start()
    
    def create_banner(self):
        """Create final banner"""
        try:
            width = int(self.width.get())
            height = int(self.height.get())
            text = self.text_input.get()
            
            if not text:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập dòng chữ!")
                return
            
            # Parse colors
            try:
                text_color = tuple(map(int, self.text_color.get().split(",")))
                bg_color = tuple(map(int, self.bg_color.get().split(",")))
            except:
                messagebox.showerror("Lỗi", "Màu phải là định dạng: R,G,B (ví dụ: 255,100,50)")
                return
            
            self.status_label.config(text="⏳ Đang tạo banner...", fg="orange")
            self.root.update()
            
            # Create compositor
            compositor = LayerCompositor(width=width, height=height)
            
            # Layer 1: Background
            if self.background_image_path:
                bg_img = Image.open(self.background_image_path).resize((width, height))
                compositor.background_layer = bg_img
            else:
                compositor.create_background(color_gradient=True)
                compositor.background_layer = Image.new('RGB', (width, height), color=bg_color)
            
            # Layer 2: Product
            if self.product_image_path:
                try:
                    product_img = Image.open(self.product_image_path)
                    max_size = int(min(width, height) * 0.4)
                    product_img.thumbnail((max_size, max_size))
                    compositor.product_layer = product_img
                    compositor.composite_layers()
                except:
                    pass
            
            # Layer 3: Text
            compositor.add_text_overlay(
                text=text,
                font_size=self.font_size.get(),
                text_color=text_color,
                background_overlay=True
            )
            
            # Save
            output_path = self.output_folders / f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            compositor.save_result(str(output_path))
            
            # Update preview
            self.current_preview = Image.open(output_path)
            self.show_preview(self.current_preview)
            
            self.status_label.config(text=f"✓ Banner tạo thành công! ({output_path.name})", fg="green")
            messagebox.showinfo("Thành công", f"Banner đã tạo tại:\n{output_path}")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tạo banner: {e}")
            self.status_label.config(text="Lỗi!", fg="red")
    
    def show_preview(self, image):
        """Show preview on canvas"""
        # Resize to fit canvas
        preview_image = image.copy()
        preview_image.thumbnail((450, 550))
        
        photo = ImageTk.PhotoImage(preview_image)
        
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(225, 275, image=photo)
        self.preview_canvas.image = photo  # Keep a reference
        
        self.info_label.config(text=f"Size: {image.size[0]}×{image.size[1]}", fg="#667eea")
    
    def save_result(self):
        """Save result to file"""
        if self.current_preview is None:
            messagebox.showwarning("Cảnh báo", "Chưa tạo banner!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if file_path:
            self.current_preview.save(file_path)
            messagebox.showinfo("Thành công", f"Lưu tại: {file_path}")
    
    def open_output_folder(self):
        """Open output folder"""
        import subprocess
        import sys
        
        try:
            if sys.platform == "win32":
                subprocess.Popen(f'explorer "{self.output_folders.absolute()}"')
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(self.output_folders.absolute())])
            else:
                subprocess.Popen(["xdg-open", str(self.output_folders.absolute())])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở thư mục: {e}")


def main():
    root = tk.Tk()
    app = ImageCompositorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
