from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.app.database.database import get_db
from backend.app.services.video_ingestion import ingest_sign_video
from backend.app.services.video_retrieval import retrieve_video_for_concept, retrieve_videos_for_sentence_concepts

router = APIRouter()

@router.post("/upload", summary="Ingest authentic human ISL signing video")
def upload_sign_video(
    sign_record_id: int = Form(...),
    title: str = Form(...),
    signer_name: Optional[str] = Form(None),
    source_attribution: str = Form(...),
    license_type: str = Form(default="Government Educational Reference / Fair Dealing"),
    is_native_signer: bool = Form(default=True),
    notes: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Ingests an authentic human ISL signing recording, extracts technical metadata,
    generates a thumbnail via FFmpeg, and registers the video under NEEDS_REVIEW.
    """
    video = ingest_sign_video(
        file=file,
        sign_record_id=sign_record_id,
        title=title,
        signer_name=signer_name,
        source_attribution=source_attribution,
        license_type=license_type,
        is_native_signer=is_native_signer,
        notes=notes,
        db=db
    )

    return {
        "status": "success",
        "video_id": video.id,
        "sign_record_id": video.sign_record_id,
        "title": video.title,
        "video_path": video.video_path,
        "thumbnail_path": video.thumbnail_path,
        "duration_seconds": video.duration_seconds,
        "resolution": video.resolution,
        "validation_status": video.validation_status.value,
        "message": "Video successfully ingested and placed in expert validation queue."
    }

@router.get("/retrieve/{concept_id}", summary="Retrieve signing video for technical concept")
def get_video_for_concept(concept_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the authentic signing video match for a concept.
    Distinguishes EXACT_MATCH, CONTEXTUAL_MATCH, and NO_MATCH.
    """
    match = retrieve_video_for_concept(concept_id, db)
    return match.to_dict()

@router.get("/sentence-retrieval", summary="Retrieve signing videos for multiple concepts")
def get_videos_for_sentence(concept_ids: str, db: Session = Depends(get_db)):
    """
    Retrieves video matches for comma-separated concept IDs.
    Refuses fake sentence concatenation as per Zero-Fabrication policy.
    """
    try:
        c_ids = [int(x.strip()) for x in concept_ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="concept_ids must be a comma-separated list of integers."
        )

    return retrieve_videos_for_sentence_concepts(c_ids, db)
