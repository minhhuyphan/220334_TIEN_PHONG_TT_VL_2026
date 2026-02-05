"""
Script: Web API Flask
====================
API web để upload ảnh sản phẩm, tạo nền AI, ghép lớp + thêm chữ

Yêu cầu:
- pip install flask pillow rembg requests
"""

from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import io
import json
from datetime import datetime
from werkzeug.utils import secure_filename

# Import các module của chúng ta
import sys
sys.path.insert(0, str(Path(__file__).parent))

from layer_compositing import LayerCompositor
from background_removal import BackgroundRemover
from stable_diffusion_integration import StableDiffusionGenerator


app = Flask(__name__)

# Cấu hình
UPLOAD_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "service": "3-Layer Image Compositing API",
        "version": "1.0"
    })


@app.route('/api/generate-background', methods=['POST'])
def generate_background():
    """
    API: Tạo nền bằng Stable Diffusion
    
    Body:
    {
        "prompt": "modern blue background, sportswear",
        "width": 800,
        "height": 600,
        "api_type": "local" (hoặc "replicate")
    }
    """
    try:
        data = request.json or {}
        
        prompt = data.get('prompt', 'professional product background')
        width = data.get('width', 800)
        height = data.get('height', 600)
        api_type = data.get('api_type', 'local')
        
        print(f"\n📡 Request: Tạo nền AI")
        print(f"   Prompt: {prompt}")
        print(f"   Kích thước: {width}x{height}")
        
        generator = StableDiffusionGenerator(api_type=api_type)
        image = generator.generate_background(prompt, width, height)
        
        if image:
            # Lưu ảnh
            filename = f"bg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = OUTPUT_FOLDER / filename
            image.save(filepath)
            
            return jsonify({
                "success": True,
                "filename": filename,
                "size": image.size,
                "message": "Tạo nền thành công"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Không thể tạo nền (kiểm tra API)"
            }), 400
    
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    """
    API: Tách nền ảnh sản phẩm
    
    Form:
    - file: ảnh upload
    """
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "Không có file"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"success": False, "error": "File trống"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Format không hỗ trợ"}), 400
        
        print(f"\n📡 Request: Tách nền")
        print(f"   File: {file.filename}")
        
        # Lưu file tạm
        filename = secure_filename(file.filename)
        input_path = UPLOAD_FOLDER / filename
        file.save(input_path)
        
        # Tách nền
        remover = BackgroundRemover()
        output_filename = f"{Path(filename).stem}_no_bg.png"
        output_path = OUTPUT_FOLDER / output_filename
        
        result_image = remover.remove_background(str(input_path), str(output_path))
        
        if result_image:
            return jsonify({
                "success": True,
                "filename": output_filename,
                "size": result_image.size,
                "mode": result_image.mode,
                "message": "Tách nền thành công"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Không thể tách nền"
            }), 400
    
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/create-banner', methods=['POST'])
def create_banner():
    """
    API: Tạo banner từ sản phẩm + nền + chữ
    
    Body:
    {
        "background_file": "bg.png" (hoặc "solid_color"),
        "product_file": "product_no_bg.png",
        "text": "Siêu Sale",
        "text_color": [255, 255, 0],
        "bg_color": [100, 150, 200],
        "width": 800,
        "height": 600
    }
    """
    try:
        data = request.json or {}
        
        width = data.get('width', 800)
        height = data.get('height', 600)
        text = data.get('text', 'Sale')
        text_color = tuple(data.get('text_color', [255, 255, 0]))
        bg_color = tuple(data.get('bg_color', [100, 150, 200]))
        background_file = data.get('background_file', 'solid_color')
        product_file = data.get('product_file')
        
        print(f"\n📡 Request: Tạo banner")
        print(f"   Text: {text}")
        print(f"   Kích thước: {width}x{height}")
        
        # Tạo compositor
        compositor = LayerCompositor(width=width, height=height)
        
        # Lớp 1: Background
        if background_file == 'solid_color':
            compositor.create_background(color_gradient=False)
            # Đặt màu nền
            compositor.background_layer = Image.new('RGB', (width, height), color=bg_color)
        elif background_file.startswith(('http://', 'https://')):
            # Load từ URL
            import requests
            response = requests.get(background_file)
            bg_img = Image.open(io.BytesIO(response.content))
            bg_img = bg_img.resize((width, height))
            compositor.background_layer = bg_img
        else:
            # Load từ file
            bg_path = OUTPUT_FOLDER / background_file
            if bg_path.exists():
                bg_img = Image.open(bg_path).resize((width, height))
                compositor.background_layer = bg_img
            else:
                compositor.create_background(color_gradient=True)
        
        # Lớp 2: Product
        if product_file:
            prod_path = OUTPUT_FOLDER / product_file
            if prod_path.exists():
                product_img = Image.open(prod_path)
                # Resize product để phù hợp
                max_size = int(min(width, height) * 0.4)
                product_img.thumbnail((max_size, max_size))
                compositor.product_layer = product_img
                compositor.composite_layers()
        
        # Lớp 3: Text
        if text:
            compositor.add_text_overlay(
                text=text,
                font_size=50,
                text_color=text_color,
                background_overlay=True
            )
        
        # Lưu kết quả
        output_filename = f"banner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        output_path = OUTPUT_FOLDER / output_filename
        compositor.save_result(str(output_path))
        
        return jsonify({
            "success": True,
            "filename": output_filename,
            "size": (width, height),
            "message": "Tạo banner thành công"
        })
    
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_image(filename):
    """Tải ảnh xuống"""
    try:
        filepath = OUTPUT_FOLDER / secure_filename(filename)
        
        if not filepath.exists():
            return jsonify({"error": "File không tồn tại"}), 404
        
        return send_file(
            filepath,
            mimetype='image/png',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    """Liệt kê tất cả ảnh đã tạo"""
    try:
        files = []
        for file in OUTPUT_FOLDER.glob("*"):
            if file.is_file() and allowed_file(file.name):
                files.append({
                    "name": file.name,
                    "size": file.stat().st_size,
                    "created": datetime.fromtimestamp(file.stat().st_ctime).isoformat()
                })
        
        return jsonify({
            "success": True,
            "count": len(files),
            "files": sorted(files, key=lambda x: x['created'], reverse=True)
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# HTML frontend
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>3-Layer Image Compositing API</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }
            header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            h1 { font-size: 28px; margin-bottom: 10px; }
            .subtitle { opacity: 0.9; font-size: 14px; }
            main {
                padding: 30px;
            }
            .section {
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: #f9f9f9;
            }
            h2 {
                font-size: 18px;
                margin-bottom: 15px;
                color: #333;
                border-bottom: 2px solid #667eea;
                padding-bottom: 10px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #555;
            }
            input, textarea, select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-family: inherit;
                font-size: 14px;
            }
            button {
                background: #667eea;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.3s;
            }
            button:hover {
                background: #764ba2;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .status {
                margin-top: 15px;
                padding: 15px;
                border-radius: 4px;
                display: none;
            }
            .status.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                display: block;
            }
            .status.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
                display: block;
            }
            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            @media (max-width: 600px) {
                .grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🎨 3-Layer Image Compositing API</h1>
                <p class="subtitle">Tạo banner quảng cáo với AI + Image Processing</p>
            </header>
            
            <main>
                <!-- Section 1: Remove Background -->
                <div class="section">
                    <h2>1️⃣ Tách nền sản phẩm (Lớp 2)</h2>
                    <div class="form-group">
                        <label>Chọn ảnh sản phẩm:</label>
                        <input type="file" id="productFile" accept="image/*">
                    </div>
                    <button onclick="removeBackground()">Tách nền</button>
                    <div id="bgStatus" class="status"></div>
                </div>
                
                <!-- Section 2: Generate Background -->
                <div class="section">
                    <h2>2️⃣ Tạo nền AI (Lớp 1)</h2>
                    <div class="form-group">
                        <label>Mô tả nền:</label>
                        <textarea id="bgPrompt" rows="3" placeholder="VD: modern blue gradient background for fashion"></textarea>
                    </div>
                    <div class="grid">
                        <div class="form-group">
                            <label>Rộng (pixels):</label>
                            <input type="number" id="bgWidth" value="800" min="256" max="1024">
                        </div>
                        <div class="form-group">
                            <label>Cao (pixels):</label>
                            <input type="number" id="bgHeight" value="600" min="256" max="1024">
                        </div>
                    </div>
                    <button onclick="generateBackground()">Tạo nền</button>
                    <div id="genStatus" class="status"></div>
                </div>
                
                <!-- Section 3: Create Banner -->
                <div class="section">
                    <h2>3️⃣ Tạo banner (Ghép lớp + chữ)</h2>
                    <div class="form-group">
                        <label>Dòng chữ:</label>
                        <input type="text" id="bannerText" value="🔥 SIÊU SALE 50%">
                    </div>
                    <div class="grid">
                        <div class="form-group">
                            <label>Màu chữ (R):</label>
                            <input type="number" id="colorR" value="255" min="0" max="255">
                        </div>
                        <div class="form-group">
                            <label>Màu chữ (G):</label>
                            <input type="number" id="colorG" value="255" min="0" max="255">
                        </div>
                    </div>
                    <button onclick="createBanner()">Tạo Banner</button>
                    <div id="bannerStatus" class="status"></div>
                </div>
            </main>
        </div>
        
        <script>
            async function removeBackground() {
                const file = document.getElementById('productFile').files[0];
                if (!file) {
                    showStatus('bgStatus', 'Chọn ảnh trước', 'error');
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    const response = await fetch('/api/remove-background', {
                        method: 'POST',
                        body: formData
                    });
                    const data = await response.json();
                    
                    if (data.success) {
                        showStatus('bgStatus', '✅ ' + data.message + ' (' + data.filename + ')', 'success');
                    } else {
                        showStatus('bgStatus', '❌ ' + data.error, 'error');
                    }
                } catch (e) {
                    showStatus('bgStatus', '❌ Lỗi: ' + e.message, 'error');
                }
            }
            
            async function generateBackground() {
                const prompt = document.getElementById('bgPrompt').value;
                const width = parseInt(document.getElementById('bgWidth').value);
                const height = parseInt(document.getElementById('bgHeight').value);
                
                if (!prompt) {
                    showStatus('genStatus', 'Nhập mô tả nền', 'error');
                    return;
                }
                
                try {
                    const response = await fetch('/api/generate-background', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt, width, height, api_type: 'local' })
                    });
                    const data = await response.json();
                    
                    if (data.success) {
                        showStatus('genStatus', '✅ Tạo nền thành công (' + data.filename + ')', 'success');
                    } else {
                        showStatus('genStatus', '❌ ' + data.error, 'error');
                    }
                } catch (e) {
                    showStatus('genStatus', '❌ Lỗi: ' + e.message, 'error');
                }
            }
            
            async function createBanner() {
                const text = document.getElementById('bannerText').value;
                const r = parseInt(document.getElementById('colorR').value);
                const g = parseInt(document.getElementById('colorG').value);
                
                if (!text) {
                    showStatus('bannerStatus', 'Nhập dòng chữ', 'error');
                    return;
                }
                
                try {
                    const response = await fetch('/api/create-banner', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            background_file: 'solid_color',
                            product_file: null,
                            text: text,
                            text_color: [r, g, 0],
                            bg_color: [100, 150, 200],
                            width: 800,
                            height: 600
                        })
                    });
                    const data = await response.json();
                    
                    if (data.success) {
                        showStatus('bannerStatus', '✅ ' + data.message + ' (' + data.filename + ')', 'success');
                    } else {
                        showStatus('bannerStatus', '❌ ' + data.error, 'error');
                    }
                } catch (e) {
                    showStatus('bannerStatus', '❌ Lỗi: ' + e.message, 'error');
                }
            }
            
            function showStatus(elementId, message, type) {
                const el = document.getElementById(elementId);
                el.textContent = message;
                el.className = 'status ' + type;
            }
        </script>
    </body>
    </html>
    """


def main():
    print("\n" + "="*60)
    print("🚀 3-LAYER IMAGE COMPOSITING API")
    print("="*60)
    print("\n📡 Server chạy tại: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET  /               - Giao diện web")
    print("  GET  /api/health     - Kiểm tra trạng thái")
    print("  POST /api/remove-background  - Tách nền")
    print("  POST /api/generate-background - Tạo nền AI")
    print("  POST /api/create-banner     - Tạo banner")
    print("  GET  /api/files     - Liệt kê ảnh")
    print("  GET  /api/download/<filename> - Tải ảnh")
    print("\n" + "="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
