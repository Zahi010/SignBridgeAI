from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database.database import get_db
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health", summary="Service health status")
def check_health(db: Session = Depends(get_db)):
    db_healthy = True
    db_message = "Connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_healthy = False
        db_message = str(e)

    return {
        "status": "healthy" if db_healthy else "degraded",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": {
            "status": "connected" if db_healthy else "disconnected",
            "message": db_message
        },
        "zero_fabrication_policy": "enforced",
        "supported_input_types": ["text", "pdf", "docx", "pptx", "audio_mic"]
    }

