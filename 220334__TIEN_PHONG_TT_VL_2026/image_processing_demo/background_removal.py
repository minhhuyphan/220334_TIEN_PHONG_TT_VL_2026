"""
Script: Background Removal Integration
========================================
Tích hợp rembg để tách nền sản phẩm
Dùng cho Lớp 2 (Product)

rembg là thư viện Python dùng model AI U²-Net để tách nền
- Hỗ trợ PNG, JPG, WebP
- Xuất ra PNG trong suốt (RGBA)
"""

from PIL import Image
from pathlib import Path
import os


class BackgroundRemover:
    """Tách nền ảnh sản phẩm"""
    
    def __init__(self, model="u2net"):
        """
        Args:
            model: "u2net" (mặc định, tốt), "u2netp" (nhanh), "u2net_human_seg"
        """
        self.model = model
        self.session = None
        self._init_rembg()
    
    def _init_rembg(self):
        """Khởi tạo rembg model"""
        try:
            from rembg import new_session
            self.session = new_session(self.model)
            print(f"✓ rembg: Tải model '{self.model}' thành công")
        except ImportError:
            print("❌ rembg chưa cài: pip install rembg")
            self.session = None
        except Exception as e:
            print(f"⚠ Lỗi khởi tạo rembg: {e}")
            self.session = None
    
    def remove_background(self, input_path, output_path=None):
        """
        Tách nền từ ảnh input
        
        Args:
            input_path: Đường dẫn ảnh sản phẩm
            output_path: Đường dẫn lưu (None = output/<input_name>_no_bg.png)
        
        Returns:
            PIL.Image (RGBA) hoặc None nếu lỗi
        """
        if self.session is None:
            print("❌ rembg session chưa khởi tạo")
            return None
        
        try:
            from rembg import remove
            
            print(f"🔄 Tách nền: {input_path}...")
            
            # Mở ảnh
            input_image = Image.open(input_path)
            
            # Tách nền
            output_image = remove(input_image, session=self.session)
            
            # Xác định đường dẫn output
            if output_path is None:
                input_file = Path(input_path)
                output_path = f"output/{input_file.stem}_no_bg.png"
            
            # Tạo thư mục nếu cần
            Path(output_path).parent.mkdir(exist_ok=True)
            
            # Lưu ảnh
            output_image.save(output_path)
            
            print(f"✅ Tách nền thành công! ({output_image.size})")
            print(f"✓ Lưu: {output_path}")
            
            return output_image
        
        except ImportError:
            print("❌ rembg chưa cài: pip install rembg")
            return None
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file: {input_path}")
            return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def batch_remove_background(self, input_folder, output_folder="output"):
        """
        Tách nền cho tất cả ảnh trong thư mục
        
        Args:
            input_folder: Thư mục chứa ảnh (*.jpg, *.png)
            output_folder: Thư mục lưu kết quả
        """
        input_dir = Path(input_folder)
        output_dir = Path(output_folder)
        output_dir.mkdir(exist_ok=True)
        
        image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
        
        if not image_files:
            print(f"⚠ Không tìm thấy ảnh trong {input_folder}")
            return
        
        print(f"\n📦 Tách nền cho {len(image_files)} ảnh...\n")
        
        for i, image_path in enumerate(image_files, 1):
            output_path = output_dir / f"{image_path.stem}_no_bg.png"
            print(f"[{i}/{len(image_files)}]", end=" ")
            self.remove_background(str(image_path), str(output_path))
        
        print(f"\n✅ Hoàn thành tách nền cho {len(image_files)} ảnh!")


def demo_background_removal():
    """Demo tách nền"""
    print("\n🚀 DEMO: Tách nền sản phẩm bằng rembg\n")
    
    # Tạo ảnh sample để test
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)
    
    # Tạo ảnh test: Logo hình tròn trên nền trắng
    print("📝 Tạo ảnh test...")
    test_image = Image.new('RGB', (200, 200), color=(255, 255, 255))
    draw_import = __import__('PIL.ImageDraw', fromlist=['ImageDraw'])
    draw = draw_import.ImageDraw.Draw(test_image)
    draw.ellipse([50, 50, 150, 150], fill=(255, 100, 50), outline=(0, 0, 0), width=2)
    
    test_path = input_dir / "test_product.png"
    test_image.save(test_path)
    print(f"✓ Tạo ảnh test: {test_path}\n")
    
    # Tách nền
    remover = BackgroundRemover(model="u2net")
    
    output = remover.remove_background(str(test_path))
    
    if output:
        print(f"\n✅ Kết quả:")
        print(f"  - Mode: {output.mode} (RGBA = transparent)")
        print(f"  - Kích thước: {output.size}")
        print(f"  - Có alpha channel: {'Yes' if output.mode == 'RGBA' else 'No'}")
    
    # Demo batch processing
    print(f"\n💡 Để tách nền nhiều ảnh: remover.batch_remove_background('input/')")


if __name__ == "__main__":
    demo_background_removal()
