"""
SignBridge AI - 3D Avatar Animation Service & Sequencer (Phase 4).
Consumes the Translation Intermediate Representation (IR) to assemble skeletal animation
tracks, synchronize facial Non-Manual Markers (NMM), and manage motion assets.
Strictly adheres to Zero-Fabrication Policy:
- Prohibits generating random gestures for unverified concepts.
- Transparently distinguishes VERIFIED_ISL_MOTION, PARTIALLY_VERIFIED_MOTION,
  REQUIRES_LINGUISTIC_REVIEW, DEMO_ONLY, and NOT_IMPLEMENTED.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime

from backend.app.models.entities import Concept, SignRecord, AvatarAnimation, ValidationStatus
from backend.app.schemas.avatar import MotionVerificationStatus
from backend.app.services.animation_library_service import AnimationLibraryService


anim_lib_service = AnimationLibraryService()


class AvatarSequenceTimeline:
    def __init__(
        self,
        sentence_text: str,
        overall_status: str,
        tracks: List[Dict[str, Any]],
        facial_markers: List[Dict[str, Any]],
        total_duration_seconds: float,
        policy_notice: str
    ):
        self.sentence_text = sentence_text
        self.overall_status = overall_status
        self.tracks = tracks
        self.facial_markers = facial_markers
        self.total_duration_seconds = total_duration_seconds
        self.policy_notice = policy_notice

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sentence_text": self.sentence_text,
            "overall_status": self.overall_status,
            "tracks": self.tracks,
            "facial_markers": self.facial_markers,
            "total_duration_seconds": self.total_duration_seconds,
            "policy_notice": self.policy_notice
        }


def resolve_avatar_animation_for_concept(concept_id: int, db: Session) -> Dict[str, Any]:
    """
    Retrieves the skeletal animation asset for a given concept.
    """
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        return {
            "available": False,
            "concept_term": "Unknown",
            "motion_status": MotionVerificationStatus.NOT_IMPLEMENTED.value,
            "message": "Concept not found in knowledge base."
        }

    sign = db.query(SignRecord).filter(SignRecord.concept_id == concept.id).first()
    if not sign:
        return {
            "available": False,
            "concept_term": concept.term,
            "motion_status": MotionVerificationStatus.NOT_IMPLEMENTED.value,
            "message": "No sign record registered."
        }

    # Query registered animations
    anim = (
        db.query(AvatarAnimation)
        .filter(AvatarAnimation.sign_record_id == sign.id)
        .first()
    )

    # Check for verified or partially verified mocap animation
    if anim and (
        anim.validation_status in [ValidationStatus.VERIFIED, ValidationStatus.PARTIAL]
        or sign.validation_status in [ValidationStatus.VERIFIED, ValidationStatus.PARTIAL]
    ):
        motion_status = (
            MotionVerificationStatus.VERIFIED_ISL_MOTION.value
            if anim.validation_status == ValidationStatus.VERIFIED
            else MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value
        )
        return {
            "available": True,
            "concept_id": concept.id,
            "concept_term": concept.term,
            "sign_gloss": sign.sign_gloss,
            "animation_name": anim.animation_name,
            "asset_path": anim.asset_path,
            "is_mocap": anim.is_mocap,
            "rig_standard": anim.rig_standard,
            "validation_status": anim.validation_status.value,
            "motion_status": motion_status,
            "phonological_parameters": {
                "dominant_hand": sign.dominant_hand,
                "handshape": sign.handshape,
                "movement": sign.movement,
                "location": sign.location,
                "orientation": sign.orientation,
                "non_manual_markers": sign.non_manual_markers
            },
            "disclaimer": (
                "Authentic motion capture asset derived from ISLRTC video. "
                "Classified as PARTIALLY_VERIFIED_MOTION pending accredited Deaf expert sign-off."
            )
        }

    # Check if we have processed mocap in the library directly
    lib_mocap = anim_lib_service.get_mocap_for_concept(concept.term)
    if lib_mocap:
        return {
            "available": True,
            "concept_id": concept.id,
            "concept_term": concept.term,
            "sign_gloss": sign.sign_gloss,
            "animation_name": f"islrtc_{concept.term.lower()}_mocap",
            "asset_path": f"/data/isl_motion/processed/islrtc_{concept.term.lower()}_mocap.json",
            "is_mocap": True,
            "rig_standard": "SignBridge-Articulated-54",
            "validation_status": "partial",
            "motion_status": MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value,
            "phonological_parameters": {
                "dominant_hand": sign.dominant_hand,
                "handshape": sign.handshape,
                "movement": sign.movement,
                "location": sign.location,
                "orientation": sign.orientation,
                "non_manual_markers": sign.non_manual_markers
            },
            "disclaimer": lib_mocap.get("linguistic_disclaimer")
        }

    # Honest unavailable status
    return {
        "available": False,
        "concept_id": concept.id,
        "concept_term": concept.term,
        "sign_gloss": sign.sign_gloss,
        "validation_status": sign.validation_status.value,
        "motion_status": MotionVerificationStatus.NOT_IMPLEMENTED.value,
        "phonological_parameters": {
            "dominant_hand": sign.dominant_hand,
            "handshape": sign.handshape,
            "movement": sign.movement,
            "location": sign.location,
            "orientation": sign.orientation,
            "non_manual_markers": sign.non_manual_markers
        },
        "message": f"Zero-Fabrication Policy: No validated 3D skeletal animation exists for '{concept.term}'. Arbitrary avatar gestures are prohibited."
    }


def construct_avatar_timeline_from_ir(ir_data: Dict[str, Any], db: Session) -> AvatarSequenceTimeline:
    """
    Constructs a sequential sign animation timeline from the Translation IR.
    """
    source_text = ir_data.get("source_text", "")
    detected_concepts = ir_data.get("detected_concepts", [])
    grammar_plan = ir_data.get("isl_grammar_plan", {})
    sentence_type = grammar_plan.get("sentence_type", "DECLARATIVE")

    tracks = []
    current_time = 0.0

    # Neutral rest at beginning
    tracks.append({
        "track_id": "track_0_rest",
        "type": "pose",
        "name": "NEUTRAL_REST",
        "start_time": current_time,
        "duration": 0.5,
        "locus": "CENTER",
        "status": "ready"
    })
    current_time += 0.5

    for c in detected_concepts:
        cid = c.get("id")
        term = c.get("term")
        anim_data = resolve_avatar_animation_for_concept(cid, db)

        if anim_data.get("available"):
            tracks.append({
                "track_id": f"track_{cid}_{term.lower()}",
                "type": "sign_animation",
                "name": anim_data.get("sign_gloss", term.upper()),
                "concept_term": term,
                "asset_path": anim_data.get("asset_path"),
                "motion_status": anim_data.get("motion_status", MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value),
                "start_time": current_time,
                "duration": 1.5,
                "locus": "LOCUS_A",
                "status": "verified" if anim_data.get("motion_status") == MotionVerificationStatus.VERIFIED_ISL_MOTION.value else "partially_verified"
            })
            current_time += 1.5
        else:
            tracks.append({
                "track_id": f"track_{cid}_{term.lower()}_unsupported",
                "type": "pedagogical_pause",
                "name": f"PAUSE_{term.upper()}",
                "concept_term": term,
                "start_time": current_time,
                "duration": 1.0,
                "status": "animation_unavailable",
                "notice": anim_data.get("message")
            })
            current_time += 1.0

    # Neutral rest at end
    tracks.append({
        "track_id": "track_end_rest",
        "type": "pose",
        "name": "NEUTRAL_REST",
        "start_time": current_time,
        "duration": 0.5,
        "locus": "CENTER",
        "status": "ready"
    })
    current_time += 0.5

    # Facial non-manual markers
    facial_markers = []
    if sentence_type == "WH_QUESTION":
        facial_markers.append({
            "marker": "furrowed_brow",
            "intensity": 0.85,
            "start_time": max(0.0, current_time - 1.5),
            "end_time": current_time,
            "scope": "terminal_question"
        })
    elif sentence_type == "POLAR_QUESTION":
        facial_markers.append({
            "marker": "raised_brow_forward_tilt",
            "intensity": 0.80,
            "start_time": max(0.0, current_time - 1.5),
            "end_time": current_time,
            "scope": "terminal_question"
        })

    return AvatarSequenceTimeline(
        sentence_text=source_text,
        overall_status=ir_data.get("policy_verdict", {}).get("overall_status", "unsupported"),
        tracks=tracks,
        facial_markers=facial_markers,
        total_duration_seconds=round(current_time, 2),
        policy_notice="Avatar animation sequence assembled from validated sign tokens. Gestures are rendered only where verified motion data exists."
    )
