"""
SignBridge AI - Phase 8 Institutional Outreach Endpoints.
Provides structured institutional tracking, outreach lifecycle management, and interaction logging.
Zero-Fabrication Policy:
- Maintains verified contacts and audit trails without sending unauthorized messages.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from backend.app.database.database import get_db
from backend.app.models.validation_models import Reviewer, ReviewerRole
from backend.app.models.outreach_models import (
    InstitutionalOutreach,
    OutreachInteraction,
    OutreachCategory,
    OutreachStatus,
    InteractionType
)
from backend.app.schemas.outreach import (
    OutreachCreateRequest,
    OutreachUpdateRequest,
    InteractionCreateRequest,
    InteractionResponse,
    InstitutionalOutreachResponse,
    InstitutionalOutreachDetailResponse,
    OutreachSummaryStatsResponse
)
from backend.app.core.auth import (
    security_scheme,
    decode_access_token,
    get_current_reviewer,
    require_roles
)

router = APIRouter()


def get_optional_reviewer(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Optional[Reviewer]:
    if not credentials or not credentials.credentials:
        return None
    try:
        payload = decode_access_token(credentials.credentials, db=db)
        reviewer_id = payload.get("sub")
        if reviewer_id:
            return db.query(Reviewer).filter(Reviewer.id == reviewer_id).first()
    except Exception:
        return None
    return None


@router.get("/organizations", response_model=List[InstitutionalOutreachResponse], summary="List verified institutions with filtering")
def list_organizations(
    category: Optional[OutreachCategory] = Query(None, description="Filter by institutional category"),
    status: Optional[OutreachStatus] = Query(None, description="Filter by outreach lifecycle status"),
    search: Optional[str] = Query(None, description="Search term for organization name or acronym"),
    db: Session = Depends(get_db)
):
    """
    Returns verified institutions and their current outreach pipeline state.
    """
    query = db.query(InstitutionalOutreach)

    if category:
        query = query.filter(InstitutionalOutreach.category == category)
    if status:
        query = query.filter(InstitutionalOutreach.outreach_status == status)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                InstitutionalOutreach.organization_name.ilike(search_filter),
                InstitutionalOutreach.acronym.ilike(search_filter),
                InstitutionalOutreach.department.ilike(search_filter)
            )
        )

    records = query.order_by(InstitutionalOutreach.id.asc()).all()

    # Populate interaction count
    results = []
    for r in records:
        count = len(r.interactions)
        item = InstitutionalOutreachResponse(
            id=r.id,
            organization_name=r.organization_name,
            acronym=r.acronym,
            category=r.category,
            website=r.website,
            public_contact=r.public_contact,
            telephone=r.telephone,
            department=r.department,
            contact_person=r.contact_person,
            designation=r.designation,
            verification_source=r.verification_source,
            verification_date=r.verification_date,
            collaboration_role=r.collaboration_role,
            outreach_status=r.outreach_status,
            proposed_collaboration_tier=r.proposed_collaboration_tier,
            follow_up_date=r.follow_up_date,
            notes=r.notes,
            interaction_count=count,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        results.append(item)

    return results


@router.get("/stats", response_model=OutreachSummaryStatsResponse, summary="Summary statistics of institutional outreach")
def get_outreach_stats(db: Session = Depends(get_db)):
    """
    Returns summary statistics for the institutional outreach pipeline.
    """
    records = db.query(InstitutionalOutreach).all()
    interactions = db.query(OutreachInteraction).all()

    by_category: Dict[str, int] = {}
    for cat in OutreachCategory:
        by_category[cat.value] = 0

    by_status: Dict[str, int] = {}
    for st in OutreachStatus:
        by_status[st.value] = 0

    pending_follow_ups = 0
    now = datetime.now(timezone.utc)

    for r in records:
        cat_val = r.category.value if hasattr(r.category, "value") else str(r.category)
        st_val = r.outreach_status.value if hasattr(r.outreach_status, "value") else str(r.outreach_status)
        by_category[cat_val] = by_category.get(cat_val, 0) + 1
        by_status[st_val] = by_status.get(st_val, 0) + 1

        if r.follow_up_date:
            follow_dt = r.follow_up_date
            if follow_dt.tzinfo is None:
                follow_dt = follow_dt.replace(tzinfo=timezone.utc)
            if follow_dt <= now:
                pending_follow_ups += 1

    return OutreachSummaryStatsResponse(
        total_organizations=len(records),
        by_category=by_category,
        by_status=by_status,
        pending_follow_ups=pending_follow_ups,
        total_interactions=len(interactions)
    )


@router.get("/organizations/{id}", response_model=InstitutionalOutreachDetailResponse, summary="Get institution details and interaction log")
def get_organization_detail(id: int, db: Session = Depends(get_db)):
    """
    Returns detailed institutional profile and full chronological interaction history.
    """
    record = db.query(InstitutionalOutreach).filter(InstitutionalOutreach.id == id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {id} not found."
        )

    interactions = [
        InteractionResponse(
            id=i.id,
            outreach_id=i.outreach_id,
            interaction_type=i.interaction_type,
            summary=i.summary,
            details=i.details,
            outcome=i.outcome,
            next_steps=i.next_steps,
            logged_by_id=i.logged_by_id,
            logged_by_name=i.logged_by_name,
            timestamp=i.timestamp
        )
        for i in record.interactions
    ]

    return InstitutionalOutreachDetailResponse(
        id=record.id,
        organization_name=record.organization_name,
        acronym=record.acronym,
        category=record.category,
        website=record.website,
        public_contact=record.public_contact,
        telephone=record.telephone,
        department=record.department,
        contact_person=record.contact_person,
        designation=record.designation,
        verification_source=record.verification_source,
        verification_date=record.verification_date,
        collaboration_role=record.collaboration_role,
        outreach_status=record.outreach_status,
        proposed_collaboration_tier=record.proposed_collaboration_tier,
        follow_up_date=record.follow_up_date,
        notes=record.notes,
        interaction_count=len(interactions),
        created_at=record.created_at,
        updated_at=record.updated_at,
        interactions=interactions
    )


@router.post("/organizations", response_model=InstitutionalOutreachResponse, status_code=status.HTTP_201_CREATED, summary="Create a new institution entry")
def create_organization(
    req: OutreachCreateRequest,
    db: Session = Depends(get_db),
    reviewer: Optional[Reviewer] = Depends(get_optional_reviewer)
):
    """
    Registers a new institution into the outreach tracking system.
    """
    existing = db.query(InstitutionalOutreach).filter(
        InstitutionalOutreach.organization_name == req.organization_name
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Organization '{req.organization_name}' already exists."
        )

    entry = InstitutionalOutreach(
        organization_name=req.organization_name,
        acronym=req.acronym,
        category=req.category,
        website=req.website,
        public_contact=req.public_contact,
        telephone=req.telephone,
        department=req.department,
        contact_person=req.contact_person,
        designation=req.designation,
        verification_source=req.verification_source,
        verification_date=req.verification_date,
        collaboration_role=req.collaboration_role,
        outreach_status=req.outreach_status,
        proposed_collaboration_tier=req.proposed_collaboration_tier,
        follow_up_date=req.follow_up_date,
        notes=req.notes
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return InstitutionalOutreachResponse(
        id=entry.id,
        organization_name=entry.organization_name,
        acronym=entry.acronym,
        category=entry.category,
        website=entry.website,
        public_contact=entry.public_contact,
        telephone=entry.telephone,
        department=entry.department,
        contact_person=entry.contact_person,
        designation=entry.designation,
        verification_source=entry.verification_source,
        verification_date=entry.verification_date,
        collaboration_role=entry.collaboration_role,
        outreach_status=entry.outreach_status,
        proposed_collaboration_tier=entry.proposed_collaboration_tier,
        follow_up_date=entry.follow_up_date,
        notes=entry.notes,
        interaction_count=0,
        created_at=entry.created_at,
        updated_at=entry.updated_at
    )


@router.patch("/organizations/{id}", response_model=InstitutionalOutreachResponse, summary="Update institution outreach status or notes")
def update_organization(
    id: int,
    req: OutreachUpdateRequest,
    db: Session = Depends(get_db),
    reviewer: Optional[Reviewer] = Depends(get_optional_reviewer)
):
    """
    Updates status, notes, contact information, or follow-up dates.
    """
    entry = db.query(InstitutionalOutreach).filter(InstitutionalOutreach.id == id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {id} not found."
        )

    for field, val in req.model_dump(exclude_unset=True).items():
        setattr(entry, field, val)

    entry.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(entry)

    return InstitutionalOutreachResponse(
        id=entry.id,
        organization_name=entry.organization_name,
        acronym=entry.acronym,
        category=entry.category,
        website=entry.website,
        public_contact=entry.public_contact,
        telephone=entry.telephone,
        department=entry.department,
        contact_person=entry.contact_person,
        designation=entry.designation,
        verification_source=entry.verification_source,
        verification_date=entry.verification_date,
        collaboration_role=entry.collaboration_role,
        outreach_status=entry.outreach_status,
        proposed_collaboration_tier=entry.proposed_collaboration_tier,
        follow_up_date=entry.follow_up_date,
        notes=entry.notes,
        interaction_count=len(entry.interactions),
        created_at=entry.created_at,
        updated_at=entry.updated_at
    )


@router.post("/organizations/{id}/interactions", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED, summary="Log an outreach interaction")
def log_interaction(
    id: int,
    req: InteractionCreateRequest,
    db: Session = Depends(get_db),
    reviewer: Optional[Reviewer] = Depends(get_optional_reviewer)
):
    """
    Appends an interaction record (email, meeting, presentation, note) to the institutional timeline.
    """
    entry = db.query(InstitutionalOutreach).filter(InstitutionalOutreach.id == id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {id} not found."
        )

    logged_by_id = reviewer.id if reviewer else None
    logged_by_name = reviewer.full_name if reviewer else "SignBridge Researcher"

    interaction = OutreachInteraction(
        outreach_id=entry.id,
        interaction_type=req.interaction_type,
        summary=req.summary,
        details=req.details,
        outcome=req.outcome,
        next_steps=req.next_steps,
        logged_by_id=logged_by_id,
        logged_by_name=logged_by_name
    )
    db.add(interaction)

    # Automatically advance status if logical
    if req.interaction_type == InteractionType.EMAIL_SENT and entry.outreach_status == OutreachStatus.READY_FOR_OUTREACH:
        entry.outreach_status = OutreachStatus.CONTACTED
    elif req.interaction_type == InteractionType.EMAIL_RECEIVED and entry.outreach_status == OutreachStatus.CONTACTED:
        entry.outreach_status = OutreachStatus.RESPONSE_RECEIVED
    elif req.interaction_type in (InteractionType.VIRTUAL_MEETING, InteractionType.IN_PERSON_MEETING, InteractionType.PRESENTATION):
        if entry.outreach_status in (OutreachStatus.CONTACTED, OutreachStatus.RESPONSE_RECEIVED, OutreachStatus.MEETING_REQUESTED):
            entry.outreach_status = OutreachStatus.MEETING_COMPLETED
    elif req.interaction_type == InteractionType.MOU_DRAFT:
        entry.outreach_status = OutreachStatus.AGREEMENT_PENDING

    entry.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(interaction)

    return InteractionResponse(
        id=interaction.id,
        outreach_id=interaction.outreach_id,
        interaction_type=interaction.interaction_type,
        summary=interaction.summary,
        details=interaction.details,
        outcome=interaction.outcome,
        next_steps=interaction.next_steps,
        logged_by_id=interaction.logged_by_id,
        logged_by_name=interaction.logged_by_name,
        timestamp=interaction.timestamp
    )


@router.get("/export", summary="Export outreach directory as JSON")
def export_outreach(db: Session = Depends(get_db)):
    """
    Exports full outreach registry and interaction histories for audit and governance packages.
    """
    records = db.query(InstitutionalOutreach).order_by(InstitutionalOutreach.id.asc()).all()
    export_data = []
    for r in records:
        export_data.append({
            "id": r.id,
            "organization_name": r.organization_name,
            "acronym": r.acronym,
            "category": r.category.value if hasattr(r.category, "value") else str(r.category),
            "website": r.website,
            "public_contact": r.public_contact,
            "telephone": r.telephone,
            "department": r.department,
            "contact_person": r.contact_person,
            "designation": r.designation,
            "verification_source": r.verification_source,
            "verification_date": r.verification_date,
            "collaboration_role": r.collaboration_role,
            "outreach_status": r.outreach_status.value if hasattr(r.outreach_status, "value") else str(r.outreach_status),
            "proposed_collaboration_tier": r.proposed_collaboration_tier,
            "follow_up_date": r.follow_up_date.isoformat() if r.follow_up_date else None,
            "notes": r.notes,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            "interactions": [
                {
                    "id": i.id,
                    "type": i.interaction_type.value if hasattr(i.interaction_type, "value") else str(i.interaction_type),
                    "summary": i.summary,
                    "details": i.details,
                    "outcome": i.outcome,
                    "next_steps": i.next_steps,
                    "logged_by": i.logged_by_name,
                    "timestamp": i.timestamp.isoformat() if i.timestamp else None
                }
                for i in r.interactions
            ]
        })

    return {
        "export_timestamp": datetime.now(timezone.utc).isoformat(),
        "total_organizations": len(export_data),
        "organizations": export_data
    }
