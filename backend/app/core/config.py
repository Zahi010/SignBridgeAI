import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "SignBridge AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Environment & Security
    ENVIRONMENT: str = os.getenv("SIGNBRIDGE_ENV", "development")
    DEBUG: bool = os.getenv("SIGNBRIDGE_DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SIGNBRIDGE_SECRET_KEY", "signbridge-isl-governance-secret-salt-2026-accredited")
    DELETION_PEPPER: str = os.getenv("SIGNBRIDGE_DELETION_PEPPER", "signbridge-isl-gdpr-pepper-2026-nonreversible")
    TOKEN_EXPIRATION_SECONDS: int = int(os.getenv("SIGNBRIDGE_TOKEN_EXP_SECONDS", str(86400 * 7)))
    SECURITY_HEADERS_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("SIGNBRIDGE_RATE_LIMIT", "120"))
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("SIGNBRIDGE_DATABASE_URL", f"sqlite:///{BASE_DIR / 'signbridge.db'}")
    
    # Storage Paths
    DATA_DIR: Path = ROOT_DIR / "data"
    VOCABULARY_DIR: Path = ROOT_DIR / "data" / "vocabulary"
    SIGN_VIDEOS_DIR: Path = ROOT_DIR / "data" / "sign_videos"
    AVATAR_ANIMATIONS_DIR: Path = ROOT_DIR / "data" / "avatar_animations"
    UPLOADS_DIR: Path = ROOT_DIR / "data" / "uploads"
    BACKUPS_DIR: Path = ROOT_DIR / "data" / "backups"
    
    # File limits
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".pptx"]

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="allow"
    )

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.VOCABULARY_DIR.mkdir(parents=True, exist_ok=True)
settings.SIGN_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
settings.AVATAR_ANIMATIONS_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
settings.BACKUPS_DIR.mkdir(parents=True, exist_ok=True)


