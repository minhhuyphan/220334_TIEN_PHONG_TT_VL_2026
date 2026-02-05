"""
SETUP SCRIPT - Chuan bi toan bo moi truong

Giai phap don gian - khong dung Unicode special characters
"""

import os
import sys
import json
from pathlib import Path


def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def main():
    print("\n" + "="*70)
    print("  BANNER CREATOR v2.0 - SETUP & PREPARATION")
    print("="*70)
    
    # Step 1: Environment
    print_header("STEP 1: ENVIRONMENT CHECK")
    python_version = sys.version_info
    print(f"Python: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 10):
        print("ERROR: Python 3.10+ required!")
        return False
    print("[OK] Python version OK")
    
    if sys.prefix != sys.base_prefix:
        print("[OK] Virtual environment activated")
    else:
        print("[WARNING] Not in virtual environment")
    
    # Step 2: Check imports
    print_header("STEP 2: VERIFY IMPORTS")
    
    imports = {
        "torch": "PyTorch",
        "PIL": "Pillow",
        "diffusers": "Diffusers",
        "groq": "Groq",
        "numpy": "NumPy",
        "cv2": "OpenCV",
    }
    
    failed_imports = []
    for module, name in imports.items():
        try:
            __import__(module)
            print(f"[OK] {name}")
        except ImportError as e:
            print(f"[FAIL] {name}")
            failed_imports.append(name)
    
    if failed_imports:
        print(f"\nERROR: Missing packages: {', '.join(failed_imports)}")
        print("\nInstall with:")
        print(f"  {sys.executable} -m pip install -r requirements_inpainting.txt")
        return False
    
    print("\n[OK] All imports verified!")
    
    # Step 3: GPU check
    print_header("STEP 3: GPU CHECK")
    
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print("[OK] GPU detected!")
            device = torch.cuda.get_device_name(0)
            vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"     Device: {device}")
            print(f"     VRAM: {vram:.1f} GB")
            
            if vram < 12:
                print(f"     [WARNING] {vram:.1f}GB < 12GB recommended")
        else:
            print("[WARNING] No GPU detected")
            print("           Using CPU (will be slow)")
    except Exception as e:
        print(f"[ERROR] GPU check failed: {str(e)[:100]}")
    
    # Step 4: Directory prep
    print_header("STEP 4: PREPARE DIRECTORIES")
    
    dirs = ["output", "input", "models"]
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"[OK] {dir_name}/ exists")
        else:
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"[OK] Created {dir_name}/")
            except Exception as e:
                print(f"[FAIL] Could not create {dir_name}/: {e}")
                return False
    
    # Step 5: Config
    print_header("STEP 5: CONFIGURATION")
    
    config_file = Path("inpainting_config.json")
    if not config_file.exists():
        print("[INFO] Creating default config...")
        config = {
            "banner_settings": {
                "width": 1200,
                "height": 630,
                "product_width_percent": 0.35
            },
            "inpainting_settings": {
                "num_inference_steps": 50,
                "guidance_scale": 7.5
            },
            "groq_settings": {
                "enabled": True,
                "model": "mixtral-8x7b-32768"
            }
        }
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"[OK] Created {config_file}")
        except Exception as e:
            print(f"[ERROR] Could not create config: {e}")
            return False
    else:
        print(f"[OK] Config file exists: {config_file}")
    
    # Step 6: Groq API
    print_header("STEP 6: GROQ API SETUP")
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        print(f"[OK] GROQ_API_KEY is set (first 10: {api_key[:10]}...)")
    else:
        print("[WARNING] GROQ_API_KEY not set")
        print("")
        print("To setup Groq API:")
        print("1. Go to: https://console.groq.com")
        print("2. Create free account")
        print("3. Get API key")
        print("4. Set environment:")
        print("   Windows: set GROQ_API_KEY=your_key")
        print("   Linux: export GROQ_API_KEY='your_key'")
        print("")
        print("Without API key: Text will use product name as fallback")
    
    # Final summary
    print_header("SETUP COMPLETE!")
    
    print("""
SUMMARY:
  [OK] Python environment ready
  [OK] All dependencies installed  
  [OK] Imports verified
  [OK] Directories prepared
  [OK] Configuration ready
  
NEXT STEPS:

1. (Optional) Setup Groq API key:
   https://console.groq.com
   
2. Run the application:
   python banner_creator_free_ai.py
   
3. Create your first banner!

FIRST RUN:
  - Model will download automatically (~7GB, 10-30 min)
  - Select PNG image with transparent background
  - Fill in Product Name and Groq API key
  - Click CREATE BANNER
  
DOCUMENTATION:
  - QUICKSTART_INPAINTING.py - 5 min setup
  - README_INPAINTING.md - Complete guide
  - INPAINTING_GUIDE.py - Detailed docs
  
REQUIREMENTS:
  - GPU: Optional (RTX 3060+ 12GB recommended)
  - RAM: 16GB
  - Storage: 20GB
  
READY TO GO!
""")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
