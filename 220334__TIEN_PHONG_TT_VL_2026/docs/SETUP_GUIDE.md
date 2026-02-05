# Setup Guide - Image Processing Demo

## Prerequisites

- Python 3.8+
- pip or conda
- CUDA (optional, for GPU acceleration)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/220334_TIEN_PHONG_TT_VL_2026
cd 220334_TIEN_PHONG_TT_VL_2026
```

### 2. Create virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download models (optional)

```bash
python download_model.py
```

### 5. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Running the Application

### Web Interface

```bash
python app.py
```

### CLI Interface

```bash
python cli_interface.py --help
```

### GUI Desktop

```bash
python gui_desktop.py
```

## Documentation

- See [ARCHITECTURE.md](ARCHITECTURE.md) for project structure
- See [API_GUIDE.md](API_GUIDE.md) for API documentation
