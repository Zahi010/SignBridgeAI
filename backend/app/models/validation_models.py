"""
SignBridge AI - Phase 5 Linguistic Validation, Reviewer Credentials & Community Research Models.
Strict adherence to Zero-Fabrication Policy:
- Clear separation between technical accuracy and linguistic validity.
- Preserves reviewer credentials, accreditation status, disagreements, annotations, and audit logs.
- Supports ethical community research: informed consent, participant pseudonymization, data deletion.
"""

import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Float
)
from sqlalchemy.orm import relationship
from backend.app.database.database import Base

def get_utc_now():
    return datetime.now(timezone.utc)


# --- ENUMS ---

class ReviewerRole(str, enum.Enum):
    REVIEWER = "reviewer"
    EXPERT_REVIEWER = "expert_reviewer"
    DEAF_NATIVE_SIGNER = "deaf_native_signer"
    CERTIFIED_INTERPRETER = "certified_interpreter"
    ADMIN = "admin"
    COMMUNITY_PARTICIPANT = "community_participant"


class ReviewerVerificationStatus(str, enum.Enum):
    UNVERIFIED = "unverified"
    VERIFICATION_PENDING = "verification_pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    SUSPENDED = "suspended"


class CredentialType(str, enum.Enum):
    RCI_CERTIFICATE = "rci_certificate"                     # Rehabilitation Council of India
    DEAF_ASSOCIATION_MEMBERSHIP = "deaf_association_member" # AIFD, State Deaf Association
    INTERPRETER_LICENSE = "interpreter_license"             # National/State ISL Interpreter License
    ACADEMIC_DEGREE = "academic_degree"                     # Linguistics / Deaf Studies Degree
    OTHER_CREDENTIAL = "other_credential"


class ValidationTaskStatus(str, enum.Enum):
    UNREVIEWED = "unreviewed"
    PENDING_REVIEW = "pending_review"
    UNDER_REVIEW = "under_review"
    REVIEWED = "reviewed"
    DISAGREEMENT_DETECTED = "disagreement_detected"
    ADJUDICATION_REQUIRED = "adjudication_required"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"


class RubricCriterionRating(str, enum.Enum):
    PASS = "pass"
    MINOR_ISSUE = "minor_issue"
    MAJOR_ISSUE = "major_issue"
    INCORRECT = "incorrect"
    NOT_APPLICABLE = "not_applicable"
    UNABLE_TO_ASSESS = "unable_to_assess"


class AdjudicationDecisionEnum(str, enum.Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"
    ADDITIONAL_REVIEW_REQUIRED = "additional_review_required"


# --- MODELS ---

class Reviewer(Base):
    __tablename__ = "phase5_reviewers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    
    # Qualifications & Community Identity
    is_deaf_native_signer = Column(Boolean, default=False)
    is_certified_interpreter = Column(Boolean, default=False)
    years_of_experience = Column(Integer, default=0)
    institution_affiliation = Column(String(200), nullable=True)
    role = Column(SQLEnum(ReviewerRole), default=ReviewerRole.REVIEWER, nullable=False)
    
    # Credential Verification Status (Explicit Administrative Gate)
    verification_status = Column(SQLEnum(ReviewerVerificationStatus), default=ReviewerVerificationStatus.UNVERIFIED, nullable=False)
    verification_notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)

    # Relationships
    credentials = relationship("ReviewerCredential", back_populates="reviewer", cascade="all, delete-orphan")
    verifications_received = relationship("ReviewerVerification", foreign_keys="ReviewerVerification.reviewer_id", back_populates="reviewer")
    evaluations = relationship("SignEvaluation", back_populates="reviewer", cascade="all, delete-orphan")
    annotations = relationship("ReviewerAnnotation", back_populates="reviewer", cascade="all, delete-orphan")


class ReviewerCredential(Base):
    __tablename__ = "phase5_reviewer_credentials"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=False)
    credential_type = Column(SQLEnum(CredentialType), nullable=False)
    credential_identifier = Column(String(150), nullable=False) # e.g. RCI Registration Number
    issuing_body = Column(String(200), nullable=False)          # e.g. Rehabilitation Council of India
    issue_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)
    document_url = Column(String(255), nullable=True)
    verification_status = Column(SQLEnum(ReviewerVerificationStatus), default=ReviewerVerificationStatus.VERIFICATION_PENDING, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    reviewer = relationship("Reviewer", back_populates="credentials")


class ReviewerVerification(Base):
    __tablename__ = "phase5_reviewer_verifications"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=False)
    admin_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=False)
    previous_status = Column(SQLEnum(ReviewerVerificationStatus), nullable=False)
    new_status = Column(SQLEnum(ReviewerVerificationStatus), nullable=False)
    rationale = Column(Text, nullable=False)
    evidence_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, default=get_utc_now)

    reviewer = relationship("Reviewer", foreign_keys=[reviewer_id], back_populates="verifications_received")
    admin = relationship("Reviewer", foreign_keys=[admin_id])


class ValidationProject(Base):
    __tablename__ = "phase5_validation_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_domain = Column(String(100), default="Engineering Education")
    rubric_config_json = Column(Text, nullable=True) # JSON criteria configurations
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_utc_now)

    tasks = relationship("ValidationTask", back_populates="project", cascade="all, delete-orphan")


class ValidationTask(Base):
    __tablename__ = "phase5_validation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("phase5_validation_projects.id"), nullable=True)
    sign_record_id = Column(Integer, ForeignKey("sign_records.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    status = Column(SQLEnum(ValidationTaskStatus), default=ValidationTaskStatus.UNREVIEWED, nullable=False)
    
    assigned_reviewers_count = Column(Integer, default=0)
    completed_reviews_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    project = relationship("ValidationProject", back_populates="tasks")
    sign_record = relationship("SignRecord")
    concept = relationship("Concept")
    evaluations = relationship("SignEvaluation", back_populates="task", cascade="all, delete-orphan")
    annotations = relationship("ReviewerAnnotation", back_populates="task", cascade="all, delete-orphan")
    disagreements = relationship("EvaluationDisagreement", back_populates="task", cascade="all, delete-orphan")
    decisions = relationship("ValidationDecision", back_populates="task", cascade="all, delete-orphan")


class SignEvaluation(Base):
    __tablename__ = "phase5_sign_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("phase5_validation_tasks.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=False)
    sign_record_id = Column(Integer, ForeignKey("sign_records.id"), nullable=False)
    
    is_draft = Column(Boolean, default=False)
    overall_recommendation = Column(String(50), nullable=False) # accept, reject, needs_revision, inconclusive
    general_feedback = Column(Text, nullable=True)
    suggested_dialect = Column(String(100), nullable=True)
    submitted_at = Column(DateTime, default=get_utc_now)

    task = relationship("ValidationTask", back_populates="evaluations")
    reviewer = relationship("Reviewer", back_populates="evaluations")
    sign_record = relationship("SignRecord")
    criteria_ratings = relationship("EvaluationCriterionRating", back_populates="evaluation", cascade="all, delete-orphan")


class EvaluationCriterionRating(Base):
    __tablename__ = "phase5_evaluation_criteria_ratings"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("phase5_sign_evaluations.id"), nullable=False)
    criterion_name = Column(String(100), nullable=False) # e.g. handshape, orientation, location, movement, etc.
    rating = Column(SQLEnum(RubricCriterionRating), nullable=False)
    notes = Column(Text, nullable=True)
    is_critical_error = Column(Boolean, default=False)

    evaluation = relationship("SignEvaluation", back_populates="criteria_ratings")


class ReviewerAnnotation(Base):
    __tablename__ = "phase5_reviewer_annotations"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("phase5_validation_tasks.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=False)
    timestamp_ms = Column(Integer, nullable=False)
    duration_ms = Column(Integer, default=0)
    target_type = Column(String(50), default="avatar") # "video", "avatar", "comparison"
    category = Column(String(100), nullable=False)     # "handshape_error", "movement_jerk", "orientation_flaw", "expression_missing", "general"
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=get_utc_now)

    task = relationship("ValidationTask", back_populates="annotations")
    reviewer = relationship("Reviewer", back_populates="annotations")


class EvaluationDisagreement(Base):
    __tablename__ = "phase5_evaluation_disagreements"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("phase5_validation_tasks.id"), nullable=False)
    criterion_name = Column(String(100), nullable=False)
    disagreement_type = Column(String(100), nullable=False) # "rating_conflict", "recommendation_conflict", "regional_variation"
    reviewer_ratings_json = Column(Text, nullable=False)   # {"rev_1": "pass", "rev_2": "major_issue"}
    status = Column(String(50), default="open")            # "open", "adjudicated", "dismissed"
    detected_at = Column(DateTime, default=get_utc_now)

    task = relationship("ValidationTask", back_populates="disagreements")


class ValidationDecision(Base):
    __tablename__ = "phase5_validation_decisions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("phase5_validation_tasks.id"), nullable=False)
    adjudicator_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=False)
    decision = Column(SQLEnum(AdjudicationDecisionEnum), nullable=False)
    resulting_motion_status = Column(String(50), nullable=False) # e.g. "PARTIALLY_VERIFIED_MOTION", "VERIFIED_ISL_MOTION", "REJECTED"
    rationale = Column(Text, nullable=False)
    evidence_summary = Column(Text, nullable=True)
    decided_at = Column(DateTime, default=get_utc_now)

    task = relationship("ValidationTask", back_populates="decisions")
    adjudicator = relationship("Reviewer")


class ParticipantConsent(Base):
    __tablename__ = "phase5_participant_consents"

    id = Column(Integer, primary_key=True, index=True)
    pseudonym = Column(String(100), unique=True, index=True, nullable=False) # e.g. "DEAF-PARTICIPANT-83A"
    study_name = Column(String(200), nullable=False)
    consent_version = Column(String(50), default="v1.0-2026")
    consent_given = Column(Boolean, default=True)
    can_withdraw_anytime = Column(Boolean, default=True)
    data_deletion_requested = Column(Boolean, default=False)
    
    # Granular Multi-Part Consent Flags (Phase 6 Ethics)
    consent_general_research = Column(Boolean, default=True)
    consent_video_recording = Column(Boolean, default=False)
    consent_data_sharing = Column(Boolean, default=True)
    consent_academic_publication = Column(Boolean, default=True)
    
    is_anonymized = Column(Boolean, default=False)
    original_pseudonym_hash = Column(String(64), nullable=True)
    consent_date = Column(DateTime, default=get_utc_now)
    withdrawal_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)

    sessions = relationship("ResearchSession", back_populates="consent")


class ResearchSession(Base):
    __tablename__ = "phase5_research_sessions"

    id = Column(Integer, primary_key=True, index=True)
    consent_id = Column(Integer, ForeignKey("phase5_participant_consents.id"), nullable=False)
    session_code = Column(String(100), unique=True, index=True, nullable=False)
    session_type = Column(String(100), default="comprehension_survey") # "comprehension_survey", "naturalness_rating", "dialect_feedback"
    concepts_tested_json = Column(Text, nullable=True)
    comprehension_score = Column(Float, nullable=True) # 0.0 to 1.0 or percentage
    naturalness_rating = Column(Float, nullable=True)  # 1.0 to 5.0
    feedback_notes = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=get_utc_now)

    consent = relationship("ParticipantConsent", back_populates="sessions")


class ValidationAuditLog(Base):
    __tablename__ = "phase5_validation_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, nullable=True)
    actor_username = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False) # e.g. "REVIEWER_REGISTERED", "CREDENTIAL_SUBMITTED", "DECISION_ADJUDICATED"
    target_type = Column(String(100), nullable=False) # "reviewer", "task", "evaluation", "consent"
    target_id = Column(String(100), nullable=False)
    details_json = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=get_utc_now)


class RevokedToken(Base):
    __tablename__ = "phase6_revoked_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_signature = Column(String(100), unique=True, index=True, nullable=False)
    revoked_at = Column(DateTime, default=get_utc_now)
    expires_at = Column(DateTime, nullable=False)
    revoked_by_user_id = Column(Integer, nullable=True)


