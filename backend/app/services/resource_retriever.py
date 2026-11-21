"""
SignBridge AI - Authentic ISL Resource Retrieval Engine
Standardizes retrieval of authentic sign videos, 3D mocap assets, and pedagogical
explanations by canonical concept ID, contextual meaning, and engineering branch.
Enforces the Zero-Fabrication Policy: never concatenates disjoint videos to fake continuous discourse.
"""

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from backend.app.models.entities import Concept, SignRecord, SignVideo, AvatarAnimation, ValidationStatus
from backend.app.services.explanation_service import EducationalExplanationService

class AuthenticResourceRetriever:
    """
    Retrieval service for validated ISL assets with graceful degradation.
    """

    @staticmethod
    def retrieve_by_concept_id(
        concept_id: int,
        db: Session,
        prefer_video: bool = True
    ) -> Dict[str, Any]:
        """
        Retrieves authentic assets for a specific concept ID with full provenance and license metadata.
        """
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if not concept:
            return {
                "found": False,
                "error": f"Concept with ID {concept_id} not found in knowledge base."
            }

        sign = db.query(SignRecord).filter(SignRecord.concept_id == concept.id).first()
        video = db.query(SignVideo).filter(SignVideo.sign_record_id == sign.id).first() if sign else None
        avatar = db.query(AvatarAnimation).filter(AvatarAnimation.sign_record_id == sign.id).first() if sign else None

        has_authentic_video = (
            video is not None and
            sign is not None and
            sign.validation_status in (ValidationStatus.VERIFIED, ValidationStatus.PARTIAL)
        )

        has_pedagogical = (
            sign is not None and
            sign.validation_status in (ValidationStatus.EXPLANATION_REQUIRED, ValidationStatus.EXPLANATION_NEEDED)
        )

        result: Dict[str, Any] = {
            "found": True,
            "concept_id": concept.id,
            "term": concept.term,
            "slug": concept.slug,
            "category": concept.category,
            "branch_id": concept.branch_id,
            "branch_code": concept.branch.code if concept.branch else None,
            "validation_status": sign.validation_status.value if sign else ValidationStatus.UNSUPPORTED.value,
            "sign_gloss": sign.sign_gloss if sign else concept.term.upper(),
            "has_video": has_authentic_video,
            "video_asset": None,
            "has_avatar": avatar is not None,
            "avatar_asset": None,
            "pedagogical_explanation": None,
            "fingerspelling_sequence": [c.upper() for c in concept.term if c.isalnum()]
        }

        if has_authentic_video and video:
            result["video_asset"] = {
                "id": video.id,
                "title": video.title,
                "video_url": video.video_path,
                "thumbnail_url": video.thumbnail_path,
                "duration_seconds": video.duration_seconds,
                "resolution": video.resolution,
                "signer_name": video.signer_name,
                "source_attribution": video.source_attribution,
                "license": video.license,
                "validation_status": video.validation_status.value,
                "notes": video.notes
            }

        if avatar:
            result["avatar_asset"] = {
                "id": avatar.id,
                "animation_name": avatar.animation_name,
                "asset_path": avatar.asset_path,
                "is_mocap": avatar.is_mocap,
                "is_neutral_preview": avatar.is_neutral_preview,
                "rig_standard": avatar.rig_standard,
                "validation_status": avatar.validation_status.value
            }

        if has_pedagogical or not has_authentic_video:
            pedagogical_data = EducationalExplanationService.get_explanation(concept.term)
            if not pedagogical_data:
                pedagogical_data = EducationalExplanationService.generate_generic_pedagogical_plan(
                    concept.term, category=concept.category, definition=concept.definition
                )
            result["pedagogical_explanation"] = pedagogical_data

        return result

    @staticmethod
    def retrieve_by_term(
        term: str,
        db: Session,
        branch_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Retrieves authentic resources matching a term, optionally filtered by engineering branch.
        """
        query = db.query(Concept).filter(Concept.term.ilike(term.strip()))
        if branch_code:
            from backend.app.models.entities import EngineeringBranch
            branch = db.query(EngineeringBranch).filter(EngineeringBranch.code == branch_code.lower()).first()
            if branch:
                query = query.filter(Concept.branch_id == branch.id)

        concept = query.first()
        if not concept:
            # Fallback to fingerspelling payload
            clean_letters = [c.upper() for c in term if c.isalnum()]
            return {
                "found": False,
                "term": term,
                "validation_status": ValidationStatus.UNSUPPORTED.value,
                "has_video": False,
                "has_avatar": False,
                "fingerspelling_sequence": clean_letters,
                "notice": f"Term '{term}' has no registered sign in knowledge base. Enforcing Zero-Fabrication Policy."
            }

        return AuthenticResourceRetriever.retrieve_by_concept_id(concept.id, db)

