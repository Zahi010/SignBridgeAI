from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from backend.app.database.database import get_db
from backend.app.models.entities import TranslationHistory
from backend.app.schemas.translation import TranslationHistoryItem

router = APIRouter()

@router.get("/history", response_model=List[TranslationHistoryItem], summary="Get translation history")
def get_translation_history(
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items = (
        db.query(TranslationHistory)
        .order_by(TranslationHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return items

