@echo off
chcp 65001 >nul
echo Downloading Stable Diffusion 2.1 Model...
echo.
echo This will take 5-15 minutes
echo Keep this window open!
echo.
cd /d "d:\Dự án thực tập\image_processing_demo"
"D:\Dự án thực tập\.venv\Scripts\python.exe" download_model.py
pause
