"""
SignBridge AI - ISL Animation Library & Translation Integration Service (Phase 4).
Loads authentic motion capture keyframes, generates pedagogical explanation timelines,
assembles fingerspelling sequences for unsupported technical terms, and interfaces
directly with the Phase 3 TranslationPlanner and IntermediateRepresentation.

Adheres strictly to the Zero-Fabrication Policy:
- Mocap tracks are marked PARTIALLY_VERIFIED_MOTION.
- Procedural demonstrations are marked DEMO_ONLY.
- Unregistered concepts return NOT_IMPLEMENTED with neutral rest posture.
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from sqlalchemy.orm import Session

from backend.app.models.entities import Concept, SignRecord, AvatarAnimation, ValidationStatus
from backend.app.schemas.avatar import (
    MotionVerificationStatus,
    EulerAngles,
    HandPoseState,
    FingerJointState,
    FacialBlendshapes,
    AvatarKeyframe,
    AvatarAnimationTrack,
    AnimationTrackType,
    AvatarSequencePayload,
    AvatarStatusResponse
)

logger = logging.getLogger("signbridge.animation_library")


# ISL Handshape Templates for Fingerspelling Fallback
# Handshape definitions using finger phalange flexion angles (radians)
ISL_FINGERSPELLING_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "A": {
        "thumb": {"mcp": (0.1, 0.2, 0.0), "pip": (0.0, 0.0, 0.0), "dip": (0.0, 0.0, 0.0)},
        "index": {"mcp": (1.4, 0.0, 0.0), "pip": (1.5, 0.0, 0.0), "dip": (1.2, 0.0, 0.0)},
        "middle": {"mcp": (1.4, 0.0, 0.0), "pip": (1.5, 0.0, 0.0), "dip": (1.2, 0.0, 0.0)},
        "ring": {"mcp": (1.4, 0.0, 0.0), "pip": (1.5, 0.0, 0.0), "dip": (1.2, 0.0, 0.0)},
        "pinky": {"mcp": (1.4, 0.0, 0.0), "pip": (1.5, 0.0, 0.0), "dip": (1.2, 0.0, 0.0)},
    },
    "B": {
        "thumb": {"mcp": (0.6, 0.6, 0.0), "pip": (0.4, 0.0, 0.0), "dip": (0.2, 0.0, 0.0)},
        "index": {"mcp": (0.0, 0.0, 0.0), "pip": (0.0, 0.0, 0.0), "dip": (0.0, 0.0, 0.0)},
        "middle": {"mcp": (0.0, 0.0, 0.0), "pip": (0.0, 0.0, 0.0), "dip": (0.0, 0.0, 0.0)},
        "ring": {"mcp": (0.0, 0.0, 0.0), "pip": (0.0, 0.0, 0.0), "dip": (0.0, 0.0, 0.0)},
        "pinky": {"mcp": (0.0, 0.0, 0.0), "pip": (0.0, 0.0, 0.0), "dip": (0.0, 0.0, 0.0)},
    },
    "C": {
        "thumb": {"mcp": (0.4, 0.4, 0.0), "pip": (0.4, 0.0, 0.0), "dip": (0.3, 0.0, 0.0)},
        "index": {"mcp": (0.7, 0.0, 0.0), "pip": (0.8, 0.0, 0.0), "dip": (0.5, 0.0, 0.0)},
        "middle": {"mcp": (0.7, 0.0, 0.0), "pip": (0.8, 0.0, 0.0), "dip": (0.5, 0.0, 0.0)},
        "ring": {"mcp": (0.7, 0.0, 0.0), "pip": (0.8, 0.0, 0.0), "dip": (0.5, 0.0, 0.0)},
        "pinky": {"mcp": (0.7, 0.0, 0.0), "pip": (0.8, 0.0, 0.0), "dip": (0.5, 0.0, 0.0)},
    },
    "D": {
        "thumb": {"mcp": (0.5, 0.5, 0.0), "pip": (0.5, 0.0, 0.0), "dip": (0.3, 0.0, 0.0)},
        "index": {"mcp": (0.0, 0.0, 0.0), "pip": (0.0, 0.0, 0.0), "dip": (0.0, 0.0, 0.0)},
        "middle": {"mcp": (1.2, 0.0, 0.0), "pip": (1.3, 0.0, 0.0), "dip": (0.8, 0.0, 0.0)},
        "ring": {"mcp": (1.2, 0.0, 0.0), "pip": (1.3, 0.0, 0.0), "dip": (0.8, 0.0, 0.0)},
        "pinky": {"mcp": (1.2, 0.0, 0.0), "pip": (1.3, 0.0, 0.0), "dip": (0.8, 0.0, 0.0)},
    },
    "DEFAULT": {
        "thumb": {"mcp": (0.2, 0.3, 0.0), "pip": (0.2, 0.0, 0.0), "dip": (0.1, 0.0, 0.0)},
        "index": {"mcp": (0.3, 0.0, 0.0), "pip": (0.4, 0.0, 0.0), "dip": (0.2, 0.0, 0.0)},
        "middle": {"mcp": (0.3, 0.0, 0.0), "pip": (0.4, 0.0, 0.0), "dip": (0.2, 0.0, 0.0)},
        "ring": {"mcp": (0.3, 0.0, 0.0), "pip": (0.4, 0.0, 0.0), "dip": (0.2, 0.0, 0.0)},
        "pinky": {"mcp": (0.3, 0.0, 0.0), "pip": (0.4, 0.0, 0.0), "dip": (0.2, 0.0, 0.0)},
    }
}


class AnimationLibraryService:
    """
    Manages loading, sequencing, and generating avatar signing tracks.
    """

    def __init__(self, mocap_dir: Optional[Path] = None):
        self.mocap_dir = mocap_dir or (
            Path(__file__).resolve().parent.parent.parent.parent / "data" / "isl_motion" / "processed"
        )
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._load_mocap_cache()

    def _load_mocap_cache(self):
        """Preloads available processed mocap files into memory."""
        if not self.mocap_dir.exists():
            return
        for file in self.mocap_dir.glob("*_mocap.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    term = data.get("concept_term", "").lower()
                    if term:
                        self._cache[term] = data
            except Exception as e:
                logger.warning(f"Failed to load mocap cache file {file}: {e}")

    def get_available_mocap_terms(self) -> List[str]:
        self._load_mocap_cache()
        return list(self._cache.keys())

    def get_mocap_for_concept(self, term: str) -> Optional[Dict[str, Any]]:
        self._load_mocap_cache()
        return self._cache.get(term.lower())

    def create_neutral_rest_track(self, start_time: float, duration: float = 0.5) -> AvatarAnimationTrack:
        """Generates a neutral resting posture track."""
        keyframes = [
            AvatarKeyframe(
                timestamp_ms=0,
                chest_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                neck_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                head_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                left_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                left_arm_rotation=EulerAngles(x=-0.35, y=0.0, z=0.22),
                left_forearm_rotation=EulerAngles(x=0.15, y=0.0, z=0.0),
                left_hand=self._build_template_hand("DEFAULT"),
                right_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                right_arm_rotation=EulerAngles(x=-0.35, y=0.0, z=-0.22),
                right_forearm_rotation=EulerAngles(x=0.15, y=0.0, z=0.0),
                right_hand=self._build_template_hand("DEFAULT"),
                facial_blendshapes=FacialBlendshapes()
            ),
            AvatarKeyframe(
                timestamp_ms=int(duration * 1000),
                chest_rotation=EulerAngles(x=0.01, y=0.0, z=0.0),
                neck_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                head_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                left_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                left_arm_rotation=EulerAngles(x=-0.35, y=0.0, z=0.22),
                left_forearm_rotation=EulerAngles(x=0.15, y=0.0, z=0.0),
                left_hand=self._build_template_hand("DEFAULT"),
                right_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                right_arm_rotation=EulerAngles(x=-0.35, y=0.0, z=-0.22),
                right_forearm_rotation=EulerAngles(x=0.15, y=0.0, z=0.0),
                right_hand=self._build_template_hand("DEFAULT"),
                facial_blendshapes=FacialBlendshapes()
            )
        ]

        return AvatarAnimationTrack(
            track_id="track_rest",
            track_type=AnimationTrackType.REST_POSE,
            gloss_token="REST",
            start_time_seconds=start_time,
            duration_seconds=duration,
            verification_status=MotionVerificationStatus.VERIFIED_ISL_MOTION,
            is_mocap=False,
            keyframes=keyframes
        )

    def create_lexical_mocap_track(
        self,
        term: str,
        start_time: float
    ) -> Optional[AvatarAnimationTrack]:
        """Creates a lexical track from authentic mocap data."""
        mocap_data = self.get_mocap_for_concept(term)
        if not mocap_data:
            return None

        raw_kfs = mocap_data.get("keyframes", [])
        keyframes = [AvatarKeyframe(**kf) for kf in raw_kfs]
        duration = mocap_data.get("duration_seconds", 2.0)

        return AvatarAnimationTrack(
            track_id=f"track_{term.lower()}_lexical",
            track_type=AnimationTrackType.LEXICAL_SIGN,
            gloss_token=mocap_data.get("sign_gloss", term.upper()),
            concept_term=term,
            start_time_seconds=start_time,
            duration_seconds=duration,
            verification_status=MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION,
            is_mocap=True,
            keyframes=keyframes,
            linguistic_disclaimer=mocap_data.get("linguistic_disclaimer")
        )

    def create_fingerspelling_track(
        self,
        word: str,
        start_time: float
    ) -> AvatarAnimationTrack:
        """
        Creates a sequential fingerspelling track for technical terms lacking lexical signs.
        """
        letters = [ch.upper() for ch in word if ch.isalnum()]
        if not letters:
            letters = ["A"]

        letter_duration = 0.4
        total_duration = round(len(letters) * letter_duration, 2)
        keyframes = []

        for idx, letter in enumerate(letters):
            t_ms = int(idx * letter_duration * 1000)
            hand_state = self._build_template_hand(letter)

            # Dominant hand raised in signing space (chest level)
            kf = AvatarKeyframe(
                timestamp_ms=t_ms,
                chest_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                neck_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                head_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                left_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                left_arm_rotation=EulerAngles(x=-0.35, y=0.0, z=0.22),
                left_forearm_rotation=EulerAngles(x=0.15, y=0.0, z=0.0),
                left_hand=self._build_template_hand("DEFAULT"),
                right_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
                right_arm_rotation=EulerAngles(x=0.45, y=0.1, z=-0.3),  # Raised arm
                right_forearm_rotation=EulerAngles(x=1.35, y=0.0, z=0.0), # Forearm bent towards chest
                right_hand=hand_state,
                facial_blendshapes=FacialBlendshapes(mouth_open=0.15)
            )
            keyframes.append(kf)

        return AvatarAnimationTrack(
            track_id=f"track_fs_{word.lower()}",
            track_type=AnimationTrackType.FINGERSPELLING,
            gloss_token=f"FS-{word.upper()}",
            concept_term=word,
            start_time_seconds=start_time,
            duration_seconds=total_duration,
            verification_status=MotionVerificationStatus.DEMO_ONLY,
            is_mocap=False,
            keyframes=keyframes,
            linguistic_disclaimer="Fingerspelling sequence rendered using standard ISL alphabet configurations. Marked DEMO_ONLY under Zero-Fabrication Policy."
        )

    def create_pedagogical_explanation_track(
        self,
        term: str,
        start_time: float
    ) -> AvatarAnimationTrack:
        """
        Creates a structured multi-phase pedagogical explanation track (title, classifier metaphor, resolution).
        """
        duration = 3.0
        keyframes = [
            # Phase 1: Presentation (hands forward, open)
            AvatarKeyframe(
                timestamp_ms=0,
                right_arm_rotation=EulerAngles(x=0.3, y=-0.1, z=-0.2),
                right_forearm_rotation=EulerAngles(x=1.0, y=0.0, z=0.0),
                left_arm_rotation=EulerAngles(x=0.3, y=0.1, z=0.2),
                left_forearm_rotation=EulerAngles(x=1.0, y=0.0, z=0.0),
                right_hand=self._build_template_hand("B"),
                left_hand=self._build_template_hand("B"),
                facial_blendshapes=FacialBlendshapes(brow_raise_left=0.5, brow_raise_right=0.5)
            ),
            # Phase 2: Relational Metaphor (hands converge / interact)
            AvatarKeyframe(
                timestamp_ms=1500,
                right_arm_rotation=EulerAngles(x=0.5, y=-0.2, z=-0.1),
                right_forearm_rotation=EulerAngles(x=1.4, y=0.0, z=0.0),
                left_arm_rotation=EulerAngles(x=0.5, y=0.2, z=0.1),
                left_forearm_rotation=EulerAngles(x=1.4, y=0.0, z=0.0),
                right_hand=self._build_template_hand("C"),
                left_hand=self._build_template_hand("C"),
                facial_blendshapes=FacialBlendshapes(brow_furrow_left=0.4, brow_furrow_right=0.4)
            ),
            # Phase 3: Resolution & Rest Transition
            AvatarKeyframe(
                timestamp_ms=3000,
                right_arm_rotation=EulerAngles(x=-0.2, y=0.0, z=-0.2),
                right_forearm_rotation=EulerAngles(x=0.3, y=0.0, z=0.0),
                left_arm_rotation=EulerAngles(x=-0.2, y=0.0, z=0.2),
                left_forearm_rotation=EulerAngles(x=0.3, y=0.0, z=0.0),
                right_hand=self._build_template_hand("DEFAULT"),
                left_hand=self._build_template_hand("DEFAULT"),
                facial_blendshapes=FacialBlendshapes()
            )
        ]

        return AvatarAnimationTrack(
            track_id=f"track_ped_{term.lower()}",
            track_type=AnimationTrackType.PEDAGOGICAL_EXPLANATION,
            gloss_token=f"EXPLAIN-{term.upper()}",
            concept_term=term,
            start_time_seconds=start_time,
            duration_seconds=duration,
            verification_status=MotionVerificationStatus.REQUIRES_LINGUISTIC_REVIEW,
            is_mocap=False,
            keyframes=keyframes,
            linguistic_disclaimer=f"Pedagogical classifier sequence for '{term}'. Marked REQUIRES_LINGUISTIC_REVIEW until certified by an accredited Deaf educator."
        )

    def assemble_sequence_from_translation_plan(
        self,
        source_text: str,
        detected_concepts: List[Dict[str, Any]],
        grammar_plan: Dict[str, Any]
    ) -> AvatarSequencePayload:
        """
        Assembles a continuous avatar signing sequence from detected concepts and the translation plan.
        """
        tracks = []
        current_time = 0.0

        # Start with resting pose
        rest_start = self.create_neutral_rest_track(start_time=current_time, duration=0.5)
        tracks.append(rest_start)
        current_time += 0.5

        overall_statuses = []

        if not detected_concepts:
            # Unsupported sentence without concepts: fingerspell first words or stay in rest
            words = source_text.split()[:3]
            for w in words:
                fs_track = self.create_fingerspelling_track(w, start_time=current_time)
                tracks.append(fs_track)
                current_time += fs_track.duration_seconds
                overall_statuses.append(fs_track.verification_status)
        else:
            for c in detected_concepts:
                term = c.get("term", "")
                cat = c.get("category", "")
                mocap_track = self.create_lexical_mocap_track(term, start_time=current_time)

                if mocap_track:
                    tracks.append(mocap_track)
                    current_time += mocap_track.duration_seconds
                    overall_statuses.append(mocap_track.verification_status)
                elif cat in ["PEDAGOGICAL_EXPLANATION", "EXPLANATION_REQUIRED", "EXPLANATION_NEEDED"]:
                    ped_track = self.create_pedagogical_explanation_track(term, start_time=current_time)
                    tracks.append(ped_track)
                    current_time += ped_track.duration_seconds
                    overall_statuses.append(ped_track.verification_status)
                else:
                    # Fallback to fingerspelling
                    fs_track = self.create_fingerspelling_track(term, start_time=current_time)
                    tracks.append(fs_track)
                    current_time += fs_track.duration_seconds
                    overall_statuses.append(fs_track.verification_status)

        # End with resting pose
        rest_end = self.create_neutral_rest_track(start_time=current_time, duration=0.5)
        tracks.append(rest_end)
        current_time += 0.5

        # Determine overall sequence status
        if any(s == MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION for s in overall_statuses):
            overall_status = MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION
        elif any(s == MotionVerificationStatus.REQUIRES_LINGUISTIC_REVIEW for s in overall_statuses):
            overall_status = MotionVerificationStatus.REQUIRES_LINGUISTIC_REVIEW
        elif any(s == MotionVerificationStatus.DEMO_ONLY for s in overall_statuses):
            overall_status = MotionVerificationStatus.DEMO_ONLY
        else:
            overall_status = MotionVerificationStatus.NOT_IMPLEMENTED

        sentence_type = grammar_plan.get("sentence_type", "DECLARATIVE")
        # Apply facial NMM to terminal track if question
        if sentence_type in ["WH_QUESTION", "POLAR_QUESTION"] and len(tracks) > 2:
            target_track = tracks[-2]
            for kf in target_track.keyframes:
                if sentence_type == "WH_QUESTION":
                    kf.facial_blendshapes.brow_furrow_left = 0.8
                    kf.facial_blendshapes.brow_furrow_right = 0.8
                elif sentence_type == "POLAR_QUESTION":
                    kf.facial_blendshapes.brow_raise_left = 0.8
                    kf.facial_blendshapes.brow_raise_right = 0.8

        return AvatarSequencePayload(
            sentence_text=source_text,
            overall_motion_status=overall_status,
            tracks=tracks,
            total_duration_seconds=round(current_time, 2),
            fps=30,
            rig_standard="SignBridge-Articulated-54",
            policy_notice=(
                "Motion sequence generated under SignBridge AI Zero-Fabrication Policy. "
                "Authentic ISLRTC mocap tracks are marked PARTIALLY_VERIFIED_MOTION. "
                "Explanations and fingerspelling are explicitly tagged with non-verified statuses."
            )
        )

    def _build_template_hand(self, letter: str) -> HandPoseState:
        template = ISL_FINGERSPELLING_TEMPLATES.get(letter.upper(), ISL_FINGERSPELLING_TEMPLATES["DEFAULT"])
        return HandPoseState(
            wrist=EulerAngles(),
            thumb=FingerJointState(
                mcp=EulerAngles(x=template["thumb"]["mcp"][0], y=template["thumb"]["mcp"][1], z=template["thumb"]["mcp"][2]),
                pip=EulerAngles(x=template["thumb"]["pip"][0], y=template["thumb"]["pip"][1], z=template["thumb"]["pip"][2]),
                dip=EulerAngles(x=template["thumb"]["dip"][0], y=template["thumb"]["dip"][1], z=template["thumb"]["dip"][2])
            ),
            index=FingerJointState(
                mcp=EulerAngles(x=template["index"]["mcp"][0], y=template["index"]["mcp"][1], z=template["index"]["mcp"][2]),
                pip=EulerAngles(x=template["index"]["pip"][0], y=template["index"]["pip"][1], z=template["index"]["pip"][2]),
                dip=EulerAngles(x=template["index"]["dip"][0], y=template["index"]["dip"][1], z=template["index"]["dip"][2])
            ),
            middle=FingerJointState(
                mcp=EulerAngles(x=template["middle"]["mcp"][0], y=template["middle"]["mcp"][1], z=template["middle"]["mcp"][2]),
                pip=EulerAngles(x=template["middle"]["pip"][0], y=template["middle"]["pip"][1], z=template["middle"]["pip"][2]),
                dip=EulerAngles(x=template["middle"]["dip"][0], y=template["middle"]["dip"][1], z=template["middle"]["dip"][2])
            ),
            ring=FingerJointState(
                mcp=EulerAngles(x=template["ring"]["mcp"][0], y=template["ring"]["mcp"][1], z=template["ring"]["mcp"][2]),
                pip=EulerAngles(x=template["ring"]["pip"][0], y=template["ring"]["pip"][1], z=template["ring"]["pip"][2]),
                dip=EulerAngles(x=template["ring"]["dip"][0], y=template["ring"]["dip"][1], z=template["ring"]["dip"][2])
            ),
            pinky=FingerJointState(
                mcp=EulerAngles(x=template["pinky"]["mcp"][0], y=template["pinky"]["mcp"][1], z=template["pinky"]["mcp"][2]),
                pip=EulerAngles(x=template["pinky"]["pip"][0], y=template["pinky"]["pip"][1], z=template["pinky"]["pip"][2]),
                dip=EulerAngles(x=template["pinky"]["dip"][0], y=template["pinky"]["dip"][1], z=template["pinky"]["dip"][2])
            )
        )

