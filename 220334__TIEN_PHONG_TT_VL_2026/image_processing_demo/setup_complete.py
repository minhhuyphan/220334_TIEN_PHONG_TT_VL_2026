"""
🚀 SETUP SCRIPT - Chuẩn Bị Toàn Bộ Môi Trường

Bước chuẩn bị 5 bước để chạy Banner Creator v2.0
"""

import os
import sys
import json
from pathlib import Path
import subprocess


def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def run_command(cmd, description=""):
    """Run a command and return success status"""
    if description:
        print(f"⏳ {description}...")
    try:
        # Use shell and handle encoding
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=str(Path.cwd())
        )
        if result.returncode == 0:
            print(f"✓ {description} - OK")
            return True
        else:
            print(f"✗ {description} - FAILED")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"✗ {description} - ERROR: {str(e)[:100]}")
        return False


def setup_environment():
    """Setup Python environment"""
    print_header("STEP 1: ENVIRONMENT SETUP")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 10):
        print("❌ Python 3.10+ required!")
        return False
    print("✓ Python version OK")
    
    # Check virtual environment
    if sys.prefix != sys.base_prefix:
        print("✓ Virtual environment activated")
    else:
        print("⚠️  Not in virtual environment (recommended to activate)")
    
    return True


def install_dependencies():
    """Install all required dependencies"""
    print_header("STEP 2: INSTALL DEPENDENCIES")
    
    # Check if requirements file exists
    req_file = Path("requirements_inpainting.txt")
    if not req_file.exists():
        print("❌ requirements_inpainting.txt not found!")
        return False
    
    print(f"Installing from: {req_file}")
    
    # Install PyTorch GPU
    print("\n📦 Installing PyTorch (GPU - CUDA 11.8)...")
    torch_cmd = f'"{sys.executable}" -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --upgrade -q'
    if not run_command(torch_cmd, "PyTorch"):
        print("⚠️  PyTorch install failed (might work anyway)")
    
    # Install main requirements
    print("\n📦 Installing all requirements...")
    pip_cmd = f'"{sys.executable}" -m pip install -r "{req_file}" --upgrade -q'
    if not run_command(pip_cmd, "Requirements"):
        print("❌ Failed to install requirements")
        return False
    
    print("\n✓ All dependencies installed successfully!")
    return True


def verify_imports():
    """Verify all imports work"""
    print_header("STEP 3: VERIFY IMPORTS")
    
    imports_to_check = {
        "torch": "PyTorch",
        "PIL": "Pillow",
        "diffusers": "Diffusers",
        "groq": "Groq",
        "numpy": "NumPy",
        "cv2": "OpenCV",
        "rembg": "RemBg"
    }
    
    failed = []
    for module, name in imports_to_check.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - MISSING")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Missing: {', '.join(failed)}")
        return False
    
    print(f"\n✓ All imports verified!")
    return True


def check_gpu():
    """Check GPU availability"""
    print_header("STEP 4: CHECK GPU & HARDWARE")
    
    import torch
    
    print(f"PyTorch version: {torch.__version__}")
    
    if torch.cuda.is_available():
        print(f"✓ GPU detected!")
        device_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
        print(f"   Device: {device_name}")
        print(f"   VRAM: {vram_gb:.1f} GB")
        
        if vram_gb < 12:
            print(f"   ⚠️  Warning: {vram_gb:.1f}GB < 12GB recommended")
            print(f"   You can still use CPU mode (slower)")
        
        return True
    else:
        print("⚠️  No GPU detected")
        print("   You can use CPU mode (will be slow)")
        print("   For GPU: Install NVIDIA drivers + CUDA toolkit")
        return False


def setup_groq():
    """Setup Groq API"""
    print_header("STEP 5: SETUP GROQ API (Optional but Recommended)")
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if api_key:
        print(f"✓ GROQ_API_KEY already set (first 10 chars: {api_key[:10]}...)")
        return True
    else:
        print("⚠️  GROQ_API_KEY not set")
        print("\nTo setup Groq API:")
        print("1. Go to: https://console.groq.com")
        print("2. Create free account")
        print("3. Create API key")
        print("4. Set environment variable:")
        print("   Windows: set GROQ_API_KEY=your_key")
        print("   Linux/Mac: export GROQ_API_KEY='your_key'")
        print("\nWithout API key: Text generation will use fallback (product name)")
        return False


def prepare_directories():
    """Prepare output directories"""
    print_header("STEP 6: PREPARE DIRECTORIES")
    
    dirs = ["output", "models", "input"]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}/ exists")
        else:
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"✓ Created {dir_name}/")
            except Exception as e:
                print(f"✗ Failed to create {dir_name}/: {e}")
                return False
    
    return True


def download_model():
    """Download Stable Diffusion Inpainting model"""
    print_header("STEP 7: DOWNLOAD MODEL (Optional - 7GB)")
    
    print("Stable Diffusion Inpainting Model:")
    print("• Size: ~7GB (download once)")
    print("• Location: ~/.cache/huggingface/")
    print("• First time: 10-30 minutes")
    
    response = input("\nDownload model now? (y/n): ").lower().strip()
    
    if response == 'y':
        print("\n⏳ Downloading model (this may take 10-30 minutes)...")
        print("Please wait...\n")
        
        try:
            import torch
            from diffusers import StableDiffusionInpaintPipeline
            
            print("Loading Stable Diffusion Inpainting...")
            
            pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None
            )
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            pipe = pipe.to(device)
            
            print(f"\n✓ Model loaded successfully on {device}!")
            return True
        
        except Exception as e:
            print(f"\n❌ Model download failed: {str(e)[:200]}")
            print("You can download it later when running the application")
            return False
    else:
        print("⏭️  Skipping model download")
        print("   You can download later when running the application")
        return None


def create_config():
    """Create/update configuration file"""
    print_header("STEP 8: CONFIGURE SETTINGS")
    
    config_file = Path("inpainting_config.json")
    
    # Create default config if not exists
    if not config_file.exists():
        default_config = {
            "banner_settings": {
                "width": 1200,
                "height": 630,
                "product_width_percent": 0.35
            },
            "inpainting_settings": {
                "num_inference_steps": 50,
                "guidance_scale": 7.5,
                "enabled": True
            },
            "groq_settings": {
                "enabled": True,
                "model": "mixtral-8x7b-32768"
            }
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"✓ Created {config_file}")
        except Exception as e:
            print(f"❌ Failed to create config: {e}")
            return False
    else:
        print(f"✓ Config file already exists: {config_file}")
    
    return True


def run_tests():
    """Run test suite"""
    print_header("STEP 9: RUN TESTS")
    
    print("Running validation tests...\n")
    
    result = subprocess.run(
        f'"{sys.executable}" test_inpainting_setup.py',
        shell=True,
        capture_output=False,
        text=True
    )
    
    return result.returncode == 0


def final_summary():
    """Show final summary and next steps"""
    print_header("✅ SETUP COMPLETE!")
    
    print("""
📋 WHAT'S READY:
  ✓ Python environment configured
  ✓ All dependencies installed
  ✓ Imports verified
  ✓ Directories created
  ✓ Configuration prepared

⚠️  WHAT'S OPTIONAL:
  • GPU setup (works on CPU, slower)
  • Groq API key (works without, text = product name)
  • Model download (done automatically on first run)

🚀 NEXT STEPS:

1. (Optional) Get Groq API Key:
   https://console.groq.com
   Set: export GROQ_API_KEY="your_key"

2. Run the application:
   python banner_creator_free_ai.py

3. Create your first banner!

📚 DOCUMENTATION:
  • QUICKSTART_INPAINTING.py - 5 min quick start
  • README_INPAINTING.md - Complete guide
  • INPAINTING_GUIDE.py - Detailed documentation

🎯 REQUIREMENTS RECAP:
  • GPU: Optional (RTX 3060+ recommended)
  • RAM: 16GB
  • Disk: 20GB (for models)
  • Internet: For Groq API & model download

═══════════════════════════════════════════════════

Ready to create amazing banners! 🎉

Run: python banner_creator_free_ai.py
""")


def main():
    """Main setup flow"""
    
    print("\n")
    print("=" * 70)
    print("=  BANNER CREATOR v2.0 - SETUP & PREPARATION")
    print("=" * 70)
    
    steps = [
        ("Environment", setup_environment),
        ("Dependencies", install_dependencies),
        ("Imports", verify_imports),
        ("GPU", check_gpu),
        ("Groq", setup_groq),
        ("Directories", prepare_directories),
        ("Model", download_model),
        ("Config", create_config),
    ]
    
    passed = 0
    failed = 0
    
    for i, (name, func) in enumerate(steps, 1):
        try:
            if name == "Model":  # Optional step
                result = func()
                if result is None:
                    print(f"⏭️  {name} skipped (optional)")
                elif result:
                    passed += 1
                else:
                    failed += 1
            else:  # Required steps
                if func():
                    passed += 1
                else:
                    failed += 1
                    if name in ["Environment", "Dependencies", "Imports"]:
                        print(f"\n❌ Setup incomplete! Cannot continue.")
                        return False
        except Exception as e:
            print(f"\n❌ Error in {name}: {str(e)[:100]}")
            failed += 1
    
    final_summary()
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
