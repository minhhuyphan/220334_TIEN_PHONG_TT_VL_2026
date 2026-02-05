"""
FREE & OPEN-SOURCE AI SYSTEM FOR BANNER CREATION
================================================
Hệ thống AI hoàn toàn miễn phí, chạy offline, không cần API keys

AI MODELS MIỄN PHÍ:
1. Stable Diffusion (ControlNet) - Tạo ảnh từ text
2. LLaMA / Mistral - Tạo text, slogan
3. YOLOv8 - Phát hiện đối tượng
4. OpenCV - Xử lý ảnh
5. PIL/Pillow - Thiết kế banner

LỢI ÍCH:
✅ Hoàn toàn miễn phí
✅ Không cần API keys
✅ Chạy offline (sau khi download model)
✅ Có thể tự huấn luyện
✅ Kiểm soát toàn bộ quy trình
"""

import os
import sys
from pathlib import Path

def print_free_ai_options():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   FREE & OPEN-SOURCE AI OPTIONS                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

1️⃣  STABLE DIFFUSION (TẠO ẢNH)
────────────────────────────────────
Model: stabilityai/stable-diffusion-2 (hoặc v3)
Size: ~7GB (mô hình nhỏ)
Chạy: Local GPU/CPU
Chi phí: Miễn phí
Speed: 30-60 giây/ảnh (GPU), 3-5 phút (CPU)

Cài đặt:
    pip install diffusers transformers torch xformers
    pip install accelerate safetensors omegaconf

Code:
    from diffusers import StableDiffusionPipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2",
        torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda")  # GPU
    image = pipe("modern tech background").images[0]
    image.save("banner_bg.png")

═══════════════════════════════════════════════════════════════════════════════

2️⃣  CONTROLNET (KIỂM SOÁT LAYOUT)
────────────────────────────────────
Model: lllyasviel/ControlNet
Size: ~2GB
Dùng với: Stable Diffusion
Tính năng: Kiểm soát pose, edge, depth

Code:
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
    
    controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny")
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        controlnet=controlnet
    )

═══════════════════════════════════════════════════════════════════════════════

3️⃣  LLAMA 2 / MISTRAL (TẠO TEXT & SLOGAN)
────────────────────────────────────────
Model: meta-llama/Llama-2-7b hoặc mistralai/Mistral-7B
Size: ~14GB (7B model)
Chạy: Local CPU/GPU
Chi phí: Miễn phí
Speed: 20-100 tokens/giây

Cài đặt:
    pip install transformers torch bitsandbytes

Code:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    model_name = "mistralai/Mistral-7B-Instruct-v0.1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    prompt = "Tạo 5 slogan quảng cáo cho sản phẩm điện thoại sale 30%"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=200)
    text = tokenizer.decode(outputs[0])

═══════════════════════════════════════════════════════════════════════════════

4️⃣  YOLOV8 (PHÁT HIỆN & PHÂN TÍCH SẢN PHẨM)
─────────────────────────────────────────
Model: YOLOv8
Size: ~50MB
Dùng: Phát hiện sản phẩm, background
Chi phí: Miễn phí
Speed: <100ms

Cài đặt:
    pip install ultralytics

Code:
    from ultralytics import YOLO
    
    model = YOLO("yolov8m.pt")  # medium model
    results = model.predict(source="product.jpg")
    
    # Lấy bounding box, confidence
    for r in results:
        for box in r.boxes:
            print(f"Confidence: {box.conf}")

═══════════════════════════════════════════════════════════════════════════════

5️⃣  OPENCV & PIL (XỬ LÝ & THIẾT KẾ)
──────────────────────────────────
Chi phí: Miễn phí
Dùng: Xử lý ảnh, overlay, gradient

Code:
    import cv2
    from PIL import Image, ImageDraw
    
    # Tách nền bằng GrabCut
    img = cv2.imread("product.jpg")
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    
    cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, 
                cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]

═══════════════════════════════════════════════════════════════════════════════

6️⃣  WHISPER (SPEECH TO TEXT - BONUS)
──────────────────────────────────
Model: openai/whisper
Size: ~400MB-3GB
Chi phí: Miễn phí
Dùng: Chuyển giọng nói → text → slogan

Cài đặt:
    pip install openai-whisper

Code:
    import whisper
    
    model = whisper.load_model("base")  # or "small", "medium"
    result = model.transcribe("audio.mp3")
    print(result["text"])

═══════════════════════════════════════════════════════════════════════════════

SETUP INSTRUCTIONS
==================

1. CÀI ĐẶT PYTORCH (GPU - khuyến nghị):
   
   # NVIDIA GPU:
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   
   # Apple Silicon (M1/M2/M3):
   pip install torch torchvision torchaudio
   
   # CPU only:
   pip install torch torchvision torchaudio

2. CÀI ĐẶT AI LIBRARIES:
   
   pip install diffusers transformers accelerate
   pip install ultralytics yolo
   pip install pillow opencv-python numpy
   pip install xformers safetensors omegaconf einops

3. DOWNLOAD MODELS (lần đầu):
   
   python download_models.py  # Sẽ tạo file này

4. RUN SYSTEM:
   
   python banner_creator_free_ai.py

REQUIREMENTS FILE
=================

Tạo requirements.txt:

torch==2.1.0
torchvision==0.16.0
torchaudio==2.1.0
transformers==4.36.0
diffusers==0.21.0
accelerate==0.24.0
safetensors==0.4.0
xformers==0.0.23
pillow==10.0.0
opencv-python==4.8.0
ultralytics==8.0.0
numpy==1.24.0
omegaconf==2.3.0

Cài đặt:
    pip install -r requirements.txt

QUANT MODELS (NHỎ & NHANH HƠN)
==============================

Nếu GPU RAM <8GB, dùng quantized models:

1. Stable Diffusion (4GB vram):
   from diffusers import StableDiffusionPipeline
   pipe = StableDiffusionPipeline.from_pretrained(
       "runwayml/stable-diffusion-v1-5",
       torch_dtype=torch.float16
   )

2. LLaMA (8-bit):
   from transformers import AutoModelForCausalLM
   model = AutoModelForCausalLM.from_pretrained(
       "mistralai/Mistral-7B",
       load_in_8bit=True,
       device_map="auto"
   )

TỰ HUẤN LUYỆN (TRAINING)
========================

Option 1: FINE-TUNE STABLE DIFFUSION
─────────────────────────────────────
Dùng LoRA (Low-Rank Adaptation) - chỉ cần 8GB VRAM

Cài đặt:
    pip install peft diffusers transformers accelerate

Script:
    python train_lora.py \\
        --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \\
        --dataset_name="path/to/images" \\
        --output_dir="./lora_weights"

Option 2: FINE-TUNE LLAMA
────────────────────────
Dùng QLoRA - chỉ cần 6GB VRAM

Cài đặt:
    pip install peft bitsandbytes datasets

Script:
    python train_qlora.py \\
        --model_name="mistralai/Mistral-7B" \\
        --data_path="slogan_dataset.json" \\
        --output_dir="./qlora_weights"

PERFORMANCE & HARDWARE
======================

GPU REQUIREMENTS:
- RTX 3060 (12GB): ✓ Stable Diffusion + LLaMA 7B
- RTX 4070 (12GB): ✓ Stable Diffusion (fast) + LLaMA 13B
- RTX 4090 (24GB): ✓✓ Tất cả models, batch processing

CPU ONLY:
- Intel i7/i9: ✓ LLaMA 7B (slow, ~10s/prompt)
- Intel i9-13900K: ✓ SD (slow, ~2min/image)

SPEED ESTIMATES:
- Stable Diffusion: 5-30s (GPU), 2-5min (CPU)
- LLaMA 7B: 0.5-2s (GPU), 5-30s (CPU)
- YOLO detection: <100ms (GPU), <1s (CPU)

COST BREAKDOWN
==============

ONE-TIME:
- GPU card (RTX 4070): $500-700
- Or use free tier: Google Colab, Kaggle

PER BANNER:
- GPU electricity: ~$0.001
- Storage: ~$0.0001
- TOTAL: ~$0.001 per banner

vs Replicate API: $0.01 per banner = 10x cheaper!

RECOMMENDATION
==============

Best Setup for FREE:
1. GPU: RTX 3060 or better (used ~$200-300)
2. Or: Use Google Colab Free + Drive
3. Models: Mistral-7B + SD 2.1 Turbo

Result:
- 0 API costs
- Unlimited banners
- Full control
- Can train on your data

NEXT STEPS
==========

1. ✅ Install PyTorch
2. ✅ Install diffusers + transformers
3. ✅ Download models (or use Colab)
4. ✅ Run banner_creator_free_ai.py
5. ⏳ Fine-tune on your product images
6. ⏳ Train custom slogan generator
""")

if __name__ == "__main__":
    print_free_ai_options()
