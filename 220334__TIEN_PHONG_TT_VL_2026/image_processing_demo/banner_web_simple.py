# -*- coding: utf-8 -*-
"""
AI BANNER CREATOR - WEB APP (Streamlit)
Simple version without Unicode issues
"""

import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw, ImageFont
import io
import os
from datetime import datetime

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except (ImportError, Exception):
    REMBG_AVAILABLE = False
    remove = None

# PAGE CONFIG
st.set_page_config(
    page_title="AI Banner Creator",
    page_icon="art",
    layout="wide"
)

# Load model
@st.cache_resource
def load_sd_model():
    try:
        with st.spinner('Loading Stable Diffusion 1.5...'):
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if device == "cuda" else torch.float32
            
            model = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=dtype,
                safety_checker=None
            )
            model = model.to(device)
            st.success(f"Model loaded! (Device: {device})")
            return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# ===== HELPER FUNCTIONS =====

@st.cache_resource
def remove_product_background(_image_pil):
    """Tách nền sản phẩm bằng rembg (AI-powered)"""
    if not REMBG_AVAILABLE:
        return _image_pil.convert('RGBA')
    
    try:
        # Chuyển sang RGBA để giữ transparency
        if _image_pil.mode != 'RGBA':
            _image_pil = _image_pil.convert('RGBA')
        
        # Tách nền bằng rembg
        image_no_bg = remove(_image_pil)
        return image_no_bg
    except Exception as e:
        st.warning(f"Lỗi tách nền: {e}")
        return _image_pil.convert('RGBA')

def create_gradient_background(width=1000, height=600, color="blue"):
    """Create simple gradient background"""
    bg = Image.new('RGB', (width, height))
    pixels = bg.load()
    
    if color == "blue":
        for y in range(height):
            r = int(30 + (y / height) * 80)
            g = int(100 + (y / height) * 120)
            b = int(150 + (y / height) * 70)
            for x in range(width):
                pixels[x, y] = (r, g, b)
    
    elif color == "red":
        for y in range(height):
            r = int(200 + (y / height) * 55)
            g = int(50 + (y / height) * 30)
            b = int(50 + (y / height) * 30)
            for x in range(width):
                pixels[x, y] = (r, g, b)
    
    elif color == "green":
        for y in range(height):
            r = int(30 + (y / height) * 50)
            g = int(150 + (y / height) * 100)
            b = int(80 + (y / height) * 50)
            for x in range(width):
                pixels[x, y] = (r, g, b)
    
    return bg

def generate_ai_background(sd_model, prompt, width=1000, height=600):
    """Generate background using Stable Diffusion"""
    try:
        with torch.no_grad():
            image = sd_model(
                prompt=prompt,
                height=height,
                width=width,
                num_inference_steps=20,
                guidance_scale=7.5
            ).images[0]
        return image
    except Exception as e:
        st.warning(f"AI failed: {e}. Using gradient.")
        return None

def create_banner(product_img, title, subtitle, background_img, text_color=(255, 255, 255)):
    """Composite banner"""
    
    # Resize product
    product_img.thumbnail((350, 350), Image.Resampling.LANCZOS)
    
    # Convert modes
    if product_img.mode != 'RGBA':
        product_img = product_img.convert('RGBA')
    if background_img.mode != 'RGBA':
        background_img = background_img.convert('RGBA')
    
    # Composite
    x = (background_img.width - product_img.width) // 2
    y = (background_img.height - product_img.height) // 2
    background_img.paste(product_img, (x, y), product_img)
    
    # Convert to RGB
    background_img = background_img.convert('RGB')
    
    # Add text
    draw = ImageDraw.Draw(background_img)
    try:
        font_title = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 52)
        font_subtitle = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 36)
    except:
        font_title = font_subtitle = ImageFont.load_default()
    
    # Shadow + text
    shadow_color = (0, 0, 0)
    draw.text((52, 52), title, font=font_title, fill=shadow_color)
    draw.text((50, 50), title, font=font_title, fill=text_color)
    
    draw.text((52, 122), subtitle, font=font_subtitle, fill=shadow_color)
    draw.text((50, 120), subtitle, font=font_subtitle, fill=text_color)
    
    return background_img

# ===== MAIN APP =====

st.title("Tạo Banner Quảng Cáo AI")
st.write("Tạo banner chuyên nghiệp bằng AI - HOÀN TOÀN MIỄN PHÍ")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Cài Đặt")
    
    mode = st.radio(
        "Chọn chế độ:",
        ["Chế độ Nhanh (Gradient)", "Chế độ AI (Stable Diffusion)"],
        index=0
    )
    
    banner_width = st.slider("Chiều rộng", 800, 1400, 1000, step=100)
    banner_height = st.slider("Chiều cao", 400, 800, 600, step=100)
    
    st.markdown("---")
    st.write(f"Thiết bị: {'CUDA (GPU)' if torch.cuda.is_available() else 'CPU'}")

# Tabs
tabs = st.tabs(["Banner Nhanh", "Banner AI", "Thông Tin"])

# ===== TAB 1: QUICK BANNER =====
with tabs[0]:
    st.header("Tạo Banner Nhanh (Không cần AI)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Ảnh Sản Phẩm")
        uploaded_file = st.file_uploader("Tải lên ảnh sản phẩm", type=["jpg", "jpeg", "png"])
        
        product_img_clean = None
        if uploaded_file:
            product_img = Image.open(uploaded_file)
            
            # Hiển thị nút tách nền
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Tách Nền", key="remove_bg", use_container_width=True):
                    with st.spinner("Đang tách nền..."):
                        try:
                            product_img_clean = remove_product_background(product_img)
                            st.success("Tách nền thành công!")
                        except Exception as e:
                            st.error(f"Lỗi tách nền: {e}")
            
            with col_btn2:
                if st.button("Dùng Gốc", key="use_original", use_container_width=True):
                    product_img_clean = None
            
            # Hiển thị ảnh
            if product_img_clean:
                st.image(product_img_clean, caption="Sản Phẩm (Không Nền)", width=1000)
            else:
                st.image(product_img, caption="Sản Phẩm (Gốc)", width=1000)
    
    with col2:
        st.subheader("Cài Đặt Chữ")
        title = st.text_input("Tiêu Đề", value="Sản Phẩm Premium")
        subtitle = st.text_input("Phụ Đề", value="Ưu Đãi Hạn Chế - Giảm 50%")
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Màu Nền")
        color_scheme = st.selectbox(
            "Chọn màu:",
            ["Xanh (Chuyên Nghiệp)", "Đỏ (Nóng Bỏng)", "Xanh Lá (Tự Nhiên)"],
            index=0
        )
        color_map = {"Xanh": "blue", "Đỏ": "red", "Xanh Lá": "green"}
        scheme = [v for k, v in color_map.items() if k in color_scheme][0]
    
    with col4:
        st.subheader("Màu Chữ")
        text_color_preset = st.radio(
            "Chọn màu chữ:",
            ["Trắng", "Đen", "Vàng"],
            index=0
        )
        text_color_map = {"Trắng": (255, 255, 255), "Đen": (0, 0, 0), "Vàng": (255, 255, 0)}
        text_color = text_color_map[[k for k in text_color_map if k in text_color_preset][0]]
    
    if uploaded_file:
        st.markdown("---")
        if st.button("Tạo Banner", key="quick_create", use_container_width=True):
            try:
                with st.spinner("Đang tạo banner..."):
                    # Use cleaned image if available, otherwise original
                    img_to_use = product_img_clean if product_img_clean else product_img
                    bg_img = create_gradient_background(banner_width, banner_height, scheme)
                    banner = create_banner(img_to_use, title, subtitle, bg_img, text_color)
                    
                    st.success("Tạo banner thành công!")
                    st.image(banner, caption="Banner Của Bạn", width=1000)
                    
                    # Download
                    img_bytes = io.BytesIO()
                    banner.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    
                    st.download_button(
                        label="Tải Banner",
                        data=img_bytes.getvalue(),
                        file_name=f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Lỗi: {e}")

# ===== TAB 2: AI BANNER =====
with tabs[1]:
    st.header("Tạo Banner với AI (Stable Diffusion)")
    
    sd_model = load_sd_model()
    
    if sd_model is None:
        st.error("Không thể tải model. Vui lòng cài đặt các phụ thuộc.")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Ảnh Sản Phẩm")
            uploaded_file = st.file_uploader("Tải lên ảnh sản phẩm", type=["jpg", "jpeg", "png"], key="ai_upload")
            
            product_img_clean_ai = None
            if uploaded_file:
                product_img = Image.open(uploaded_file)
                
                # Hiển thị nút tách nền
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Tách Nền", key="remove_bg_ai", use_container_width=True):
                        with st.spinner("Đang tách nền..."):
                            try:
                                product_img_clean_ai = remove_product_background(product_img)
                                st.success("Tách nền thành công!")
                            except Exception as e:
                                st.error(f"Lỗi tách nền: {e}")
                
                with col_btn2:
                    if st.button("Dùng Gốc", key="use_original_ai", use_container_width=True):
                        product_img_clean_ai = None
                
                # Hiển thị ảnh
                if product_img_clean_ai:
                    st.image(product_img_clean_ai, caption="Sản Phẩm (Không Nền)", width=1000)
                else:
                    st.image(product_img, caption="Sản Phẩm (Gốc)", width=1000)
        
        with col2:
            st.subheader("Cài Đặt Chữ")
            title = st.text_input("Tiêu Đề", value="Sản Phẩm Premium", key="ai_title")
            subtitle = st.text_input("Phụ Đề", value="Ưu Đãi Hạn Chế", key="ai_subtitle")
        
        st.markdown("---")
        
        st.subheader("AI Background Prompt")
        st.write("*Tiếng Việt hoặc English đều được*")
        ai_prompt = st.text_area(
            "Mô tả nền (hãy miêu tả chi tiết):",
            value="Nền hiện đại tối giản với gradient xanh, thiết kế chuyên nghiệp, sạch sẽ",
            height=80
        )
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.write("**Ví dụ mẫu (Gợi ý):**")
            if st.button("Chuyên nghiệp: nền văn phòng hiện đại...", key="example_Professional"):
                ai_prompt = "nền văn phòng hiện đại, gradient xanh lam, chuyên nghiệp"
            if st.button("Hè: bãi biển nắng đẹp...", key="example_Summer"):
                ai_prompt = "bãi biển nắng đẹp, cát vàng, biển xanh, không khí hè"
        
        with col_ex2:
            if st.button("Sang trọng: nền tối luxury...", key="example_Luxury"):
                ai_prompt = "nền tối sang trọng, accent đỏ, thiết kế cao cấp"
            if st.button("Công nghệ: nền tương lai...", key="example_Tech"):
                ai_prompt = "nền tương lai công nghệ, đèn neon, hiện đại"
        
        if uploaded_file:
            st.markdown("---")
            if st.button("Tạo Banner AI", key="ai_create", use_container_width=True):
                try:
                    with st.spinner("Đang tạo nền (30-60 giây)..."):
                        # Use cleaned image if available, otherwise original
                        img_to_use_ai = product_img_clean_ai if product_img_clean_ai else product_img
                        
                        # Generate background
                        bg_img = generate_ai_background(sd_model, ai_prompt, banner_width, banner_height)
                        
                        if bg_img is None:
                            bg_img = create_gradient_background(banner_width, banner_height, "blue")
                        
                        # Create banner
                        banner = create_banner(img_to_use_ai, title, subtitle, bg_img)
                        
                        st.success("Tạo banner thành công!")
                        st.image(banner, caption="Banner AI Của Bạn", width=1000)
                        
                        # Download
                        img_bytes = io.BytesIO()
                        banner.save(img_bytes, format='PNG')
                        img_bytes.seek(0)
                        
                        st.download_button(
                            label="Tải Banner",
                            data=img_bytes.getvalue(),
                            file_name=f"banner_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                            mime="image/png"
                        )
                except Exception as e:
                    st.error(f"Lỗi: {e}")

# ===== TAB 3: ABOUT =====
with tabs[2]:
    st.header("Thông Tin")
    
    st.write("""
    Công Cụ Tạo Banner AI - Tạo banner quảng cáo chuyên nghiệp bằng AI
    
    TÍNH NĂNG:
    - Chế độ Nhanh: Tạo banner với gradient (không dùng AI)
    - Chế độ AI: Tạo nền bằng Stable Diffusion
    - Tải xuống: Lưu thành PNG
    
    CÔNG NGHỆ:
    - Stable Diffusion 1.5
    - PyTorch
    - Streamlit
    - Pillow
    - rembg (tách nền)
    
    CHI PHÍ:
    - Miễn phí: Chạy local hoặc Colab
    - Replicate API: $0.01/banner
    - Ứng dụng này: $0/banner
    
    TỐC ĐỘ:
    - GPU T4 (Colab): 30-60 giây/banner
    - CPU (Local): 2-5 phút/banner
    """)

st.markdown("---")
st.write("Công Cụ Tạo Banner AI - Làm với Streamlit - Sử dụng Stable Diffusion")
