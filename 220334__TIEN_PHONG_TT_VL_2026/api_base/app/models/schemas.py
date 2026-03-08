"""
Banner, BannerDetails, Models, Payment, WebConfigs - SQLAlchemy models
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base_db import Base


class Model(Base):
    """API Key quản lý (OpenAI, Gemini, LLM...)"""
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_key = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class BannerDetails(Base):
    """Chi tiết yêu cầu tạo banner từ user"""
    __tablename__ = "banner_details"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    description = Column(Text, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    number = Column(Integer, default=1)
    status = Column(Integer, default=0)  # 0: pending, 1: processing, 2: done, 3: failed
    model_used = Column(Integer, nullable=True)  # FK Models
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)


class Banner(Base):
    """Kết quả ảnh banner sinh ra"""
    __tablename__ = "banners"
    
    id = Column(Integer, primary_key=True, index=True)
    banner_details_id = Column(Integer, nullable=False, index=True)
    link_banner = Column(String(255), nullable=True)
    image_metadata = Column(Text, nullable=True)  # JSON metadata
    file_size = Column(BigInteger, nullable=True)
    is_published = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True), nullable=True)
    favorite_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Payment(Base):
    """Hóa đơn nạp token"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    amount_vnd = Column(Float, nullable=False)
    tokens_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")  # pending, completed, failed
    hex_id = Column(String(255), unique=True, nullable=True)  # XOR encrypted ID
    sepay_tx_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    expired_at = Column(DateTime(timezone=True), nullable=True)


class WebConfig(Base):
    """Cấu hình hệ thống"""
    __tablename__ = "web_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)


class AuditLog(Base):
    """Log các hành động của user"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    action = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
