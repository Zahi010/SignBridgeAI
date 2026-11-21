import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, Float
)
from sqlalchemy.orm import relationship
from backend.app.database.database import Base

def get_utc_now():
    return datetime.now(timezone.utc)

class ValidationStatus(str, enum.Enum):
    VERIFIED = "verified"
    PARTIAL = "partial"
    EXPLANATION_NEEDED = "explanation_needed"
    EXPLANATION_REQUIRED = "explanation_required"
    NEEDS_REVIEW = "needs_review"
    UNSUPPORTED = "unsupported"
    DEMO_ONLY = "demo_only"
    BLOCKED = "blocked"
    NOT_IMPLEMENTED = "not_implemented"

class ConsentStatus(str, enum.Enum):
    VERIFIED_CONSENT = "verified_consent"
    PENDING_CONSENT = "pending_consent"
    RESTRICTED_EDUCATIONAL = "restricted_educational"
    EXEMPT_OPEN_GOVERNMENT = "exempt_open_government"

class ValidationDecision(str, enum.Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_CORRECTION = "requires_correction"
    STATUS_MODIFIED = "status_modified"

class RecordingSession(Base):
    __tablename__ = "recording_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_uid = Column(String(100), unique=True, index=True, nullable=False) # e.g. "REC-20261120-CS-01"
    signer_id = Column(String(100), nullable=False) # e.g. "DEAF-SIGNER-01"
    signer_name = Column(String(150), nullable=True)
    is_native_signer = Column(Boolean, default=True)
    camera_setup = Column(String(150), default="Frontal 1080p60 Studio Setup")
    lighting_environment = Column(String(150), default="Three-point softbox, zero harsh shadows")
    background = Column(String(150), default="Neutral 18% Gray / Chroma Green")
    consent_status = Column(Enum(ConsentStatus), default=ConsentStatus.PENDING_CONSENT, nullable=False)
    consent_document_ref = Column(String(200), nullable=True) # e.g. "CONSENT-ISLRTC-2026-004"
    consent_date = Column(DateTime, nullable=True)
    recording_date = Column(DateTime, default=get_utc_now)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    signs = relationship("SignRecord", back_populates="recording_session")
    videos = relationship("SignVideo", back_populates="recording_session")

class ReviewerProfile(Base):
    __tablename__ = "reviewer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "REV-AUTH-01"
    full_name = Column(String(150), nullable=False)
    is_certified_interpreter = Column(Boolean, default=False)
    is_deaf_native_signer = Column(Boolean, default=False)
    accreditation_body = Column(String(150), nullable=True) # e.g. "Rehabilitation Council of India (RCI)"
    accreditation_number = Column(String(100), nullable=True) # e.g. "RCI-CRR-A12345"
    institution_affiliation = Column(String(150), nullable=True) # e.g. "ISLRTC Technical Working Group"
    qualifications = Column(Text, nullable=True)
    is_authorized_expert = Column(Boolean, default=False) # Only authorized experts can certify VERIFIED
    created_at = Column(DateTime, default=get_utc_now)

    validations = relationship("ReviewerValidation", back_populates="reviewer_profile")

class EngineeringBranch(Base):
    __tablename__ = "engineering_branches"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "cs", "ece", "mech", "civil", "eee"
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    subjects = relationship("Subject", back_populates="branch", cascade="all, delete-orphan")
    concepts = relationship("Concept", back_populates="branch")

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("engineering_branches.id"), nullable=False)
    code = Column(String(50), index=True, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    branch = relationship("EngineeringBranch", back_populates="subjects")
    concepts = relationship("Concept", back_populates="subject")

class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("engineering_branches.id"), nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    
    term = Column(String(150), index=True, nullable=False) # e.g. "Operating System", "Deadlock"
    slug = Column(String(150), unique=True, index=True, nullable=False)
    aliases = Column(Text, nullable=True) # comma or json separated synonyms/aliases
    category = Column(String(100), nullable=True)
    domain = Column(String(100), nullable=True) # sub-domain context e.g. "Electrical Circuits", "Data Structures"
    definition = Column(Text, nullable=False)
    technical_context = Column(Text, nullable=True)
    example_usage = Column(Text, nullable=True)
    difficulty_level = Column(String(50), default="intermediate")
    created_at = Column(DateTime, default=get_utc_now)

    branch = relationship("EngineeringBranch", back_populates="concepts")
    subject = relationship("Subject", back_populates="concepts")
    signs = relationship("SignRecord", back_populates="concept", cascade="all, delete-orphan")
    grammar_annotations = relationship("GrammarAnnotation", back_populates="concept")

class DatasetProvenance(Base):
    __tablename__ = "dataset_provenances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False) # e.g. "ISLRTC Technical Terminology Benchmark"
    organization = Column(String(150), nullable=False)
    license = Column(String(100), nullable=False) # e.g. "CC-BY-4.0", "Educational Research"
    source_url = Column(String(255), nullable=True)
    methodology = Column(Text, nullable=True)
    peer_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=get_utc_now)

    signs = relationship("SignRecord", back_populates="provenance")

class ExpertReview(Base):
    __tablename__ = "expert_reviews"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_name = Column(String(120), nullable=False)
    reviewer_role = Column(String(120), nullable=False) # "Certified ISL Interpreter", "Deaf Engineering Scholar"
    affiliation = Column(String(150), nullable=True)
    status = Column(Enum(ValidationStatus), default=ValidationStatus.NEEDS_REVIEW)
    review_notes = Column(Text, nullable=True)
    sign_accuracy_rating = Column(Float, nullable=True) # 1-5 scale
    reviewed_at = Column(DateTime, default=get_utc_now)

    signs = relationship("SignRecord", back_populates="expert_review")

class SignRecord(Base):
    __tablename__ = "sign_records"

    id = Column(Integer, primary_key=True, index=True)
    sign_id = Column(String(50), unique=True, index=True, nullable=True) # e.g. "ISL-CS-001"
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    provenance_id = Column(Integer, ForeignKey("dataset_provenances.id"), nullable=True)
    expert_review_id = Column(Integer, ForeignKey("expert_reviews.id"), nullable=True)
    
    sign_gloss = Column(String(100), nullable=False) # e.g. "OPERATING-SYSTEM" or "DEADLOCK"
    validation_status = Column(Enum(ValidationStatus), default=ValidationStatus.UNSUPPORTED, nullable=False)
    is_authentic = Column(Boolean, default=False)
    linguistic_notes = Column(Text, nullable=True)
    regional_dialect = Column(String(100), default="Standard ISL (Pan-India)")
    
    # Authenticated Phonological Parameters
    dominant_hand = Column(String(50), nullable=True) # "Right", "Two-Handed", "Symmetric", "Left"
    handshape = Column(String(100), nullable=True) # e.g. "Flat Open-B", "Index Finger Extended"
    movement = Column(String(150), nullable=True) # e.g. "Linear outward thrust", "Circular horizontal oscillation"
    location = Column(String(150), nullable=True) # e.g. "Neutral signing space in front of chest"
    orientation = Column(String(150), nullable=True) # e.g. "Palm facing inwards toward torso"
    non_manual_markers = Column(String(150), nullable=True) # e.g. "Furrowed Brow", "Raised Brow", "Mouth Morpheme"
    
    # Source, License and Consent Metadata
    source_institution = Column(String(150), nullable=True) # e.g. "ISLRTC Reference Standard", "SignBridge Candidate Archive"
    source_url_or_dataset_id = Column(String(255), nullable=True)
    license = Column(String(100), nullable=True) # e.g. "Government Educational Reference / Fair Dealing"
    consent_info = Column(String(255), nullable=True) # e.g. "Deaf Signer Institutional Consent Protocol #ISL-2026"
    validation_date = Column(DateTime, nullable=True)
    confidence_score = Column(Float, nullable=True) # Only where measured meaningfully
    
    # Phase 2 Recording Session & Ingestion Link
    recording_session_id = Column(Integer, ForeignKey("recording_sessions.id"), nullable=True)
    recording_filename = Column(String(255), nullable=True)
    recording_metadata_json = Column(Text, nullable=True) # duration, resolution, fps, codec
    regional_variation_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=get_utc_now)

    concept = relationship("Concept", back_populates="signs")
    provenance = relationship("DatasetProvenance", back_populates="signs")
    expert_review = relationship("ExpertReview", back_populates="signs")
    recording_session = relationship("RecordingSession", back_populates="signs")
    variants = relationship("SignVariant", back_populates="sign_record", cascade="all, delete-orphan")
    videos = relationship("SignVideo", back_populates="sign_record", cascade="all, delete-orphan")
    avatar_animations = relationship("AvatarAnimation", back_populates="sign_record", cascade="all, delete-orphan")
    validation_reviews = relationship("ReviewerValidation", back_populates="sign_record", cascade="all, delete-orphan")

class ReviewerValidation(Base):
    __tablename__ = "reviewer_validations"

    id = Column(Integer, primary_key=True, index=True)
    sign_record_id = Column(Integer, ForeignKey("sign_records.id"), nullable=False)
    reviewer_profile_id = Column(Integer, ForeignKey("reviewer_profiles.id"), nullable=True)
    
    reviewer_name = Column(String(120), nullable=False)
    reviewer_role = Column(String(120), nullable=False) # "certified_interpreter", "deaf_educator", "linguist_researcher", "test_reviewer_local"
    affiliation = Column(String(150), nullable=True)
    accreditation_evidence = Column(Text, nullable=True) # RCI number, AIFD registration, or test account flag
    
    decision = Column(String(50), default="requires_correction") # approved, rejected, requires_correction, status_modified
    assigned_status = Column(Enum(ValidationStatus), default=ValidationStatus.NEEDS_REVIEW, nullable=False)
    
    corrections = Column(Text, nullable=True)
    suggested_regional_variation = Column(String(100), nullable=True)
    comments = Column(Text, nullable=True)
    accuracy_rating = Column(Float, nullable=True) # 1-5 scale
    reviewed_at = Column(DateTime, default=get_utc_now)

    sign_record = relationship("SignRecord", back_populates="validation_reviews")
    reviewer_profile = relationship("ReviewerProfile", back_populates="validations")

class SignVariant(Base):
    __tablename__ = "sign_variants"

    id = Column(Integer, primary_key=True, index=True)
    sign_record_id = Column(Integer, ForeignKey("sign_records.id"), nullable=False)
    variant_name = Column(String(100), nullable=False) # e.g. "Compound Two-Handed", "Initialized Sign"
    handshape = Column(String(100), nullable=True)
    movement = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    non_manual_features = Column(Text, nullable=True)

    sign_record = relationship("SignRecord", back_populates="variants")

class SignVideo(Base):
    __tablename__ = "sign_videos"

    id = Column(Integer, primary_key=True, index=True)
    sign_record_id = Column(Integer, ForeignKey("sign_records.id"), nullable=False)
    recording_session_id = Column(Integer, ForeignKey("recording_sessions.id"), nullable=True)
    title = Column(String(150), nullable=False)
    video_path = Column(String(255), nullable=False)
    thumbnail_path = Column(String(255), nullable=True)
    signer_name = Column(String(100), nullable=True)
    is_native_signer = Column(Boolean, default=True)
    duration_seconds = Column(Float, default=0.0)
    resolution = Column(String(50), default="1080p")
    source_attribution = Column(String(255), nullable=False)
    license = Column(String(100), nullable=False)
    validation_status = Column(Enum(ValidationStatus), default=ValidationStatus.VERIFIED)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    sign_record = relationship("SignRecord", back_populates="videos")
    recording_session = relationship("RecordingSession", back_populates="videos")

class AvatarAnimation(Base):
    __tablename__ = "avatar_animations"

    id = Column(Integer, primary_key=True, index=True)
    sign_record_id = Column(Integer, ForeignKey("sign_records.id"), nullable=False)
    animation_name = Column(String(150), nullable=False)
    asset_path = Column(String(255), nullable=False) # glb or json keyframe path
    is_mocap = Column(Boolean, default=False)
    is_procedural = Column(Boolean, default=False)
    is_neutral_preview = Column(Boolean, default=True) # honest indicator if it is neutral preview
    validation_status = Column(Enum(ValidationStatus), default=ValidationStatus.NEEDS_REVIEW)
    rig_standard = Column(String(50), default="MediaPipe-Holistic / ReadyPlayerMe")
    created_at = Column(DateTime, default=get_utc_now)

    sign_record = relationship("SignRecord", back_populates="avatar_animations")

class SignSequence(Base):
    __tablename__ = "sign_sequences"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    gloss_sequence = Column(Text, nullable=False) # e.g. "COMPUTER OPERATING SYSTEM WHAT EXPLAIN"
    created_at = Column(DateTime, default=get_utc_now)

class GrammarAnnotation(Base):
    __tablename__ = "grammar_annotations"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)
    rule_type = Column(String(100), nullable=False) # e.g. "Topic-Comment", "Time-First", "Non-Manual Marker"
    english_pattern = Column(String(200), nullable=True)
    isl_structure = Column(String(200), nullable=False)
    explanation = Column(Text, nullable=False)

    concept = relationship("Concept", back_populates="grammar_annotations")

class TranslationSession(Base):
    __tablename__ = "translation_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_uid = Column(String(100), unique=True, index=True, nullable=False)
    source_type = Column(String(50), default="text") # "text", "document", "live_lecture"
    branch_code = Column(String(50), nullable=True)
    subject_code = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=get_utc_now)

    translations = relationship("TranslationHistory", back_populates="session", cascade="all, delete-orphan")

class TranslationHistory(Base):
    __tablename__ = "translation_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("translation_sessions.id"), nullable=True)
    source_text = Column(Text, nullable=False)
    branch_name = Column(String(100), nullable=True)
    subject_name = Column(String(100), nullable=True)
    
    extracted_concepts_json = Column(Text, nullable=True) # JSON list of concepts
    isl_gloss_output = Column(Text, nullable=True)
    status = Column(Enum(ValidationStatus), default=ValidationStatus.PARTIAL, nullable=False)
    status_reason = Column(Text, nullable=True)
    
    verified_signs_count = Column(Integer, default=0)
    unsupported_signs_count = Column(Integer, default=0)
    has_video = Column(Boolean, default=False)
    has_avatar = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=get_utc_now)

    session = relationship("TranslationSession", back_populates="translations")
