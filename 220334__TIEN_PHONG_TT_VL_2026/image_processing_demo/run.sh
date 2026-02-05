#!/bin/bash

# Startup Script for 3-Layer Image Compositing
# Mac/Linux bash script

echo ""
echo "========================================"
echo "3-LAYER IMAGE COMPOSITING STARTUP"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1] Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "[2] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "[3] Installing dependencies..."
pip install -r requirements.txt
echo ""

# Create directories if they don't exist
mkdir -p input
mkdir -p output
mkdir -p fonts

echo "========================================"
echo "AVAILABLE COMMANDS:"
echo "========================================"
echo ""
echo "1. Basic Demo:"
echo "   python layer_compositing.py"
echo ""
echo "2. Test Full Pipeline:"
echo "   python test_pipeline.py"
echo ""
echo "3. Web API (Flask):"
echo "   python app.py"
echo "   Then open: http://localhost:5000"
echo ""
echo "4. Background Removal:"
echo "   python background_removal.py"
echo ""
echo "5. Stable Diffusion Integration:"
echo "   python stable_diffusion_integration.py"
echo ""
echo "========================================"
echo ""
echo "Choose an option (1-5) or type command manually:"
echo ""

read -p "Enter your choice (1-5 or command): " choice

case $choice in
    1)
        python layer_compositing.py
        ;;
    2)
        python test_pipeline.py
        ;;
    3)
        echo "Starting Flask API server..."
        echo "Open browser: http://localhost:5000"
        echo "Press Ctrl+C to stop"
        python app.py
        ;;
    4)
        python background_removal.py
        ;;
    5)
        python stable_diffusion_integration.py
        ;;
    *)
        if [ -z "$choice" ]; then
            echo "No option selected, launching Flask API..."
            python app.py
        else
            echo "Running custom command: $choice"
            eval $choice
        fi
        ;;
esac
