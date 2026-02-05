"""
Test Script - Inpainting + Groq Workflow
=========================================

Kiểm tra từng bước:
1. Imports
2. Models
3. Text generation (Groq)
4. Inpainting
5. Full workflow
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def test_imports():
    """Test import dependencies"""
    print("\n" + "="*60)
    print("TEST 1: CHECKING IMPORTS")
    print("="*60)
    
    packages = {
        "torch": "torch",
        "PIL": "Pillow",
        "diffusers": "diffusers",
        "groq": "groq",
        "numpy": "numpy",
        "cv2": "opencv-python"
    }
    
    missing = []
    for module, package_name in packages.items():
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - Missing: pip install {package_name}")
            missing.append(package_name)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        return False
    
    print("\n✓ All imports OK")
    return True


def test_gpu():
    """Test GPU availability"""
    print("\n" + "="*60)
    print("TEST 2: CHECKING GPU")
    print("="*60)
    
    try:
        import torch
        
        print(f"PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✓ GPU Available")
            print(f"  Device: {torch.cuda.get_device_name(0)}")
            print(f"  VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Check for 12GB+ for inpainting
            vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            if vram_gb < 12:
                print(f"\n⚠️  Warning: {vram_gb:.1f}GB VRAM, 12GB+ recommended")
                print("   Reduce batch size or use CPU (slower)")
            
            return True
        else:
            print("✗ No GPU detected")
            print("⚠️  Warning: Using CPU (will be very slow)")
            return False
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_groq():
    """Test Groq API"""
    print("\n" + "="*60)
    print("TEST 3: CHECKING GROQ API")
    print("="*60)
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("⚠️  GROQ_API_KEY not set in environment")
        print("   Get key from: https://console.groq.com")
        print("   Set: export GROQ_API_KEY='your_key'")
        return False
    
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        
        # Test API call
        print("Testing API call...")
        message = client.messages.create(
            model="mixtral-8x7b-32768",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say: Test OK"}]
        )
        
        print(f"✓ Groq API working")
        print(f"  Response: {message.content[0].text[:50]}...")
        return True
    
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return False


def test_models():
    """Test model loading"""
    print("\n" + "="*60)
    print("TEST 4: CHECKING MODELS")
    print("="*60)
    
    try:
        import torch
        from diffusers import StableDiffusionInpaintPipeline
        
        print("Loading Stable Diffusion Inpainting model...")
        print("(This may take 2-5 minutes on first run)")
        
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            torch_dtype=torch.float16,
            safety_checker=None
        )
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        
        print(f"✓ Model loaded on: {device}")
        print(f"  Model: {pipe.__class__.__name__}")
        return True, pipe
    
    except Exception as e:
        print(f"❌ Model loading error: {e}")
        return False, None


def test_inpainting(pipeline):
    """Test inpainting inference"""
    print("\n" + "="*60)
    print("TEST 5: TESTING INPAINTING")
    print("="*60)
    
    if not pipeline:
        print("❌ Pipeline not loaded")
        return False
    
    try:
        from PIL import Image, ImageDraw
        import torch
        
        # Create test images
        print("Creating test images...")
        
        # Init image (white canvas)
        init_img = Image.new("RGB", (512, 512), "white")
        
        # Mask (paint everywhere except center square)
        mask = Image.new("L", (512, 512), 255)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rectangle([150, 150, 350, 350], fill=0)
        
        # Test inpainting
        print("Running inpainting (30 steps)...")
        with torch.no_grad():
            result = pipeline(
                prompt="Professional product backdrop, studio lighting",
                image=init_img,
                mask_image=mask,
                num_inference_steps=30,
                guidance_scale=7.5,
                height=512,
                width=512
            ).images[0]
        
        print("✓ Inpainting works")
        
        # Save test result
        result.save("output/test_inpainting.png")
        print(f"  Test result saved: output/test_inpainting.png")
        
        return True
    
    except Exception as e:
        print(f"❌ Inpainting error: {e}")
        return False


def test_full_workflow():
    """Test full workflow"""
    print("\n" + "="*60)
    print("TEST 6: FULL WORKFLOW")
    print("="*60)
    
    try:
        from PIL import Image
        from groq_integration import GroqTextGenerator
        
        # Create test product image
        print("Creating test product image...")
        product = Image.new("RGBA", (300, 400), (255, 100, 0, 255))
        product.save("output/test_product.png")
        print(f"✓ Test product: output/test_product.png")
        
        # Test Groq text generation
        print("\nTesting Groq text generation...")
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            gen = GroqTextGenerator(api_key)
            title = gen.generate_title("Test Shoes")
            print(f"✓ Generated title: {title}")
        else:
            print("⚠️  Skipping Groq (no API key)")
        
        # Test inpainting workflow
        print("\nTesting inpainting workflow...")
        import torch
        from diffusers import StableDiffusionInpaintPipeline
        from inpainting_helper import InpaintingHelper
        
        pipe = StableDiffusionInpaintPipeline.from_pretrained(
            "runwayml/stable-diffusion-inpainting",
            torch_dtype=torch.float16,
            safety_checker=None
        ).to("cuda" if torch.cuda.is_available() else "cpu")
        
        helper = InpaintingHelper(pipe)
        
        # Create mask
        product_img = Image.open("output/test_product.png").convert("RGBA")
        mask, resized, pos = helper.create_inpainting_mask(product_img)
        
        print(f"✓ Mask created: {mask.size}")
        print(f"✓ Resized product: {resized.size}")
        print(f"✓ Position: {pos}")
        
        print("\n✓ Full workflow test complete!")
        return True
    
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("=  INPAINTING + GROQ WORKFLOW TEST SUITE")
    print("="*60)
    
    # Create output folder
    Path("output").mkdir(exist_ok=True)
    
    results = {}
    
    # Test 1: Imports
    results["imports"] = test_imports()
    
    if not results["imports"]:
        print("\n❌ Installation incomplete. Please install dependencies first.")
        return
    
    # Test 2: GPU
    results["gpu"] = test_gpu()
    
    # Test 3: Groq
    results["groq"] = test_groq()
    
    # Test 4: Models
    models_ok, pipeline = test_models()
    results["models"] = models_ok
    
    # Test 5: Inpainting (if model loaded)
    if models_ok:
        results["inpainting"] = test_inpainting(pipeline)
    else:
        print("\nSkipping inpainting test (model not loaded)")
    
    # Test 6: Full workflow
    if results["imports"] and results.get("models"):
        results["workflow"] = test_full_workflow()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_pass = all(results.values())
    
    if all_pass:
        print("\n" + "🎉 "*10)
        print("✓ ALL TESTS PASSED!")
        print("✓ Ready to run: python banner_creator_free_ai.py")
    else:
        print("\n❌ Some tests failed. Check errors above.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
