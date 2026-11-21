"""
SignBridge AI - 3D Avatar & Motion Capture Endpoints (Phase 4).
Provides status, animation listing, detailed keyframe data,
sentence animation sequencing, and on-the-fly retargeting.
"""

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query
from sqlalchemy.orm import Session
from pathlib import Path
from typing import Optional, Dict, Any, List
import json

from backend.app.database.database import get_db
from backend.app.core.config import settings
from backend.app.models.entities import Concept, SignRecord, AvatarAnimation, ValidationStatus
from backend.app.schemas.avatar import (
    MotionVerificationStatus,
    AvatarStatusResponse,
    AvatarSequencePayload,
    AvatarAnimationTrack
)
from backend.app.services.avatar_animation import (
    resolve_avatar_animation_for_concept, construct_avatar_timeline_from_ir
)
from backend.app.services.animation_library_service import AnimationLibraryService
from backend.app.services.motion_retargeting_service import MotionRetargetingService
from backend.app.services.motion_fidelity_service import MotionFidelityService

router = APIRouter()

ALLOWED_ANIMATION_EXTS = {".glb", ".gltf", ".json"}
anim_lib_service = AnimationLibraryService()
retarget_service = MotionRetargetingService()
fidelity_service = MotionFidelityService()


@router.get("/status", response_model=AvatarStatusResponse, summary="Avatar and motion capture subsystem status")
def get_avatar_subsystem_status(db: Session = Depends(get_db)):
    """
    Returns the technical status of the 3D avatar rig, motion capture library,
    and Zero-Fabrication Policy compliance.
    """
    total_anims = db.query(AvatarAnimation).count()
    status_counts = {}
    for st in ValidationStatus:
        cnt = db.query(AvatarAnimation).filter(AvatarAnimation.validation_status == st).count()
        if cnt > 0:
            status_counts[st.value] = cnt

    # Add active mocap files count
    available_terms = anim_lib_service.get_available_mocap_terms()

    return AvatarStatusResponse(
        avatar_name="SignBridge Signer-01",
        rig_standard="SignBridge-Articulated-54",
        total_joints_count=54,
        finger_joints_count_per_hand=15,
        supported_facial_morph_targets=[
            "brow_furrow_left",
            "brow_furrow_right",
            "brow_raise_left",
            "brow_raise_right",
            "mouth_open",
            "mouth_wide",
            "eye_blink_left",
            "eye_blink_right",
            "head_pitch",
            "head_yaw",
            "head_roll"
        ],
        motion_capture_pipeline_available=True,
        active_mocap_animations_count=len(available_terms),
        status_breakdown=status_counts,
        zero_fabrication_policy_enforced=True,
        disclaimer=(
            "All motions are governed by the Zero-Fabrication Policy. "
            "Extracted ISLRTC mocap motions are marked PARTIALLY_VERIFIED_MOTION. "
            "Procedural animations are marked DEMO_ONLY. Arbitrary sign invention is strictly prohibited."
        )
    )


@router.get("/animations", summary="List all registered 3D signing animations")
def list_avatar_animations(
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db)
):
    """
    Lists registered avatar animations with concept association and verification status.
    """
    query = db.query(AvatarAnimation)
    if status_filter:
        try:
            val_status = ValidationStatus(status_filter.lower())
            query = query.filter(AvatarAnimation.validation_status == val_status)
        except ValueError:
            pass

    records = query.all()
    results = []
    for anim in records:
        sign = db.query(SignRecord).filter(SignRecord.id == anim.sign_record_id).first()
        concept = db.query(Concept).filter(Concept.id == sign.concept_id).first() if sign else None

        results.append({
            "id": anim.id,
            "sign_record_id": anim.sign_record_id,
            "concept_id": concept.id if concept else None,
            "concept_term": concept.term if concept else "Unknown",
            "sign_gloss": sign.sign_gloss if sign else None,
            "animation_name": anim.animation_name,
            "asset_path": anim.asset_path,
            "is_mocap": anim.is_mocap,
            "rig_standard": anim.rig_standard,
            "validation_status": anim.validation_status.value,
            "motion_status": (
                MotionVerificationStatus.VERIFIED_ISL_MOTION.value
                if anim.validation_status == ValidationStatus.VERIFIED
                else MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value
                if anim.validation_status == ValidationStatus.PARTIAL
                else MotionVerificationStatus.DEMO_ONLY.value
            ),
            "created_at": anim.created_at.isoformat() if anim.created_at else None
        })

    return {
        "total_count": len(results),
        "animations": results
    }


@router.get("/animations/{animation_id}", summary="Get detailed animation data with keyframes")
def get_avatar_animation_detail(animation_id: int, db: Session = Depends(get_db)):
    """
    Retrieves full animation keyframe track data for an animation by ID.
    """
    anim = db.query(AvatarAnimation).filter(AvatarAnimation.id == animation_id).first()
    if not anim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Animation with ID {animation_id} not found."
        )

    sign = db.query(SignRecord).filter(SignRecord.id == anim.sign_record_id).first()
    concept = db.query(Concept).filter(Concept.id == sign.concept_id).first() if sign else None
    term = concept.term if concept else ""

    # Check for processed mocap data file
    mocap_data = anim_lib_service.get_mocap_for_concept(term)

    return {
        "id": anim.id,
        "animation_name": anim.animation_name,
        "concept_term": term,
        "sign_gloss": sign.sign_gloss if sign else None,
        "rig_standard": anim.rig_standard,
        "is_mocap": anim.is_mocap,
        "validation_status": anim.validation_status.value,
        "asset_path": anim.asset_path,
        "keyframes_count": len(mocap_data.get("keyframes", [])) if mocap_data else 0,
        "duration_seconds": mocap_data.get("duration_seconds", 0.0) if mocap_data else 0.0,
        "keyframes": mocap_data.get("keyframes", []) if mocap_data else [],
        "linguistic_disclaimer": mocap_data.get("linguistic_disclaimer") if mocap_data else None
    }


@router.get("/animations/concept/{concept_id}", summary="Get animation by concept ID or term")
def get_avatar_animation_by_concept(concept_id: int, db: Session = Depends(get_db)):
    """
    Retrieves animation keyframe tracks for a specific concept.
    """
    return resolve_avatar_animation_for_concept(concept_id, db)


@router.get("/fidelity", summary="Get motion fidelity evaluation across all concepts")
def get_all_motion_fidelity():
    """
    Returns quantitative motion fidelity metrics (NMLE, DTW, Handshape, NMM) for all ingested signs.
    """
    return fidelity_service.evaluate_all_available_concepts()


@router.get("/fidelity/{concept_term}", summary="Get motion fidelity evaluation for a concept")
def get_motion_fidelity(concept_term: str):
    """
    Returns quantitative motion fidelity metrics for a specific concept term.
    """
    res = fidelity_service.evaluate_concept_fidelity(concept_term)
    if res.get("available") is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=res.get("error", f"Fidelity evaluation unavailable for '{concept_term}'")
        )
    return res


@router.post("/sequence", response_model=AvatarSequencePayload, summary="Assemble multi-concept animation sequence")
def generate_avatar_sequence(payload: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Generates a full continuous animation sequence from source text and translation plan.
    """
    source_text = payload.get("source_text", "")
    detected_concepts = payload.get("detected_concepts", [])
    grammar_plan = payload.get("grammar_plan", {})

    sequence = anim_lib_service.assemble_sequence_from_translation_plan(
        source_text=source_text,
        detected_concepts=detected_concepts,
        grammar_plan=grammar_plan
    )
    return sequence


@router.post("/retarget", summary="Retarget raw landmark frames to avatar rig")
def retarget_landmarks(payload: Dict[str, Any]):
    """
    Retargets a list of raw landmark frames into avatar bone Euler keyframes on the fly.
    """
    frames = payload.get("frames", [])
    if not frames:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload must include 'frames' list of landmark dictionaries."
        )

    keyframes = retarget_service.retarget_frames_to_keyframes(frames)
    return {
        "status": "success",
        "retargeted_keyframes_count": len(keyframes),
        "keyframes": [kf.model_dump() for kf in keyframes]
    }


# Retain backward-compatible existing endpoints
@router.get("/retrieve/{concept_id}", summary="Legacy retrieve 3D sign animation metadata")
def get_avatar_animation_legacy(concept_id: int, db: Session = Depends(get_db)):
    return resolve_avatar_animation_for_concept(concept_id, db)


@router.post("/timeline", summary="Legacy assemble animation timeline from IR")
def generate_avatar_timeline_legacy(ir_data: Dict[str, Any], db: Session = Depends(get_db)):
    timeline = construct_avatar_timeline_from_ir(ir_data, db)
    return timeline.to_dict()


@router.post("/upload", summary="Ingest authentic 3D signing animation asset")
def upload_avatar_animation(
    sign_record_id: int = Form(...),
    animation_name: str = Form(...),
    rig_standard: str = Form(default="SignBridge-Articulated-54"),
    is_mocap: bool = Form(default=True),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    sign_record = db.query(SignRecord).filter(SignRecord.id == sign_record_id).first()
    if not sign_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sign record with ID {sign_record_id} does not exist."
        )

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_ANIMATION_EXTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported animation file extension '{ext}'. Allowed: {', '.join(ALLOWED_ANIMATION_EXTS)}"
        )

    anim_dir = settings.DATA_DIR / "avatar_animations"
    anim_dir.mkdir(parents=True, exist_ok=True)

    safe_filename = Path(file.filename).name
    target_path = anim_dir / safe_filename

    with open(target_path, "wb") as f_out:
        content = file.file.read()
        f_out.write(content)

    rel_path = f"/data/avatar_animations/{safe_filename}"

    animation = AvatarAnimation(
        sign_record_id=sign_record.id,
        animation_name=animation_name,
        asset_path=rel_path,
        is_mocap=is_mocap,
        is_procedural=False,
        is_neutral_preview=False,
        validation_status=ValidationStatus.NEEDS_REVIEW,
        rig_standard=rig_standard
    )
    db.add(animation)
    db.commit()
    db.refresh(animation)

    return {
        "status": "success",
        "animation_id": animation.id,
        "sign_record_id": animation.sign_record_id,
        "animation_name": animation.animation_name,
        "asset_path": animation.asset_path,
        "rig_standard": animation.rig_standard,
        "validation_status": animation.validation_status.value,
        "message": "Skeletal animation successfully ingested and placed in validation queue."
    }
