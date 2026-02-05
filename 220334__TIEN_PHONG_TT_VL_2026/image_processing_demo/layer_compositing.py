"""
Script Demo: 3-Layer Architecture Image Compositing
====================================================
Phần mềm hỗ trợ tự động ghép ảnh + thêm chữ tiếng Việt

Lớp 1 (Bottom): Background (Nền)
Lớp 2 (Middle): Product/Logo (Sản phẩm)
Lớp 3 (Top): Text & Overlay (Chữ & Họa tiết)
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
from pathlib import Path


class LayerCompositor:
    """
    Lớp xử lý ghép ảnh theo kiến trúc 3 lớp
    """
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.background_layer = None
        self.product_layer = None
        self.result_image = None
    
    def create_background(self, color_gradient=True):
        """
        Lớp 1: Tạo nền (hoặc có thể tải từ Stable Diffusion)
        
        Trong thực tế, nền này sẽ được sinh bởi AI model.
        Ở đây chúng ta demo tạo nền đơn giản hoặc gradient.
        """
        if color_gradient:
            # Tạo gradient nền từ xanh lam sang xanh lục
            image = Image.new('RGB', (self.width, self.height), color=(100, 150, 200))
            pixels = image.load()
            
            for y in range(self.height):
                # Gradient: từ xanh lam (top) -> xanh lục (bottom)
                r = int(100 + (50 * y / self.height))
                g = int(150 + (80 * y / self.height))
                b = int(200 - (100 * y / self.height))
                
                for x in range(self.width):
                    pixels[x, y] = (r, g, b)
        else:
            # Nền đơn giản
            image = Image.new('RGB', (self.width, self.height), color=(220, 220, 220))
        
        self.background_layer = image
        print(f"✓ Lớp 1 (Background): Tạo nền {self.width}x{self.height}")
        return image
    
    def create_product_circle(self, radius=80, color=(255, 100, 100)):
        """
        Lớp 2: Tạo "sản phẩm" (Ở đây là hình tròn để demo)
        
        Trong thực tế, bạn sẽ dùng rembg để tách nền khỏi ảnh sản phẩm thực.
        """
        # Tạo ảnh trong suốt (RGBA) để giữ lại transparency
        product = Image.new('RGBA', (radius*2, radius*2), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(product)
        
        # Vẽ hình tròn (sản phẩm)
        draw.ellipse(
            [0, 0, radius*2-1, radius*2-1],
            fill=color,
            outline=(0, 0, 0, 255),
            width=3
        )
        
        # Vẽ một số chi tiết bên trong để giống "sản phẩm"
        draw.ellipse(
            [radius//2, radius//2, radius+radius//2, radius+radius//2],
            fill=(255, 255, 255, 200)
        )
        
        self.product_layer = product
        print(f"✓ Lớp 2 (Product): Tạo sản phẩm (hình tròn bán kính {radius}px)")
        return product
    
    def composite_layers(self, product_position=None):
        """
        Ghép Lớp 2 lên Lớp 1
        """
        if self.background_layer is None:
            raise ValueError("Chưa tạo background layer!")
        
        if self.product_layer is None:
            raise ValueError("Chưa tạo product layer!")
        
        # Vị trí mặc định: giữa ảnh
        if product_position is None:
            x = (self.width - self.product_layer.width) // 2
            y = (self.height - self.product_layer.height) // 2
            product_position = (x, y)
        
        # Copy background làm nền cho kết quả
        result = self.background_layer.copy()
        
        # Dán product lên background
        result.paste(
            self.product_layer,
            product_position,
            self.product_layer  # Sử dụng alpha channel làm mask
        )
        
        self.result_image = result
        print(f"✓ Ghép Lớp 2 vào Lớp 1 tại vị trí {product_position}")
        return result
    
    def add_text_overlay(self, text, font_size=60, text_color=(255, 255, 255), 
                        position=None, font_path=None, background_overlay=True):
        """
        Lớp 3: Thêm chữ + Tính toán vị trí và màu sắc tối ưu
        
        Args:
            text: Chuỗi tiếng Việt cần viết
            font_size: Kích thước font
            text_color: Màu chữ (RGB tuple)
            position: Vị trí (x, y) - None = tính toán tự động
            font_path: Đường dẫn file .ttf (None = dùng font mặc định)
            background_overlay: Thêm hộp nền phía sau chữ để dễ đọc
        """
        if self.result_image is None:
            raise ValueError("Chưa ghép layers!")
        
        # Chuyển sang RGBA nếu cần (để hỗ trợ transparency)
        if self.result_image.mode != 'RGBA':
            result = self.result_image.convert('RGBA')
        else:
            result = self.result_image.copy()
        
        draw = ImageDraw.Draw(result)
        
        # Tải font - hỗ trợ tiếng Việt
        try:
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Thử font mặc định của Windows (hỗ trợ tiếng Việt)
                font = ImageFont.truetype("arial.ttf", font_size)
        except:
            # Nếu không có font, dùng default
            print("⚠ Không tìm thấy font, sử dụng font mặc định")
            font = ImageFont.load_default()
        
        # Tính kích thước bounding box của text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Xác định vị trí text
        if position is None:
            # Vị trí mặc định: phía trên cùng, căn giữa
            x = (self.width - text_width) // 2
            y = 30
            position = (x, y)
        
        # Nếu bật background overlay
        if background_overlay:
            padding = 10
            bg_box = [
                position[0] - padding,
                position[1] - padding,
                position[0] + text_width + padding,
                position[1] + text_height + padding
            ]
            # Vẽ hộp nền (màu đen, độ trong suốt)
            draw.rectangle(bg_box, fill=(0, 0, 0, 180))
        
        # Vẽ chữ
        draw.text(position, text, font=font, fill=text_color)
        
        # Chuyển lại thành RGB nếu cần
        if result.mode == 'RGBA':
            result = result.convert('RGB')
        
        self.result_image = result
        print(f"✓ Lớp 3 (Text): Thêm chữ '{text}' tại {position}")
        return result
    
    def save_result(self, output_path):
        """Lưu kết quả cuối cùng"""
        if self.result_image is None:
            raise ValueError("Chưa có kết quả để lưu!")
        
        self.result_image.save(output_path)
        print(f"✓ Lưu kết quả: {output_path}")
    
    def display_workflow(self):
        """In ra workflow các lớp"""
        print("\n" + "="*60)
        print("WORKFLOW: 3-LAYER ARCHITECTURE")
        print("="*60)
        print("INPUT: Ảnh sản phẩm + Dòng chữ tiếng Việt")
        print("  ↓")
        print("Lớp 1 (Bottom): Background")
        print("  ├─ Tạo nền bằng Generative AI (hoặc tải từ API)")
        print("  └─ Output: background_layer.png")
        print("  ↓")
        print("Lớp 2 (Middle): Product")
        print("  ├─ Input: Ảnh sản phẩm + Background cũ")
        print("  ├─ Xử lý: rembg (tách nền)")
        print("  └─ Output: product_layer.png (trong suốt)")
        print("  ↓")
        print("Lớp 3 (Top): Text & Overlay")
        print("  ├─ Input: Dòng chữ tiếng Việt")
        print("  ├─ Xử lý: Pillow (vẽ chữ + tính vị trí tối ưu)")
        print("  └─ Output: Final banner")
        print("  ↓")
        print("OUTPUT: Ảnh Banner hoàn chỉnh")
        print("="*60 + "\n")


def main():
    """
    DEMO: Tạo banner quảng cáo với 3 lớp
    """
    print("\n🎨 DEMO: 3-Layer Image Compositing Architecture\n")
    
    # Khởi tạo compositor
    compositor = LayerCompositor(width=800, height=600)
    compositor.display_workflow()
    
    # ============ LỚPBASE 1: BACKGROUND ============
    compositor.create_background(color_gradient=True)
    
    # ============ LỚPBASE 2: PRODUCT ============
    compositor.create_product_circle(radius=80, color=(255, 150, 100))
    
    # ============ GHÉP ============
    compositor.composite_layers()
    
    # ============ LỚPBASE 3: TEXT OVERLAY ============
    compositor.add_text_overlay(
        text="🔥 SIÊU SALE 50%",
        font_size=50,
        text_color=(255, 255, 0),  # Vàng
        position=None,  # Tự động tính
        background_overlay=True
    )
    
    # Thêm text thứ 2 ở phía dưới
    compositor.add_text_overlay(
        text="Mua ngay!",
        font_size=40,
        text_color=(255, 255, 255),  # Trắng
        position=(250, 520),
        background_overlay=True
    )
    
    # ============ LƯU KẾT QUẢ ============
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / "banner_final.png"
    compositor.save_result(str(output_path))
    
    print(f"\n✅ Hoàn thành! Kết quả được lưu tại: {output_path}\n")


if __name__ == "__main__":
    main()
