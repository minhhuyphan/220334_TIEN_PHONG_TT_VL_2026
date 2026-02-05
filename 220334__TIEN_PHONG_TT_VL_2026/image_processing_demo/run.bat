@echo off
REM Startup Script for 3-Layer Image Compositing
REM Windows batch file to setup and run the application

echo.
echo ========================================
echo 3-LAYER IMAGE COMPOSITING STARTUP
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1] Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo [2] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [3] Installing dependencies...
pip install -r requirements.txt
echo.

REM Create directories if they don't exist
if not exist "input\" mkdir input
if not exist "output\" mkdir output
if not exist "fonts\" mkdir fonts

echo ========================================
echo AVAILABLE COMMANDS:
echo ========================================
echo.
echo 1. Basic Demo:
echo    python layer_compositing.py
echo.
echo 2. Test Full Pipeline:
echo    python test_pipeline.py
echo.
echo 3. Web API (Flask):
echo    python app.py
echo    Then open: http://localhost:5000
echo.
echo 4. Background Removal:
echo    python background_removal.py
echo.
echo 5. Stable Diffusion Integration:
echo    python stable_diffusion_integration.py
echo.
echo ========================================
echo.
echo Choose an option (1-5) or type command manually:
echo.

set /p choice="Enter your choice (1-5 or command): "

if "%choice%"=="1" (
    python layer_compositing.py
) else if "%choice%"=="2" (
    python test_pipeline.py
) else if "%choice%"=="3" (
    echo Starting Flask API server...
    echo Open browser: http://localhost:5000
    echo Press Ctrl+C to stop
    python app.py
) else if "%choice%"=="4" (
    python background_removal.py
) else if "%choice%"=="5" (
    python stable_diffusion_integration.py
) else if "%choice%"=="" (
    echo No option selected, launching Flask API...
    python app.py
) else (
    echo Running custom command: %choice%
    %choice%
)

pause
