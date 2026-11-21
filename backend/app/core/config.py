from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "SignBridge AI"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Database
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'signbridge.db'}"
    
    # Storage Paths
    DATA_DIR: Path = ROOT_DIR / "data"
    VOCABULARY_DIR: Path = ROOT_DIR / "data" / "vocabulary"
    SIGN_VIDEOS_DIR: Path = ROOT_DIR / "data" / "sign_videos"
    AVATAR_ANIMATIONS_DIR: Path = ROOT_DIR / "data" / "avatar_animations"
    UPLOADS_DIR: Path = ROOT_DIR / "data" / "uploads"
    
    # File limits
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".pptx"]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# Ensure directories exist
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.VOCABULARY_DIR.mkdir(parents=True, exist_ok=True)
settings.SIGN_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
settings.AVATAR_ANIMATIONS_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

