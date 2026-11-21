from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from backend.app.models.entities import ValidationStatus

class ReviewerProfileSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reviewer_code: str
    full_name: str
    is_certified_interpreter: bool
    is_deaf_native_signer: bool
    accreditation_body: Optional[str] = None
    accreditation_number: Optional[str] = None
    institution_affiliation: Optional[str] = None
    qualifications: Optional[str] = None
    is_authorized_expert: bool
    created_at: datetime

class ValidationSubmitRequest(BaseModel):
    sign_record_id: int
    reviewer_profile_id: Optional[int] = None
    reviewer_code: Optional[str] = None
    reviewer_name: str = Field(..., min_length=2, max_length=120)
    reviewer_role: str = Field(default="test_reviewer_local", max_length=120)
    affiliation: Optional[str] = Field(default="SignBridge Community Reviewer", max_length=150)
    decision: str = Field(default="requires_correction") # approved, rejected, requires_correction, status_modified
    assigned_status: ValidationStatus = Field(default=ValidationStatus.NEEDS_REVIEW)
    corrections: Optional[str] = None
    suggested_regional_variation: Optional[str] = None
    comments: Optional[str] = None
    accuracy_rating: Optional[float] = Field(default=None, ge=1.0, le=5.0)

class ValidationDecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sign_record_id: int
    reviewer_name: str
    reviewer_role: str
    decision: str
    assigned_status: ValidationStatus
    comments: Optional[str] = None
    reviewed_at: datetime
    message: str

class PendingValidationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sign_record_id: int
    sign_id: Optional[str] = None
    concept_term: str
    branch_name: Optional[str] = None
    subject_name: Optional[str] = None
    current_status: ValidationStatus
    sign_gloss: str
    regional_dialect: Optional[str] = None
    has_video: bool = False
    has_animation: bool = False
    source_institution: Optional[str] = None
    license: Optional[str] = None
    review_count: int = 0
