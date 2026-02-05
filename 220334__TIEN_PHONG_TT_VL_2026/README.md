# Image Processing Demo - 220334_TIEN_PHONG_TT_VL_2026

Advanced image processing and banner creation application with AI integration.

## 📁 Project Structure

```
220334_TIEN_PHONG_TT_VL_2026/
├── src/                      # Source code
│   ├── core/                 # Core processing modules
│   ├── models/               # AI models integration
│   ├── utils/                # Utility functions
│   └── interfaces/           # User interfaces (CLI, GUI, Web)
├── data/
│   ├── input/                # Input images
│   ├── output/               # Output images
│   └── models/               # Pre-trained models
├── config/                   # Configuration files
├── docs/                     # Documentation
├── tests/                    # Unit tests
├── .github/workflows/        # CI/CD pipelines
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── .env.example             # Environment variables template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/220334_TIEN_PHONG_TT_VL_2026
cd 220334_TIEN_PHONG_TT_VL_2026

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

## 📚 Documentation

- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation instructions
- [Architecture](ARCHITECTURE.md) - Project architecture overview
- [Changelog](CHANGELOG.md) - Version history

## 🔧 Available Interfaces

### Web Interface

```bash
python app.py
```

Access at `http://localhost:5000`

### CLI Interface

```bash
python cli_interface.py --help
```

### Desktop GUI

```bash
python gui_desktop.py
```

## 📦 Key Features

- **Image Processing**: Advanced image manipulation and compositing
- **Banner Creation**: AI-powered banner generation
- **Inpainting**: Content-aware image inpainting
- **Background Removal**: Smart background removal
- **Multiple Interfaces**: Web, CLI, and Desktop GUI

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Your Name - Email: your.email@example.com

## 🙏 Acknowledgments

- Built with Python and modern AI frameworks
- Thanks to the open-source community
