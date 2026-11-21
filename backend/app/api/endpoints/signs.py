from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.entities import Concept, SignRecord, ValidationStatus
from backend.app.schemas.vocabulary import (
    SignRecordDetailSchema, ProvenanceSchema, ExpertReviewSchema,
    SignVariantSchema, ReviewerValidationSchema
)

router = APIRouter()

@router.get("/signs/{concept_id}", response_model=SignRecordDetailSchema, summary="Get authentic sign data for concept")
def get_sign_for_concept(concept_id: int, db: Session = Depends(get_db)):
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    sign = db.query(SignRecord).filter(SignRecord.concept_id == concept_id).first()
    if not sign:
        raise HTTPException(status_code=404, detail="No sign record registered for this concept")

    prov = ProvenanceSchema.model_validate(sign.provenance) if sign.provenance else None
    rev = ExpertReviewSchema.model_validate(sign.expert_review) if sign.expert_review else None
    variants = [SignVariantSchema.model_validate(v) for v in sign.variants]
    val_reviews = [ReviewerValidationSchema.model_validate(r) for r in sign.validation_reviews]
    has_vid = (len(sign.videos) > 0 and sign.validation_status == ValidationStatus.VERIFIED)
    vid_url = sign.videos[0].video_path if (sign.videos and has_vid) else None

    return SignRecordDetailSchema(
        id=sign.id,
        sign_id=sign.sign_id,
        sign_gloss=sign.sign_gloss,
        validation_status=sign.validation_status,
        is_authentic=sign.is_authentic,
        linguistic_notes=sign.linguistic_notes,
        regional_dialect=sign.regional_dialect or "Standard ISL (Pan-India)",
        dominant_hand=sign.dominant_hand,
        handshape=sign.handshape,
        movement=sign.movement,
        location=sign.location,
        orientation=sign.orientation,
        non_manual_markers=sign.non_manual_markers,
        source_institution=sign.source_institution,
        source_url_or_dataset_id=sign.source_url_or_dataset_id,
        license=sign.license,
        consent_info=sign.consent_info,
        validation_date=sign.validation_date,
        confidence_score=sign.confidence_score,
        provenance=prov,
        expert_review=rev,
        validation_reviews=val_reviews,
        variants=variants,
        has_video=has_vid,
        video_url=vid_url
    )
