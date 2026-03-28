from fastapi import APIRouter, Depends, HTTPException, Body, Request
from app.models.banner_db import UserManager, PaymentManager, BannerHistoryManager, PackageManager, ConfigManager
from app.security.jwt import get_current_user
from app.utils.url import fix_banner_url
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

def get_user_manager():
    manager = UserManager()
    try:
        yield manager
    finally:
        manager.close()

def get_payment_manager():
    manager = PaymentManager()
    try:
        yield manager
    finally:
        manager.close()

def get_banner_manager():
    manager = BannerHistoryManager()
    try:
        yield manager
    finally:
        manager.close()

def get_package_manager():
    manager = PackageManager()
    try:
        yield manager
    finally:
        manager.close()

def verify_admin(user: dict = Depends(get_current_user)):
    """Verify that the current user is an admin"""
    if not user.get('is_admin'):
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def get_config_manager():
    manager = ConfigManager()
    try:
        yield manager
    finally:
        manager.close()

@router.post("/config/homepage")
async def update_homepage_config(
    data: dict = Body(...),
    admin: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    import json
    try:
        # Save as JSON string
        config_manager.set_value("homepage_config", json.dumps(data, ensure_ascii=False))
        return {"success": True, "message": "Updated homepage config"}
    except Exception as e:
        logger.error(f"Error updating homepage config: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save config")

@router.get("/users")
async def get_all_users(
    admin: dict = Depends(verify_admin),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Get all users (admin only)"""
    try:
        # Get all users from database
        conn = user_manager.conn
        # Use the pre-configured dictionary cursor from manager
        cursor = user_manager.cursor
        cursor.execute("""
            SELECT id, email, full_name, tokens, is_admin, created_at, updated_at
            FROM users
            ORDER BY created_at DESC
        """)
        users = cursor.fetchall()
        return users
    except Exception as e:
        logger.error(f"Admin Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi khi tải danh sách người dùng")

@router.get("/payments")
async def get_all_payments(
    admin: dict = Depends(verify_admin),
    payment_manager: PaymentManager = Depends(get_payment_manager)
):
    """Get all payments (admin only)"""
    try:
        conn = payment_manager.conn
        cursor = payment_manager.cursor
        cursor.execute("""
            SELECT p.*, pk.name as package_name
            FROM payments p
            LEFT JOIN packages pk ON p.package_id = pk.id
            ORDER BY p.created_at DESC
        """)
        payments = cursor.fetchall()
        return payments
    except Exception as e:
        logger.error(f"Admin Error fetching payments: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi khi tải lịch sử thanh toán")

@router.get("/banners")
async def get_all_banners(
    request: Request,
    admin: dict = Depends(verify_admin),
    banner_manager: BannerHistoryManager = Depends(get_banner_manager)
):
    """Get all banners (admin only)"""
    try:
        banners = banner_manager.get_all()
        for b in banners:
            b['image_url'] = fix_banner_url(b['image_url'], request)
        return banners
    except Exception as e:
        logger.error(f"Admin Error fetching banners: {str(e)}")
        raise HTTPException(status_code=500, detail="Lỗi khi tải danh sách banner")

@router.get("/stats")
async def get_stats(
    request: Request,
    admin: dict = Depends(verify_admin),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Get system statistics (admin only)"""
    try:
        conn = user_manager.conn
        cursor = user_manager.cursor
        
        # Total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        row_users = cursor.fetchone()
        total_users = row_users['count'] if row_users else 0
        
        # Total admins
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_admin = 1")
        row_admins = cursor.fetchone()
        total_admins = row_admins['count'] if row_admins else 0
        
        # Total revenue (completed payments only)
        cursor.execute("SELECT COALESCE(SUM(amount_vnd), 0) as total FROM payments WHERE status = 'completed'")
        row_revenue = cursor.fetchone()
        total_revenue = row_revenue['total'] if row_revenue else 0
        
        # Total banners
        cursor.execute("SELECT COUNT(*) as count FROM banner_history")
        row_banners = cursor.fetchone()
        total_banners = row_banners['count'] if row_banners else 0
        
        # Total tokens sold
        cursor.execute("SELECT COALESCE(SUM(tokens_received), 0) as total FROM payments WHERE status = 'completed'")
        row_tokens = cursor.fetchone()
        total_tokens_sold = row_tokens['total'] if row_tokens else 0
        
        # Daily banners (last 7 days)
        cursor.execute(f"""
            SELECT date(created_at) as date, COUNT(*) as count
            FROM banner_history
            WHERE created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
            GROUP BY date(created_at)
            ORDER BY date ASC
        """)
        daily_banners = cursor.fetchall()
        
        # Daily revenue (last 7 days)
        cursor.execute(f"""
            SELECT date(created_at) as date, SUM(amount_vnd) as revenue
            FROM payments 
            WHERE status = 'completed' AND created_at >= DATE_SUB(CURRENT_DATE, INTERVAL 7 DAY)
            GROUP BY date(created_at)
            ORDER BY date ASC
        """)
        daily_revenue = cursor.fetchall()
        
        # Recent 5 payments
        cursor.execute("""
            SELECT p.id, p.amount_vnd, pk.name as package_name, p.status, p.created_at, u.email as user_email
            FROM payments p
            LEFT JOIN packages pk ON p.package_id = pk.id
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.status = 'completed'
            ORDER BY p.created_at DESC LIMIT 5
        """)
        recent_payments = [dict(row) for row in cursor.fetchall()]
        
        # Recent 5 banners
        cursor.execute("""
            SELECT b.id, b.image_url, b.request_description, b.created_at, u.email as user_email
            FROM banner_history b
            LEFT JOIN users u ON b.user_id = u.id
            ORDER BY b.created_at DESC LIMIT 5
        """)
        recent_banners = []
        for row in cursor.fetchall():
            d = dict(row)
            d['image_url'] = fix_banner_url(d['image_url'], request)
            recent_banners.append(d)

        # Cost estimate: API cost (assume 100 VNĐ per banner for Image Gen + LLM)
        api_cost_estimate = total_banners * 100
        
        # Combine chart data
        chart_data_map = {}
        for row in daily_banners:
            chart_data_map[row['date']] = {'date': row['date'], 'banners': row['count'], 'revenue': 0}
        for row in daily_revenue:
            if row['date'] not in chart_data_map:
                chart_data_map[row['date']] = {'date': row['date'], 'banners': 0, 'revenue': row['revenue']}
            else:
                chart_data_map[row['date']]['revenue'] = row['revenue']
        
        chart_data = sorted(list(chart_data_map.values()), key=lambda x: x['date'])

        return {
            "total_users": total_users,
            "total_admins": total_admins,
            "total_revenue": total_revenue,
            "total_banners": total_banners,
            "total_tokens_sold": total_tokens_sold,
            "api_cost_estimate": api_cost_estimate,
            "chart_data": chart_data,
            "recent_payments": recent_payments,
            "recent_banners": recent_banners
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")

@router.post("/users/{user_id}/toggle-admin")
async def toggle_admin(
    user_id: int,
    admin: dict = Depends(verify_admin),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Toggle admin status for a user (admin only)"""
    try:
        # Get current user
        target_user = user_manager.get_by_id(user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Prevent admin from removing their own admin status
        if target_user['id'] == admin['id']:
            raise HTTPException(status_code=400, detail="Cannot modify your own admin status")
        
        # Toggle admin status
        new_status = 0 if target_user['is_admin'] == 1 else 1
        conn = user_manager.conn
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET is_admin = {user_manager.p}, updated_at = CURRENT_TIMESTAMP WHERE id = {user_manager.p}",
            (new_status, user_id)
        )
        conn.commit()
        
        return {
            "success": True,
            "user_id": user_id,
            "is_admin": new_status == 1,
            "message": f"User {'promoted to' if new_status == 1 else 'demoted from'} admin"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error toggling admin: {str(e)}")

@router.get("/packages")
async def get_all_packages(
    admin: dict = Depends(verify_admin),
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Get all packages (admin only)"""
    try:
        return package_manager.get_all(include_inactive=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching packages: {str(e)}")

from pydantic import BaseModel

class PackageCreate(BaseModel):
    name: str
    description: str
    amount_vnd: int
    tokens: int
    is_active: bool = True

class PackageUpdate(BaseModel):
    name: str = None
    description: str = None
    amount_vnd: int = None
    tokens: int = None
    is_active: bool = None

@router.post("/packages")
async def create_package(
    package: PackageCreate,
    admin: dict = Depends(verify_admin),
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Create a new package"""
    try:
        package_id = package_manager.create(
            name=package.name,
            description=package.description,
            amount_vnd=package.amount_vnd,
            tokens=package.tokens,
            is_active=1 if package.is_active else 0
        )
        return {"id": package_id, "message": "Package created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating package: {str(e)}")

@router.put("/packages/{package_id}")
async def update_package(
    package_id: int,
    package: PackageUpdate,
    admin: dict = Depends(verify_admin),
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Update a package"""
    try:
        existing = package_manager.get_by_id(package_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Package not found")
        
        # Use existing values if not provided in update
        name = package.name if package.name is not None else existing['name']
        description = package.description if package.description is not None else existing['description']
        amount_vnd = package.amount_vnd if package.amount_vnd is not None else existing['amount_vnd']
        tokens = package.tokens if package.tokens is not None else existing['tokens']
        is_active = (1 if package.is_active else 0) if package.is_active is not None else existing['is_active']

        package_manager.update(
            package_id=package_id,
            name=name,
            description=description,
            amount_vnd=amount_vnd,
            tokens=tokens,
            is_active=is_active
        )
        return {"message": "Package updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating package: {str(e)}")

@router.delete("/packages/{package_id}")
async def delete_package(
    package_id: int,
    admin: dict = Depends(verify_admin),
    package_manager: PackageManager = Depends(get_package_manager)
):
    """Delete a package"""
    try:
        package_manager.delete(package_id)
        return {"message": "Package deleted successfully"}
    except Exception as e:
        if "Deactivate it instead" in str(e):
             raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Error deleting package: {str(e)}")

# User Management Extensions
@router.post("/users/{user_id}/add-tokens")
async def add_tokens_to_user(
    user_id: int,
    tokens: int = Body(..., embed=True, gt=0),
    admin: dict = Depends(verify_admin),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Manually add tokens to a user account"""
    try:
        user = user_manager.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        conn = user_manager.conn
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE users SET tokens = tokens + {user_manager.p}, updated_at = CURRENT_TIMESTAMP WHERE id = {user_manager.p}",
            (tokens, user_id)
        )
        conn.commit()
        
        return {"success": True, "message": f"Added {tokens} tokens to {user['email']}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding tokens: {str(e)}")

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: dict = Depends(verify_admin),
    user_manager: UserManager = Depends(get_user_manager)
):
    """Delete a user account (admin only)"""
    try:
        user = user_manager.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if user['id'] == admin['id']:
            raise HTTPException(status_code=400, detail="Cannot delete your own admin account")
            
        conn = user_manager.conn
        cursor = conn.cursor()
        # Delete user related data
        cursor.execute(f"DELETE FROM banner_history WHERE user_id = {user_manager.p}", (user_id,))
        cursor.execute(f"DELETE FROM payments WHERE user_id = {user_manager.p}", (user_id,))
        cursor.execute(f"DELETE FROM users WHERE id = {user_manager.p}", (user_id,))
        conn.commit()
        
        return {"success": True, "message": f"User {user['email']} and their data have been deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

@router.get("/users/{user_id}/banners")
async def get_user_banners(
    user_id: int,
    request: Request,
    admin: dict = Depends(verify_admin),
    banner_manager: BannerHistoryManager = Depends(get_banner_manager)
):
    """Get banner history for a specific user"""
    try:
        banners = banner_manager.get_all(user_id)
        for b in banners:
            b['image_url'] = fix_banner_url(b['image_url'], request)
        return banners
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user banners: {str(e)}")

@router.patch("/banners/{banner_id}/visibility")
async def admin_toggle_banner_visibility(
    banner_id: int,
    is_hidden: bool = Body(..., embed=True),
    admin: dict = Depends(verify_admin),
    banner_manager: BannerHistoryManager = Depends(get_banner_manager)
):
    """Admin ẩn/hiện banner trên trang chủ (không xóa)"""
    try:
        count = banner_manager.admin_set_hidden(banner_id, is_hidden)
        if count == 0:
            raise HTTPException(status_code=404, detail="Banner không tìm thấy")
        action = "Ẩn" if is_hidden else "Hiện"
        return {"message": f"{action} banner thành công", "is_hidden": is_hidden}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/banners/{banner_id}")
async def admin_delete_banner(
    banner_id: int,
    admin: dict = Depends(verify_admin),
    banner_manager: BannerHistoryManager = Depends(get_banner_manager)
):
    """Admin xóa bất kỳ banner nào"""
    try:
        banner = banner_manager.get_by_id(banner_id)
        if not banner:
            raise HTTPException(status_code=404, detail="Banner không tìm thấy")
        banner_manager.admin_delete(banner_id)
        return {"message": "Xóa banner thành công"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Config Management
def get_config_manager():
    manager = ConfigManager()
    try:
        yield manager
    finally:
        manager.close()

@router.post("/config/cost")
async def update_banner_cost(
    cost: int = Body(..., embed=True, gt=0),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update global banner generation cost"""
    try:
        config_manager.set_value("banner_cost", cost)
        return {"message": "Updated banner cost", "cost": cost}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/reference-image-cost")
async def update_reference_image_cost(
    cost: float = Body(..., embed=True, gt=0),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update cost per reference image (default 0.5 tokens)"""
    try:
        config_manager.set_value("reference_image_cost", str(cost))
        return {"message": "Updated reference image cost", "cost": cost}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/gemini-safe-mode")
async def update_gemini_safe_mode(
    mode: str = Body(..., embed=True),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update Google Gemini Safey Settings (OFF, BLOCK_LOW_AND_ABOVE, etc)"""
    try:
        config_manager.set_value("gemini_safe_mode", mode)
        return {"message": "Updated safe mode", "mode": mode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/ai-model")
async def update_ai_model(
    model: str = Body(..., embed=True),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update AI Model for Text/Brain processing"""
    try:
        config_manager.set_value("ai_model", model)
        return {"message": "Updated AI model", "model": model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/image-model")
async def update_image_model(
    model: str = Body(..., embed=True),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update Image Generation Model"""
    try:
        config_manager.set_value("image_model", model)
        return {"message": "Updated Image model", "model": model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/system-prompt")
async def update_system_prompt(
    prompt: str = Body(..., embed=True),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update System Prompt for generation"""
    try:
        config_manager.set_value("system_prompt", prompt)
        return {"message": "Updated System Prompt"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/config/google-api-key")
async def update_google_api_key(
    api_key: str = Body(..., embed=True),
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update Google API Key"""
    try:
        config_manager.set_value("google_api_key", api_key)
        return {"message": "Updated API Key"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_all_config(
    current_user: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Get all configuration values"""
    try:
        banner_cost = int(config_manager.get_value("banner_cost", "1"))
        reference_image_cost = float(config_manager.get_value("reference_image_cost", "0.5"))
        gemini_safe_mode = config_manager.get_value("gemini_safe_mode", "OFF")
        ai_model = config_manager.get_value("ai_model", "gemini-2.5-flash")
        image_model = config_manager.get_value("image_model", "gemini-3.0-fast-image-preview")
        system_prompt = config_manager.get_value("system_prompt", "")
        google_api_key = config_manager.get_value("google_api_key", "")
        
        return {
            "banner_cost": banner_cost,
            "reference_image_cost": reference_image_cost,
            "gemini_safe_mode": gemini_safe_mode,
            "ai_model": ai_model,
            "image_model": image_model,
            "system_prompt": system_prompt,
            "google_api_key": google_api_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# SEO Management
import re
import os

class SeoSettings(BaseModel):
    site_title: str
    description: str
    keywords: str
    author: str
    favicon_url: str
    logo_url: str
    canonical_url: str = "/"
    robots: str = "index, follow"

def update_index_html_seo(settings: SeoSettings):
    path = "frontend/index.html"
    if not os.path.exists(path):
        raise Exception(f"File not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Thay đổi thẻ Title
    content = re.sub(r'<title>.*?</title>', f'<title>{settings.site_title}</title>', content, flags=re.DOTALL)

    # 2. Thay đổi các thẻ Meta (Name & Property)
    meta_maps = {
        "description": settings.description,
        "keywords": settings.keywords,
        "author": settings.author,
        "og:title": settings.site_title,
        "og:description": settings.description,
        "twitter:title": settings.site_title,
        "twitter:description": settings.description,
        "robots": settings.robots
    }

    for key, value in meta_maps.items():
        pattern = fr'<(meta\s+[^>]*?(?:name|property)=["\']{re.escape(key)}["\'][^>]*?content=)["\'].*?["\']([^>]*?)>'
        if re.search(pattern, content, re.IGNORECASE):
            replacement = fr'<\1"{value}"\2>'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        elif key == "robots":
            # If robots tag is missing, insert it before </head>
            content = content.replace('</head>', f'  <meta name="robots" content="{value}">\n</head>')

    # 3. Thay đổi Favicon & Logo (Link tags)
    content = re.sub(r'(<link\s+rel=["\']icon["\'][^>]*?href=)["\'].*?["\']', fr'\1"{settings.favicon_url}"', content, flags=re.IGNORECASE)
    
    # 4. Canonical
    if re.search(r'<link\s+rel=["\']canonical["\'][^>]*?href=.*?>', content, re.IGNORECASE):
        content = re.sub(r'(<link\s+rel=["\']canonical["\'][^>]*?href=)["\'].*?["\']', fr'\1"{settings.canonical_url}"', content, flags=re.IGNORECASE)
    else:
         content = content.replace('</head>', f'  <link rel="canonical" href="{settings.canonical_url}" />\n</head>')
    
    # OG Image / Twitter Image (Logo)
    logo_maps = ["og:image", "twitter:image"]
    for key in logo_maps:
        pattern = fr'<(meta\s+[^>]*?(?:name|property)=["\']{re.escape(key)}["\'][^>]*?content=)["\'].*?["\']([^>]*?)>'
        if re.search(pattern, content, re.IGNORECASE):
            replacement = fr'<\1"{settings.logo_url}"\2>'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def extract_seo_from_index_html() -> dict:
    path = "frontend/index.html"
    if not os.path.exists(path):
         return {}
         
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    seo_data = {}
    
    # Title
    match_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    seo_data['site_title'] = match_title.group(1) if match_title else ""
    
    # Meta tags
    keys = ["description", "keywords", "author", "robots"]
    for key in keys:
        pattern = fr'<meta\s+[^>]*?name=["\']{re.escape(key)}["\'][^>]*?content=["\'](.*?)["\']'
        match = re.search(pattern, content, re.IGNORECASE)
        seo_data[key] = match.group(1) if match else ("index, follow" if key == "robots" else "")
        
    # Favicon
    match_fav = re.search(r'<link\s+rel=["\']icon["\'][^>]*?href=["\'](.*?)["\']', content, re.IGNORECASE)
    seo_data['favicon_url'] = match_fav.group(1) if match_fav else ""
    
    # Canonical
    match_canon = re.search(r'<link\s+rel=["\']canonical["\'][^>]*?href=["\'](.*?)["\']', content, re.IGNORECASE)
    seo_data['canonical_url'] = match_canon.group(1) if match_canon else "/"
    
    # Logo (take from og:image)
    match_logo = re.search(r'<meta\s+[^>]*?property=["\']og:image["\'][^>]*?content=["\'](.*?)["\']', content, re.IGNORECASE)
    seo_data['logo_url'] = match_logo.group(1) if match_logo else ""
    
    return seo_data

@router.get("/seo")
async def get_seo_settings(
    admin: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Get SEO settings"""
    try:
        # Try to get from DB first
        seo_json = config_manager.get_value("seo_settings")
        if seo_json:
            import json
            return json.loads(seo_json)
        
        # Fallback to HTML extraction
        return extract_seo_from_index_html()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/seo")
async def update_seo_settings(
    settings: SeoSettings,
    admin: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Update SEO settings (DB + HTML)"""
    try:
        # 1. Update HTML
        update_index_html_seo(settings)
        
        # 2. Save to DB
        import json
        config_manager.set_value("seo_settings", json.dumps(settings.dict()))
        
        return {"message": "SEO settings updated successfully"}
    except Exception as e:
        logger.error(f"Error updating SEO: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seo/sync")
async def sync_seo_from_html(
    admin: dict = Depends(verify_admin),
    config_manager: ConfigManager = Depends(get_config_manager)
):
    """Sync SEO settings from HTML to Database"""
    try:
        data = extract_seo_from_index_html()
        if not data:
            raise HTTPException(status_code=404, detail="Could not read index.html")
            
        import json
        config_manager.set_value("seo_settings", json.dumps(data))
        return {"message": "Synced from HTML successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


