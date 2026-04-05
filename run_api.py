import subprocess

# Chạy ứng dụng FastAPI
if __name__ == "__main__":
    import sys
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"])