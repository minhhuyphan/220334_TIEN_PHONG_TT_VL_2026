"""
CLI Interface: 3-Layer Image Compositing Tool
==============================================
Giao diện dòng lệnh interactive với menu đẹp

Chạy: python cli_interface.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from layer_compositing import LayerCompositor
from background_removal import BackgroundRemover
from stable_diffusion_integration import StableDiffusionGenerator


class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    """Clear console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print styled header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.ENDC}\n")


def print_section(title):
    """Print section title"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}→ {title}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'-'*40}{Colors.ENDC}")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.ENDC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.ENDC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ {message}{Colors.ENDC}")


def input_colored(prompt, color=Colors.CYAN):
    """Input with colored prompt"""
    return input(f"{color}{prompt}{Colors.ENDC}")


def main_menu():
    """Main menu"""
    clear_screen()
    print_header("🎨 3-LAYER IMAGE COMPOSITING TOOL")
    
    print("Chọn chế độ:")
    print("1. 🎯 Tạo Banner Nhanh")
    print("2. 📦 Tách nền sản phẩm")
    print("3. 🤖 Tạo nền AI (Stable Diffusion)")
    print("4. 🔧 Tùy chỉnh nâng cao")
    print("5. 📊 Chạy test toàn bộ")
    print("0. ❌ Thoát")
    
    choice = input_colored("\nNhập lựa chọn (0-5): ")
    return choice


def quick_banner_mode():
    """Quick banner creation"""
    print_header("🎯 TẠO BANNER NHANH")
    
    # Input
    text = input_colored("Nhập dòng chữ (VD: 'Siêu Sale 50%'): ")
    if not text:
        print_error("Dòng chữ không được trống!")
        return
    
    width = input_colored("Chiều rộng (mặc định 800): ") or "800"
    height = input_colored("Chiều cao (mặc định 600): ") or "600"
    
    try:
        width, height = int(width), int(height)
    except:
        print_error("Kích thước phải là số!")
        return
    
    # Process
    print_info("Đang tạo banner...")
    
    try:
        compositor = LayerCompositor(width=width, height=height)
        compositor.create_background(color_gradient=True)
        compositor.create_product_circle(radius=80, color=(255, 100, 50))
        compositor.composite_layers()
        compositor.add_text_overlay(
            text=text,
            font_size=50,
            text_color=(255, 255, 0),
            background_overlay=True
        )
        
        output_path = Path("output") / f"quick_banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path.parent.mkdir(exist_ok=True)
        compositor.save_result(str(output_path))
        
        print_success(f"Banner đã tạo: {output_path}")
        print_info(f"Kích thước: {width}×{height}")
    
    except Exception as e:
        print_error(f"Lỗi: {e}")


def background_removal_mode():
    """Background removal mode"""
    print_header("✂️ TÁCH NỀN SẢN PHẨM")
    
    # Select image
    input_dir = Path("input")
    input_dir.mkdir(exist_ok=True)
    
    image_files = list(input_dir.glob("*.jpg")) + list(input_dir.glob("*.png"))
    
    if image_files:
        print_section("Ảnh trong thư mục input/")
        for i, f in enumerate(image_files, 1):
            print(f"{i}. {f.name}")
    
    choice = input_colored("Nhập số thứ tự hoặc đường dẫn file: ")
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(image_files):
            image_path = str(image_files[idx])
        else:
            image_path = choice
    except:
        image_path = choice
    
    if not Path(image_path).exists():
        print_error("File không tồn tại!")
        return
    
    # Process
    print_info("Đang tách nền (có thể mất 2-5 giây)...")
    
    try:
        remover = BackgroundRemover()
        output_path = Path("output") / f"{Path(image_path).stem}_no_bg.png"
        output_path.parent.mkdir(exist_ok=True)
        
        remover.remove_background(image_path, str(output_path))
        print_success(f"Ảnh đã tách nền: {output_path}")
    
    except Exception as e:
        print_error(f"Lỗi: {e}")


def ai_background_mode():
    """AI background generation"""
    print_header("🤖 TẠO NỀN AI")
    
    print_section("Tạo nền bằng Stable Diffusion")
    
    prompt = input_colored("Nhập mô tả nền (tiếng Anh):\n> ")
    if not prompt:
        print_error("Prompt không được trống!")
        return
    
    width = input_colored("Chiều rộng (mặc định 800): ") or "800"
    height = input_colored("Chiều cao (mặc định 600): ") or "600"
    
    try:
        width, height = int(width), int(height)
    except:
        print_error("Kích thước phải là số!")
        return
    
    # Choose API
    print_section("Chọn API")
    print("1. Replicate (Cloud - nhanh, không cần local server)")
    print("2. Local WebUI (cần Stable Diffusion chạy tại http://localhost:7860)")
    
    api_choice = input_colored("Lựa chọn (1-2): ")
    
    api_type = "replicate" if api_choice == "1" else "local"
    
    # Process
    print_info(f"Đang tạo nền AI (API: {api_type})...")
    print_info("(Quá trình có thể mất 1-2 phút)")
    
    try:
        gen = StableDiffusionGenerator(api_type=api_type)
        image = gen.generate_background(prompt, width, height)
        
        if image:
            output_path = Path("output") / f"bg_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            output_path.parent.mkdir(exist_ok=True)
            image.save(output_path)
            print_success(f"Nền AI đã tạo: {output_path}")
        else:
            print_error("Không thể tạo nền")
    
    except Exception as e:
        print_error(f"Lỗi: {e}")


def advanced_mode():
    """Advanced custom mode"""
    print_header("🔧 TÙYỲ CHỈNH NÂNG CAO")
    
    print_section("Lớp 1: Background (Nền)")
    bg_type = input_colored("Loại nền (gradient/solid/file): ") or "gradient"
    
    if bg_type == "file":
        bg_path = input_colored("Đường dẫn file nền: ")
        if not Path(bg_path).exists():
            print_error("File không tồn tại!")
            return
        bg_image = bg_path
    else:
        bg_image = None
    
    print_section("Lớp 2: Product (Sản phẩm)")
    product_path = input_colored("Đường dẫn file sản phẩm (để trống = bỏ qua): ")
    
    if product_path and not Path(product_path).exists():
        print_error("File không tồn tại!")
        return
    
    print_section("Lớp 3: Text (Chữ)")
    text = input_colored("Dòng chữ: ")
    if not text:
        print_error("Dòng chữ không được trống!")
        return
    
    font_size = input_colored("Kích thước chữ (mặc định 50): ") or "50"
    text_color = input_colored("Màu chữ R,G,B (mặc định 255,255,0): ") or "255,255,0"
    
    width = input_colored("Chiều rộng (mặc định 800): ") or "800"
    height = input_colored("Chiều cao (mặc định 600): ") or "600"
    
    # Parse inputs
    try:
        font_size = int(font_size)
        text_color = tuple(map(int, text_color.split(",")))
        width, height = int(width), int(height)
    except:
        print_error("Định dạng input không đúng!")
        return
    
    # Process
    print_info("Đang tạo banner...")
    
    try:
        compositor = LayerCompositor(width=width, height=height)
        
        # Layer 1
        if bg_image and bg_type == "file":
            from PIL import Image
            bg = Image.open(bg_image).resize((width, height))
            compositor.background_layer = bg
        else:
            compositor.create_background(color_gradient=(bg_type == "gradient"))
        
        # Layer 2
        if product_path:
            from PIL import Image
            prod = Image.open(product_path)
            max_size = int(min(width, height) * 0.4)
            prod.thumbnail((max_size, max_size))
            compositor.product_layer = prod
            compositor.composite_layers()
        
        # Layer 3
        compositor.add_text_overlay(
            text=text,
            font_size=font_size,
            text_color=text_color,
            background_overlay=True
        )
        
        output_path = Path("output") / f"custom_banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path.parent.mkdir(exist_ok=True)
        compositor.save_result(str(output_path))
        
        print_success(f"Banner đã tạo: {output_path}")
    
    except Exception as e:
        print_error(f"Lỗi: {e}")


def test_mode():
    """Run full test"""
    print_header("📊 CHẠY TEST TOÀN BỘ")
    
    print_info("Đang chạy test pipeline...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_pipeline.py"])
        
        if result.returncode == 0:
            print_success("Test hoàn thành!")
        else:
            print_error("Test thất bại!")
    
    except Exception as e:
        print_error(f"Lỗi: {e}")


def run_loop():
    """Main loop"""
    while True:
        choice = main_menu()
        
        if choice == "0":
            print_header("👋 TẠM BIỆT!")
            break
        elif choice == "1":
            quick_banner_mode()
        elif choice == "2":
            background_removal_mode()
        elif choice == "3":
            ai_background_mode()
        elif choice == "4":
            advanced_mode()
        elif choice == "5":
            test_mode()
        else:
            print_error("Lựa chọn không hợp lệ!")
        
        input_colored("\nNhấn Enter để tiếp tục...")


if __name__ == "__main__":
    try:
        run_loop()
    except KeyboardInterrupt:
        print_header("❌ ĐÃ DỪNG")
    except Exception as e:
        print_error(f"Lỗi chương trình: {e}")
