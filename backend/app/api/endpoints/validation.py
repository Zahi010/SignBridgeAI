from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from backend.app.database.database import get_db
from backend.app.models.entities import (
    SignRecord, Concept, Subject, EngineeringBranch,
    ReviewerValidation, ReviewerProfile, ValidationStatus, ValidationDecision
)
from backend.app.schemas.validation import (
    ValidationSubmitRequest, ValidationDecisionResponse, PendingValidationItem, ReviewerProfileSchema
)
from backend.app.schemas.vocabulary import SignRecordDetailSchema

router = APIRouter()

@router.get("/reviewers", response_model=List[ReviewerProfileSchema])
def list_reviewer_profiles(db: Session = Depends(get_db)):
    """
    Retrieves the registry of authorized and candidate ISL reviewers.
    Enables UI to differentiate certified Deaf educators / RCI interpreters from developer test accounts.
    """
    return db.query(ReviewerProfile).order_by(ReviewerProfile.is_authorized_expert.desc(), ReviewerProfile.full_name.asc()).all()

@router.get("/pending", response_model=List[PendingValidationItem])
def get_pending_validations(
    branch_code: Optional[str] = None,
    validation_status: Optional[str] = "needs_review",
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieves signs in the validation queue awaiting expert ISL review.
    """
    query = (
        db.query(SignRecord)
        .join(Concept, SignRecord.concept_id == Concept.id)
        .outerjoin(EngineeringBranch, Concept.branch_id == EngineeringBranch.id)
        .outerjoin(Subject, Concept.subject_id == Subject.id)
    )

    if branch_code:
        query = query.filter(EngineeringBranch.code == branch_code)

    if validation_status:
        try:
            status_enum = ValidationStatus(validation_status)
            query = query.filter(SignRecord.validation_status == status_enum)
        except ValueError:
            pass

    records = query.limit(limit).all()

    items = []
    for r in records:
        concept = r.concept
        branch = concept.branch if concept else None
        subject = concept.subject if concept else None
        review_count = len(r.validation_reviews)

        items.append(
            PendingValidationItem(
                sign_record_id=r.id,
                sign_id=r.sign_id,
                concept_term=concept.term if concept else "Unknown",
                branch_name=branch.name if branch else None,
                subject_name=subject.name if subject else None,
                current_status=r.validation_status,
                sign_gloss=r.sign_gloss,
                regional_dialect=r.regional_dialect,
                has_video=bool(r.videos),
                has_animation=bool(r.avatar_animations),
                source_institution=r.source_institution,
                license=r.license,
                review_count=review_count
            )
        )

    return items

@router.get("/signs/{sign_record_id}", response_model=SignRecordDetailSchema)
def get_sign_for_validation(
    sign_record_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieves full phonological, linguistic, and provenance details for a sign under review.
    """
    sign = db.query(SignRecord).filter(SignRecord.id == sign_record_id).first()
    if not sign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sign record with ID {sign_record_id} not found."
        )

    video = sign.videos[0] if sign.videos else None
    video_url = video.video_path if video else None

    # Construct schema representation
    return SignRecordDetailSchema(
        id=sign.id,
        sign_id=sign.sign_id,
        sign_gloss=sign.sign_gloss,
        validation_status=sign.validation_status,
        is_authentic=sign.is_authentic,
        linguistic_notes=sign.linguistic_notes,
        regional_dialect=sign.regional_dialect,
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
        provenance=sign.provenance,
        expert_review=sign.expert_review,
        validation_reviews=sign.validation_reviews,
        variants=sign.variants,
        has_video=bool(sign.videos),
        video_url=video_url
    )

@router.post("/submit", response_model=ValidationDecisionResponse)
def submit_validation_decision(
    req: ValidationSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submits an expert ISL review decision for a candidate sign.
    Updates sign validation status and appends an immutable audit log entry.
    """
    sign = db.query(SignRecord).filter(SignRecord.id == req.sign_record_id).first()
    if not sign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sign record with ID {req.sign_record_id} not found."
        )

    # Validate decision
    valid_decisions = ["approved", "rejected", "requires_correction", "status_modified"]
    if req.decision not in valid_decisions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid decision '{req.decision}'. Valid options: {valid_decisions}"
        )

    # Check Reviewer Profile and Authorization
    profile = None
    if req.reviewer_profile_id:
        profile = db.query(ReviewerProfile).filter(ReviewerProfile.id == req.reviewer_profile_id).first()
    elif req.reviewer_code:
        profile = db.query(ReviewerProfile).filter(ReviewerProfile.reviewer_code == req.reviewer_code).first()
    else:
        profile = db.query(ReviewerProfile).filter(ReviewerProfile.full_name == req.reviewer_name).first()

    # Rule: Assigning VERIFIED status strictly requires an authorized expert profile
    if req.assigned_status == ValidationStatus.VERIFIED:
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Forbidden: Reviewer '{req.reviewer_name}' does not have a registered expert profile. "
                    "Only certified Deaf native signers or licensed RCI ISL interpreters can certify a sign as VERIFIED."
                )
            )
        if not profile.is_authorized_expert:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Forbidden: Reviewer '{profile.full_name}' ({profile.reviewer_code}) is not an authorized expert "
                    f"(Accreditation: {profile.accreditation_body or 'None'}). "
                    "Test accounts and unaccredited reviewers cannot certify signs as VERIFIED. "
                    "You may only submit review comments or assign needs_review / unsupported."
                )
            )

    # Create ReviewerValidation record
    review = ReviewerValidation(
        sign_record_id=sign.id,
        reviewer_profile_id=profile.id if profile else None,
        reviewer_name=profile.full_name if profile else req.reviewer_name,
        reviewer_role=profile.qualifications if profile else req.reviewer_role,
        affiliation=profile.institution_affiliation if profile else req.affiliation,
        accreditation_evidence=f"{profile.accreditation_body} (Ref: {profile.accreditation_number})" if profile and profile.accreditation_number else None,
        decision=req.decision,
        assigned_status=req.assigned_status,
        corrections=req.corrections,
        suggested_regional_variation=req.suggested_regional_variation,
        comments=req.comments,
        accuracy_rating=req.accuracy_rating,
        reviewed_at=datetime.utcnow()
    )
    db.add(review)

    # Update SignRecord
    sign.validation_status = req.assigned_status
    if req.assigned_status == ValidationStatus.VERIFIED:
        sign.is_authentic = True
        sign.validation_date = datetime.utcnow()
    elif req.assigned_status == ValidationStatus.UNSUPPORTED:
        sign.is_authentic = False

    if req.suggested_regional_variation:
        sign.regional_dialect = req.suggested_regional_variation

    if req.accuracy_rating is not None:
        sign.confidence_score = req.accuracy_rating / 5.0

    db.commit()
    db.refresh(review)

    return ValidationDecisionResponse(
        id=review.id,
        sign_record_id=sign.id,
        reviewer_name=review.reviewer_name,
        reviewer_role=review.reviewer_role,
        decision=review.decision,
        assigned_status=review.assigned_status,
        comments=review.comments,
        reviewed_at=review.reviewed_at,
        message=f"Validation decision '{req.decision}' successfully recorded for sign {sign.sign_gloss}."
    )

@router.get("/audit-trail/{sign_record_id}", response_model=List[dict])
def get_validation_audit_trail(
    sign_record_id: int,
    db: Session = Depends(get_db)
):
    """
    Returns the complete chronological review history and decision trail for a given sign.
    """
    sign = db.query(SignRecord).filter(SignRecord.id == sign_record_id).first()
    if not sign:
        raise HTTPException(status_code=404, detail="Sign not found")

    reviews = (
        db.query(ReviewerValidation)
        .filter(ReviewerValidation.sign_record_id == sign_record_id)
        .order_by(ReviewerValidation.reviewed_at.desc())
        .all()
    )

    trail = []
    for rev in reviews:
        trail.append({
            "id": rev.id,
            "reviewer_profile_id": rev.reviewer_profile_id,
            "reviewer_name": rev.reviewer_name,
            "reviewer_role": rev.reviewer_role,
            "affiliation": rev.affiliation,
            "accreditation_evidence": rev.accreditation_evidence,
            "decision": rev.decision,
            "assigned_status": rev.assigned_status.value if rev.assigned_status else None,
            "corrections": rev.corrections,
            "suggested_regional_variation": rev.suggested_regional_variation,
            "comments": rev.comments,
            "accuracy_rating": rev.accuracy_rating,
            "reviewed_at": rev.reviewed_at.isoformat() if rev.reviewed_at else None
        })

    return trail
