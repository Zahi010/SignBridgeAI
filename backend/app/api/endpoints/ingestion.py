"""
SignBridge AI - Authentic Dataset Ingestion & Recording Session Endpoints
Provides authenticated APIs to:
1. Register recording sessions with verified signer consent.
2. Ingest genuine human signing videos with automated FFprobe metadata extraction.
3. Batch-ingest CSV and JSON sign annotation datasets.
4. Enqueue new records under strict NEEDS_REVIEW status.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.entities import RecordingSession, ConsentStatus, Concept, SignRecord
from backend.app.services.dataset_ingestion import (
    create_recording_session,
    ingest_human_signing_video,
    ingest_json_dataset,
    ingest_csv_dataset
)

router = APIRouter()

class RecordingSessionCreateRequest(BaseModel):
    session_uid: str = Field(..., description="Unique session code e.g. REC-20261120-CS-01")
    signer_id: str = Field(..., description="Anonymized or official signer identifier e.g. SIGNER-AIFD-01")
    signer_name: Optional[str] = Field(None, description="Signer name or attribution pseudonym")
    is_native_signer: bool = Field(True, description="Whether signer is a native Deaf signer")
    camera_setup: str = Field("Frontal 1080p60 Studio Setup", description="Camera resolution, angle, and framerate")
    lighting_environment: str = Field("Three-point softbox studio lighting", description="Lighting conditions")
    background: str = Field("Neutral 18% Gray / Chroma Green", description="Studio backdrop")
    consent_status: str = Field("verified_consent", description="verified_consent, pending_consent, restricted_educational")
    consent_document_ref: Optional[str] = Field(None, description="Archived consent document tracking ID")
    notes: Optional[str] = None

class RecordingSessionResponse(BaseModel):
    id: int
    session_uid: str
    signer_id: str
    signer_name: Optional[str]
    is_native_signer: bool
    camera_setup: str
    consent_status: str
    consent_document_ref: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

@router.post("/recording-session", response_model=RecordingSessionResponse, summary="Register authentic sign recording session")
def register_recording_session(
    payload: RecordingSessionCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Registers an official recording session with explicit signer consent metadata before video ingestion.
    """
    try:
        consent_enum = ConsentStatus(payload.consent_status.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid consent status '{payload.consent_status}'. Must be verified_consent, pending_consent, or restricted_educational."
        )

    session = create_recording_session(
        db=db,
        session_uid=payload.session_uid,
        signer_id=payload.signer_id,
        signer_name=payload.signer_name,
        is_native_signer=payload.is_native_signer,
        camera_setup=payload.camera_setup,
        lighting_environment=payload.lighting_environment,
        background=payload.background,
        consent_status=consent_enum,
        consent_document_ref=payload.consent_document_ref,
        consent_date=datetime.now(timezone.utc),
        notes=payload.notes
    )
    return session

@router.get("/recording-sessions", response_model=List[RecordingSessionResponse], summary="List registered recording sessions")
def list_recording_sessions(db: Session = Depends(get_db)):
    """
    Lists all registered recording sessions with consent and equipment metadata.
    """
    return db.query(RecordingSession).order_by(RecordingSession.created_at.desc()).all()

@router.post("/sign-video", summary="Ingest authentic human signing video file")
def upload_signing_video(
    concept_id: int = Form(..., description="Target engineering concept ID"),
    recording_session_id: Optional[int] = Form(None, description="Associated recording session ID"),
    title: str = Form(..., description="Descriptive title of the sign demonstration"),
    signer_name: Optional[str] = Form(None, description="Signer name or attribution"),
    source_attribution: str = Form(..., description="Accredited institution or dataset citation"),
    license_type: str = Form("Government Educational Reference / Fair Dealing"),
    dominant_hand: Optional[str] = Form(None),
    handshape: Optional[str] = Form(None),
    movement: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    orientation: Optional[str] = Form(None),
    non_manual_markers: Optional[str] = Form(None),
    regional_dialect: Optional[str] = Form("Standard ISL (Pan-India)"),
    file: UploadFile = File(..., description="Video file: MP4, MOV, or WebM"),
    db: Session = Depends(get_db)
):
    """
    Ingests an authentic human signing recording. Validates format (MP4/MOV/WebM <100MB),
    probes video stream via FFprobe, generates thumbnail, stores provenance,
    and sets validation status to NEEDS_REVIEW.
    """
    result = ingest_human_signing_video(
        file=file,
        concept_id=concept_id,
        recording_session_id=recording_session_id,
        title=title,
        signer_name=signer_name,
        source_attribution=source_attribution,
        license_type=license_type,
        dominant_hand=dominant_hand,
        handshape=handshape,
        movement=movement,
        location=location,
        orientation=orientation,
        non_manual_markers=non_manual_markers,
        regional_dialect=regional_dialect,
        db=db
    )
    return result

@router.post("/batch-json", summary="Batch ingest JSON dataset annotations")
def upload_json_annotations(
    file: UploadFile = File(..., description="JSON dataset file containing sign records"),
    db: Session = Depends(get_db)
):
    """
    Batch ingests sign language annotations from JSON format.
    """
    content = file.file.read().decode("utf-8")
    return ingest_json_dataset(content, db)

@router.post("/batch-csv", summary="Batch ingest CSV dataset annotations")
def upload_csv_annotations(
    file: UploadFile = File(..., description="CSV dataset file with phonological headers"),
    db: Session = Depends(get_db)
):
    """
    Batch ingests sign language annotations from CSV format.
    """
    content = file.file.read().decode("utf-8")
    return ingest_csv_dataset(content, db)

