"""
TEST IMPORT - Kiem tra tat ca cac module hoat dong
"""

print("\n" + "="*70)
print("  TESTING ALL IMPORTS & FUNCTIONALITY")
print("="*70 + "\n")

# Test 1: Core imports
print("[1/6] Testing core imports...")
try:
    import torch
    from PIL import Image
    import numpy as np
    import json
    from pathlib import Path
    print("      [OK] Core imports: torch, PIL, numpy, json, pathlib")
except Exception as e:
    print(f"      [FAIL] {e}")
    exit(1)

# Test 2: AI libraries
print("[2/6] Testing AI libraries...")
try:
    from diffusers import StableDiffusionInpaintPipeline
    from groq import Groq
    print("      [OK] AI libraries: diffusers, groq")
except Exception as e:
    print(f"      [FAIL] {e}")
    exit(1)

# Test 3: Project modules
print("[3/6] Testing project modules...")
try:
    from inpainting_helper import InpaintingHelper, BatchInpaintingProcessor
    from groq_integration import GroqTextGenerator, BatchTextGenerator
    print("      [OK] Project modules: inpainting_helper, groq_integration")
except Exception as e:
    print(f"      [FAIL] {e}")
    exit(1)

# Test 4: Create test image
print("[4/6] Creating test image...")
try:
    test_img = Image.new("RGBA", (200, 300), (255, 0, 0, 255))
    test_path = Path("output/test_image.png")
    test_img.save(test_path)
    print(f"      [OK] Test image created: {test_path}")
except Exception as e:
    print(f"      [FAIL] {e}")
    exit(1)

# Test 5: InpaintingHelper
print("[5/6] Testing InpaintingHelper...")
try:
    helper = InpaintingHelper()
    mask, resized, pos = helper.create_inpainting_mask(test_img)
    print(f"      [OK] Mask created: {mask.size}")
    print(f"          Resized product: {resized.size}")
    print(f"          Position: {pos}")
except Exception as e:
    print(f"      [FAIL] {e}")
    exit(1)

# Test 6: GroqTextGenerator
print("[6/6] Testing GroqTextGenerator...")
try:
    gen = GroqTextGenerator()  # No API key needed for init
    print("      [OK] GroqTextGenerator initialized")
    print("          (API key needed for actual generation)")
except Exception as e:
    print(f"      [FAIL] {e}")
    exit(1)

print("\n" + "="*70)
print("  ALL TESTS PASSED!")
print("="*70)

print("""
SUMMARY:
  [OK] Core libraries working
  [OK] AI libraries installed
  [OK] Project modules importable
  [OK] Test image creation works
  [OK] InpaintingHelper functional
  [OK] GroqTextGenerator ready

CONFIGURATION:
  Python: """ + f"{torch.__version__}" + """
  GPU: """ + ("Available" if torch.cuda.is_available() else "Not available (using CPU)") + """

READY TO RUN:
  python banner_creator_free_ai.py

OPTIONAL:
  - Get Groq API key: https://console.groq.com
  - Set: set GROQ_API_KEY=your_key (Windows)
  - Without key: Text generation will use fallback

FIRST RUN:
  1. Click "Download Inpainting" in Models tab
  2. Wait for model download (10-30 min, 7GB)
  3. Go to Quick Mode
  4. Select PNG product image
  5. Fill in Product Name
  6. (Optional) Add Groq API key
  7. Click CREATE BANNER
  8. Wait 1-2 minutes
  9. Banner ready!

GOOD TO GO!
""")
