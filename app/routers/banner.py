from app.models.banner_db import UserManager, BannerHistoryManager, ConfigManager, TasksManager
from fastapi import APIRouter, Request, Form, HTTPException, Depends, Body, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.security.security import get_api_key
from app.security.jwt import get_current_user
from app.utils.image_processing import (
    get_compatible_aspect_ratio,
    resize_image,
    get_resolution,
    create_text_reference_image
)
from chatbot.chatbot.utils.prompt_generator import PromptGenerator
from chatbot.chatbot.utils.prompt_analyzer import PromptAnalyzer
from chatbot.chatbot.utils.llm import LLM
from app.utils.font_manager import download_fonts, get_font_path
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import uuid
import os
import json
import asyncio
from typing import Optional
from app.utils.task_manager import ram_task_manager
from app.utils.cloudinary_utils import upload_to_cloudinary

router = APIRouter(prefix="/generate", tags=["banner"])

def get_config_manager():
    manager = ConfigManager()
    try:
        yield manager
    finally:
        manager.close()

def get_user_manager():
    manager = UserManager()
    try:
        yield manager
    finally:
        manager.close()

def get_banner_history_manager():
    manager = BannerHistoryManager()
    try:
        yield manager
    finally:
        manager.close()

def get_tasks_manager():
    manager = TasksManager()
    try:
        yield manager
    finally:
        manager.close()

# Định nghĩa thư mục chứa banner
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.join(project_root, "banners")
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

from app.utils.url import fix_banner_url

async def generate_prompt_text(aspect_ratio: str, resolution: str, user_request: str):
    llm_generate = PromptGenerator(LLM().get_llm(settings.LLM_PROVIDER)).get_chain()
    prompt = await llm_generate.ainvoke({
        "aspect_ratio": aspect_ratio,
        "size_images": resolution,
        "user_request": user_request,
    })
    return prompt

async def generate_banner(
    prompt: str, 
    aspect_ratio: str = "1:1", 
    reference_images: Optional[list] = None,
    api_key: str = None,
    model_id: str = None
) -> Optional[Image.Image]:
    full_prompt = prompt
    
    contents = [full_prompt]
    if reference_images:
        for img in reference_images:
            contents.append(img)

    api_key = api_key or settings.KEY_API_GOOGLE
    model_id = model_id or settings.GOOGLE_LLM_IMAGE
    client = genai.Client(api_key=api_key)
    try:
        image_config = types.ImageConfig(aspect_ratio=aspect_ratio)
        
        # Chạy block call trong thread để không block event loop
        def sync_generate():
            return client.models.generate_content(
                model=model_id,
                contents=contents,
                config=types.GenerateContentConfig(
                    image_config=image_config,
                    response_modalities=['IMAGE']
                )
            )

        response = await asyncio.to_thread(sync_generate)

        if not response:
            return None

        # New SDK structure (Gemini 3.1 / 2.x)
        if hasattr(response, 'candidates') and response.candidates:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image = await asyncio.to_thread(Image.open, BytesIO(part.inline_data.data))
                    return image
        
        # Fallback for direct parts shortcut (if exists)
        if hasattr(response, 'parts') and response.parts:
            for part in response.parts:
                if part.inline_data:
                    image = await asyncio.to_thread(Image.open, BytesIO(part.inline_data.data))
                    return image
                    
        return None
    except Exception as e:
        import traceback
        print(f"Lỗi khi tạo banner (Chi tiết): {e}")
        traceback.print_exc()
        return None

@router.get("/view/{file_id}")
async def view_banner(file_id: str, download: bool = False):
    """
    Tự động tìm ảnh theo UUID hoặc tên file trong thư mục banners.
    Hỗ trợ tìm kiếm cả khi có hoặc không có đuôi mở rộng .png.
    """
    # Nếu file_id đã có đuôi mở rộng phổ biến
    if any(file_id.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp']):
        filename = file_id
    else:
        filename = f"{file_id}.png"
        
    file_path = os.path.join(BASE_DIR, filename)
    
    if not os.path.exists(file_path):
        # Thử tìm file bất kỳ bắt đầu bằng file_id nếu không tìm thấy chính xác
        try:
            files = [f for f in os.listdir(BASE_DIR) if f.startswith(file_id)]
            if files:
                file_path = os.path.join(BASE_DIR, files[0])
            else:
                raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")
        except:
             raise HTTPException(status_code=404, detail="Không tìm thấy ảnh")
            
    if download:
        return FileResponse(file_path, filename=filename)
    return FileResponse(file_path)

@router.get("/reference/{filename}")
async def view_reference_image(filename: str):
    """
    Xem ảnh tham chiếu đã upload
    """
    file_path = os.path.join(project_root, "uploads", "references", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Không tìm thấy ảnh tham chiếu")
    return FileResponse(file_path)

async def process_banner_task(task_id: str, user_id: int, request_data: dict):
    """
    Background worker to process banner generation
    """
    tasks_manager = TasksManager()
    user_manager = UserManager()
    banner_history = BannerHistoryManager()
    config_manager = ConfigManager()
    
    try:
        tasks_manager.update_task(task_id, "processing")
        
        # Extract params
        width = request_data.get("width")
        height = request_data.get("height")
        number = request_data.get("number")
        user_request = request_data.get("user_request")
        reference_image_paths = request_data.get("reference_image_paths", [])  # Danh sách đường dẫn ảnh tham chiếu
        reference_labels = request_data.get("reference_labels", [])  # Danh sách nhãn tương ứng
        
        # Get dynamic cost
        cost_per_image = int(config_manager.get_value("banner_cost", "1"))
        # Mỗi ảnh tham chiếu tính thêm token (có thể cấu hình trong admin)
        reference_image_cost = len(reference_image_paths) * float(config_manager.get_value("reference_image_cost", "0.5"))
        total_cost = number * (cost_per_image + reference_image_cost)
        
        # Check balance again (double check)
        user = user_manager.get_by_id(user_id)
        if user['tokens'] < total_cost:
            tasks_manager.update_task(task_id, "failed", error_message="Insufficient tokens during processing")
            return

        # 0. Chuẩn bị font chữ
        download_fonts()

        aspect_ratio = get_compatible_aspect_ratio(width, height)
        resolution = get_resolution(aspect_ratio)

        passed_banner = []
        
        # 1. Phân tích yêu cầu
        print("🔍 Đang phân tích yêu cầu...")
        analyzer = PromptAnalyzer(LLM().get_llm(settings.LLM_PROVIDER)).get_chain()
        conditions = await analyzer.ainvoke({"description": user_request})
        text_elements = conditions.text_elements if hasattr(conditions, 'text_elements') and conditions.text_elements else []
        
        # 2. Load ảnh tham chiếu từ người dùng (nếu có)
        user_reference_images = []
        if reference_image_paths:
            print(f"📸 Đang load {len(reference_image_paths)} ảnh tham chiếu từ người dùng...")
            for i, img_path in enumerate(reference_image_paths):
                try:
                    img = await asyncio.to_thread(Image.open, img_path)
                    user_reference_images.append(img)
                    label = reference_labels[i] if i < len(reference_labels) else f"img_{i}"
                    print(f"  ✅ Đã load: {os.path.basename(img_path)} as @{label}")
                except Exception as e:
                    print(f"  ⚠️ Không thể load ảnh {img_path}: {e}")
        
        # 3. Tạo danh sách các ảnh tham chiếu từ text
        text_refs = []
        for el in text_elements:
            font_path = get_font_path(el.font_suggestion)
            # create_text_reference_image usually involves drawing, better in thread
            ref = await asyncio.to_thread(
                create_text_reference_image,
                width * 2, height * 2, 
                text=el.content, 
                font_path=font_path, 
                text_color=el.color_suggestion,
                position=el.position_suggestion
            )
            text_refs.append(ref)

        # 4. Tạo prompt chi tiết
        text_descriptions = [f"'{el.content}' (Màu: {el.color_suggestion}, Vị trí: {el.position_suggestion})" for el in text_elements]
        base_prompt = await generate_prompt_text(aspect_ratio, resolution, user_request)
        
        # Thêm System Prompt từ Admin Config
        custom_system_prompt = config_manager.get_value("system_prompt", "")
        if custom_system_prompt:
            base_prompt += "\n\nCRITICAL DESIGN STYLE/SYSTEM PROMPT:\n" + custom_system_prompt + "\n"
        
        # Thêm thông tin về ảnh tham chiếu từ người dùng với label rõ ràng
        reference_info = ""
        if user_reference_images:
            labeled_refs = []
            for i, label in enumerate(reference_labels):
                if i < len(user_reference_images):
                    labeled_refs.append(f"Image {i+1} is labeled as '@{label}'")
            
            reference_info = f"""
        USER REFERENCE IMAGES IDENTIFICATION:
        - The user has provided {len(user_reference_images)} reference image(s).
        - {'. '.join(labeled_refs)}
        - Use these labels to identify which image the user is referring to in their prompt (e.g., if they say 'sử dụng logo từ @logo', look at the image labeled as @logo).
        - Maintain consistency with the reference images while following the user's request.
        """
        
        has_text = len(text_elements) > 0
        
        premium_instructions = ""
        if has_text:
            premium_instructions = f"""
            VIETNAMESE TEXT RENDERING RULES:
            - Strictly use Unicode-compliant rendering for Vietnamese diacritics (accents).
            - Ensure accents are clearly separated from the base character but correctly positioned.
            - ABSOLUTELY NO spelling errors. The text must match the reference image exactly.
            
            CRITICAL INSTRUCTIONS FOR VIETNAMESE RENDERING:
            1. GREEN SCREEN AWARENESS: The GREEN BACKGROUND in reference images is a MASK. Only focus on the white text within that green area.
            2. ELEVATED DIACRITICS: Render Vietnamese accents with extra vertical clearance.
            3. SPELLING VIGILANCE: Zero spelling errors. Copy text exactly as shown.
            4. MAINTAIN BACKGROUND INTEGRITY: Focus only on adding text. Do NOT alter the festive background.
            5. EXACT POSITIONING: Render each text element at the EXACT location shown in its respective reference image.
            6. PROFESSIONAL COMPOSITING: Use premium effects (soft glows, subtle shadows, metallic sheen) for final text.
            - Specific Elements: {', '.join(text_descriptions)}
            {reference_info}
            """
        else:
            premium_instructions = f"""
            NO TEXT INSTRUCTIONS:
            - Do NOT add any text, typography, letters, or watermark to the image.
            - Focus purely on the visual description and artistic style.
            {reference_info}
            """
        
        full_prompt_to_ai = base_prompt + premium_instructions
        
        # Kết hợp tất cả ảnh tham chiếu: ảnh từ người dùng + ảnh text reference
        all_reference_images = user_reference_images + text_refs

        # Lấy cấu hình API Key và Image Model từ DB
        db_api_key = config_manager.get_value("google_api_key", "")
        db_image_model = config_manager.get_value("image_model", "")

        # 5. Sinh banner
        # Tính chi phí đầy đủ cho mỗi banner (bao gồm ảnh tham chiếu)
        reference_image_cost_per_banner = len(reference_image_paths) * float(config_manager.get_value("reference_image_cost", "0.5"))
        total_cost_per_banner = cost_per_image + reference_image_cost_per_banner
        
        generated_count = 0
        for _ in range(number):
            try:
                banner = await generate_banner(
                    full_prompt_to_ai, 
                    aspect_ratio, 
                    reference_images=all_reference_images,
                    api_key=db_api_key if db_api_key else None,
                    model_id=db_image_model if db_image_model else None
                )
                
                if not banner:
                    continue

                # Resize và lưu
                banner = await asyncio.to_thread(resize_image, banner, width, height)
                file_name = f"{uuid.uuid4()}.png"
                file_path = os.path.join(BASE_DIR, file_name)
                await asyncio.to_thread(banner.save, file_path, "PNG")
                
                # Tải lên Cloudinary để lưu trữ vĩnh viễn (Phòng trường hợp chạy local/restart Render)
                cloud_url = await asyncio.to_thread(upload_to_cloudinary, file_path, folder="banners")
                
                # Ưu tiên dùng Cloud URL, nếu thất bại mới dùng Local URL
                banner_url = cloud_url if cloud_url else f"{settings.API_URL}/api/v1/generate/view/{file_name}"
                # Fallback if API_URL not set in settings? app/config.py usually has it?
                # If not, let's use relative path "/banners/..." and let frontend prepend host if needed.
                # User's previous code used `request.url_for`.
                # Let's use relative for now: `/banners/{file_name}`.
                
                passed_banner.append(banner_url)
                
                # Update task results in DB immediately to prevent loss on F5
                tasks_manager.update_task(task_id, "processing", result=json.dumps(passed_banner)) 

                # Trải phẳng reference_images để lưu vào DB
                ref_images_data = []
                if reference_image_paths:
                    for i, p in enumerate(reference_image_paths):
                        ref_images_data.append({
                            "path": os.path.basename(p),
                            "label": reference_labels[i] if i < len(reference_labels) else f"img_{i}"
                        })

                # Trừ token và lưu lịch sử (bao gồm cả chi phí ảnh tham chiếu)
                user_manager.update_token(user_id, -total_cost_per_banner)
                banner_history.create(
                    user_id=user_id,
                    description=user_request,
                    aspect_ratio=aspect_ratio,
                    resolution=resolution,
                    prompt=full_prompt_to_ai,
                    image_url=banner_url,
                    token_cost=total_cost_per_banner,
                    reference_images=json.dumps(ref_images_data) if ref_images_data else None
                )
                generated_count += 1

            except Exception as e:
                print(f"Lỗi tạo banner: {str(e)}")
                continue
        
        if generated_count > 0:
            tasks_manager.update_task(task_id, "completed", result=json.dumps(passed_banner))
        else:
            tasks_manager.update_task(task_id, "failed", error_message="Failed to generate any banners")
            
    except Exception as e:
        print(f"Task failed: {e}")
        tasks_manager.update_task(task_id, "failed", error_message=str(e))
    finally:
        tasks_manager.close()
        user_manager.close()
        banner_history.close()
        config_manager.close()

@router.get("/stats")
async def get_dashboard_stats(
    request: Request,
    current_user: dict = Depends(get_current_user),
    banner_history: BannerHistoryManager = Depends(get_banner_history_manager)
):
    user_id = current_user['id']
    total_banners = banner_history.count_by_user(user_id)
    recent_banners = banner_history.get_recent_by_user(user_id, limit=4)
    
    score_label = "Beginner"
    if total_banners > 10:
        score_label = "Top 20%"
    if total_banners > 50:
        score_label = "Top 5%"
    if total_banners > 100:
        score_label = "Top 1%"

    # Fix URLs và reference images
    for project in recent_banners:
        project['image_url'] = fix_banner_url(project['image_url'], request)
        if project.get('reference_images'):
            try:
                refs = json.loads(project['reference_images'])
                base = str(request.base_url).rstrip('/')
                for r in refs:
                    r['url'] = f"{base}/api/v1/generate/reference/{r['path']}"
                project['reference_images_list'] = refs
            except:
                project['reference_images_list'] = []

    return {
        "total_banners": total_banners,
        "token_balance": current_user['tokens'],
        "generation_score": score_label,
        "recent_projects": recent_banners
    }

@router.get("/cost")
async def get_banner_cost(config_manager: ConfigManager = Depends(get_config_manager)):
    cost = config_manager.get_value("banner_cost", "1")
    return {"cost": int(cost)}

@router.post("/banners")
async def create_generate_task(
    background_tasks: BackgroundTasks,
    request: Request,
    width: int = Form(..., gt=0),
    height: int = Form(..., gt=0),
    number: int = Form(..., gt=0),
    user_request: str = Form(""),
    reference_images: list[UploadFile] = File(default=[]),  # Danh sách ảnh tham chiếu mới
    reference_labels: list[str] = Form(default=[]),  # Danh sách nhãn cho ảnh tham chiếu mới
    existing_reference_images: Optional[str] = Form(None), # JSON string: [{"path": "...", "label": "..."}]
    current_user: dict = Depends(get_current_user),
    config_manager: ConfigManager = Depends(get_config_manager),
    tasks_manager: TasksManager = Depends(get_tasks_manager)
):
    """
    Initiates banner generation task with optional reference images.
    Returns a Task ID.
    """
    user_id = current_user['id']
    
    # 1. Lưu ảnh tham chiếu (nếu có)
    reference_image_paths = []
    valid_labels = []

    # Xử lý ảnh tham chiếu cũ (từ lịch sử/tái tạo)
    if existing_reference_images:
        try:
            existing_refs = json.loads(existing_reference_images)
            for ref in existing_refs:
                # Kiểm tra file có tồn tại trong uploads/references
                file_path = os.path.join(project_root, "uploads", "references", ref['path'])
                if os.path.exists(file_path):
                    reference_image_paths.append(file_path)
                    valid_labels.append(ref['label'])
        except Exception as e:
            print(f"Error parsing existing_reference_images: {e}")

    # Xử lý ảnh tham chiếu mới upload
    # Đảm bảo reference_labels có cùng độ dài với reference_images
    new_labels = reference_labels[:len(reference_images)]
    while len(new_labels) < len(reference_images):
        new_labels.append(f"image_{len(new_labels) + 1}")

    upload_dir = os.path.join(project_root, "uploads", "references")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    for i, img_file in enumerate(reference_images):
        if img_file.filename:  # Kiểm tra file có tồn tại
            # Tạo tên file unique
            file_ext = os.path.splitext(img_file.filename)[1] or ".png"
            safe_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(upload_dir, safe_filename)
            
            # Lưu file
            import shutil
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(img_file.file, buffer)
            
            reference_image_paths.append(file_path)
            valid_labels.append(new_labels[i])
            
            # Tải lên Cloudinary ngay lập tức (Reference Images)
            try:
                cloud_url = await asyncio.to_thread(upload_to_cloudinary, file_path, folder="references")
                if cloud_url:
                    print(f"Reference image uploaded to Cloudinary: {cloud_url}")
            except Exception as e:
                print(f"Lỗi tải ảnh tham chiếu lên Cloudinary: {e}")
    
    # 2. Validate Balance (bao gồm cả chi phí ảnh tham chiếu)
    cost_per_image = int(config_manager.get_value("banner_cost", "1"))
    reference_image_cost_per_banner = len(reference_image_paths) * float(config_manager.get_value("reference_image_cost", "0.5"))
    total_cost_per_banner = cost_per_image + reference_image_cost_per_banner
    total_cost = number * total_cost_per_banner

    if current_user['tokens'] < total_cost:
        # Xóa các file đã upload nếu không đủ token
        for path in reference_image_paths:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(
            status_code=400, 
            detail=f"Không đủ token. Bạn còn {current_user['tokens']} token, nhưng cần {total_cost:.1f} token ({cost_per_image} token/ảnh + {reference_image_cost_per_banner:.1f} token cho {len(reference_image_paths)} ảnh tham chiếu)."
        )

    # 3. Create Task
    task_id = str(uuid.uuid4())
    request_data = {
        "width": width,
        "height": height,
        "number": number,
        "user_request": user_request,
        "reference_image_paths": reference_image_paths,  # Danh sách đường dẫn
        "reference_labels": valid_labels  # Danh sách nhãn tương ứng
    }
    
    tasks_manager.create_task(task_id, user_id, json.dumps(request_data))
    
    # 4. Trigger RAM Background Process (Sequential)
    await ram_task_manager.add_task(task_id, user_id, request_data, process_banner_task)
    
    # Thông báo về ảnh tham chiếu
    message = "Task queued successfully"
    if reference_image_paths:
        ref_names = [os.path.basename(p) for p in reference_image_paths]
        message += f". {len(reference_image_paths)} ảnh tham chiếu đã được tải lên: {', '.join(ref_names)}"
    
    return {"task_id": task_id, "status": "pending", "message": message, "reference_images_count": len(reference_image_paths)}

@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    tasks_manager: TasksManager = Depends(get_tasks_manager)
):
    task = tasks_manager.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task['user_id'] != current_user['id']:
        raise HTTPException(status_code=403, detail="Not authorized to view this task")
        
    result = None
    if task['result']:
        try:
            result = json.loads(task['result'])
            if isinstance(result, list):
                result = [fix_banner_url(u, request) for u in result]
        except:
            result = task['result']
            
    return {
        "id": task['id'],
        "status": task['status'],
        "result": result,
        "error": task['error_message'],
        "created_at": task['created_at']
    }

@router.get("/history")
async def get_user_history(
    request: Request,
    current_user: dict = Depends(get_current_user),
    banner_history: BannerHistoryManager = Depends(get_banner_history_manager)
):
    """Get all history for current user"""
    history = banner_history.get_all(user_id=current_user['id'])
    for item in history:
        item['image_url'] = fix_banner_url(item['image_url'], request)
        if item.get('reference_images'):
            try:
                refs = json.loads(item['reference_images'])
                base = str(request.base_url).rstrip('/')
                for r in refs:
                    r['url'] = f"{base}/api/v1/generate/reference/{r['path']}"
                item['reference_images_list'] = refs
            except:
                item['reference_images_list'] = []
    return history

@router.delete("/history/{banner_id}")
async def delete_history_item(
    banner_id: int,
    current_user: dict = Depends(get_current_user),
    banner_history: BannerHistoryManager = Depends(get_banner_history_manager)
):
    """Delete a specific history item"""
    # Verify ownership? Manager.delete checks user_id so it's safe if implemented correctly
    count = banner_history.delete(banner_id, user_id=current_user['id'])
    if count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Deleted successfully"}

@router.delete("/history")
async def delete_all_history(
    current_user: dict = Depends(get_current_user),
    banner_history: BannerHistoryManager = Depends(get_banner_history_manager)
):
    """Clear all history for current user"""
    banner_history.delete_all(user_id=current_user['id'])
    return {"message": "History cleared"}
