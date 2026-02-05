"""
Inpainting Helper - Advanced Background Generation
===================================================

Hỗ trợ quy trình:
1. Load sản phẩm (PNG transparent)
2. Tạo mask (vùng cần vẽ)
3. Run Inpainting
4. Composite kết quả

Lợi ích: Sản phẩm không bị méo mó, nền hoàn toàn do AI tạo
"""

from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
import torch


class InpaintingHelper:
    """Hỗ trợ Inpainting workflow"""
    
    def __init__(self, pipeline=None):
        self.pipeline = pipeline
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def create_inpainting_mask(self, product_img: Image.Image, canvas_size=(1200, 630), product_width_percent=0.35):
        """
        Tạo mask cho inpainting
        
        Args:
            product_img: Ảnh sản phẩm (RGBA)
            canvas_size: Kích thước banner (width, height)
            product_width_percent: % chiều rộng sản phẩm vs banner
        
        Returns:
            mask: PIL Image (L mode) - trắng = vẽ, đen = giữ nguyên
        """
        width, height = canvas_size
        
        # Resize sản phẩm
        max_width = int(width * product_width_percent)
        product_img.thumbnail((max_width, height - 100), Image.Resampling.LANCZOS)
        
        # Vị trí sản phẩm (căn giữa)
        prod_x = (width - product_img.width) // 2
        prod_y = (height - product_img.height) // 2
        
        # Tạo mask
        mask = Image.new("L", (width, height), 255)  # Toàn bộ trắng (vẽ)
        
        # Vùng sản phẩm = đen (giữ nguyên)
        mask.paste(0, (
            prod_x - 10,
            prod_y - 10,
            prod_x + product_img.width + 10,
            prod_y + product_img.height + 10
        ))
        
        return mask, product_img, (prod_x, prod_y)
    
    def create_init_image(self, canvas_size=(1200, 630), fill_color="white"):
        """Tạo ảnh khởi đầu cho inpainting"""
        return Image.new("RGB", canvas_size, fill_color)
    
    def run_inpainting(self, init_image: Image.Image, mask: Image.Image, prompt: str, num_steps=50, guidance_scale=7.5):
        """
        Chạy inpainting
        
        Args:
            init_image: Ảnh ban đầu (RGB)
            mask: Mask (L mode)
            prompt: Text description
            num_steps: Số inference steps
            guidance_scale: Classifier-free guidance scale
        
        Returns:
            PIL Image kết quả
        """
        if not self.pipeline:
            raise Exception("Pipeline not initialized")
        
        try:
            with torch.no_grad():
                result = self.pipeline(
                    prompt=prompt,
                    image=init_image,
                    mask_image=mask,
                    num_inference_steps=num_steps,
                    guidance_scale=guidance_scale,
                    height=init_image.height,
                    width=init_image.width
                ).images[0]
            
            return result
        except Exception as e:
            raise Exception(f"Inpainting failed: {str(e)}")
    
    def composite_final(self, background: Image.Image, product: Image.Image, product_pos=(0, 0), title: str = None, font=None):
        """
        Ghép nền + sản phẩm + text
        
        Args:
            background: Nền (result từ inpainting)
            product: Sản phẩm (PNG RGBA)
            product_pos: Vị trí (x, y)
            title: Tiêu đề (tuỳ chọn)
            font: PIL Font
        
        Returns:
            PIL Image (RGB)
        """
        # Convert bg to RGBA
        result = background.convert("RGBA")
        
        # Paste sản phẩm
        result.paste(product, product_pos, product)
        
        # Add text nếu có
        if title and font:
            from PIL import ImageDraw
            draw = ImageDraw.Draw(result)
            
            # Tính vị trí text
            title_bbox = draw.textbbox((0, 0), title, font=font)
            title_x = (result.width - (title_bbox[2] - title_bbox[0])) // 2
            title_y = 50
            
            draw.text((title_x, title_y), title, font=font, fill=(255, 255, 255))
        
        return result.convert("RGB")
    
    def save_output(self, image: Image.Image, output_folder: Path, filename: str = None):
        """Lưu ảnh output"""
        if not filename:
            from datetime import datetime
            filename = f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        output_folder.mkdir(exist_ok=True)
        output_path = output_folder / filename
        image.save(output_path)
        
        return output_path


class BatchInpaintingProcessor:
    """Xử lý batch inpainting cho nhiều sản phẩm"""
    
    def __init__(self, pipeline=None):
        self.helper = InpaintingHelper(pipeline)
    
    def process_products(self, product_paths: list, prompt: str, output_folder: Path):
        """
        Xử lý nhiều sản phẩm
        
        Args:
            product_paths: List đường dẫn ảnh
            prompt: Prompt inpainting
            output_folder: Thư mục output
        
        Returns:
            List đường dẫn output
        """
        results = []
        
        for i, product_path in enumerate(product_paths):
            try:
                product_img = Image.open(product_path).convert("RGBA")
                
                # Create mask
                mask, resized_product, pos = self.helper.create_inpainting_mask(product_img)
                
                # Create init image
                init_img = self.helper.create_init_image()
                
                # Run inpainting
                bg_result = self.helper.run_inpainting(init_img, mask, prompt)
                
                # Composite
                final_img = self.helper.composite_final(bg_result, resized_product, pos)
                
                # Save
                output_path = self.helper.save_output(final_img, output_folder, f"banner_{i:03d}.png")
                results.append(output_path)
                
                print(f"✓ Processed: {product_path}")
            
            except Exception as e:
                print(f"✗ Error processing {product_path}: {str(e)}")
        
        return results


if __name__ == "__main__":
    # Demo: Tạo mock inpainting workflow
    
    print("Inpainting Helper - Demo")
    print("=" * 50)
    
    # Tạo ảnh sản phẩm giả (đỏ + transparent)
    product = Image.new("RGBA", (200, 300), (255, 0, 0, 255))
    
    # Tạo mask
    helper = InpaintingHelper()
    mask, resized, pos = helper.create_inpainting_mask(product)
    
    print(f"✓ Mask size: {mask.size}")
    print(f"✓ Product position: {pos}")
    print(f"✓ Resized product: {resized.size}")
    
    # Save mask để xem
    mask.save("output/mask_demo.png")
    print("✓ Demo mask saved to output/mask_demo.png")
