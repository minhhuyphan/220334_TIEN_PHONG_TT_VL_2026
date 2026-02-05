"""
Groq Integration - Free Text Generation
========================================

Groq API: Nhanh, miễn phí, không cần GPU

Sử dụng:
1. Get API key: https://console.groq.com
2. Set environment: GROQ_API_KEY=your_key
3. Call API trong code
"""

import os
from typing import Optional


class GroqTextGenerator:
    """Tạo text sử dụng Groq API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Groq API key. Nếu None, đọc từ GROQ_API_KEY env
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            print("⚠️ Warning: GROQ_API_KEY not set")
            print("   Get it at: https://console.groq.com")
        
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize Groq client"""
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            print("✓ Groq client initialized")
        except ImportError:
            print("❌ Groq not installed: pip install groq")
        except Exception as e:
            print(f"❌ Groq init error: {e}")
    
    def generate_title(self, product_name: str, style: str = "marketing") -> str:
        """
        Tạo tiêu đề marketing cho sản phẩm
        
        Args:
            product_name: Tên sản phẩm
            style: "marketing", "casual", "luxury", etc.
        
        Returns:
            Text tiêu đề
        """
        if not self.client:
            return product_name
        
        prompt = f"""Generate a SHORT catchy {style} title for this product in Vietnamese.
Keep it under 50 characters.

Product: {product_name}

TITLE:"""
        
        try:
            message = self.client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"Groq error: {e}")
            return product_name
    
    def generate_description(self, product_name: str, features: list = None) -> str:
        """
        Tạo mô tả sản phẩm
        
        Args:
            product_name: Tên sản phẩm
            features: Danh sách đặc điểm (tuỳ chọn)
        
        Returns:
            Mô tả sản phẩm
        """
        if not self.client:
            return product_name
        
        features_str = ", ".join(features) if features else "quality, style"
        
        prompt = f"""Write a SHORT engaging product description in Vietnamese.
Keep it under 100 characters.

Product: {product_name}
Features: {features_str}

DESCRIPTION:"""
        
        try:
            message = self.client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"Groq error: {e}")
            return product_name
    
    def generate_inpainting_prompt(self, product_type: str, mood: str = "professional") -> str:
        """
        Tạo prompt cho inpainting background
        
        Args:
            product_type: Loại sản phẩm (shoes, watch, etc.)
            mood: Cảm giác background (professional, cozy, luxury, etc.)
        
        Returns:
            Prompt cho inpainting
        """
        if not self.client:
            return f"{mood} studio backdrop for {product_type}"
        
        prompt = f"""Create a SHORT descriptive prompt for an AI image generation model.
The prompt should describe a {mood} background suitable for showcasing a {product_type}.
Keep it under 80 characters.
Avoid mentioning the product itself, only describe the environment/lighting/mood.

PROMPT:"""
        
        try:
            message = self.client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=80,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"Groq error: {e}")
            return f"{mood} studio backdrop for {product_type}"
    
    def generate_slogan(self, brand_name: str, industry: str = "general") -> str:
        """
        Tạo slogan branding
        
        Args:
            brand_name: Tên brand
            industry: Ngành hàng
        
        Returns:
            Slogan
        """
        if not self.client:
            return f"Experience {brand_name}"
        
        prompt = f"""Generate a SHORT catchy brand slogan in Vietnamese.
Keep it under 40 characters. Make it memorable.

Brand: {brand_name}
Industry: {industry}

SLOGAN:"""
        
        try:
            message = self.client.messages.create(
                model="mixtral-8x7b-32768",
                max_tokens=40,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text.strip()
        except Exception as e:
            print(f"Groq error: {e}")
            return f"Experience {brand_name}"


class BatchTextGenerator:
    """Tạo text cho batch sản phẩm"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.generator = GroqTextGenerator(api_key)
    
    def generate_for_products(self, products: list) -> dict:
        """
        Tạo text cho danh sách sản phẩm
        
        Args:
            products: List dict với keys: name, type (shoes/watch/etc), features
        
        Returns:
            Dict kết quả
        """
        results = {}
        
        for i, product in enumerate(products):
            product_name = product.get("name", f"Product {i}")
            product_type = product.get("type", "general")
            features = product.get("features", [])
            
            results[product_name] = {
                "title": self.generator.generate_title(product_name),
                "description": self.generator.generate_description(product_name, features),
                "inpaint_prompt": self.generator.generate_inpainting_prompt(product_type),
                "slogan": self.generator.generate_slogan(product_name, product_type)
            }
            
            print(f"✓ Generated content for: {product_name}")
        
        return results


# Example usage
if __name__ == "__main__":
    # Cần set GROQ_API_KEY env variable hoặc pass vào
    # export GROQ_API_KEY="your_api_key"
    
    gen = GroqTextGenerator()
    
    print("\n=== Groq Text Generation Demo ===\n")
    
    # Demo 1: Title
    title = gen.generate_title("Premium Leather Shoes")
    print(f"Title: {title}")
    
    # Demo 2: Description
    desc = gen.generate_description("Premium Leather Shoes", ["leather", "comfortable", "stylish"])
    print(f"Description: {desc}")
    
    # Demo 3: Inpainting prompt
    inpaint_prompt = gen.generate_inpainting_prompt("shoes", "luxury")
    print(f"Inpainting Prompt: {inpaint_prompt}")
    
    # Demo 4: Slogan
    slogan = gen.generate_slogan("AirWalk", "footwear")
    print(f"Slogan: {slogan}")
