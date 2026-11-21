from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from backend.app.models.entities import ValidationStatus

class BranchSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    description: Optional[str] = None
    subject_count: int = 0
    concept_count: int = 0

class SubjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    branch_id: int
    code: str
    name: str
    description: Optional[str] = None
    concept_count: int = 0

class ProvenanceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    organization: str
    license: str
    source_url: Optional[str] = None
    methodology: Optional[str] = None
    peer_reviewed: bool = False

class ExpertReviewSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reviewer_name: str
    reviewer_role: str
    affiliation: Optional[str] = None
    status: ValidationStatus
    review_notes: Optional[str] = None
    sign_accuracy_rating: Optional[float] = None

class ReviewerValidationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sign_record_id: int
    reviewer_name: str
    reviewer_role: str
    affiliation: Optional[str] = None
    decision: str
    assigned_status: ValidationStatus
    corrections: Optional[str] = None
    suggested_regional_variation: Optional[str] = None
    comments: Optional[str] = None
    accuracy_rating: Optional[float] = None
    reviewed_at: datetime

class SignVariantSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    variant_name: str
    handshape: Optional[str] = None
    movement: Optional[str] = None
    location: Optional[str] = None
    non_manual_features: Optional[str] = None

class SignRecordDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sign_id: Optional[str] = None
    sign_gloss: str
    validation_status: ValidationStatus
    is_authentic: bool
    linguistic_notes: Optional[str] = None
    regional_dialect: Optional[str] = "Standard ISL"
    
    dominant_hand: Optional[str] = None
    handshape: Optional[str] = None
    movement: Optional[str] = None
    location: Optional[str] = None
    orientation: Optional[str] = None
    non_manual_markers: Optional[str] = None
    
    source_institution: Optional[str] = None
    source_url_or_dataset_id: Optional[str] = None
    license: Optional[str] = None
    consent_info: Optional[str] = None
    validation_date: Optional[datetime] = None
    confidence_score: Optional[float] = None

    provenance: Optional[ProvenanceSchema] = None
    expert_review: Optional[ExpertReviewSchema] = None
    validation_reviews: List[ReviewerValidationSchema] = []
    variants: List[SignVariantSchema] = []
    has_video: bool = False
    video_url: Optional[str] = None

class ConceptDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    branch_id: Optional[int] = None
    branch_name: Optional[str] = None
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    term: str
    slug: str
    aliases: Optional[str] = None
    category: Optional[str] = None
    domain: Optional[str] = None
    definition: str
    technical_context: Optional[str] = None
    example_usage: Optional[str] = None
    difficulty_level: str
    validation_status: ValidationStatus
    signs: List[SignRecordDetailSchema] = []
    created_at: datetime

class VocabularyListResponse(BaseModel):
    total: int
    verified_count: int
    partial_count: int
    unsupported_count: int
    needs_review_count: int = 0
    items: List[ConceptDetailSchema]
