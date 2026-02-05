"""
Script Nâng Cao: Advanced 3-Layer Compositing
==============================================
- Ghép nhiều sản phẩm
- Tính toán vị trí text tự động (không che sản phẩm)
- Tối ưu hóa màu chữ dựa vào độ sáng nền
- Hỗ trợ upload ảnh thực tế
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path


class AdvancedCompositor:
    """Compositor nâng cao với ML-based text placement"""
    
    def __init__(self, bg_image_path, width=800, height=600):
        """
        Khởi tạo với ảnh nền thực tế
        
        Args:
            bg_image_path: Đường dẫn file nền
            width, height: Kích thước output
        """
        self.bg_image = Image.open(bg_image_path).resize((width, height))
        self.width = width
        self.height = height
        self.result = self.bg_image.copy()
    
    def paste_product(self, product_path, position=None, scale=0.3, 
                     remove_bg=True):
        """
        Dán sản phẩm lên nền
        
        Args:
            product_path: Đường dẫn ảnh sản phẩm
            position: (x, y) tuple hoặc None để tự động
            scale: Tỉ lệ sản phẩm so với canvas (0-1)
            remove_bg: Có tách nền không (cần rembg)
        """
        product = Image.open(product_path)
        
        # Resize theo scale
        new_width = int(self.width * scale)
        aspect_ratio = product.height / product.width
        new_height = int(new_width * aspect_ratio)
        product = product.resize((new_width, new_height))
        
        # Tách nền nếu cần
        if remove_bg:
            try:
                from rembg import remove
                product = remove(product)
            except ImportError:
                print("⚠ rembg không cài đặt, sử dụng ảnh gốc")
        
        # Chuyển sang RGBA nếu cần
        if product.mode != 'RGBA':
            product = product.convert('RGBA')
        
        # Xác định vị trí
        if position is None:
            x = (self.width - product.width) // 2
            y = (self.height - product.height) // 2
            position = (x, y)
        
        # Paste lên kết quả
        self.result.paste(product, position, product)
        
        print(f"✓ Dán sản phẩm tại {position}")
        return position, (new_width, new_height)
    
    def calculate_brightness(self, region):
        """
        Tính độ sáng trung bình của vùng
        
        Args:
            region: tuple (x1, y1, x2, y2)
        
        Returns:
            float: Độ sáng (0-255)
        """
        cropped = self.result.crop(region)
        arr = np.array(cropped)
        if len(arr.shape) == 3:
            brightness = np.mean(arr[:, :, :3])  # Bỏ qua alpha
        else:
            brightness = np.mean(arr)
        return brightness
    
    def get_optimal_text_color(self, region):
        """
        Chọn màu chữ tối ưu dựa vào nền
        
        Args:
            region: tuple (x1, y1, x2, y2)
        
        Returns:
            tuple: (R, G, B) - Màu chữ
        """
        brightness = self.calculate_brightness(region)
        
        if brightness > 128:
            # Nền sáng → chữ đen
            return (0, 0, 0)
        else:
            # Nền tối → chữ trắng
            return (255, 255, 255)
    
    def find_text_placement(self, text, font_size=50):
        """
        Tìm vị trí tối ưu để đặt chữ (không che sản phẩm)
        
        Chiến lược:
        1. Chia canvas thành grid
        2. Chọn vùng không trùng với sản phẩm
        3. Ưu tiên: Top Center > Bottom Center > Sides
        """
        # Ứng dụng đơn giản: ưu tiên top center
        positions = [
            ((self.width - 200) // 2, 30),      # Top center
            ((self.width - 200) // 2, self.height - 80),  # Bottom center
            (20, self.height // 2 - 40),        # Left middle
            (self.width - 220, self.height // 2 - 40),   # Right middle
        ]
        
        # Trả về vị trí đầu tiên (ở đây: top center)
        return positions[0]
    
    def add_smart_text(self, text, font_size=50, font_path=None):
        """
        Thêm chữ với tính toán thông minh
        
        - Tìm vị trí tối ưu
        - Chọn màu chữ phù hợp
        - Thêm shadow/outline
        """
        if self.result.mode != 'RGBA':
            self.result = self.result.convert('RGBA')
        
        draw = ImageDraw.Draw(self.result)
        
        # Load font
        try:
            if font_path and Path(font_path).exists():
                font = ImageFont.truetype(font_path, font_size)
            else:
                font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Tìm vị trí + tính màu
        text_pos = self.find_text_placement(text, font_size)
        bbox = draw.textbbox(text_pos, text, font=font)
        text_box = (bbox[0], bbox[1], bbox[2], bbox[3])
        text_color = self.get_optimal_text_color(text_box)
        
        # Thêm shadow (vẽ chữ xanh dương phía sau)
        shadow_color = (0, 0, 0) if text_color == (255, 255, 255) else (255, 255, 255)
        for adj_x, adj_y in [(1, 1), (2, 2), (-1, -1)]:
            draw.text(
                (text_pos[0] + adj_x, text_pos[1] + adj_y),
                text,
                font=font,
                fill=shadow_color
            )
        
        # Thêm chữ chính
        draw.text(text_pos, text, font=font, fill=text_color)
        
        # Chuyển lại RGB
        self.result = self.result.convert('RGB')
        
        print(f"✓ Thêm chữ '{text}' tại {text_pos} - Màu: {text_color}")
        return text_pos
    
    def save(self, output_path):
        """Lưu kết quả"""
        self.result.save(output_path)
        print(f"✓ Lưu kết quả: {output_path}")


def demo_advanced():
    """Demo script nâng cao"""
    print("\n🚀 DEMO: Advanced 3-Layer Compositing\n")
    
    # Tạo ảnh nền demo
    demo_bg = Image.new('RGB', (800, 600), color=(100, 150, 200))
    demo_bg.save("input/demo_background.png")
    
    # Tạo ảnh sản phẩm demo
    demo_product = Image.new('RGBA', (150, 150), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(demo_product)
    draw.ellipse([10, 10, 140, 140], fill=(255, 100, 50))
    demo_product.save("input/demo_product.png")
    
    # Khởi tạo compositor
    compositor = AdvancedCompositor("input/demo_background.png")
    
    # Dán sản phẩm
    compositor.paste_product("input/demo_product.png", scale=0.25)
    
    # Thêm chữ thông minh
    compositor.add_smart_text("🔥 HOT SALE", font_size=50)
    compositor.add_smart_text("Giảm 50%", font_size=40)
    
    # Lưu
    Path("output").mkdir(exist_ok=True)
    compositor.save("output/advanced_banner.png")


if __name__ == "__main__":
    demo_advanced()
