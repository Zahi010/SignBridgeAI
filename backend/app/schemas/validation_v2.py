"""
SignBridge AI - Phase 5 Pydantic Schemas for Linguistic Validation & Academic Evaluation.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from backend.app.models.validation_models import (
    ReviewerRole,
    ReviewerVerificationStatus,
    CredentialType,
    ValidationTaskStatus,
    RubricCriterionRating,
    AdjudicationDecisionEnum
)


# --- REVIEWER & AUTH SCHEMAS ---

class ReviewerRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=150)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2, max_length=150)
    is_deaf_native_signer: bool = False
    is_certified_interpreter: bool = False
    years_of_experience: int = Field(default=0, ge=0)
    institution_affiliation: Optional[str] = None
    role: ReviewerRole = ReviewerRole.REVIEWER


class ReviewerLoginRequest(BaseModel):
    username_or_email: str
    password: str


class ReviewerTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    reviewer_id: int
    username: str
    full_name: str
    role: ReviewerRole
    verification_status: ReviewerVerificationStatus


class ReviewerCredentialCreateRequest(BaseModel):
    credential_type: CredentialType
    credential_identifier: str = Field(..., min_length=2, description="e.g. RCI Registration Number or Membership ID")
    issuing_body: str = Field(..., min_length=2, description="e.g. Rehabilitation Council of India")
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    document_url: Optional[str] = None
    notes: Optional[str] = None


class ReviewerCredentialResponse(BaseModel):
    id: int
    reviewer_id: int
    credential_type: CredentialType
    credential_identifier: str
    issuing_body: str
    verification_status: ReviewerVerificationStatus
    notes: Optional[str] = None
    created_at: datetime


class ReviewerProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_deaf_native_signer: bool
    is_certified_interpreter: bool
    years_of_experience: int
    institution_affiliation: Optional[str] = None
    role: ReviewerRole
    verification_status: ReviewerVerificationStatus
    verification_notes: Optional[str] = None
    credentials: List[ReviewerCredentialResponse] = []
    created_at: datetime


class ReviewerVerificationRequest(BaseModel):
    new_status: ReviewerVerificationStatus
    rationale: str = Field(..., min_length=5)
    evidence_verified: bool = Field(..., description="Whether administrative staff checked authoritative RCI/association databases")


# --- VALIDATION TASK & EVALUATION RUBRIC SCHEMAS ---

class CriterionRatingItem(BaseModel):
    criterion_name: str = Field(..., description="e.g. handshape, orientation, location, movement, facial_nmm, grammar, etc.")
    rating: RubricCriterionRating
    notes: Optional[str] = None
    is_critical_error: bool = False


class ReviewerAnnotationCreateRequest(BaseModel):
    task_id: int
    timestamp_ms: int = Field(..., ge=0)
    duration_ms: int = Field(default=0, ge=0)
    target_type: str = Field(default="avatar", description="'video', 'avatar', or 'comparison'")
    category: str = Field(..., description="'handshape_error', 'movement_jerk', 'orientation_flaw', etc.")
    comment: str = Field(..., min_length=2)


class ReviewerAnnotationResponse(BaseModel):
    id: int
    task_id: int
    reviewer_id: int
    reviewer_name: str
    timestamp_ms: int
    duration_ms: int
    target_type: str
    category: str
    comment: str
    created_at: datetime


class SignEvaluationSubmitRequest(BaseModel):
    task_id: int
    is_draft: bool = False
    overall_recommendation: str = Field(..., description="'accept', 'reject', 'needs_revision', 'inconclusive'")
    general_feedback: Optional[str] = None
    suggested_dialect: Optional[str] = None
    criteria_ratings: List[CriterionRatingItem] = []
    annotations: List[ReviewerAnnotationCreateRequest] = []


class EvaluationCriterionResponse(BaseModel):
    criterion_name: str
    rating: RubricCriterionRating
    notes: Optional[str] = None
    is_critical_error: bool


class SignEvaluationResponse(BaseModel):
    id: int
    task_id: int
    reviewer_id: int
    reviewer_name: str
    reviewer_verification_status: ReviewerVerificationStatus
    is_draft: bool
    overall_recommendation: str
    general_feedback: Optional[str] = None
    suggested_dialect: Optional[str] = None
    criteria_ratings: List[EvaluationCriterionResponse] = []
    submitted_at: datetime


class ValidationTaskResponse(BaseModel):
    id: int
    project_id: Optional[int]
    sign_record_id: int
    concept_id: int
    concept_term: str
    sign_gloss: str
    status: ValidationTaskStatus
    assigned_reviewers_count: int
    completed_reviews_count: int
    has_video: bool
    has_animation: bool
    evaluations: List[SignEvaluationResponse] = []
    annotations_count: int = 0
    disagreements_count: int = 0
    created_at: datetime
    updated_at: datetime


# --- DISAGREEMENT & ADJUDICATION SCHEMAS ---

class EvaluationDisagreementResponse(BaseModel):
    id: int
    task_id: int
    criterion_name: str
    disagreement_type: str
    reviewer_ratings: Dict[str, str]
    status: str
    detected_at: datetime


class AdjudicationDecisionRequest(BaseModel):
    decision: AdjudicationDecisionEnum
    resulting_motion_status: str = Field(..., description="'PARTIALLY_VERIFIED_MOTION', 'VERIFIED_ISL_MOTION', or 'REJECTED'")
    rationale: str = Field(..., min_length=10)
    evidence_summary: Optional[str] = None


class AdjudicationDecisionResponse(BaseModel):
    id: int
    task_id: int
    adjudicator_id: int
    adjudicator_name: str
    decision: AdjudicationDecisionEnum
    resulting_motion_status: str
    rationale: str
    decided_at: datetime


# --- PARTICIPANT CONSENT & COMMUNITY EVALUATION SCHEMAS ---

class ParticipantConsentCreateRequest(BaseModel):
    pseudonym: str = Field(..., min_length=3, description="Anonymized ID e.g. DEAF-PARTICIPANT-01")
    study_name: str = Field(default="SignBridge AI Deaf Community Evaluation Pilot 2026")
    consent_version: str = Field(default="v1.0-2026")
    consent_given: bool = True
    can_withdraw_anytime: bool = True
    notes: Optional[str] = None


class ParticipantConsentResponse(BaseModel):
    id: int
    pseudonym: str
    study_name: str
    consent_given: bool
    data_deletion_requested: bool
    consent_date: datetime


class ResearchSessionCreateRequest(BaseModel):
    participant_pseudonym: str
    session_code: str
    session_type: str = "comprehension_survey"
    concepts_tested: List[Dict[str, Any]] = []
    comprehension_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    naturalness_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    feedback_notes: Optional[str] = None


class ResearchSessionResponse(BaseModel):
    id: int
    session_code: str
    participant_pseudonym: str
    session_type: str
    comprehension_score: Optional[float]
    naturalness_rating: Optional[float]
    completed_at: datetime


class DataDeletionRequest(BaseModel):
    participant_pseudonym: str
    reason: Optional[str] = None


# --- ACADEMIC METRICS & DASHBOARD SCHEMAS ---

class CriterionAgreementStat(BaseModel):
    criterion_name: str
    total_evaluations: int
    agreement_percentage: float
    pass_rate: float
    major_error_rate: float


class AcademicEvaluationMetricsResponse(BaseModel):
    sample_size_category: str = Field(..., description="'NO_DATA', 'INSUFFICIENT_SAMPLE_SIZE', 'PRELIMINARY_RESULTS', or 'COMPLETED_EVALUATION'")
    total_signs_reviewed: int
    total_verified_reviewers: int
    total_evaluations: int
    cohens_kappa: Optional[float]
    fleiss_kappa: Optional[float]
    average_inter_reviewer_agreement_percent: float
    disagreement_frequency_percent: float
    critical_error_count: int
    criterion_statistics: List[CriterionAgreementStat]
    confidence_interval_95: Dict[str, float]
    academic_disclaimer: str


class ValidationDashboardStatsResponse(BaseModel):
    total_validation_tasks: int
    unreviewed_tasks_count: int
    under_review_tasks_count: int
    reviewed_tasks_count: int
    disagreements_count: int
    adjudicated_tasks_count: int
    verified_reviewers_count: int
    pending_credential_verifications_count: int
    community_participants_count: int
    technical_vs_linguistic_status: Dict[str, Any]
    critical_issues_summary: List[Dict[str, Any]]
