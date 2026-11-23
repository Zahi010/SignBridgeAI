"""
SignBridge AI - Phase 8 Pydantic Schemas for Institutional Outreach & Collaboration Readiness.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from backend.app.models.outreach_models import (
    OutreachCategory,
    OutreachStatus,
    InteractionType
)


class InteractionCreateRequest(BaseModel):
    interaction_type: InteractionType
    summary: str = Field(..., min_length=3, max_length=255)
    details: Optional[str] = None
    outcome: Optional[str] = None
    next_steps: Optional[str] = None


class InteractionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    outreach_id: int
    interaction_type: InteractionType
    summary: str
    details: Optional[str] = None
    outcome: Optional[str] = None
    next_steps: Optional[str] = None
    logged_by_id: Optional[int] = None
    logged_by_name: Optional[str] = None
    timestamp: datetime


class OutreachCreateRequest(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=200)
    acronym: Optional[str] = None
    category: OutreachCategory
    website: str = Field(..., min_length=5, max_length=255)
    public_contact: str = Field(..., min_length=3, max_length=255)
    telephone: Optional[str] = None
    department: Optional[str] = None
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    verification_source: str = Field(..., min_length=5, max_length=255)
    verification_date: str = Field(..., min_length=5, max_length=50)
    collaboration_role: str = Field(..., min_length=3, max_length=200)
    outreach_status: OutreachStatus = OutreachStatus.VERIFIED
    proposed_collaboration_tier: str = Field(default="Tier 1: Expert Linguistic Validation")
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class OutreachUpdateRequest(BaseModel):
    organization_name: Optional[str] = None
    acronym: Optional[str] = None
    category: Optional[OutreachCategory] = None
    website: Optional[str] = None
    public_contact: Optional[str] = None
    telephone: Optional[str] = None
    department: Optional[str] = None
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    collaboration_role: Optional[str] = None
    outreach_status: Optional[OutreachStatus] = None
    proposed_collaboration_tier: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class InstitutionalOutreachResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_name: str
    acronym: Optional[str] = None
    category: OutreachCategory
    website: str
    public_contact: str
    telephone: Optional[str] = None
    department: Optional[str] = None
    contact_person: Optional[str] = None
    designation: Optional[str] = None
    verification_source: str
    verification_date: str
    collaboration_role: str
    outreach_status: OutreachStatus
    proposed_collaboration_tier: str
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None
    interaction_count: int = 0
    created_at: datetime
    updated_at: datetime


class InstitutionalOutreachDetailResponse(InstitutionalOutreachResponse):
    interactions: List[InteractionResponse] = []


class OutreachSummaryStatsResponse(BaseModel):
    total_organizations: int
    by_category: Dict[str, int]
    by_status: Dict[str, int]
    pending_follow_ups: int
    total_interactions: int
