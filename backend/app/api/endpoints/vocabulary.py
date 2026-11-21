from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List

from backend.app.database.database import get_db
from backend.app.models.entities import Concept, SignRecord, ValidationStatus
from backend.app.schemas.vocabulary import (
    ConceptDetailSchema, VocabularyListResponse, SignRecordDetailSchema,
    ProvenanceSchema, ExpertReviewSchema, SignVariantSchema, ReviewerValidationSchema
)

router = APIRouter()

def build_concept_schema(c: Concept, s: Optional[SignRecord]) -> ConceptDetailSchema:
    signs_detail = []
    val_status = ValidationStatus.UNSUPPORTED

    if s:
        val_status = s.validation_status
        prov_schema = ProvenanceSchema.model_validate(s.provenance) if s.provenance else None
        rev_schema = ExpertReviewSchema.model_validate(s.expert_review) if s.expert_review else None
        var_schemas = [SignVariantSchema.model_validate(v) for v in s.variants]
        val_reviews = [ReviewerValidationSchema.model_validate(r) for r in s.validation_reviews]
        has_vid = (len(s.videos) > 0 and s.validation_status == ValidationStatus.VERIFIED)
        vid_url = s.videos[0].video_path if (s.videos and has_vid) else None

        signs_detail.append(
            SignRecordDetailSchema(
                id=s.id,
                sign_id=s.sign_id,
                sign_gloss=s.sign_gloss,
                validation_status=s.validation_status,
                is_authentic=s.is_authentic,
                linguistic_notes=s.linguistic_notes,
                regional_dialect=s.regional_dialect or "Standard ISL (Pan-India)",
                dominant_hand=s.dominant_hand,
                handshape=s.handshape,
                movement=s.movement,
                location=s.location,
                orientation=s.orientation,
                non_manual_markers=s.non_manual_markers,
                source_institution=s.source_institution,
                source_url_or_dataset_id=s.source_url_or_dataset_id,
                license=s.license,
                consent_info=s.consent_info,
                validation_date=s.validation_date,
                confidence_score=s.confidence_score,
                provenance=prov_schema,
                expert_review=rev_schema,
                validation_reviews=val_reviews,
                variants=var_schemas,
                has_video=has_vid,
                video_url=vid_url
            )
        )

    return ConceptDetailSchema(
        id=c.id,
        branch_id=c.branch_id,
        branch_name=c.branch.name if c.branch else None,
        subject_id=c.subject_id,
        subject_name=c.subject.name if c.subject else None,
        term=c.term,
        slug=c.slug,
        aliases=c.aliases,
        category=c.category,
        domain=c.domain,
        definition=c.definition,
        technical_context=c.technical_context,
        example_usage=c.example_usage,
        difficulty_level=c.difficulty_level or "intermediate",
        validation_status=val_status,
        signs=signs_detail,
        created_at=c.created_at
    )

@router.get("/vocabulary", response_model=VocabularyListResponse, summary="Retrieve ISL technical vocabulary")
def get_vocabulary(
    search: Optional[str] = Query(None, description="Search term or alias"),
    branch_id: Optional[int] = Query(None, description="Filter by branch ID"),
    validation_status: Optional[str] = Query(None, description="Filter by validation status"),
    db: Session = Depends(get_db)
):
    query = db.query(Concept)

    if branch_id:
        query = query.filter(Concept.branch_id == branch_id)

    if search:
        search_fmt = f"%{search.strip().lower()}%"
        query = query.filter(
            or_(
                Concept.term.ilike(search_fmt),
                Concept.aliases.ilike(search_fmt),
                Concept.definition.ilike(search_fmt),
                Concept.domain.ilike(search_fmt)
            )
        )

    all_concepts = query.all()
    results: List[ConceptDetailSchema] = []
    
    verified_c = 0
    partial_c = 0
    unsupported_c = 0
    needs_review_c = 0

    for c in all_concepts:
        s = db.query(SignRecord).filter(SignRecord.concept_id == c.id).first()
        status = s.validation_status if s else ValidationStatus.UNSUPPORTED

        if validation_status and status.value != validation_status.lower():
            continue

        if status == ValidationStatus.VERIFIED:
            verified_c += 1
        elif status == ValidationStatus.NEEDS_REVIEW:
            needs_review_c += 1
        elif status in (ValidationStatus.PARTIAL, ValidationStatus.EXPLANATION_NEEDED, ValidationStatus.EXPLANATION_REQUIRED):
            partial_c += 1
        else:
            unsupported_c += 1

        results.append(build_concept_schema(c, s))

    return VocabularyListResponse(
        total=len(results),
        verified_count=verified_c,
        partial_count=partial_c,
        unsupported_count=unsupported_c,
        needs_review_count=needs_review_c,
        items=results
    )

@router.get("/vocabulary/{concept_id}", response_model=ConceptDetailSchema, summary="Get single vocabulary concept detail")
def get_concept_by_id(concept_id: int, db: Session = Depends(get_db)):
    c = db.query(Concept).filter(Concept.id == concept_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Concept not found")
    
    s = db.query(SignRecord).filter(SignRecord.concept_id == c.id).first()
    return build_concept_schema(c, s)
