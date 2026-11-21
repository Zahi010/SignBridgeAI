from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.database import get_db
from backend.app.schemas.translation import TranslationRequest, TranslationResponse
from backend.app.translation.engine import TranslationEngine

router = APIRouter()

@router.post("/translate", response_model=TranslationResponse, summary="Translate English text to ISL concepts and grammar")
def translate_text(request: TranslationRequest, db: Session = Depends(get_db)):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=422, detail="Text cannot be empty.")
    
    engine = TranslationEngine(db)
    response = engine.process_translation(request)
    return response

