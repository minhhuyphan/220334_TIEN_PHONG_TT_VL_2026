from fastapi import FastAPI
from app.routers import file_upload
from fastapi.middleware.cors import CORSMiddleware
import os

# Prefix API theo version
api_prefix = f"/api/{os.environ['VERSION_APP']}"

# Tạo instance của FastAPI
app = FastAPI(
    title=os.environ["TITLE_APP"],
    docs_url=f"{api_prefix}/docs",
    redoc_url=f"{api_prefix}/redoc",
    openapi_url=f"{api_prefix}/openapi.json",
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["ALLOW_ORIGINS"],  # Cho phép tất cả nguồn (hoặc chỉ định danh sách ["http://example.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả phương thức (GET, POST, PUT, DELETE, v.v.)
    allow_headers=["*"],  # Cho phép tất cả headers
)


# Include các router vào ứng dụng chính
app.include_router(file_upload.router, prefix=api_prefix)


@app.get(f"{api_prefix}/")
def read_root():
    return {"message": f"Welcome to {os.environ['TITLE_APP']}"}
