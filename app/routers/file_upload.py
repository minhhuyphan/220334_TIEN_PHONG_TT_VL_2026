from fastapi import APIRouter
from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Request, Form  # noqa: E402, F401
from fastapi.responses import FileResponse  # noqa: E402
from app.config import settings
from mimetypes import guess_type
import os

# Tạo router cho người dùng
router = APIRouter(prefix="/upload-file", tags=["file-upload"])


@router.get("/download/{filename}")
async def download_file(filename: str):
    """
    API để tải xuống tệp.

    Tham số:
    - `filename`: Tên tệp cần tải xuống.

    Trả về:
    - Nếu tệp tồn tại, trả về tệp dưới dạng phản hồi tải xuống.
    - Nếu tệp không tồn tại, trả về lỗi 404 với thông báo "File not found".
    """
    file_path = os.path.join(os.path.join(settings.DIR_ROOT, "utils", "download"), filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")
    raise HTTPException(status_code=404, detail="File not found")


@router.get("/view/{filename}")
async def view_file(filename: str):
    """
    API để xem trước file (hình ảnh, video, audio, v.v.)

    Tham số:
    - `filename`: Tên file cần xem.

    Trả về:
    - File với media type phù hợp nếu tồn tại.
    - 404 nếu không tìm thấy file.
    """
    file_path = os.path.join(os.path.join(settings.DIR_ROOT, "utils", "download"), filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type, _ = guess_type(file_path)
    media_type = media_type or "application/octet-stream"  # fallback nếu không đoán được

    return FileResponse(
        path=file_path, media_type=media_type, filename=filename, headers={"Content-Disposition": f"inline; filename={filename}"}
    )
@router.post("/upload")
async def upload_file_handler(file: UploadFile = File(...)):
    """
    Upload file logic for SEO images (Logo/Favicon) or other assets.
    """
    import uuid
    import shutil
    
    # 1. Sanitize Filename
    # Use uuid to prevent collision and path traversal
    ext = os.path.splitext(file.filename)[1]
    # Ensure simplified extension if missing
    if not ext:
        ext = ".png"
        
    safe_filename = f"{uuid.uuid4()}{ext}"
    
    # 2. Storage
    # According to guide: utils/download/
    upload_dir = os.path.join(settings.DIR_ROOT, "utils", "download")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        
    file_path = os.path.join(upload_dir, safe_filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
        
    # 3. URL Mapping
    # Return URL for Frontend display
    return {
        "filename": safe_filename,
        "url": f"{settings.URL_API}/api/v1/upload-file/view/{safe_filename}"
    }
