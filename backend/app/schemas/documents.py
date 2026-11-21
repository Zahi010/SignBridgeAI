"""
SignBridge AI - Document Processing Schemas
Defines request/response schemas for document ingestion, section-by-section analysis,
and engineering concept coverage summaries.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from backend.app.schemas.translation import TranslationResponse

class DocumentSectionTranslation(BaseModel):
    section_index: int = Field(..., description="Section position in document (1-indexed)")
    heading: str = Field(..., description="Inferred section title or slide label")
    text_preview: str = Field(..., description="Preview of section text")
    sentence_count: int = Field(default=1)
    detected_concepts: List[str] = Field(default_factory=list)
    supported_count: int = Field(default=0)
    explanation_count: int = Field(default=0)
    unsupported_count: int = Field(default=0)
    status: str = Field(default="supported", description="supported, explanation_required, unsupported, neutral")
    isl_gloss_summary: str = Field(default="")

class DocumentAnalysisSummary(BaseModel):
    total_sections: int = Field(default=1)
    total_concepts_found: int = Field(default=0)
    supported_concepts_count: int = Field(default=0)
    explanation_required_count: int = Field(default=0)
    unsupported_concepts_count: int = Field(default=0)
    overall_status: str = Field(default="partial")
    coverage_percentage: float = Field(default=100.0, ge=0.0, le=100.0)

class DocumentUploadResponse(BaseModel):
    filename: str
    file_type: str
    file_size_bytes: int
    page_or_slide_count: int
    extracted_text_preview: str
    total_words: int
    total_sentences: int
    detected_concepts_count: int
    translation_summary: TranslationResponse
    sections: List[DocumentSectionTranslation] = Field(default_factory=list)
    document_analysis: Optional[DocumentAnalysisSummary] = None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
