"""
Script: Stable Diffusion Integration
=====================================
Tích hợp Stable Diffusion API để tạo nền AI theo mô tả
Dùng cho Lớp 1 (Background)

Yêu cầu:
- Stable Diffusion WebUI chạy tại http://localhost:7860
- Hoặc sử dụng Replicate API: replicate.com
"""

import requests
from PIL import Image
from io import BytesIO
import json
from pathlib import Path


class StableDiffusionGenerator:
    """Tạo ảnh nền bằng Stable Diffusion"""
    
    def __init__(self, api_type="local", api_key=None):
        """
        Args:
            api_type: "local" (WebUI), "replicate", hoặc "hf" (Hugging Face)
            api_key: API key nếu dùng remote
        """
        self.api_type = api_type
        self.api_key = api_key
        
        if api_type == "local":
            self.base_url = "http://localhost:7860"
        elif api_type == "replicate":
            self.base_url = "https://api.replicate.com/v1/predictions"
        elif api_type == "hf":
            self.base_url = "https://api-inference.huggingface.co/models"
    
    def generate_background_local(self, prompt, width=512, height=512, steps=20):
        """
        Tạo ảnh nền dùng local Stable Diffusion WebUI
        
        Args:
            prompt: Mô tả ảnh (tiếng Anh)
            width, height: Kích thước ảnh
            steps: Số lần iterating (20-30 tốt)
        
        Returns:
            PIL.Image
        """
        print(f"🎨 Tạo nền AI: '{prompt}'...")
        
        try:
            payload = {
                "prompt": prompt,
                "negative_prompt": "blurry, low quality, text, watermark",
                "steps": steps,
                "width": width,
                "height": height,
                "cfg_scale": 7.5,
                "sampler_name": "Euler",
            }
            
            response = requests.post(
                f"{self.base_url}/sdapi/v1/txt2img",
                json=payload,
                timeout=120
            )
            
            if response.status_code != 200:
                raise Exception(f"API Error: {response.text}")
            
            result = response.json()
            
            if "images" in result and len(result["images"]) > 0:
                image_data = result["images"][0]
                # Decode base64
                import base64
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                
                print(f"✅ Tạo nền thành công! ({width}x{height})")
                return image
            else:
                raise Exception("No image in response")
        
        except requests.exceptions.ConnectionError:
            print("❌ Không kết nối được đến Stable Diffusion WebUI")
            print("💡 Hãy chạy: python -m venv sd_env && sd_env\\Scripts\\activate")
            print("   Hoặc mở Stable Diffusion WebUI trước")
            return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def generate_background_replicate(self, prompt, width=512, height=512):
        """
        Tạo ảnh dùng Replicate API (không cần local server)
        
        Args:
            prompt: Mô tả ảnh
            width, height: Kích thước
        
        Yêu cầu:
            - Cài: pip install replicate
            - Đặt API key: export REPLICATE_API_TOKEN=<your_token>
        """
        try:
            import replicate
            
            print(f"🎨 Tạo nền AI (Replicate): '{prompt}'...")
            
            output = replicate.run(
                "stability-ai/stable-diffusion:db21e45d3f7023abc9f30f5ab5dbe5eb410fef562ab76169910c9eae5534b959",
                input={
                    "prompt": prompt,
                    "negative_prompt": "blurry, low quality, text",
                    "num_outputs": 1,
                    "num_inference_steps": 25,
                    "guidance_scale": 7.5,
                    "width": width,
                    "height": height,
                }
            )
            
            if output and len(output) > 0:
                image_url = output[0]
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                
                print(f"✅ Tạo nền thành công!")
                return image
        
        except ImportError:
            print("❌ Replicate chưa cài: pip install replicate")
            return None
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            return None
    
    def generate_background(self, prompt, width=512, height=512):
        """Tạo nền (tự động chọn API phù hợp)"""
        if self.api_type == "local":
            return self.generate_background_local(prompt, width, height)
        elif self.api_type == "replicate":
            return self.generate_background_replicate(prompt, width, height)
        else:
            print(f"❌ API type '{self.api_type}' chưa hỗ trợ")
            return None


def demo_stable_diffusion():
    """Demo tạo nền AI"""
    print("\n🚀 DEMO: Tạo nền AI bằng Stable Diffusion\n")
    
    # Cách 1: Dùng local server
    print("=" * 60)
    print("CÁCH 1: Local Stable Diffusion WebUI")
    print("=" * 60)
    
    generator = StableDiffusionGenerator(api_type="local")
    
    prompts = [
        "modern minimalist background, blue gradient, sportswear theme",
        "luxury gold background, elegant product photography",
        "vibrant summer beach theme, tropical colors",
    ]
    
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    for i, prompt in enumerate(prompts, 1):
        image = generator.generate_background(prompt, width=800, height=600)
        if image:
            output_path = output_dir / f"bg_sd_local_{i}.png"
            image.save(output_path)
            print(f"✓ Lưu: {output_path}\n")
    
    # Cách 2: Dùng Replicate API (nếu có token)
    print("\n" + "=" * 60)
    print("CÁCH 2: Replicate API (Recommended - không cần local server)")
    print("=" * 60)
    
    generator_replicate = StableDiffusionGenerator(api_type="replicate")
    
    prompt = "professional product photography, modern blue background, studio lighting"
    image = generator_replicate.generate_background(prompt, width=800, height=600)
    
    if image:
        output_path = output_dir / "bg_replicate.png"
        image.save(output_path)
        print(f"✓ Lưu: {output_path}\n")
    
    print("\n✅ Hoàn thành demo!\n")


if __name__ == "__main__":
    demo_stable_diffusion()
