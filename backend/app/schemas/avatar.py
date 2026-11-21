"""
SignBridge AI - 3D Avatar & Motion Capture Schemas (Phase 4).
Defines standard typed Pydantic models for skeletal joint hierarchies,
finger joints, facial blendshapes, keyframe timelines, motion statuses,
and avatar API payloads under the Zero-Fabrication Policy.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MotionVerificationStatus(str, Enum):
    """
    Formal motion verification statuses adhering to the Zero-Fabrication Policy.
    """
    VERIFIED_ISL_MOTION = "VERIFIED_ISL_MOTION"
    PARTIALLY_VERIFIED_MOTION = "PARTIALLY_VERIFIED_MOTION"
    UNVERIFIED_MOTION = "UNVERIFIED_MOTION"
    DEMO_ONLY = "DEMO_ONLY"
    REQUIRES_LINGUISTIC_REVIEW = "REQUIRES_LINGUISTIC_REVIEW"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    SOURCE_RESTRICTED = "SOURCE_RESTRICTED"


class Vector3D(BaseModel):
    x: float = Field(..., description="X coordinate")
    y: float = Field(..., description="Y coordinate")
    z: float = Field(..., description="Z coordinate")


class Quaternion(BaseModel):
    x: float = Field(0.0, description="Quaternion X")
    y: float = Field(0.0, description="Quaternion Y")
    z: float = Field(0.0, description="Quaternion Z")
    w: float = Field(1.0, description="Quaternion W")


class EulerAngles(BaseModel):
    x: float = Field(0.0, description="Pitch (radians)")
    y: float = Field(0.0, description="Yaw (radians)")
    z: float = Field(0.0, description="Roll (radians)")


class JointLimit(BaseModel):
    min_x: float = Field(-3.14159, description="Minimum pitch in radians")
    max_x: float = Field(3.14159, description="Maximum pitch in radians")
    min_y: float = Field(-3.14159, description="Minimum yaw in radians")
    max_y: float = Field(3.14159, description="Maximum yaw in radians")
    min_z: float = Field(-3.14159, description="Minimum roll in radians")
    max_z: float = Field(3.14159, description="Maximum roll in radians")


class FingerJointState(BaseModel):
    mcp: EulerAngles = Field(default_factory=EulerAngles, description="Metacarpophalangeal / Knuckle joint rotation")
    pip: EulerAngles = Field(default_factory=EulerAngles, description="Proximal Interphalangeal joint rotation")
    dip: EulerAngles = Field(default_factory=EulerAngles, description="Distal Interphalangeal joint rotation")


class HandPoseState(BaseModel):
    wrist: EulerAngles = Field(default_factory=EulerAngles, description="Wrist rotation")
    thumb: FingerJointState = Field(default_factory=FingerJointState, description="Thumb (CMC, MCP, IP)")
    index: FingerJointState = Field(default_factory=FingerJointState, description="Index finger (MCP, PIP, DIP)")
    middle: FingerJointState = Field(default_factory=FingerJointState, description="Middle finger (MCP, PIP, DIP)")
    ring: FingerJointState = Field(default_factory=FingerJointState, description="Ring finger (MCP, PIP, DIP)")
    pinky: FingerJointState = Field(default_factory=FingerJointState, description="Pinky finger (MCP, PIP, DIP)")


class FacialBlendshapes(BaseModel):
    brow_furrow_left: float = Field(0.0, ge=0.0, le=1.0, description="Eyebrow furrow left (WH-question)")
    brow_furrow_right: float = Field(0.0, ge=0.0, le=1.0, description="Eyebrow furrow right (WH-question)")
    brow_raise_left: float = Field(0.0, ge=0.0, le=1.0, description="Eyebrow raise left (Polar question)")
    brow_raise_right: float = Field(0.0, ge=0.0, le=1.0, description="Eyebrow raise right (Polar question)")
    mouth_open: float = Field(0.0, ge=0.0, le=1.0, description="Mouth opening")
    mouth_wide: float = Field(0.0, ge=0.0, le=1.0, description="Mouth stretch / wide morpheme")
    eye_blink_left: float = Field(0.0, ge=0.0, le=1.0, description="Left eye blink")
    eye_blink_right: float = Field(0.0, ge=0.0, le=1.0, description="Right eye blink")
    head_pitch: float = Field(0.0, description="Head nod forward/back")
    head_yaw: float = Field(0.0, description="Head turn left/right")
    head_roll: float = Field(0.0, description="Head tilt left/right")


class AvatarKeyframe(BaseModel):
    timestamp_ms: int = Field(..., ge=0, description="Time offset in milliseconds from track start")
    chest_rotation: EulerAngles = Field(default_factory=EulerAngles)
    neck_rotation: EulerAngles = Field(default_factory=EulerAngles)
    head_rotation: EulerAngles = Field(default_factory=EulerAngles)
    left_shoulder_rotation: EulerAngles = Field(default_factory=EulerAngles)
    left_arm_rotation: EulerAngles = Field(default_factory=EulerAngles)
    left_forearm_rotation: EulerAngles = Field(default_factory=EulerAngles)
    left_hand: HandPoseState = Field(default_factory=HandPoseState)
    right_shoulder_rotation: EulerAngles = Field(default_factory=EulerAngles)
    right_arm_rotation: EulerAngles = Field(default_factory=EulerAngles)
    right_forearm_rotation: EulerAngles = Field(default_factory=EulerAngles)
    right_hand: HandPoseState = Field(default_factory=HandPoseState)
    facial_blendshapes: FacialBlendshapes = Field(default_factory=FacialBlendshapes)


class AnimationTrackType(str, Enum):
    LEXICAL_SIGN = "LEXICAL_SIGN"
    PEDAGOGICAL_EXPLANATION = "PEDAGOGICAL_EXPLANATION"
    FINGERSPELLING = "FINGERSPELLING"
    REST_POSE = "REST_POSE"
    TRANSITION = "TRANSITION"


class AvatarAnimationTrack(BaseModel):
    track_id: str
    track_type: AnimationTrackType
    gloss_token: str
    concept_term: Optional[str] = None
    start_time_seconds: float
    duration_seconds: float
    verification_status: MotionVerificationStatus
    is_mocap: bool = True
    keyframes: List[AvatarKeyframe] = Field(default_factory=list)
    linguistic_disclaimer: Optional[str] = None


class AvatarSequencePayload(BaseModel):
    sentence_text: str
    overall_motion_status: MotionVerificationStatus
    tracks: List[AvatarAnimationTrack] = Field(default_factory=list)
    total_duration_seconds: float
    fps: int = 30
    rig_standard: str = "SignBridge-Articulated-54"
    policy_notice: str


class AvatarStatusResponse(BaseModel):
    avatar_name: str
    rig_standard: str
    total_joints_count: int
    finger_joints_count_per_hand: int
    supported_facial_morph_targets: List[str]
    motion_capture_pipeline_available: bool
    active_mocap_animations_count: int
    status_breakdown: Dict[str, int]
    zero_fabrication_policy_enforced: bool
    disclaimer: str

