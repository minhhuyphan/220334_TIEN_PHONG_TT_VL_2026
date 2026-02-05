@echo off
chcp 65001 >nul
echo Starting AI Banner Creator Web App...
echo.
echo Opening browser...
echo.
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "d:\Dự án thực tập"
call .venv\Scripts\activate.bat
cd image_processing_demo
python -m streamlit run banner_web_simple.py --client.logger.level=error
pause
