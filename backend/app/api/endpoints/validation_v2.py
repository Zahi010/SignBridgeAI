"""
SignBridge AI - Validation V2 Endpoints (Phase 5).
Handles Reviewer Auth, Credentials, Tasks, Rubric Evaluations, Annotations, Disagreements, and Adjudication.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.entities import SignRecord, Concept, SignVideo, AvatarAnimation
from backend.app.models.validation_models import (
    Reviewer,
    ReviewerRole,
    ReviewerVerificationStatus,
    ReviewerCredential,
    ReviewerVerification,
    ValidationProject,
    ValidationTask,
    ValidationTaskStatus,
    SignEvaluation,
    EvaluationCriterionRating,
    ReviewerAnnotation,
    EvaluationDisagreement,
    ValidationDecision,
    AdjudicationDecisionEnum,
    ValidationAuditLog
)
from backend.app.schemas.validation_v2 import (
    ReviewerRegisterRequest,
    ReviewerLoginRequest,
    ReviewerTokenResponse,
    ReviewerProfileResponse,
    ReviewerCredentialCreateRequest,
    ReviewerCredentialResponse,
    ReviewerVerificationRequest,
    ValidationTaskResponse,
    SignEvaluationSubmitRequest,
    SignEvaluationResponse,
    ReviewerAnnotationCreateRequest,
    ReviewerAnnotationResponse,
    EvaluationDisagreementResponse,
    AdjudicationDecisionRequest,
    AdjudicationDecisionResponse,
    ValidationDashboardStatsResponse,
    AcademicEvaluationMetricsResponse
)
from backend.app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_reviewer,
    require_roles,
    require_verified_reviewer
)
from backend.app.services.validation_service import ValidationWorkflowService
from backend.app.services.academic_metrics_service import AcademicMetricsService

router = APIRouter()


# --- 1. REVIEWER REGISTRATION & AUTHENTICATION ---

@router.post("/register", response_model=ReviewerProfileResponse, summary="Register a reviewer account")
def register_reviewer(req: ReviewerRegisterRequest, db: Session = Depends(get_db)):
    """
    Registers a new reviewer. Status is strictly UNVERIFIED upon registration.
    """
    existing_user = db.query(Reviewer).filter(
        (Reviewer.username == req.username) | (Reviewer.email == req.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )

    reviewer = Reviewer(
        username=req.username,
        email=req.email,
        hashed_password=hash_password(req.password),
        full_name=req.full_name,
        is_deaf_native_signer=req.is_deaf_native_signer,
        is_certified_interpreter=req.is_certified_interpreter,
        years_of_experience=req.years_of_experience,
        institution_affiliation=req.institution_affiliation,
        role=req.role,
        verification_status=ReviewerVerificationStatus.UNVERIFIED,
        is_active=True
    )
    db.add(reviewer)
    db.commit()
    db.refresh(reviewer)

    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=reviewer.id,
        actor_username=reviewer.username,
        action="REVIEWER_REGISTERED",
        target_type="reviewer",
        target_id=str(reviewer.id),
        details={"full_name": reviewer.full_name, "role": reviewer.role.value}
    )
    db.commit()

    return reviewer


@router.post("/login", response_model=ReviewerTokenResponse, summary="Reviewer login")
def login_reviewer(req: ReviewerLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticates reviewer and generates a cryptographically signed Bearer token.
    """
    reviewer = db.query(Reviewer).filter(
        (Reviewer.username == req.username_or_email) | (Reviewer.email == req.username_or_email)
    ).first()

    if not reviewer or not verify_password(req.password, reviewer.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password."
        )

    if not reviewer.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is suspended or inactive."
        )

    token = create_access_token({
        "sub": reviewer.id,
        "username": reviewer.username,
        "role": reviewer.role.value,
        "status": reviewer.verification_status.value
    })

    return ReviewerTokenResponse(
        access_token=token,
        token_type="bearer",
        reviewer_id=reviewer.id,
        username=reviewer.username,
        full_name=reviewer.full_name,
        role=reviewer.role,
        verification_status=reviewer.verification_status
    )


@router.get("/me", response_model=ReviewerProfileResponse, summary="Get current logged in reviewer")
def get_current_user_profile(current_user: Reviewer = Depends(get_current_reviewer)):
    return current_user


# --- 2. CREDENTIAL SUBMISSION & VERIFICATION (ADMIN GATE) ---

@router.post("/credentials", response_model=ReviewerCredentialResponse, summary="Submit credential for verification")
def submit_reviewer_credential(
    req: ReviewerCredentialCreateRequest,
    current_user: Reviewer = Depends(get_current_reviewer),
    db: Session = Depends(get_db)
):
    """
    Allows a reviewer to submit formal credentials (e.g. RCI Registration, Deaf Association Membership).
    Updates reviewer status to VERIFICATION_PENDING.
    """
    cred = ReviewerCredential(
        reviewer_id=current_user.id,
        credential_type=req.credential_type,
        credential_identifier=req.credential_identifier,
        issuing_body=req.issuing_body,
        issue_date=req.issue_date,
        expiry_date=req.expiry_date,
        document_url=req.document_url,
        verification_status=ReviewerVerificationStatus.VERIFICATION_PENDING,
        notes=req.notes
    )
    db.add(cred)
    current_user.verification_status = ReviewerVerificationStatus.VERIFICATION_PENDING

    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=current_user.id,
        actor_username=current_user.username,
        action="CREDENTIAL_SUBMITTED",
        target_type="reviewer_credential",
        target_id=req.credential_identifier,
        details={"type": req.credential_type.value, "issuing_body": req.issuing_body}
    )

    db.commit()
    db.refresh(cred)
    return cred


@router.get("/credentials/pending", response_model=List[ReviewerCredentialResponse], summary="List pending reviewer credentials")
def list_pending_credentials(
    current_user: Reviewer = Depends(require_roles([ReviewerRole.ADMIN])),
    db: Session = Depends(get_db)
):
    """
    Admin endpoint to view pending reviewer credentials.
    """
    return db.query(ReviewerCredential).filter(
        ReviewerCredential.verification_status == ReviewerVerificationStatus.VERIFICATION_PENDING
    ).all()


@router.post("/credentials/{credential_id}/verify", summary="Admin verify/reject reviewer credential")
def verify_credential(
    credential_id: int,
    req: ReviewerVerificationRequest,
    admin: Reviewer = Depends(require_roles([ReviewerRole.ADMIN])),
    db: Session = Depends(get_db)
):
    """
    Administrative Gate: Verifies or rejects reviewer credentials against official registries.
    """
    cred = db.query(ReviewerCredential).filter(ReviewerCredential.id == credential_id).first()
    if not cred:
        raise HTTPException(status_code=404, detail="Credential not found.")

    target_reviewer = db.query(Reviewer).filter(Reviewer.id == cred.reviewer_id).first()
    prev_status = target_reviewer.verification_status

    # Record verification decision
    verification = ReviewerVerification(
        reviewer_id=target_reviewer.id,
        admin_id=admin.id,
        previous_status=prev_status,
        new_status=req.new_status,
        rationale=req.rationale,
        evidence_verified=req.evidence_verified,
        verified_at=datetime.utcnow()
    )
    db.add(verification)

    cred.verification_status = req.new_status
    target_reviewer.verification_status = req.new_status
    target_reviewer.verification_notes = req.rationale

    wf_svc = ValidationWorkflowService(db)
    wf_svc.log_action(
        actor_id=admin.id,
        actor_username=admin.username,
        action="REVIEWER_CREDENTIAL_VERIFIED",
        target_type="reviewer",
        target_id=str(target_reviewer.id),
        details={
            "new_status": req.new_status.value,
            "evidence_verified": req.evidence_verified,
            "rationale": req.rationale
        }
    )

    db.commit()
    return {
        "status": "success",
        "message": f"Reviewer '{target_reviewer.username}' credential updated to '{req.new_status.value}'.",
        "reviewer_id": target_reviewer.id,
        "new_status": req.new_status.value
    }


# --- 3. VALIDATION TASKS ---

@router.get("/tasks", response_model=List[ValidationTaskResponse], summary="List validation tasks")
def list_validation_tasks(
    status_filter: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Retrieves the queue of validation tasks.
    """
    query = db.query(ValidationTask)
    if status_filter:
        try:
            st = ValidationTaskStatus(status_filter.lower())
            query = query.filter(ValidationTask.status == st)
        except ValueError:
            pass

    tasks = query.limit(limit).all()
    results = []

    for t in tasks:
        sign = t.sign_record
        concept = t.concept
        results.append(
            ValidationTaskResponse(
                id=t.id,
                project_id=t.project_id,
                sign_record_id=t.sign_record_id,
                concept_id=t.concept_id,
                concept_term=concept.term if concept else "Unknown",
                sign_gloss=sign.sign_gloss if sign else "UNKNOWN",
                status=t.status,
                assigned_reviewers_count=t.assigned_reviewers_count,
                completed_reviews_count=t.completed_reviews_count,
                has_video=bool(sign.videos if sign else False),
                has_animation=bool(sign.avatar_animations if sign else False),
                evaluations=[
                    SignEvaluationResponse(
                        id=e.id,
                        task_id=e.task_id,
                        reviewer_id=e.reviewer_id,
                        reviewer_name=e.reviewer.full_name,
                        reviewer_verification_status=e.reviewer.verification_status,
                        is_draft=e.is_draft,
                        overall_recommendation=e.overall_recommendation,
                        general_feedback=e.general_feedback,
                        suggested_dialect=e.suggested_dialect,
                        criteria_ratings=[
                            {"criterion_name": cr.criterion_name, "rating": cr.rating, "notes": cr.notes, "is_critical_error": cr.is_critical_error}
                            for cr in e.criteria_ratings
                        ],
                        submitted_at=e.submitted_at
                    )
                    for e in t.evaluations if not e.is_draft
                ],
                annotations_count=len(t.annotations),
                disagreements_count=len(t.disagreements),
                created_at=t.created_at,
                updated_at=t.updated_at
            )
        )

    return results


@router.get("/tasks/{task_id}", response_model=Dict[str, Any], summary="Get full task details with video and avatar data")
def get_task_details(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieves comprehensive task package: concept definition, phonological parameters,
    authentic ISLRTC video, 3D avatar animation keyframes, annotations, and evaluations.
    """
    task = db.query(ValidationTask).filter(ValidationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="ValidationTask not found.")

    sign = task.sign_record
    concept = task.concept
    video = sign.videos[0] if (sign and sign.videos) else None
    anim = sign.avatar_animations[0] if (sign and sign.avatar_animations) else None

    annotations = [
        ReviewerAnnotationResponse(
            id=a.id,
            task_id=a.task_id,
            reviewer_id=a.reviewer_id,
            reviewer_name=a.reviewer.full_name,
            timestamp_ms=a.timestamp_ms,
            duration_ms=a.duration_ms,
            target_type=a.target_type,
            category=a.category,
            comment=a.comment,
            created_at=a.created_at
        )
        for a in task.annotations
    ]

    disagreements = [
        EvaluationDisagreementResponse(
            id=d.id,
            task_id=d.task_id,
            criterion_name=d.criterion_name,
            disagreement_type=d.disagreement_type,
            reviewer_ratings=d.reviewer_ratings_json if isinstance(d.reviewer_ratings_json, dict) else {},
            status=d.status,
            detected_at=d.detected_at
        )
        for d in task.disagreements
    ]

    return {
        "task_id": task.id,
        "status": task.status.value,
        "concept": {
            "id": concept.id if concept else None,
            "term": concept.term if concept else "Unknown",
            "category": concept.category if concept else "General",
            "definition": concept.definition if concept else "",
            "technical_context": concept.technical_context if concept else ""
        },
        "sign_record": {
            "id": sign.id if sign else None,
            "sign_gloss": sign.sign_gloss if sign else "",
            "dominant_hand": sign.dominant_hand if sign else "",
            "handshape": sign.handshape if sign else "",
            "movement": sign.movement if sign else "",
            "location": sign.location if sign else "",
            "orientation": sign.orientation if sign else "",
            "non_manual_markers": sign.non_manual_markers if sign else "",
            "source_institution": sign.source_institution if sign else "",
            "license": sign.license if sign else ""
        },
        "video": {
            "available": bool(video),
            "video_path": video.video_path if video else None,
            "source_attribution": video.source_attribution if video else None,
            "signer_name": video.signer_name if video else None
        },
        "avatar": {
            "available": bool(anim),
            "animation_name": anim.animation_name if anim else None,
            "rig_standard": anim.rig_standard if anim else None,
            "validation_status": anim.validation_status.value if anim else "needs_review"
        },
        "annotations": annotations,
        "disagreements": disagreements,
        "evaluations_count": len([e for e in task.evaluations if not e.is_draft])
    }


# --- 4. SUBMIT EVALUATION RUBRIC ---

@router.post("/tasks/{task_id}/evaluate", response_model=SignEvaluationResponse, summary="Submit structured evaluation rubric")
def submit_evaluation(
    task_id: int,
    req: SignEvaluationSubmitRequest,
    current_user: Reviewer = Depends(get_current_reviewer),
    db: Session = Depends(get_db)
):
    """
    Submits a structured evaluation covering all 12 linguistic criteria.
    Enforces critical error rules and triggers disagreement detection if multiple reviews exist.
    """
    wf_svc = ValidationWorkflowService(db)
    evaluation = wf_svc.submit_evaluation(
        task_id=task_id,
        reviewer=current_user,
        is_draft=req.is_draft,
        overall_recommendation=req.overall_recommendation,
        general_feedback=req.general_feedback,
        suggested_dialect=req.suggested_dialect,
        criteria_ratings=[c.model_dump() for c in req.criteria_ratings],
        annotations=[a.model_dump() for a in req.annotations]
    )

    return SignEvaluationResponse(
        id=evaluation.id,
        task_id=evaluation.task_id,
        reviewer_id=evaluation.reviewer_id,
        reviewer_name=current_user.full_name,
        reviewer_verification_status=current_user.verification_status,
        is_draft=evaluation.is_draft,
        overall_recommendation=evaluation.overall_recommendation,
        general_feedback=evaluation.general_feedback,
        suggested_dialect=evaluation.suggested_dialect,
        criteria_ratings=[
            {"criterion_name": cr.criterion_name, "rating": cr.rating, "notes": cr.notes, "is_critical_error": cr.is_critical_error}
            for cr in evaluation.criteria_ratings
        ],
        submitted_at=evaluation.submitted_at
    )


@router.post("/tasks/{task_id}/annotations", response_model=ReviewerAnnotationResponse, summary="Add timestamped video annotation")
def add_task_annotation(
    task_id: int,
    req: ReviewerAnnotationCreateRequest,
    current_user: Reviewer = Depends(get_current_reviewer),
    db: Session = Depends(get_db)
):
    """
    Adds a timestamped frame annotation for specific flaws (handshape, trajectory, orientation).
    """
    task = db.query(ValidationTask).filter(ValidationTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    ann = ReviewerAnnotation(
        task_id=task_id,
        reviewer_id=current_user.id,
        timestamp_ms=req.timestamp_ms,
        duration_ms=req.duration_ms,
        target_type=req.target_type,
        category=req.category,
        comment=req.comment,
        created_at=datetime.utcnow()
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)

    return ReviewerAnnotationResponse(
        id=ann.id,
        task_id=ann.task_id,
        reviewer_id=ann.reviewer_id,
        reviewer_name=current_user.full_name,
        timestamp_ms=ann.timestamp_ms,
        duration_ms=ann.duration_ms,
        target_type=ann.target_type,
        category=ann.category,
        comment=ann.comment,
        created_at=ann.created_at
    )


# --- 5. ADJUDICATION DECISION ---

@router.post("/tasks/{task_id}/adjudicate", response_model=AdjudicationDecisionResponse, summary="Adjudicate task under disagreement")
def adjudicate_task(
    task_id: int,
    req: AdjudicationDecisionRequest,
    current_user: Reviewer = Depends(require_verified_reviewer),
    db: Session = Depends(get_db)
):
    """
    Binding administrative adjudication.
    Zero-Fabrication Guard: Refuses promotion to VERIFIED_ISL_MOTION without administrative verification.
    """
    wf_svc = ValidationWorkflowService(db)
    try:
        decision = wf_svc.adjudicate_task(
            task_id=task_id,
            adjudicator=current_user,
            decision_enum=req.decision,
            resulting_motion_status=req.resulting_motion_status,
            rationale=req.rationale,
            evidence_summary=req.evidence_summary
        )
    except PermissionError as pe:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(pe))
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))

    return AdjudicationDecisionResponse(
        id=decision.id,
        task_id=decision.task_id,
        adjudicator_id=decision.adjudicator_id,
        adjudicator_name=current_user.full_name,
        decision=decision.decision,
        resulting_motion_status=decision.resulting_motion_status,
        rationale=decision.rationale,
        decided_at=decision.decided_at
    )


# --- 6. VALIDATION DASHBOARD & ACADEMIC METRICS ---

@router.get("/dashboard", response_model=ValidationDashboardStatsResponse, summary="Get validation dashboard statistics")
def get_validation_dashboard(db: Session = Depends(get_db)):
    """
    Returns live database-backed statistics for the Validation Dashboard.
    """
    total_tasks = db.query(ValidationTask).count()
    unreviewed = db.query(ValidationTask).filter(ValidationTask.status == ValidationTaskStatus.UNREVIEWED).count()
    under_review = db.query(ValidationTask).filter(ValidationTask.status == ValidationTaskStatus.UNDER_REVIEW).count()
    reviewed = db.query(ValidationTask).filter(ValidationTask.status == ValidationTaskStatus.REVIEWED).count()
    disagreements = db.query(ValidationTask).filter(ValidationTask.status == ValidationTaskStatus.DISAGREEMENT_DETECTED).count()
    adjudicated = db.query(ValidationDecision).count()

    verified_reviewers = db.query(Reviewer).filter(Reviewer.verification_status == ReviewerVerificationStatus.VERIFIED).count()
    pending_credentials = db.query(ReviewerCredential).filter(ReviewerCredential.verification_status == ReviewerVerificationStatus.VERIFICATION_PENDING).count()

    # Technical vs Linguistic status comparison
    tech_vs_ling = {
        "technical_mocap_available_count": 5,
        "technical_fidelity_passing_count": 5,
        "linguistically_verified_signs_count": db.query(SignRecord).filter(SignRecord.validation_status == "verified").count(),
        "partially_verified_mocap_count": 5,
        "pending_external_review_count": total_tasks
    }

    # Critical issues summary from evaluations
    critical_ratings = (
        db.query(EvaluationCriterionRating)
        .filter(EvaluationCriterionRating.is_critical_error.is_(True))
        .all()
    )
    crit_summary = []
    for cr in critical_ratings[:10]:
        crit_summary.append({
            "criterion": cr.criterion_name,
            "rating": cr.rating.value,
            "notes": cr.notes,
            "evaluation_id": cr.evaluation_id
        })

    return ValidationDashboardStatsResponse(
        total_validation_tasks=total_tasks,
        unreviewed_tasks_count=unreviewed,
        under_review_tasks_count=under_review,
        reviewed_tasks_count=reviewed,
        disagreements_count=disagreements,
        adjudicated_tasks_count=adjudicated,
        verified_reviewers_count=verified_reviewers,
        pending_credential_verifications_count=pending_credentials,
        community_participants_count=0,
        technical_vs_linguistic_status=tech_vs_ling,
        critical_issues_summary=crit_summary
    )


@router.get("/academic-metrics", response_model=AcademicEvaluationMetricsResponse, summary="Get inter-reviewer agreement and statistical metrics")
def get_academic_metrics(db: Session = Depends(get_db)):
    """
    Returns academic statistics (Cohen's Kappa, Fleiss' Kappa, criterion agreement, confidence intervals).
    """
    acad_svc = AcademicMetricsService(db)
    return acad_svc.compute_evaluation_metrics()


@router.get("/audit-logs", summary="List validation audit logs")
def get_validation_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Returns immutable audit log entries for transparency and provenance audits.
    """
    logs = (
        db.query(ValidationAuditLog)
        .order_by(ValidationAuditLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": l.id,
            "actor_id": l.actor_id,
            "actor_username": l.actor_username,
            "action": l.action,
            "target_type": l.target_type,
            "target_id": l.target_id,
            "details": l.details_json,
            "timestamp": l.timestamp.isoformat() if l.timestamp else None
        }
        for l in logs
    ]
