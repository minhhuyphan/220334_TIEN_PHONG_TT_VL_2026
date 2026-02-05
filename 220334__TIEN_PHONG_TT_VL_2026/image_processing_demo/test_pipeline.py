"""
Script Test: Toàn bộ Pipeline 3-Layer
=====================================
Test từng bước: Tách nền → Tạo nền AI → Ghép lớp → Thêm chữ
"""

from pathlib import Path
import time

# Import các module
from layer_compositing import LayerCompositor
from background_removal import BackgroundRemover
from advanced_compositing import AdvancedCompositor
from PIL import Image, ImageDraw


def create_sample_images():
    """Tạo ảnh sample để test"""
    print("\n📝 BƯỚC 1: Tạo ảnh sample")
    print("-" * 60)
    
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)
    
    # Sample 1: Sản phẩm (hình tròn)
    product = Image.new('RGB', (200, 200), color=(240, 240, 240))
    draw = ImageDraw.Draw(product)
    draw.ellipse([30, 30, 170, 170], fill=(255, 100, 50), outline=(0, 0, 0), width=3)
    draw.ellipse([80, 80, 120, 120], fill=(255, 200, 100))
    
    product_path = input_dir / "sample_product.png"
    product.save(product_path)
    print(f"✓ Tạo ảnh sản phẩm: {product_path}")
    
    # Sample 2: Sản phẩm với nền (để test tách nền)
    product_with_bg = Image.new('RGB', (300, 300), color=(200, 200, 200))
    draw = ImageDraw.Draw(product_with_bg)
    draw.ellipse([80, 80, 220, 220], fill=(0, 150, 200), outline=(0, 0, 0), width=3)
    
    product_bg_path = input_dir / "sample_product_with_bg.png"
    product_with_bg.save(product_bg_path)
    print(f"✓ Tạo ảnh sản phẩm+nền: {product_bg_path}")
    
    return product_path, product_bg_path


def test_layer_compositing():
    """Test LayerCompositor (demo cơ bản)"""
    print("\n🎨 BƯỚC 2: LayerCompositor - Ghép 3 lớp cơ bản")
    print("-" * 60)
    
    start = time.time()
    
    compositor = LayerCompositor(width=800, height=600)
    compositor.create_background(color_gradient=True)
    compositor.create_product_circle(radius=100, color=(255, 100, 50))
    compositor.composite_layers()
    compositor.add_text_overlay(
        text="🔥 SIÊU SALE",
        font_size=60,
        text_color=(255, 255, 0),
        background_overlay=True
    )
    
    output_path = Path("output/test_01_basic_compositing.png")
    output_path.parent.mkdir(exist_ok=True)
    compositor.save_result(str(output_path))
    
    elapsed = time.time() - start
    print(f"⏱ Thời gian: {elapsed:.2f}s")
    print(f"✅ Kết quả: {output_path}\n")


def test_background_removal():
    """Test BackgroundRemover (tách nền)"""
    print("\n✂️ BƯỚC 3: BackgroundRemover - Tách nền")
    print("-" * 60)
    
    start = time.time()
    
    product_path = Path("input/sample_product_with_bg.png")
    
    if not product_path.exists():
        print("⚠ Ảnh sample không tồn tại, bỏ qua")
        return None
    
    try:
        remover = BackgroundRemover(model="u2net")
        output_path = Path("output/test_02_no_background.png")
        
        result = remover.remove_background(str(product_path), str(output_path))
        
        elapsed = time.time() - start
        
        if result:
            print(f"⏱ Thời gian: {elapsed:.2f}s")
            print(f"✅ Kết quả: {output_path}\n")
            return output_path
    except Exception as e:
        print(f"⚠ Lỗi: {e}")
        print("💡 Để sử dụng rembg: pip install rembg\n")
    
    return None


def test_advanced_compositing(product_no_bg=None):
    """Test AdvancedCompositor (tính toán thông minh)"""
    print("\n🚀 BƯỚC 4: AdvancedCompositor - Ghép nâng cao")
    print("-" * 60)
    
    start = time.time()
    
    # Tạo ảnh nền sample
    from PIL import Image
    bg = Image.new('RGB', (800, 600), color=(100, 150, 200))
    bg_path = Path("input/sample_background.png")
    bg.save(bg_path)
    
    try:
        compositor = AdvancedCompositor(str(bg_path))
        
        # Dán sản phẩm
        product_path = Path("input/sample_product.png")
        pos, size = compositor.paste_product(str(product_path), scale=0.3)
        
        # Thêm chữ thông minh
        compositor.add_smart_text("HOT SALE", font_size=60)
        
        output_path = Path("output/test_03_advanced_compositing.png")
        compositor.save(str(output_path))
        
        elapsed = time.time() - start
        print(f"⏱ Thời gian: {elapsed:.2f}s")
        print(f"✅ Kết quả: {output_path}\n")
    
    except Exception as e:
        print(f"❌ Lỗi: {e}\n")


def test_stable_diffusion():
    """Test Stable Diffusion (tạo nền AI)"""
    print("\n🎨 BƯỚC 5: Stable Diffusion - Tạo nền AI")
    print("-" * 60)
    print("⚠ Bước này yêu cầu Stable Diffusion WebUI hoặc API key")
    print("💡 Để test: python stable_diffusion_integration.py\n")


def test_full_pipeline():
    """Test đầy đủ pipeline"""
    print("\n" + "="*60)
    print("✅ TEST: ĐẦY ĐỦ PIPELINE 3-LAYER")
    print("="*60)
    
    # Bước 1: Tạo sample
    product_path, product_bg_path = create_sample_images()
    
    # Bước 2: Test LayerCompositor
    test_layer_compositing()
    
    # Bước 3: Test BackgroundRemover
    product_no_bg = test_background_removal()
    
    # Bước 4: Test AdvancedCompositor
    test_advanced_compositing(product_no_bg)
    
    # Bước 5: Stable Diffusion
    test_stable_diffusion()
    
    # Kết quả
    print("\n" + "="*60)
    print("📊 KẾT QUẢ TEST")
    print("="*60)
    
    output_dir = Path("output")
    test_files = sorted(output_dir.glob("test_*.png"))
    
    if test_files:
        print(f"\n✅ Tạo được {len(test_files)} ảnh test:\n")
        for i, f in enumerate(test_files, 1):
            size = f.stat().st_size / 1024
            print(f"  {i}. {f.name:<40} ({size:.1f} KB)")
    else:
        print("\n⚠ Không có ảnh test được tạo")
    
    print("\n" + "="*60)
    print("🎯 BƯỚC TIẾP THEO:")
    print("="*60)
    print("1. Chạy web API:      python app.py")
    print("2. Tách nền real:     python background_removal.py")
    print("3. Tạo nền AI:        python stable_diffusion_integration.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    test_full_pipeline()
