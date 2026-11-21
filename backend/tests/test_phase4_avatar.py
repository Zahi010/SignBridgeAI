"""
SignBridge AI - Phase 4 Avatar, Motion Capture & Retargeting Test Suite.
Validates:
- 54-joint rig hierarchy and 15 finger phalanges per hand.
- Anatomical joint limit clamping (shoulder, elbow, wrist, fingers).
- Motion capture pipeline, smoothing, and coordinate normalization.
- Retargeting engine converting 3D landmarks to Euler rotations.
- Animation library integration (lexical mocap, pedagogical explanations, fingerspelling).
- Zero-Fabrication safeguard enforcement across all avatar endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

from backend.app.main import app
from backend.app.schemas.avatar import (
    MotionVerificationStatus,
    AnimationTrackType,
    EulerAngles
)
from backend.app.services.motion_capture_service import MotionCaptureService, OneEuroFilter
from backend.app.services.motion_retargeting_service import MotionRetargetingService, JOINT_LIMITS, clamp
from backend.app.services.animation_library_service import AnimationLibraryService

client = TestClient(app)


# 1. API Status Endpoint Test
def test_avatar_subsystem_status():
    response = client.get("/api/v1/avatar/status")
    assert response.status_code == 200
    data = response.json()

    assert data["avatar_name"] == "SignBridge Signer-01"
    assert data["rig_standard"] == "SignBridge-Articulated-54"
    assert data["total_joints_count"] == 54
    assert data["finger_joints_count_per_hand"] == 15
    assert "brow_furrow_left" in data["supported_facial_morph_targets"]
    assert "brow_raise_left" in data["supported_facial_morph_targets"]
    assert "mouth_open" in data["supported_facial_morph_targets"]
    assert data["motion_capture_pipeline_available"] is True
    assert data["active_mocap_animations_count"] >= 5
    assert data["zero_fabrication_policy_enforced"] is True
    assert "Zero-Fabrication Policy" in data["disclaimer"]


# 2. Animations Listing Test
def test_avatar_animations_listing():
    response = client.get("/api/v1/avatar/animations")
    assert response.status_code == 200
    data = response.json()

    assert data["total_count"] >= 5
    anims = data["animations"]
    terms = [a["concept_term"] for a in anims]

    assert "Algorithm" in terms
    assert "Frequency" in terms
    assert "Current" in terms
    assert "Beam" in terms
    assert "Torque" in terms

    # Check status of mocap animations
    for a in anims:
        if a["is_mocap"]:
            assert a["motion_status"] in [
                MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value,
                MotionVerificationStatus.VERIFIED_ISL_MOTION.value
            ]


# 3. Animation Detail & Keyframes Test
def test_avatar_animation_detail_mocap():
    # Fetch animations list to find Algorithm animation ID
    list_res = client.get("/api/v1/avatar/animations")
    anims = list_res.json()["animations"]
    algo_anim = next(a for a in anims if a["concept_term"] == "Algorithm")

    detail_res = client.get(f"/api/v1/avatar/animations/{algo_anim['id']}")
    assert detail_res.status_code == 200
    data = detail_res.json()

    assert data["concept_term"] == "Algorithm"
    assert data["sign_gloss"] in ["ALGORITHM", "STEP-BY-STEP RULE [COMPOUND]"]
    assert data["is_mocap"] is True
    assert data["keyframes_count"] > 50
    assert data["duration_seconds"] > 2.0
    assert len(data["keyframes"]) == data["keyframes_count"]

    # Verify keyframe structure
    kf0 = data["keyframes"][0]
    assert "timestamp_ms" in kf0
    assert "right_arm_rotation" in kf0
    assert "right_hand" in kf0
    assert "thumb" in kf0["right_hand"]
    assert "index" in kf0["right_hand"]


# 4. Concept Animation Retrieval Test
def test_avatar_animation_by_concept():
    # Concept 5 is Algorithm
    res = client.get("/api/v1/avatar/animations/concept/5")
    assert res.status_code == 200
    data = res.json()

    assert data["available"] is True
    assert data["concept_term"] == "Algorithm"
    assert data["motion_status"] == MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value
    assert data["is_mocap"] is True
    assert "phonological_parameters" in data


# 5. Unsupported Concept Zero-Fabrication Test
def test_avatar_animation_unsupported_concept():
    # Query non-existent concept
    res_404 = client.get("/api/v1/avatar/animations/concept/99999")
    assert res_404.status_code == 200
    assert res_404.json()["available"] is False

    # Query concept without verified mocap (e.g., Concept 2: Deadlock)
    res = client.get("/api/v1/avatar/animations/concept/2")
    assert res.status_code == 200
    data = res.json()

    assert data["available"] is False
    assert data["motion_status"] == MotionVerificationStatus.NOT_IMPLEMENTED.value
    assert "Zero-Fabrication Policy" in data["message"]


# 6. Sequence Generation with Lexical Mocap
def test_avatar_sequence_generation_lexical():
    payload = {
        "source_text": "Algorithm computes frequency",
        "detected_concepts": [
            {"id": 5, "term": "Algorithm", "category": "DIRECT_LEXICAL"}
        ],
        "grammar_plan": {"sentence_type": "DECLARATIVE"}
    }
    res = client.post("/api/v1/avatar/sequence", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["sentence_text"] == payload["source_text"]
    assert data["overall_motion_status"] == MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value
    assert len(data["tracks"]) >= 3  # Rest, Lexical, Rest

    # Check track types
    track_types = [t["track_type"] for t in data["tracks"]]
    assert AnimationTrackType.REST_POSE.value in track_types
    assert AnimationTrackType.LEXICAL_SIGN.value in track_types


# 7. Sequence Generation for Pedagogical Explanation
def test_avatar_sequence_generation_pedagogical():
    payload = {
        "source_text": "Deadlock prevents resource allocation",
        "detected_concepts": [
            {"id": 2, "term": "Deadlock", "category": "PEDAGOGICAL_EXPLANATION"}
        ],
        "grammar_plan": {"sentence_type": "DECLARATIVE"}
    }
    res = client.post("/api/v1/avatar/sequence", json=payload)
    assert res.status_code == 200
    data = res.json()

    track_types = [t["track_type"] for t in data["tracks"]]
    assert AnimationTrackType.PEDAGOGICAL_EXPLANATION.value in track_types

    ped_track = next(t for t in data["tracks"] if t["track_type"] == AnimationTrackType.PEDAGOGICAL_EXPLANATION.value)
    assert ped_track["verification_status"] == MotionVerificationStatus.REQUIRES_LINGUISTIC_REVIEW.value
    assert "Deadlock" in ped_track["concept_term"]


# 8. Sequence Generation for Unsupported Fingerspelling
def test_avatar_sequence_generation_fingerspelling():
    payload = {
        "source_text": "Quantum entanglement occurs",
        "detected_concepts": [],
        "grammar_plan": {"sentence_type": "DECLARATIVE"}
    }
    res = client.post("/api/v1/avatar/sequence", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["overall_motion_status"] == MotionVerificationStatus.DEMO_ONLY.value
    track_types = [t["track_type"] for t in data["tracks"]]
    assert AnimationTrackType.FINGERSPELLING.value in track_types


# 9. Facial Non-Manual Markers for Questions
def test_avatar_facial_nmm_questions():
    anim_lib = AnimationLibraryService()

    # WH-Question: should trigger brow furrow
    wh_seq = anim_lib.assemble_sequence_from_translation_plan(
        source_text="What is algorithm?",
        detected_concepts=[{"id": 5, "term": "Algorithm", "category": "DIRECT_LEXICAL"}],
        grammar_plan={"sentence_type": "WH_QUESTION"}
    )
    lexical_track = wh_seq.tracks[1]
    assert lexical_track.keyframes[0].facial_blendshapes.brow_furrow_left > 0.5

    # Polar Question: should trigger brow raise
    polar_seq = anim_lib.assemble_sequence_from_translation_plan(
        source_text="Is current flowing?",
        detected_concepts=[{"id": 10, "term": "Current", "category": "DIRECT_LEXICAL"}],
        grammar_plan={"sentence_type": "POLAR_QUESTION"}
    )
    lexical_track_polar = polar_seq.tracks[1]
    assert lexical_track_polar.keyframes[0].facial_blendshapes.brow_raise_left > 0.5


# 10. Motion Retargeting Anatomical Limit Clamping
def test_retargeting_anatomical_limit_clamping():
    retarget_svc = MotionRetargetingService()

    # Test extreme out-of-bounds angles
    assert clamp(5.0, JOINT_LIMITS["elbow_flexion"][0], JOINT_LIMITS["elbow_flexion"][1]) == JOINT_LIMITS["elbow_flexion"][1]
    assert clamp(-2.0, JOINT_LIMITS["elbow_flexion"][0], JOINT_LIMITS["elbow_flexion"][1]) == JOINT_LIMITS["elbow_flexion"][0]
    assert clamp(10.0, JOINT_LIMITS["shoulder_pitch"][0], JOINT_LIMITS["shoulder_pitch"][1]) == JOINT_LIMITS["shoulder_pitch"][1]


# 11. Hand Phalange Solver 15 Joints
def test_hand_phalange_solver_15_joints():
    retarget_svc = MotionRetargetingService()

    # Pass empty landmarks -> returns relaxed neutral handshape
    hand_pose = retarget_svc._solve_hand_phalanges([], is_left=False)

    for finger_name in ["thumb", "index", "middle", "ring", "pinky"]:
        finger = getattr(hand_pose, finger_name)
        assert finger.mcp is not None
        assert finger.pip is not None
        assert finger.dip is not None


# 12. On-The-Fly Retarget Endpoint Test
def test_retarget_endpoint():
    frame = {
        "timestamp_ms": 0,
        "pose": [{"x": 0.0, "y": 0.0, "z": 0.0} for _ in range(33)],
        "left_hand": [{"x": 0.0, "y": 0.0, "z": 0.0} for _ in range(21)],
        "right_hand": [{"x": 0.0, "y": 0.0, "z": 0.0} for _ in range(21)],
        "facial_nmm": {"brow_furrow_left": 0.5}
    }
    payload = {"frames": [frame]}

    res = client.post("/api/v1/avatar/retarget", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["status"] == "success"
    assert data["retargeted_keyframes_count"] == 1
    assert "right_hand" in data["keyframes"][0]


# 13. One-Euro Filter Smoothing Test
def test_one_euro_filter_smoothing():
    f = OneEuroFilter(t0=0.0, x0=0.0)
    val1 = f.filter(t=0.04, x=1.0)
    val2 = f.filter(t=0.08, x=1.0)

    # Filter should smoothly ramp up rather than jump instantaneously
    assert 0.0 < val1 < 1.0
    assert val1 < val2 <= 1.0
