@echo off
echo [*] Dang khoi dong Backend...
start cmd /k ".\.venv\Scripts\python -m uvicorn main:app --reload --port 8000"
echo [*] Dang khoi dong Frontend...
start cmd /k "cd frontend && npm run dev"
echo [OK] Da xong! Hay mo Chrome vao http://localhost:3000
pause
