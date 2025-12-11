"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "OPAL Unified System"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Database - Use localhost if running locally, mariadb if in Docker
    database_url: str = os.getenv("DATABASE_URL", "mysql+aiomysql://opal:opal_password@localhost:3306/opal")
    async_database_url: str = os.getenv("ASYNC_DATABASE_URL", "mysql+aiomysql://opal:opal_password@localhost:3306/opal")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_hours: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))
    
    # File Upload Settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    fats_images_dir: str = os.getenv("FATS_IMAGES_DIR", "uploads/fats")
    max_upload_size: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB default
    allowed_image_types: List[str] = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()