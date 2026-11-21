from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from backend.app.models.entities import ValidationStatus

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="English technical input text")
    branch_id: Optional[int] = Field(None, description="Selected engineering branch ID")
    subject_id: Optional[int] = Field(None, description="Selected subject ID")
    session_id: Optional[str] = Field(None, description="Session tracking ID")

class ExtractedConceptSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    term: str
    category: Optional[str] = None
    domain: Optional[str] = None
    definition: str
    difficulty_level: Optional[str] = "intermediate"
    validation_status: ValidationStatus
    disambiguation_rationale: Optional[str] = None
    dominant_hand: Optional[str] = None
    handshape: Optional[str] = None
    movement: Optional[str] = None
    location: Optional[str] = None
    orientation: Optional[str] = None
    non_manual_markers: Optional[str] = None
    has_video: bool = False
    has_avatar: bool = False
    video_url: Optional[str] = None
    source_attribution: Optional[str] = None
    sign_gloss: Optional[str] = None
    linguistic_notes: Optional[str] = None
    reviewer_info: Optional[str] = None

class GrammarNoteSchema(BaseModel):
    rule_type: str
    english_pattern: Optional[str] = None
    isl_structure: str
    explanation: str
    is_experimental_hypothesis: bool = True
    validation_status: str = "UNVALIDATED_HYPOTHESIS"
    disclaimer: str = "Experimental rule-based transformation heuristic awaiting Deaf linguistic validation. Not a certified ISL grammar standard."

class VideoOutputSchema(BaseModel):
    available: bool
    title: Optional[str] = None
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    signer_name: Optional[str] = None
    duration_seconds: float = 0.0
    resolution: Optional[str] = None
    source_attribution: Optional[str] = None
    license: Optional[str] = None
    validation_status: ValidationStatus = ValidationStatus.UNSUPPORTED
    notes: Optional[str] = None

class AvatarOutputSchema(BaseModel):
    available: bool
    model_type: str = "neutral_preview" # "authentic_mocap" or "neutral_preview"
    animation_name: Optional[str] = None
    rig_standard: str = "MediaPipe-Holistic / ReadyPlayerMe"
    validation_status: ValidationStatus = ValidationStatus.NEEDS_REVIEW
    notice: str = "3D Signing Avatar Preview — Zero Fabrication Policy active"

class PipelineStageSchema(BaseModel):
    stage_id: str
    stage_number: int
    name: str
    description: str
    status: str # "completed", "warning", "info"
    duration_ms: float
    summary: str
    details: Dict[str, Any] = {}

class TranslationResponse(BaseModel):
    id: Optional[int] = None
    source_text: str
    branch_name: Optional[str] = None
    subject_name: Optional[str] = None
    status: ValidationStatus
    status_reason: str
    
    extracted_concepts: List[ExtractedConceptSchema] = []
    semantic_relations: List[Dict[str, Any]] = []
    pedagogical_explanations: List[Dict[str, Any]] = []
    isl_gloss_sequence: List[str] = []
    grammar_notes: List[GrammarNoteSchema] = []
    
    intermediate_representation: Optional[Dict[str, Any]] = None
    translation_plan: Optional[Dict[str, Any]] = None
    
    video_output: VideoOutputSchema
    avatar_output: AvatarOutputSchema
    
    verified_signs_count: int = 0
    unsupported_signs_count: int = 0
    
    pipeline_stages: List[PipelineStageSchema] = []
    total_pipeline_duration_ms: float = 0.0
    unmatched_tokens: List[str] = []
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TranslationHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_text: str
    branch_name: Optional[str] = None
    subject_name: Optional[str] = None
    status: ValidationStatus
    status_reason: Optional[str] = None
    verified_signs_count: int
    unsupported_signs_count: int
    has_video: bool
    has_avatar: bool
    created_at: datetime
