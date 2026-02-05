#!/usr/bin/env python3
"""
QUICK START: 3-Layer Image Compositing
=======================================
Run this file to quickly test the pipeline
"""

import sys
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("🎨 3-LAYER IMAGE COMPOSITING - QUICK START")
    print("="*70 + "\n")
    
    print("📦 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check imports
    dependencies = {
        'PIL': 'Pillow',
        'numpy': 'numpy',
    }
    
    optional_deps = {
        'rembg': 'rembg (background removal)',
        'flask': 'flask (web API)',
        'replicate': 'replicate (AI)',
    }
    
    missing = []
    missing_optional = []
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"❌ {name}")
            missing.append(name)
    
    print("\nOptional dependencies:")
    for module, name in optional_deps.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"⚠ {name} (not required for basic demo)")
            missing_optional.append(name)
    
    # Show menu
    print("\n" + "="*70)
    print("AVAILABLE DEMOS")
    print("="*70 + "\n")
    
    demos = [
        ("1", "Basic Demo (Layer Compositing)", "layer_compositing.py"),
        ("2", "Advanced Demo (Smart Text)", "advanced_compositing.py"),
        ("3", "Test Full Pipeline", "test_pipeline.py"),
        ("4", "Background Removal", "background_removal.py"),
        ("5", "Stable Diffusion (AI Background)", "stable_diffusion_integration.py"),
        ("6", "Web API (Flask)", "app.py"),
    ]
    
    for num, desc, script in demos:
        print(f"{num}. {desc:<35} → python {script}")
    
    print("\n0. Exit")
    
    print("\n" + "="*70)
    
    # Get user choice
    try:
        choice = input("Choose demo (0-6): ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return True
    
    if choice == "0":
        print("👋 Goodbye!")
        return True
    
    scripts = {
        "1": "layer_compositing.py",
        "2": "advanced_compositing.py",
        "3": "test_pipeline.py",
        "4": "background_removal.py",
        "5": "stable_diffusion_integration.py",
        "6": "app.py",
    }
    
    script = scripts.get(choice)
    
    if not script:
        print("❌ Invalid choice")
        return False
    
    # Run script
    print(f"\n🚀 Running: {script}\n")
    print("="*70 + "\n")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, script], cwd=Path(__file__).parent)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
