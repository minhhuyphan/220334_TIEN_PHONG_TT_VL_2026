"""
Download Stable Diffusion 2.1 Model
This will cache the 7GB model locally for AI banner generation
"""

import torch
from diffusers import StableDiffusionPipeline
import sys

print("=" * 60)
print("Downloading Stable Diffusion 2.1 Model (7GB)")
print("=" * 60)
print()
print("⏳ This will take 5-15 minutes...")
print("✅ Model will be cached locally")
print()

try:
    print("Step 1: Checking CUDA...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    print()
    
    print("Step 2: Downloading model from Hugging Face...")
    print("(This may take several minutes)")
    print()
    
    # Try Stable Diffusion 1.5 (more accessible)
    print("Note: Using Stable Diffusion 1.5 (easier access)")
    model = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
        safety_checker=None,
        use_auth_token=False
    )
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! Model downloaded and cached!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Go back to browser (http://localhost:8501)")
    print("2. Refresh the page (Ctrl+R)")
    print("3. Go to 'AI Banner' tab")
    print("4. Upload image and create AI banner!")
    print()
    print("Model location: ~/.cache/huggingface/")
    print()
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERROR during download:")
    print("=" * 60)
    print(f"{e}")
    print()
    print("Possible fixes:")
    print("1. Check internet connection")
    print("2. Check disk space (need 10GB free)")
    print("3. Try again in a few minutes")
    print()

input("Press Enter to close...")
