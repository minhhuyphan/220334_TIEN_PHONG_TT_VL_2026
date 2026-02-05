# -*- coding: utf-8 -*-
"""
AI BANNER CREATOR - WEB APP (Streamlit)
Quick Mode Only - No PyTorch needed - Works immediately!
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

# PAGE CONFIG
st.set_page_config(
    page_title="AI Banner Creator",
    page_icon="art",
    layout="wide"
)

# ===== HELPER FUNCTIONS =====

def create_gradient_background(width=1000, height=600, color="blue"):
    """Create gradient background"""
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
    
    elif color == "purple":
        for y in range(height):
            r = int(100 + (y / height) * 80)
            g = int(50 + (y / height) * 30)
            b = int(150 + (y / height) * 70)
            for x in range(width):
                pixels[x, y] = (r, g, b)
    
    return bg

def create_banner(product_img, title, subtitle, background_img, text_color=(255, 255, 255)):
    """Composite banner: background + product + text"""
    
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
        try:
            font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
            font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
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

st.title("Banner Creator")
st.write("Create professional banners - QUICK & EASY - NO AI NEEDED")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    banner_width = st.slider("Banner Width", 800, 1400, 1000, step=100)
    banner_height = st.slider("Banner Height", 400, 800, 600, step=100)
    
    st.markdown("---")
    st.write("App: Streamlit + Pillow")

# Main
st.header("Create Banner with Gradient")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Step 1: Upload Product Image")
    uploaded_file = st.file_uploader("Choose image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        product_img = Image.open(uploaded_file)
        st.image(product_img, caption="Your Product", width=1000)

with col2:
    st.subheader("Step 2: Banner Text & Colors")
    
    title = st.text_input("Title", value="Premium Product")
    subtitle = st.text_input("Subtitle", value="Limited Offer - 50% OFF")
    
    st.markdown("**Background Color:**")
    color_scheme = st.selectbox(
        "Choose color:",
        ["Blue (Professional)", "Red (Hot Sale)", "Green (Natural)", "Purple (Premium)"],
        index=0
    )
    
    color_map = {
        "Blue (Professional)": "blue",
        "Red (Hot Sale)": "red",
        "Green (Natural)": "green",
        "Purple (Premium)": "purple"
    }
    scheme = color_map[color_scheme]
    
    st.markdown("**Text Color:**")
    text_color_option = st.radio(
        "Choose text color:",
        ["White (Best)", "Black", "Yellow"],
        index=0
    )
    
    text_color_map = {
        "White (Best)": (255, 255, 255),
        "Black": (0, 0, 0),
        "Yellow": (255, 255, 0)
    }
    text_color = text_color_map[text_color_option]

if uploaded_file:
    st.markdown("---")
    if st.button("Create Banner", use_container_width=True):
        try:
            with st.spinner("Creating your banner..."):
                product_img = Image.open(uploaded_file)
                bg_img = create_gradient_background(banner_width, banner_height, scheme)
                banner = create_banner(product_img, title, subtitle, bg_img, text_color)
                
                st.success("Banner created successfully!")
                st.image(banner, caption="Your Banner", width=1000)
                
                # Download button
                img_bytes = io.BytesIO()
                banner.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                st.download_button(
                    label="Download Banner (PNG)",
                    data=img_bytes.getvalue(),
                    file_name=f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")

# Templates
st.header("Quick Templates")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Professional Blue**")
    bg = create_gradient_background(500, 300, "blue")
    st.image(bg, width=400)

with col2:
    st.write("**Hot Red**")
    bg = create_gradient_background(500, 300, "red")
    st.image(bg, width=400)

with col3:
    st.write("**Natural Green**")
    bg = create_gradient_background(500, 300, "green")
    st.image(bg, width=400)

st.markdown("---")
st.write("Banner Creator - Fast, Easy, Free - Made with Streamlit & Pillow")
