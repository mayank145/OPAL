"""
Application configuration settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from backend directory
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """Application settings"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from environment
    )
    
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
    
    # CORS - Production origins should be set via environment variable  
    @property
    def allowed_origins(self) -> List[str]:
        """Parse allowed origins from comma-separated string"""
        origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost,http://127.0.0.1:3000")
        return [origin.strip() for origin in origins_str.split(",") if origin.strip()]


# Global settings instance
settings = Settings()