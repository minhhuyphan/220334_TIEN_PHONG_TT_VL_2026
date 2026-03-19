from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import io
import base64
import os

def get_compatible_aspect_ratio(width: int, height: int) -> str:
    """
    Tính toán và trả về tỷ lệ khung hình gần nhất dựa trên kích thước đầu vào.
    """
    if width <= 0 or height <= 0:
        raise ValueError("Chiều dài và chiều rộng phải là số dương.")
    
    input_ratio = width / height
    supported_ratios = {
        "1:1": 1.0,
        "2:3": 2 / 3,
        "3:2": 3 / 2,
        "3:4": 3 / 4,
        "4:3": 4 / 3,
        "4:5": 4 / 5,
        "5:4": 5 / 4,
        "9:16": 9 / 16,
        "16:9": 16 / 9,
        "21:9": 21 / 9,
    }
    
    closest_ratio_name = min(
        supported_ratios, key=lambda x: abs(supported_ratios[x] - input_ratio)
    )
    return closest_ratio_name

def resize_image(input_image: Image.Image, width: int, height: int) -> Image.Image:
    """
    Thay đổi kích thước của ảnh PIL.Image.
    """
    try:
        if input_image.size == (width, height):
            return input_image
        return input_image.resize((width, height), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Lỗi resize image: {e}")
        return input_image

def get_resolution(aspect_ratio: str) -> str:
    """
    Trả về độ phân giải chuẩn theo tài liệu Gemini API (Gemini 2.1 Flash).
    """
    resolution_map = {
        "1:1": "1024x1024",
        "2:3": "832x1248",
        "3:2": "1248x832",
        "3:4": "864x1184",
        "4:3": "1184x864",
        "4:5": "896x1152",
        "5:4": "1152x896",
        "9:16": "768x1344",
        "16:9": "1344x768",
        "21:9": "1536x672",
    }
    return resolution_map.get(aspect_ratio, "1024x1024")

def add_text_overlay(
    image: Image.Image, 
    title: str = "", 
    subtitle: str = "", 
    website: str = "",
    text_color: str = "white"
) -> Image.Image:
    """
    Chèn lớp text chuyên nghiệp lên ảnh.
    """
    try:
        # Tạo bản sao ảnh để vẽ
        draw_img = image.convert("RGBA")
        overlay = Image.new("RGBA", draw_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        W, H = draw_img.size
        
        # Đường dẫn font (ưu tiên Arial hoặc font hệ thống)
        font_path = "C:\\Windows\\Fonts\\arialbd.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if not os.path.exists(font_path):
            font_title = ImageFont.load_default()
            font_sub = ImageFont.load_default()
        else:
            font_title = ImageFont.truetype(font_path, int(H * 0.1)) # 10% chiều cao cho title
            font_sub = ImageFont.truetype(font_path, int(H * 0.04))  # 4% chiều cao cho subtitle
        
        # 1. Vẽ tiêu đề (Ở giữa)
        if title:
            # Drop shadow cho title
            bbox = draw.textbbox((0, 0), title, font=font_title)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x, y = (W - w) / 2, (H - h) / 2 - H * 0.05
            
            # Vẽ shadow
            draw.text((x+3, y+3), title, font=font_title, fill=(0, 0, 0, 150))
            # Vẽ main text
            draw.text((x, y), title, font=font_title, fill=text_color)

        # 2. Vẽ Subtitle/Brand (Phía dưới tiêu đề)
        if subtitle:
            bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x, y = (W - w) / 2, (H + h) / 2 + H * 0.1
            draw.text((x+2, y+2), subtitle, font=font_sub, fill=(0, 0, 0, 150))
            draw.text((x, y), subtitle, font=font_sub, fill=text_color)
            
        # 3. Vẽ Website (Góc dưới cùng)
        if website:
            font_web = ImageFont.truetype(font_path, int(H * 0.03)) if os.path.exists(font_path) else font_sub
            bbox = draw.textbbox((0, 0), website, font=font_web)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            x, y = (W - w) / 2, H - h - 30
            
            # Vẽ background cho website (glassmorphism nhẹ)
            padding = 10
            draw.rectangle([x-padding, y-padding, x+w+padding, y+h+padding], fill=(0, 0, 0, 80))
            draw.text((x, y), website, font=font_web, fill="white")

        # Kết hợp các lớp
        return Image.alpha_composite(draw_img, overlay).convert("RGB")
    except Exception as e:
        print(f"Lỗi khi chèn text overlay: {e}")
        return image

def create_text_reference_image(
    width: int, 
    height: int, 
    text: str = "",
    font_path: str = None,
    text_color: str = "white",
    position: str = "center"
) -> Image.Image:
    """
    Tạo ảnh tham chiếu bố cục chữ linh hoạt từ LLM.
    """
    try:
        if not text:
            return Image.new("RGB", (width, height), (0, 0, 0))

        # Fix Gemini returning multiple colors like 'gold, blue'
        if text_color and "," in text_color:
            text_color = text_color.split(",")[0].strip()

        image = Image.new("RGB", (width, height), (0, 255, 0))
        draw = ImageDraw.Draw(image)
        
        # Sử dụng font_path truyền vào hoặc font mặc định hệ thống
        final_font_path = font_path if font_path and os.path.exists(font_path) else (
            "C:\\Windows\\Fonts\\arialbd.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        )
        
        # Tự động tính toán font size hợp lý (Bắt đầu từ 10% height và giảm dần nếu không vừa)
        current_font_size = int(height * 0.1)
        
        while current_font_size > 20:
            if os.path.exists(final_font_path):
                current_font = ImageFont.truetype(final_font_path, current_font_size)
            else:
                current_font = ImageFont.load_default()
                
            # Chia dòng thử nghiệm
            lines = []
            words = text.split()
            current_line = []
            for word in words:
                current_line.append(word)
                test_line = " ".join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=current_font)
                if (bbox[2] - bbox[0]) > width * 0.85:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
            lines.append(" ".join(current_line))
            
            line_height = current_font_size * 2.2
            total_h = len(lines) * line_height
            
            # Nếu tổng chiều cao chữ vượt quá 70% canvas, giảm font và tính lại
            if total_h < height * 0.7:
                break
            current_font_size -= 5

        # Tính toán lại Y dựa trên font_size cuối cùng
        line_height = current_font_size * 2.2
        total_h = len(lines) * line_height
        
        # Tính toán Y dựa trên position
        if "top" in position:
            curr_y = height * 0.1
        elif "bottom" in position:
            curr_y = height * 0.9 - total_h
        else:
            curr_y = (height - total_h) / 2
            
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=current_font)
            w = bbox[2] - bbox[0]
            
            # Tính toán X
            curr_x = (width - w) / 2
            if "left" in position: curr_x = width * 0.05
            if "right" in position: curr_x = width * 0.95 - w
            
            # Vẽ
            draw.text(
                (curr_x, curr_y), 
                line, 
                font=current_font, 
                fill=text_color
            )
            curr_y += line_height

        return image
    except Exception as e:
        print(f"Lỗi tạo ảnh tham chiếu: {e}")
        return Image.new("RGB", (width, height), (0, 0, 0))

def image_to_base64(pil_image):
    """
    Chuyển đổi đối tượng PIL.Image thành chuỗi base64.
    """
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{img_base64}"

def resize_and_encode_image(pil_image: Image.Image, max_size=512) -> str:
    """
    Resize ảnh và encode base64.
    """
    img = pil_image.copy()
    img.thumbnail((max_size, max_size))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    b64_encoded = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_encoded}"
