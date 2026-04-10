import os
import urllib.request

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "fonts")

# Danh sách một số font Google Font hỗ trợ tiếng Việt tốt
GOOGLE_FONTS = {
    "BeVietnamPro-Bold": "https://github.com/google/fonts/raw/main/ofl/bevietnampro/BeVietnamPro-Bold.ttf",
    "BeVietnamPro-Regular": "https://github.com/google/fonts/raw/main/ofl/bevietnampro/BeVietnamPro-Regular.ttf",
    "Montserrat-Bold": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf", # Đây là variable font, lấy bản tĩnh nếu cần
    "PlayfairDisplay-Bold": "https://github.com/google/fonts/raw/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
    "DancingScript-Bold": "https://github.com/google/fonts/raw/main/ofl/dancingscript/DancingScript%5Bwght%5D.ttf",
    "Pacifico-Regular": "https://github.com/google/fonts/raw/main/ofl/pacifico/Pacifico-Regular.ttf"
}

def download_fonts():
    """Tải các font từ Google Fonts nếu chưa tồn tại."""
    if not os.path.exists(FONTS_DIR):
        os.makedirs(FONTS_DIR)
    
    downloaded_fonts = {}
    print("[FONT] Kiểm tra và tải font chữ hỗ trợ tiếng Việt...")
    
    for font_name, url in GOOGLE_FONTS.items():
        font_path = os.path.join(FONTS_DIR, f"{font_name}.ttf")
        if not os.path.exists(font_path):
            try:
                print(f"  [DOWN] Đang tải {font_name}...")
                urllib.request.urlretrieve(url, font_path)
                print(f"  [OK] Đã tải: {font_name}")
            except Exception as e:
                print(f"  [ERROR] Lỗi tải font {font_name}: {e}")
                continue
        downloaded_fonts[font_name] = font_path
    
    return downloaded_fonts

def get_font_path(font_name):
    """Lấy đường dẫn font theo tên."""
    path = os.path.join(FONTS_DIR, f"{font_name}.ttf")
    if os.path.exists(path):
        return path
    return None
