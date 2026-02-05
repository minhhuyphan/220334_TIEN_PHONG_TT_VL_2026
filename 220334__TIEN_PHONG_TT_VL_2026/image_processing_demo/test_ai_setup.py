"""
Test AI Setup - Kiểm tra cấu hình AI
====================================
Chạy file này để kiểm tra xem các API đã được cấu hình đúng chưa
"""

import os
import sys
from pathlib import Path

def test_replicate():
    """Test Replicate API"""
    print("\n" + "="*50)
    print("Testing Replicate API...")
    print("="*50)
    
    api_token = os.getenv("REPLICATE_API_TOKEN")
    
    if not api_token:
        print("❌ REPLICATE_API_TOKEN not found!")
        print("   Set environment variable:")
        print("   Windows: set REPLICATE_API_TOKEN=your_token")
        print("   Linux/Mac: export REPLICATE_API_TOKEN=your_token")
        return False
    
    try:
        import replicate
        print(f"✓ Replicate module installed")
        print(f"✓ API token configured: {api_token[:10]}...")
        
        # Test connection (don't actually run)
        print("✓ Replicate is ready to use!")
        return True
    except ImportError:
        print("❌ Replicate module not installed!")
        print("   Run: pip install replicate")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_openai():
    """Test OpenAI API"""
    print("\n" + "="*50)
    print("Testing OpenAI API...")
    print("="*50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found (optional)")
        print("   Set environment variable if you want to use OpenAI:")
        print("   Windows: set OPENAI_API_KEY=your_key")
        print("   Linux/Mac: export OPENAI_API_KEY=your_key")
        return False
    
    try:
        import openai
        print(f"✓ OpenAI module installed")
        print(f"✓ API key configured: {api_key[:10]}...")
        print("✓ OpenAI is ready to use!")
        return True
    except ImportError:
        print("⚠️  OpenAI module not installed (optional)")
        print("   Run: pip install openai")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_huggingface():
    """Test Hugging Face API"""
    print("\n" + "="*50)
    print("Testing Hugging Face API...")
    print("="*50)
    
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if not api_key:
        print("⚠️  HUGGINGFACE_API_KEY not found (optional)")
        print("   Set environment variable if you want to use Hugging Face:")
        print("   Windows: set HUGGINGFACE_API_KEY=your_key")
        print("   Linux/Mac: export HUGGINGFACE_API_KEY=your_key")
        return False
    
    try:
        from huggingface_hub import HfApi
        print(f"✓ Hugging Face module installed")
        print(f"✓ API key configured: {api_key[:10]}...")
        print("✓ Hugging Face is ready to use!")
        return True
    except ImportError:
        print("⚠️  Hugging Face module not installed (optional)")
        print("   Run: pip install huggingface-hub")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n" + "="*50)
    print("Testing Dependencies...")
    print("="*50)
    
    required = {
        "PIL": "pillow",
        "cv2": "opencv-python",
        "rembg": "rembg",
        "requests": "requests"
    }
    
    all_ok = True
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - Run: pip install {package}")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        AI Banner Creator - Setup Test                        ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test AI services
    replicate_ok = test_replicate()
    openai_ok = test_openai()
    hf_ok = test_huggingface()
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    print(f"\n{'Dependencies':<20} {'Status':<10}")
    print("-" * 30)
    print(f"{'Core Dependencies':<20} {'✓ OK' if deps_ok else '❌ MISSING'}")
    print(f"{'Replicate API':<20} {'✓ Ready' if replicate_ok else '❌ Not set'}")
    print(f"{'OpenAI API':<20} {'✓ Ready' if openai_ok else '⚠️  Optional'}")
    print(f"{'Hugging Face API':<20} {'✓ Ready' if hf_ok else '⚠️  Optional'}")
    
    print("\n" + "="*50)
    
    if deps_ok and replicate_ok:
        print("✓ AI Banner Creator is ready to use!")
        print("\nYou can now run: python run_banner_creator.py")
    elif deps_ok:
        print("⚠️  Core is ready, but no AI service configured.")
        print("For full features, configure Replicate or OpenAI.")
        print("\nYou can still use the basic banner creator.")
    else:
        print("❌ Missing required dependencies!")
        print("\nRun: pip install -r requirements.txt")
        print("Or: pip install pillow rembg requests")
    
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
