"""
SignBridge AI - Translation Intermediate Representation (IR) Schema
Pydantic v2 schemas defining the structured linguistic, conceptual, and multimodal
translation intermediate representation shared across the NLP pipeline, translation planner,
video retriever, 3D avatar sequencer, and frontend UI.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from backend.app.models.entities import ValidationStatus

class PhonologyIR(BaseModel):
    dominant_hand: Optional[str] = Field(None, description="Active signing hand: Right, Two-Handed, Symmetric, Left")
    handshape: Optional[str] = Field(None, description="ISL handshape: Open-B, Index, C-handshape, Fist, etc.")
    movement: Optional[str] = Field(None, description="Direction and dynamics of movement")
    location: Optional[str] = Field(None, description="Signing space location relative to body")
    orientation: Optional[str] = Field(None, description="Palm and finger orientation")
    non_manual_markers: Optional[str] = Field(None, description="Facial expressions, mouthing, head tilt")

class SemanticConceptIR(BaseModel):
    id: Optional[int] = Field(None, description="Concept database ID")
    term: str = Field(..., description="Canonical English engineering term")
    category: Optional[str] = Field(None, description="Engineering subcategory")
    domain: Optional[str] = Field(None, description="Engineering branch or domain context")
    definition: Optional[str] = Field(None, description="Pedagogical definition")
    canonical_gloss: str = Field(..., description="Standardized ISL gloss string")
    validation_status: ValidationStatus = Field(..., description="Validation and accreditation status")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Extraction confidence score")
    disambiguation_rationale: Optional[str] = Field(None, description="Contextual disambiguation rationale")
    phonology: Optional[PhonologyIR] = Field(None, description="Phonological sign parameters if known")
    has_video: bool = Field(default=False, description="Whether authentic human signing video is available")
    video_url: Optional[str] = Field(None, description="Path to video asset if available")
    source_attribution: Optional[str] = Field(None, description="Source dataset or institution attribution")

class ConceptRelationshipIR(BaseModel):
    source_concept: str = Field(..., description="Subject engineering concept")
    target_concept: str = Field(..., description="Object engineering concept")
    relation_type: str = Field(..., description="Semantic relation predicate, e.g. executes, drives_flow_of")
    description: str = Field(..., description="Human-readable explanation of relationship")
    triple_string: str = Field(..., description="Visual triple representation: [Source] -> [Relation] -> [Target]")
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)

class DiscourseContextIR(BaseModel):
    sentence_type: str = Field(..., description="DECLARATIVE, WH_QUESTION, POLAR_QUESTION, CONDITIONAL, COMPARATIVE")
    modality: str = Field(default="neutral", description="neutral, obligation, possibility, capability")
    temporal_frame: str = Field(default="present", description="present, past, future, general_principle")
    polarity: str = Field(default="positive", description="positive or negative")

class NegationMarkerIR(BaseModel):
    is_negated: bool = Field(default=False)
    marker_token: Optional[str] = Field(None, description="English negative token, e.g. not, never, cannot")
    isl_position: str = Field(default="sentence_final", description="ISL puts negation sentence-final")
    non_manual_marker: str = Field(default="Headshake", description="Co-occurring facial non-manual marker")

class InterrogativeIR(BaseModel):
    is_interrogative: bool = Field(default=False)
    question_type: Optional[str] = Field(None, description="WH_QUESTION or POLAR_QUESTION")
    wh_word: Optional[str] = Field(None, description="what, how, why, when, where, which, who")
    isl_position: str = Field(default="sentence_final", description="ISL places WH-words sentence-final")
    non_manual_marker: str = Field(default="Furrowed Brow", description="Facial NMM for WH-questions")

class TemporalMarkerIR(BaseModel):
    has_temporal: bool = Field(default=False)
    marker_token: Optional[str] = Field(None, description="Temporal word: today, now, yesterday, initially")
    isl_position: str = Field(default="sentence_initial", description="ISL puts time markers sentence-initial")

class SpatialAnchorIR(BaseModel):
    concept_term: str = Field(..., description="Concept assigned to spatial locus")
    locus_id: str = Field(..., description="LOCUS_A, LOCUS_B, NEUTRAL_CENTER")
    spatial_coordinate: str = Field(..., description="left, right, center, upper_left, upper_right")
    contrastive_role: Optional[str] = Field(None, description="source, target, comparator, agent")

class TranslationUnitIR(BaseModel):
    unit_id: int = Field(..., description="Sequence ordering index")
    source_segment: str = Field(..., description="English source word or phrase")
    strategy: str = Field(..., description="LEXICAL_SIGN_DIRECT, PEDAGOGICAL_EXPLANATION, UNSUPPORTED_FINGERSPELLING")
    assigned_gloss: str = Field(..., description="Planned ISL gloss for this unit")
    video_resource_ref: Optional[str] = Field(None, description="URL or filename of video asset")
    pedagogical_ref: Optional[Dict[str, Any]] = Field(None, description="Structured explanation payload")
    fingerspelling_sequence: Optional[List[str]] = Field(None, description="Two-handed ISL fingerspelling sequence")
    rationale: str = Field(..., description="Reasoning for chosen translation strategy")

class TranslationPlanIR(BaseModel):
    translation_units: List[TranslationUnitIR] = Field(default_factory=list)
    total_units: int = Field(default=0)
    lexical_count: int = Field(default=0)
    explanation_count: int = Field(default=0)
    unsupported_count: int = Field(default=0)
    overall_strategy_summary: str = Field(default="")

class IntermediateRepresentation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_text: str = Field(..., description="Original raw English technical input")
    engineering_branch: Dict[str, Any] = Field(default_factory=dict, description="Branch metadata: code, name")
    subject: Optional[Dict[str, Any]] = Field(None, description="Subject metadata: code, name")
    context_domain: str = Field(default="General Engineering", description="Primary engineering domain")
    
    tokens: List[Dict[str, Any]] = Field(default_factory=list, description="NLP tokens with POS and lemmas")
    detected_concepts: List[SemanticConceptIR] = Field(default_factory=list, description="Extracted engineering concepts")
    concept_relationships: List[ConceptRelationshipIR] = Field(default_factory=list, description="Extracted concept triples")
    
    discourse_context: DiscourseContextIR = Field(default_factory=lambda: DiscourseContextIR(sentence_type="DECLARATIVE"))
    negation: NegationMarkerIR = Field(default_factory=NegationMarkerIR)
    interrogative: InterrogativeIR = Field(default_factory=InterrogativeIR)
    temporal: TemporalMarkerIR = Field(default_factory=TemporalMarkerIR)
    spatial_anchors: List[SpatialAnchorIR] = Field(default_factory=list)
    
    isl_grammar_plan: Dict[str, Any] = Field(default_factory=dict, description="ISL grammar plan for backward compatibility")
    translation_plan: TranslationPlanIR = Field(default_factory=TranslationPlanIR)
    
    policy_verdict: Dict[str, Any] = Field(default_factory=dict, description="Zero-fabrication audit summary")
    asset_resolution: Dict[str, Any] = Field(default_factory=dict, description="Resolved video and 3D avatar assets")
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
