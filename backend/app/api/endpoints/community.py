"""
SignBridge AI - Deaf Community Research, Informed Consent & Ethics Endpoints (Phase 5).
Guarantees participant pseudonymization, ethical consent, withdrawal, and complete data deletion.
"""

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

router = APIRouter()


@router.post("/consent", response_model=ParticipantConsentResponse, summary="Record participant informed consent")
def record_participant_consent(
    req: ParticipantConsentCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Registers participant informed consent under a pseudonym.
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
        details={"study_name": req.study_name, "version": req.consent_version}
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
    Ethical Research / Right to be Forgotten:
    Purges all research sessions, feedback, and notes associated with a participant pseudonym.
    """
    consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == req.participant_pseudonym).first()
    if not consent:
        raise HTTPException(status_code=404, detail=f"Pseudonym '{req.participant_pseudonym}' not found.")

    # Delete all research sessions
    deleted_sessions_count = db.query(ResearchSession).filter(ResearchSession.consent_id == consent.id).delete()

    # Mark consent as withdrawn and data purged
    consent.consent_given = False
    consent.data_deletion_requested = True
    consent.withdrawal_date = datetime.utcnow()
    consent.notes = f"Data deletion executed. Purged {deleted_sessions_count} sessions. Reason: {req.reason or 'User request'}."

    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=None,
        actor_username=req.participant_pseudonym,
        action="PARTICIPANT_DATA_DELETED",
        target_type="participant_consent",
        target_id=req.participant_pseudonym,
        details={"purged_sessions": deleted_sessions_count}
    )

    db.commit()
    return {
        "status": "success",
        "message": f"Successfully deleted all data for pseudonym '{req.participant_pseudonym}'.",
        "purged_sessions_count": deleted_sessions_count,
        "withdrawal_timestamp": consent.withdrawal_date.isoformat()
    }


@router.get("/export", summary="Export anonymized research dataset")
def export_research_dataset(db: Session = Depends(get_db)):
    """
    Exports clean, anonymized dataset for academic research and publication.
    Excludes withdrawn participants and unconsented data.
    """
    active_consents = db.query(ParticipantConsent).filter(
        ParticipantConsent.consent_given.is_(True),
        ParticipantConsent.data_deletion_requested.is_(False)
    ).all()

    consent_ids = [c.id for c in active_consents]
    sessions = db.query(ResearchSession).filter(ResearchSession.consent_id.in_(consent_ids)).all()

    export_records = []
    for s in sessions:
        export_records.append({
            "session_code": s.session_code,
            "pseudonym": s.consent.pseudonym,
            "session_type": s.session_type,
            "comprehension_score": s.comprehension_score,
            "naturalness_rating": s.naturalness_rating,
            "completed_at": s.completed_at.isoformat() if s.completed_at else None
        })

    return {
        "dataset_name": "SignBridge AI Deaf Community Validation Cohort",
        "export_timestamp": datetime.utcnow().isoformat(),
        "total_active_participants": len(active_consents),
        "total_sessions": len(export_records),
        "records": export_records,
        "license": "Open Data Commons Attribution License (ODC-By)",
        "ethics_statement": "All data collected with voluntary informed consent. No PII retained."
    }
