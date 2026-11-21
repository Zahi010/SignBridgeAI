"""
SignBridge AI - Human Sign Video Retrieval Engine.
Resolves authentic signing video assets for detected concepts and gloss sequences.
Adheres strictly to the Zero Fabricated Signs Policy:
- Prohibits concatenating isolated signs into fake continuous sentence videos.
- Distinguishes EXACT_MATCH, CONTEXTUAL_MATCH, PARTIAL_MATCH, and NO_MATCH.
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from backend.app.models.entities import Concept, SignRecord, SignVideo, ValidationStatus

class VideoMatchResult:
    def __init__(
        self,
        match_type: str, # "EXACT_MATCH", "CONTEXTUAL_MATCH", "PARTIAL_MATCH", "NO_MATCH"
        concept_term: str,
        sign_gloss: str,
        video_url: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        signer_name: Optional[str] = None,
        source_attribution: Optional[str] = None,
        license: Optional[str] = None,
        duration_seconds: float = 0.0,
        resolution: Optional[str] = None,
        validation_status: str = "unsupported",
        explanation: Optional[str] = None
    ):
        self.match_type = match_type
        self.concept_term = concept_term
        self.sign_gloss = sign_gloss
        self.video_url = video_url
        self.thumbnail_url = thumbnail_url
        self.signer_name = signer_name
        self.source_attribution = source_attribution
        self.license = license
        self.duration_seconds = duration_seconds
        self.resolution = resolution
        self.validation_status = validation_status
        self.explanation = explanation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "match_type": self.match_type,
            "concept_term": self.concept_term,
            "sign_gloss": self.sign_gloss,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "signer_name": self.signer_name,
            "source_attribution": self.source_attribution,
            "license": self.license,
            "duration_seconds": self.duration_seconds,
            "resolution": self.resolution,
            "validation_status": self.validation_status,
            "explanation": self.explanation
        }

def retrieve_video_for_concept(concept_id: int, db: Session) -> VideoMatchResult:
    """
    Retrieves the authentic signing video asset for a single technical concept.
    """
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if not concept:
        return VideoMatchResult(
            match_type="NO_MATCH",
            concept_term="Unknown",
            sign_gloss="UNSUPPORTED",
            explanation="Concept does not exist in the registered knowledge base."
        )

    sign = db.query(SignRecord).filter(SignRecord.concept_id == concept.id).first()
    if not sign:
        return VideoMatchResult(
            match_type="NO_MATCH",
            concept_term=concept.term,
            sign_gloss=concept.term.upper(),
            explanation="No sign record registered for this concept."
        )

    # Check for direct video
    verified_video = None
    for vid in sign.videos:
        if vid.validation_status == ValidationStatus.VERIFIED or sign.validation_status == ValidationStatus.VERIFIED:
            verified_video = vid
            break

    if verified_video:
        return VideoMatchResult(
            match_type="EXACT_MATCH",
            concept_term=concept.term,
            sign_gloss=sign.sign_gloss,
            video_url=verified_video.video_path,
            thumbnail_url=verified_video.thumbnail_path,
            signer_name=verified_video.signer_name,
            source_attribution=verified_video.source_attribution,
            license=verified_video.license,
            duration_seconds=verified_video.duration_seconds,
            resolution=verified_video.resolution,
            validation_status=verified_video.validation_status.value,
            explanation=f"Direct sign video asset available for {concept.term}."
        )

    # If sign has video but status is NEEDS_REVIEW
    if sign.videos:
        candidate_video = sign.videos[0]
        return VideoMatchResult(
            match_type="CONTEXTUAL_MATCH",
            concept_term=concept.term,
            sign_gloss=sign.sign_gloss,
            video_url=candidate_video.video_path,
            thumbnail_url=candidate_video.thumbnail_path,
            signer_name=candidate_video.signer_name,
            source_attribution=candidate_video.source_attribution,
            license=candidate_video.license,
            duration_seconds=candidate_video.duration_seconds,
            resolution=candidate_video.resolution,
            validation_status=candidate_video.validation_status.value,
            explanation=f"Candidate video uploaded; currently under expert evaluation."
        )

    # No video on disk
    return VideoMatchResult(
        match_type="NO_MATCH",
        concept_term=concept.term,
        sign_gloss=sign.sign_gloss,
        validation_status=sign.validation_status.value,
        explanation=f"No verified signing video currently available for '{concept.term}'. Awaiting studio recording or deaf educator validation."
    )

def retrieve_videos_for_sentence_concepts(concept_ids: List[int], db: Session) -> Dict[str, Any]:
    """
    Retrieves matching videos for all concepts in a translated sentence.
    Does NOT concatenate them into a synthetic video; lists individual concept assets.
    """
    results = []
    has_exact = False
    has_missing = False

    for cid in concept_ids:
        match = retrieve_video_for_concept(cid, db)
        results.append(match.to_dict())
        if match.match_type == "EXACT_MATCH":
            has_exact = True
        else:
            has_missing = True

    if has_exact and not has_missing:
        overall_match = "EXACT_MATCH"
    elif has_exact and has_missing:
        overall_match = "PARTIAL_MATCH"
    else:
        overall_match = "NO_MATCH"

    return {
        "overall_match_type": overall_match,
        "policy_notice": "Individual concept videos are displayed in authentic isolated forms. Concatenating isolated signs into a sentence video is prohibited under the Zero Fabricated Signs Policy.",
        "continuous_sentence_video": {
            "available": False,
            "message": "Continuous sentence video stitching is prohibited under the Zero Fabricated Signs Policy to prevent ungrammatical synthetic signs."
        },
        "concept_matches": results
    }
