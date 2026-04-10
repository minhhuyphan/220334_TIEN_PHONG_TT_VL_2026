from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routers import file_upload, banner, auth, payment, admin

# Tạo instance của FastAPI với đường dẫn Docs tùy chỉnh
app = FastAPI(
    title="API BANNER AI", 
    version="v1.0",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json",
    redoc_url=None
)

# Thêm middleware xử lý Proxy Headers (cho Nginx/SSL)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Cấu hình CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

# Thêm các domain từ biến môi trường nếu có
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình thư mục tĩnh để phục vụ file banner
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNERS_DIR = os.path.join(project_root, "banners")
if not os.path.exists(BANNERS_DIR):
    os.makedirs(BANNERS_DIR)

app.mount("/banners", StaticFiles(directory=BANNERS_DIR), name="banners")

# Ensure download dir exists for generated banners
DOWNLOAD_DIR = os.path.join(project_root, "utils", "download")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

from app.routers import file_upload, banner, auth, payment, admin, pages

# Gom nhóm các router vào prefix /api/v1
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth.router)
api_router.include_router(payment.router)
api_router.include_router(file_upload.router)
api_router.include_router(banner.router)
api_router.include_router(admin.router)
api_router.include_router(pages.router)

# Include router tổng vào app
app.include_router(api_router)

from app.utils.task_manager import ram_task_manager
from app.utils.database import check_and_migrate_db

@app.on_event("startup")
async def startup_event():
    try:
        check_and_migrate_db() # Kiểm tra và update DB schema nếu thiếu
    except Exception as e:
        print(f"[ERROR] Fatal error during startup database check: {e}")
    
    # Reset các task bị kẹt từ lần chạy trước (pending/processing trong DB nhưng không có trong RAM)
    # Nếu không reset, frontend sẽ poll vô tận sau khi server restart
    try:
        from app.models.banner_db import TasksManager
        tm = TasksManager()
        conn = tm.conn
        cursor = tm.cursor
        stuck_statuses = ('pending', 'processing')
        p = tm.p
        for status in stuck_statuses:
            cursor.execute(
                f"UPDATE tasks SET status = {p}, error_message = {p}, updated_at = CURRENT_TIMESTAMP WHERE status = {p}",
                ('failed', 'Server restarted. Please try again.', status)
            )
        conn.commit()
        print("[OK] Startup: Reset stuck tasks to 'failed'")
        tm.close()
    except Exception as e:
        print(f"[WARN] Startup cleanup warning: {e}")
    
    await ram_task_manager.start_worker()

@app.get("/")
async def root():
    return {"message": "Welcome to API BANNER AI", "status": "running"}

@app.get("/api/v1/config/homepage")
async def get_homepage_config():
    import json
    from app.models.banner_db import ConfigManager
    manager = ConfigManager()
    try:
        data = manager.get_value("homepage_config", None)
        if data:
            return json.loads(data)
        return {}
    except Exception as e:
        return {}
    finally:
        manager.close()
