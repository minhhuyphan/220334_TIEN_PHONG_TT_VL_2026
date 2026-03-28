from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.banner_db import DBConnection
from app.security.auth import get_admin_user

router = APIRouter(prefix="/pages", tags=["Pages"])

class PageBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PageCreate(PageBase):
    slug: str

class PageUpdate(PageBase):
    pass

class PageDB(DBConnection):
    def get_all(self):
        self.cursor.execute(f"SELECT slug, title, content, is_published, created_at, updated_at FROM pages ORDER BY created_at DESC")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_public(self):
        self.cursor.execute(f"SELECT slug, title, content, is_published, created_at, updated_at FROM pages WHERE is_published = 1 ORDER BY created_at DESC")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_by_slug(self, slug: str):
        self.cursor.execute(f"SELECT slug, title, content, is_published, created_at, updated_at FROM pages WHERE slug = {self.p}", (slug,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def create(self, slug: str, title: str, content: str, is_published: bool):
        sql = f"INSERT INTO pages (slug, title, content, is_published) VALUES ({self.p}, {self.p}, {self.p}, {self.p})"
        self.cursor.execute(sql, (slug, title, content, 1 if is_published else 0))
        self.commit()
        return True

    def update(self, slug: str, title: str, content: str, is_published: bool):
        sql = f"UPDATE pages SET title = {self.p}, content = {self.p}, is_published = {self.p}, updated_at = CURRENT_TIMESTAMP WHERE slug = {self.p}"
        self.cursor.execute(sql, (title, content, 1 if is_published else 0, slug))
        self.commit()
        return self.cursor.rowcount

    def delete(self, slug: str):
        sql = f"DELETE FROM pages WHERE slug = {self.p}"
        self.cursor.execute(sql, (slug,))
        self.commit()
        return self.cursor.rowcount


# PUBLIC ROUTES
@router.get("", response_model=List[dict])
async def get_public_pages():
    db = PageDB()
    pages = db.get_public()
    db.close()
    return pages

@router.get("/{slug}", response_model=dict)
async def get_page(slug: str):
    db = PageDB()
    page = db.get_by_slug(slug)
    db.close()
    if not page or not page['is_published']:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

# ADMIN ROUTES
@router.get("/admin/all", response_model=List[dict])
async def get_all_pages(admin=Depends(get_admin_user)):
    db = PageDB()
    pages = db.get_all()
    db.close()
    return pages

@router.post("/admin/create")
async def create_page(page: PageCreate, admin=Depends(get_admin_user)):
    db = PageDB()
    try:
        existing = db.get_by_slug(page.slug)
        if existing:
            raise HTTPException(status_code=400, detail="Slug already exists")
        db.create(page.slug, page.title, page.content, page.is_published)
    finally:
        db.close()
    return {"message": "Page created"}

@router.put("/admin/{slug}")
async def update_page(slug: str, page: PageUpdate, admin=Depends(get_admin_user)):
    db = PageDB()
    try:
        existing = db.get_by_slug(slug)
        if not existing:
            raise HTTPException(status_code=404, detail="Page not found")
        db.update(slug, page.title, page.content, page.is_published)
    finally:
        db.close()
    return {"message": "Page updated"}

@router.delete("/admin/{slug}")
async def delete_page(slug: str, admin=Depends(get_admin_user)):
    db = PageDB()
    db.delete(slug)
    db.close()
    return {"message": "Page deleted"}
