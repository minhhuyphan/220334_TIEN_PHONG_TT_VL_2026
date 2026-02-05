# 📚 3-Layer Image Compositing - Documentation Index

## 🚀 Quick Navigation

### For Beginners

1. **Start here:** [README.md](README.md) - Basic overview
2. **Quick start:** Run `python quickstart.py`
3. **First demo:** `python layer_compositing.py`

### For Developers

1. **Integration:** [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - Detailed API docs
2. **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md) - System design
3. **Project structure:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### For Deployment

1. **Docker:** See docker-compose.yml
2. **Production:** Flask with Gunicorn
3. **Scaling:** Load balancer + Worker pool

---

## 📁 Directory Structure

```
image_processing_demo/
│
├── 📖 DOCUMENTATION
│   ├── README.md                    ← START HERE
│   ├── INTEGRATION_GUIDE.md         ← API Reference
│   ├── ARCHITECTURE.md              ← System Design
│   ├── PROJECT_SUMMARY.md           ← Overview
│   ├── INDEX.md                     ← This file
│   └── QUICK_START.md               ← Setup guide
│
├── 🎯 MAIN MODULES
│   ├── layer_compositing.py         ← Demo (Basic)
│   ├── advanced_compositing.py      ← Demo (Advanced)
│   ├── background_removal.py        ← Module (Layer 2)
│   ├── stable_diffusion_integration.py ← Module (Layer 1)
│   └── app.py                       ← Web API (Flask)
│
├── 🧪 TESTING & TOOLS
│   ├── test_pipeline.py             ← Full test suite
│   ├── quickstart.py                ← Interactive menu
│   ├── requirements.txt             ← Dependencies
│   └── run.bat / run.sh             ← Startup scripts
│
├── 🐳 DEPLOYMENT
│   ├── Dockerfile                   ← Docker image
│   ├── docker-compose.yml           ← Docker orchestration
│   └── .gitignore                   ← Git config
│
└── 📂 RUNTIME FOLDERS (created automatically)
    ├── input/                       ← Upload images here
    ├── output/                      ← Generated banners
    └── fonts/                       ← TTF font files
```

---

## 🎓 Learning Path

### Level 1: Understanding Basics

- [ ] Read: [README.md](README.md)
- [ ] Watch: Diagram in `ARCHITECTURE.md`
- [ ] Run: `python quickstart.py` → Choose option 1

### Level 2: Using APIs

- [ ] Read: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- [ ] Run: `python app.py` (Web interface)
- [ ] Test: Upload image via web UI

### Level 3: Integration & Deployment

- [ ] Read: [ARCHITECTURE.md](ARCHITECTURE.md)
- [ ] Setup: Stable Diffusion (Local or Replicate)
- [ ] Deploy: Docker or production server

### Level 4: Advanced Customization

- [ ] Study: Source code of each module
- [ ] Modify: Algorithms for your use case
- [ ] Extend: Add new features

---

## 📊 Feature Comparison

| Feature          | Layer 1        | Layer 2      | Layer 3         |
| ---------------- | -------------- | ------------ | --------------- |
| **Purpose**      | Background     | Product      | Text            |
| **Technology**   | Generative AI  | ML (U²-Net)  | Pillow          |
| **Speed**        | Slow (5-60s)   | Fast (2-5s)  | Very fast (<1s) |
| **Quality**      | Photorealistic | Precise mask | Sharp text      |
| **Customizable** | Via prompt     | Model config | Font/color      |
| **Requires GPU** | Yes            | Optional     | No              |

---

## 🔧 Quick Commands

```bash
# Setup
pip install -r requirements.txt

# Basic demo
python layer_compositing.py

# Full test
python test_pipeline.py

# Web interface
python app.py

# Background removal
python background_removal.py

# AI background generation
python stable_diffusion_integration.py

# Interactive menu
python quickstart.py
```

---

## 🌐 Web API Usage

### Start server

```bash
python app.py
# Open: http://localhost:5000
```

### Example API calls

#### 1. Remove background

```bash
curl -X POST -F "file=@product.jpg" http://localhost:5000/api/remove-background
```

#### 2. Generate background

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"prompt":"blue gradient","width":800,"height":600}' \
  http://localhost:5000/api/generate-background
```

#### 3. Create banner

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"Sale","text_color":[255,255,0]}' \
  http://localhost:5000/api/create-banner
```

---

## 🐳 Docker Quick Start

```bash
# Build image
docker build -t image-compositing .

# Run container
docker run -p 5000:5000 image-compositing

# Or use docker-compose
docker-compose up
```

---

## ⚙️ Configuration

### Environment Variables

```bash
export REPLICATE_API_TOKEN=<your_token>      # For Replicate API
export FLASK_ENV=production                  # Flask mode
export FLASK_DEBUG=0                         # Disable debug
```

### Font Configuration

```python
# Supported fonts (must be in fonts/ folder)
- Roboto-Bold.ttf ✓ Unicode support
- Arial.ttf ✓ Windows default
- DejaVuSans-Bold.ttf ✓ Linux default
```

### Model Configuration

```python
# Layer 2 (Background Removal)
model="u2net"      # Best quality (default)
model="u2netp"     # Faster
model="u2net_human_seg"  # For people
```

---

## 🎯 Use Cases

### E-commerce

- Auto-generate product banners
- Quick visual creation pipeline

### Marketing

- Social media ads
- Sale announcements
- Product showcase

### Content Creation

- Batch image processing
- Consistent branding

---

## 🐛 Troubleshooting

### Common Issues

| Issue            | Solution                                                             |
| ---------------- | -------------------------------------------------------------------- |
| "No module PIL"  | `pip install Pillow`                                                 |
| Port 5000 in use | Use port 8000: `python -c "from app import app; app.run(port=8000)"` |
| Font not found   | Copy .ttf files to `fonts/` folder                                   |
| API timeout      | Increase timeout in `stable_diffusion_integration.py`                |
| Out of memory    | Use GPU: `pip install rembg[gpu]`                                    |

### Debug Mode

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug
python -u app.py  # Unbuffered output
```

---

## 📞 Support & Resources

### External APIs

- [Replicate AI Documentation](https://replicate.com/docs)
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [rembg GitHub](https://github.com/danielgatis/rembg)

### Python Libraries

- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NumPy Documentation](https://numpy.org/doc/)

---

## 📝 For Academic Reports

### Recommended Structure

```
1. Introduction
   - Problem statement (AI text corruption)
   - Proposed solution (3-layer architecture)

2. Architecture Design
   - 3-layer model explanation
   - Data flow diagram
   - Algorithm descriptions

3. Implementation
   - Technology stack
   - Module descriptions
   - Code examples

4. Results & Comparison
   - Demo outputs
   - Performance metrics
   - Comparison with baseline

5. Conclusion
   - Benefits of approach
   - Future improvements
```

### Figures to Include

- [ ] 3-Layer architecture diagram
- [ ] Workflow pipeline
- [ ] Before/after comparison
- [ ] Sample outputs

### Code to Reference

- `layer_compositing.py` - Core algorithm
- `app.py` - Integration example
- `test_pipeline.py` - Results validation

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Run first demo: `python layer_compositing.py`
- [ ] Web API working: `python app.py`
- [ ] Folders created: `input/`, `output/`, `fonts/`
- [ ] Read documentation: README.md + INTEGRATION_GUIDE.md
- [ ] (Optional) Setup Stable Diffusion for AI backgrounds

---

## 🎉 Next Steps

1. ✅ **Understand:** Read README.md
2. ✅ **Try:** Run basic demo
3. ✅ **Explore:** Test web API
4. ✅ **Customize:** Modify for your use case
5. ✅ **Deploy:** Use Docker or production setup
6. ✅ **Document:** Add to your report

---

**Version:** 1.0  
**Last Updated:** 2026-02-02  
**Status:** Ready for production use
