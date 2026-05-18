"""
Application configuration settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
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
    
    # MariaDB database (existing FATS/reference domain)
    database_url: str = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://opal:opal_password@localhost:3306/opal"
    )
    async_database_url: str = os.getenv(
        "ASYNC_DATABASE_URL",
        "mysql+aiomysql://opal:opal_password@localhost:3306/opal"
    )
    mariadb_async_database_url: str = os.getenv("MARIADB_ASYNC_DATABASE_URL", async_database_url)

    # Postgres database (new Summit Logging domain)
    summit_async_database_url: str = os.getenv(
        "SUMMIT_ASYNC_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/opal_summit"
    )
    # Sync URL for one-off ETL (psycopg2). Defaults from SUMMIT_ASYNC_DATABASE_URL if unset.
    summit_sync_database_url: str = os.getenv("SUMMIT_SYNC_DATABASE_URL", "")

    # Legacy MariaDB `sumlogs` (Summit) — used by migrate_sumlogs_to_postgres.py
    sumlogs_database_url: str = os.getenv("SUMLOGS_DATABASE_URL", "")

    # MariaDB `clients` database — holds users, sessions, staff, props, etc.
    clients_async_database_url: str = os.getenv(
        "CLIENTS_ASYNC_DATABASE_URL",
        "mysql+aiomysql://opal:opal_password@localhost:3306/clients"
    )
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_hours: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

    # LDAP
    ldap_host: str = os.getenv("LDAP_HOST", "ldap.subaru.nao.ac.jp")
    ldap_port: int = int(os.getenv("LDAP_PORT", "389"))
    ldap_people_dn: str = os.getenv("LDAP_PEOPLE_DN", "ou=People,dc=subaru,dc=nao,dc=ac,dc=jp")
    ldap_group_dn: str = os.getenv("LDAP_GROUP_DN", "ou=group,dc=subaru,dc=nao,dc=ac,dc=jp")

    # Dev-mode local user bypass (only active when DEBUG=true)
    # Format: "username:password,username2:password2"
    dev_local_users: str = os.getenv("DEV_LOCAL_USERS", "")

    # Session cookie
    cookie_name: str = "opal_session"
    cookie_secure: bool = os.getenv("COOKIE_SECURE", "false").lower() == "true"
    cookie_httponly: bool = True
    cookie_samesite: str = "lax"
    
    # Email / SMTP
    smtp_host: str = os.getenv("SMTP_HOST", "mail.subaru.nao.ac.jp")
    smtp_port: int = int(os.getenv("SMTP_PORT", "25"))
    email_sender: str = os.getenv("EMAIL_SENDER", "opal@naoj.org")
    # Comma-separated recipient lists
    email_summitlog_recipients: str = os.getenv(
        "EMAIL_SUMMITLOG_RECIPIENTS", "summitlog@naoj.org"
    )
    email_smoka_recipients: str = os.getenv(
        "EMAIL_SMOKA_RECIPIENTS", "smokalog@smoka.nao.ac.jp"
    )
    email_dc_recipients: str = os.getenv(
        "EMAIL_DC_RECIPIENTS", "operators@naoj.org"
    )

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