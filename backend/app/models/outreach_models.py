"""
SignBridge AI - Phase 8 Institutional Outreach & Collaboration Readiness Models.
Strict adherence to Zero-Fabrication Policy:
- Records institutional profiles, verification provenance, and contact channels.
- Tracks outreach workflow stages without autonomous messaging.
- Logs human-administered interactions, meetings, and collaboration notes.
"""

import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from backend.app.database.database import Base


def get_utc_now():
    return datetime.now(timezone.utc)


class OutreachCategory(str, enum.Enum):
    GOVERNMENT_NATIONAL = "GOVERNMENT_NATIONAL"
    DEAF_ORGANIZATION = "DEAF_ORGANIZATION"
    ACADEMIC_RESEARCH = "ACADEMIC_RESEARCH"
    SPECIAL_EDUCATION = "SPECIAL_EDUCATION"
    DISABILITY_CENTER = "DISABILITY_CENTER"
    OTHER = "OTHER"


class OutreachStatus(str, enum.Enum):
    IDENTIFIED = "IDENTIFIED"
    RESEARCHED = "RESEARCHED"
    VERIFIED = "VERIFIED"
    READY_FOR_OUTREACH = "READY_FOR_OUTREACH"
    CONTACTED = "CONTACTED"
    RESPONSE_RECEIVED = "RESPONSE_RECEIVED"
    MEETING_REQUESTED = "MEETING_REQUESTED"
    MEETING_COMPLETED = "MEETING_COMPLETED"
    COLLABORATION_DISCUSSION = "COLLABORATION_DISCUSSION"
    AGREEMENT_PENDING = "AGREEMENT_PENDING"
    COLLABORATION_CONFIRMED = "COLLABORATION_CONFIRMED"
    NO_RESPONSE = "NO_RESPONSE"
    DECLINED = "DECLINED"
    ON_HOLD = "ON_HOLD"
    INVALID_CONTACT = "INVALID_CONTACT"


class InteractionType(str, enum.Enum):
    EMAIL_SENT = "EMAIL_SENT"
    EMAIL_RECEIVED = "EMAIL_RECEIVED"
    PHONE_CALL = "PHONE_CALL"
    VIRTUAL_MEETING = "VIRTUAL_MEETING"
    IN_PERSON_MEETING = "IN_PERSON_MEETING"
    PRESENTATION = "PRESENTATION"
    MOU_DRAFT = "MOU_DRAFT"
    NOTE = "NOTE"


class InstitutionalOutreach(Base):
    __tablename__ = "phase8_institutional_outreach"

    id = Column(Integer, primary_key=True, index=True)
    organization_name = Column(String(200), unique=True, index=True, nullable=False)
    acronym = Column(String(50), nullable=True)
    category = Column(SQLEnum(OutreachCategory), nullable=False)
    website = Column(String(255), nullable=False)
    public_contact = Column(String(255), nullable=False)
    telephone = Column(String(100), nullable=True)
    department = Column(String(200), nullable=True)
    contact_person = Column(String(150), nullable=True)
    designation = Column(String(150), nullable=True)
    verification_source = Column(String(255), nullable=False)
    verification_date = Column(String(50), nullable=False)
    collaboration_role = Column(String(200), nullable=False)
    outreach_status = Column(SQLEnum(OutreachStatus), default=OutreachStatus.VERIFIED, nullable=False)
    proposed_collaboration_tier = Column(String(100), default="Tier 1: Expert Linguistic Validation", nullable=False)
    follow_up_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

    interactions = relationship("OutreachInteraction", back_populates="organization", cascade="all, delete-orphan", order_by="desc(OutreachInteraction.timestamp)")


class OutreachInteraction(Base):
    __tablename__ = "phase8_outreach_interactions"

    id = Column(Integer, primary_key=True, index=True)
    outreach_id = Column(Integer, ForeignKey("phase8_institutional_outreach.id"), nullable=False)
    interaction_type = Column(SQLEnum(InteractionType), nullable=False)
    summary = Column(String(255), nullable=False)
    details = Column(Text, nullable=True)
    outcome = Column(String(255), nullable=True)
    next_steps = Column(String(255), nullable=True)
    logged_by_id = Column(Integer, ForeignKey("phase5_reviewers.id"), nullable=True)
    logged_by_name = Column(String(150), nullable=True)
    timestamp = Column(DateTime, default=get_utc_now)

    organization = relationship("InstitutionalOutreach", back_populates="interactions")
