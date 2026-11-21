"""
SignBridge AI - Deaf Community Research, Informed Consent & Ethics Endpoints (Phase 5 & 6).
Guarantees participant pseudonymization, ethical consent, withdrawal, and complete data deletion.
Enforces multi-license export segregation via ExportEligibilityService.
"""

import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.validation_models import (
    ParticipantConsent,
    ResearchSession,
    ValidationAuditLog
)
from backend.app.schemas.validation_v2 import (
    ParticipantConsentCreateRequest,
    ParticipantConsentResponse,
    ResearchSessionCreateRequest,
    ResearchSessionResponse,
    DataDeletionRequest
)
from backend.app.services.validation_service import ValidationWorkflowService
from backend.app.services.export_eligibility_service import ExportEligibilityService

router = APIRouter()


@router.post("/consent", response_model=ParticipantConsentResponse, summary="Record participant informed consent")
def record_participant_consent(
    req: ParticipantConsentCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Registers participant informed consent under a pseudonym with granular consent flags.
    No personally identifiable information (PII) is stored.
    """
    existing = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == req.pseudonym).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Consent record for pseudonym '{req.pseudonym}' already exists."
        )

    consent = ParticipantConsent(
        pseudonym=req.pseudonym,
        study_name=req.study_name,
        consent_version=req.consent_version,
        consent_given=req.consent_given,
        can_withdraw_anytime=req.can_withdraw_anytime,
        data_deletion_requested=False,
        consent_general_research=getattr(req, "consent_general_research", True),
        consent_video_recording=getattr(req, "consent_video_recording", False),
        consent_data_sharing=getattr(req, "consent_data_sharing", True),
        consent_academic_publication=getattr(req, "consent_academic_publication", True),
        is_anonymized=False,
        consent_date=datetime.utcnow(),
        notes=req.notes
    )
    db.add(consent)

    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=None,
        actor_username=req.pseudonym,
        action="PARTICIPANT_CONSENT_RECORDED",
        target_type="participant_consent",
        target_id=req.pseudonym,
        details={
            "study_name": req.study_name,
            "version": req.consent_version,
            "data_sharing": consent.consent_data_sharing,
            "publication": consent.consent_academic_publication
        }
    )

    db.commit()
    db.refresh(consent)
    return consent


@router.get("/consent/{pseudonym}", response_model=ParticipantConsentResponse, summary="Get participant consent by pseudonym")
def get_consent_by_pseudonym(pseudonym: str, db: Session = Depends(get_db)):
    consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == pseudonym).first()
    if not consent:
        raise HTTPException(status_code=404, detail=f"No consent record found for '{pseudonym}'.")
    return consent


@router.post("/sessions", response_model=ResearchSessionResponse, summary="Record community research session")
def record_research_session(
    req: ResearchSessionCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Records an anonymized community research session (comprehension or naturalness rating).
    Strict requirement: participant must have active informed consent.
    """
    consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == req.participant_pseudonym).first()
    if not consent or not consent.consent_given or consent.data_deletion_requested:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot record session: Participant '{req.participant_pseudonym}' has no valid informed consent or has withdrawn."
        )

    existing_sess = db.query(ResearchSession).filter(ResearchSession.session_code == req.session_code).first()
    if existing_sess:
        raise HTTPException(status_code=400, detail=f"Session code '{req.session_code}' already exists.")

    session_record = ResearchSession(
        consent_id=consent.id,
        session_code=req.session_code,
        session_type=req.session_type,
        concepts_tested_json=str(req.concepts_tested),
        comprehension_score=req.comprehension_score,
        naturalness_rating=req.naturalness_rating,
        feedback_notes=req.feedback_notes,
        completed_at=datetime.utcnow()
    )
    db.add(session_record)

    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=None,
        actor_username=req.participant_pseudonym,
        action="RESEARCH_SESSION_RECORDED",
        target_type="research_session",
        target_id=req.session_code,
        details={"type": req.session_type, "comprehension": req.comprehension_score}
    )

    db.commit()
    db.refresh(session_record)

    return ResearchSessionResponse(
        id=session_record.id,
        session_code=session_record.session_code,
        participant_pseudonym=consent.pseudonym,
        session_type=session_record.session_type,
        comprehension_score=session_record.comprehension_score,
        naturalness_rating=session_record.naturalness_rating,
        completed_at=session_record.completed_at
    )


@router.get("/sessions", response_model=List[ResearchSessionResponse], summary="List community research sessions")
def list_research_sessions(db: Session = Depends(get_db)):
    sessions = db.query(ResearchSession).all()
    results = []
    for s in sessions:
        results.append(
            ResearchSessionResponse(
                id=s.id,
                session_code=s.session_code,
                participant_pseudonym=s.consent.pseudonym if s.consent else "ANONYMOUS",
                session_type=s.session_type,
                comprehension_score=s.comprehension_score,
                naturalness_rating=s.naturalness_rating,
                completed_at=s.completed_at
            )
        )
    return results


@router.post("/delete-data", summary="Participant withdrawal and complete data deletion")
def delete_participant_data(
    req: DataDeletionRequest,
    db: Session = Depends(get_db)
):
    """
    Ethical Research / Right to be Forgotten (Phase 6 Hardened):
    1. Purges all research sessions, feedback, and notes associated with a participant pseudonym.
    2. Irreversibly hashes the pseudonym to protect audit integrity without retaining identifiable pseudonyms.
    3. Scrubs historical audit log entries referencing the original pseudonym.
    4. Logs a non-identifying erasure audit record.
    """
    consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == req.participant_pseudonym).first()
    if not consent:
        raise HTTPException(status_code=404, detail=f"Pseudonym '{req.participant_pseudonym}' not found.")

    # 1. Purge all research sessions
    deleted_sessions_count = db.query(ResearchSession).filter(ResearchSession.consent_id == consent.id).delete()

    # 2. Cryptographically anonymize the pseudonym
    orig_pseudonym = consent.pseudonym
    hashed_orig = hashlib.sha256(orig_pseudonym.encode("utf-8")).hexdigest()
    purged_pseudonym = f"ANONYMIZED_PURGED_{hashed_orig[:12]}"

    consent.original_pseudonym_hash = hashed_orig
    consent.pseudonym = purged_pseudonym
    consent.is_anonymized = True
    consent.consent_given = False
    consent.data_deletion_requested = True
    consent.withdrawal_date = datetime.utcnow()
    consent.notes = f"Right-to-erasure executed. Sessions purged: {deleted_sessions_count}. Reason: {req.reason or 'User withdrawal request'}."

    # 3. Scrub historical audit logs that reference the original pseudonym
    db.query(ValidationAuditLog).filter(ValidationAuditLog.actor_username == orig_pseudonym).update(
        {ValidationAuditLog.actor_username: "ANONYMIZED_PURGED_USER"}
    )
    db.query(ValidationAuditLog).filter(ValidationAuditLog.target_id == orig_pseudonym).update(
        {ValidationAuditLog.target_id: purged_pseudonym}
    )

    # 4. Log non-identifying erasure audit entry
    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=None,
        actor_username="RIGHT_TO_ERASURE_SYSTEM",
        action="RIGHT_TO_ERASURE_EXECUTED",
        target_type="participant_consent",
        target_id=purged_pseudonym,
        details={"purged_sessions": deleted_sessions_count}
    )

    db.commit()
    return {
        "status": "success",
        "message": f"Successfully deleted all data and cryptographically de-identified pseudonym.",
        "purged_sessions_count": deleted_sessions_count,
        "withdrawal_timestamp": consent.withdrawal_date.isoformat(),
        "anonymized_pseudonym": purged_pseudonym
    }


@router.get("/export", summary="Export segregated research dataset")
def export_research_dataset(
    publication_only: bool = Query(default=False, description="Filter strictly for academic publication consent"),
    db: Session = Depends(get_db)
):
    """
    Exports clean, license-segregated dataset for academic research and publication.
    Enforces multi-license segregation (ODC-By, CC-BY-4.0, GODL-India).
    Strictly excludes withdrawn participants and unconsented data.
    """
    export_svc = ExportEligibilityService(db)
    return export_svc.generate_segregated_export(academic_publication_only=publication_only)


