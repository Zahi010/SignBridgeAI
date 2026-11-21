"""
SignBridge AI - Phase 4.5 Avatar Accuracy Audit & Motion Fidelity Test Suite.
Validates:
- Motion data integrity across all 5 authentic ISLRTC mocap assets.
- Quantitative motion fidelity metrics (NMLE, DTW, Handshape curl, NMM).
- API endpoints: GET /api/v1/avatar/fidelity and GET /api/v1/avatar/fidelity/{concept_term}.
- Retargeting stress test limits: clamping, boundary conditions, zero-vector handling.
- Zero-Fabrication safeguard enforcement: strictly PARTIALLY_VERIFIED_MOTION until Deaf accredited review.
- Co-articulation boundary pauses and non-manual marker mappings.
"""

import math
import json
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.avatar import MotionVerificationStatus, AnimationTrackType
from backend.app.services.motion_fidelity_service import MotionFidelityService, compute_dtw_distance, euclidean_dist
from backend.app.services.motion_retargeting_service import MotionRetargetingService, JOINT_LIMITS, clamp
from backend.app.services.animation_library_service import AnimationLibraryService

client = TestClient(app)


# 1. Motion Data Integrity Test
def test_motion_data_integrity_audit():
    """Verify all 5 authentic ISLRTC mocap JSON files have 100% data integrity."""
    mocap_dir = Path(__file__).resolve().parent.parent.parent / "data" / "isl_motion" / "processed"
    concepts = ["algorithm", "frequency", "current", "beam", "torque"]

    for term in concepts:
        mocap_file = mocap_dir / f"islrtc_{term}_mocap.json"
        assert mocap_file.exists(), f"Mocap file missing for {term}"

        with open(mocap_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "keyframes" in data
        keyframes = data["keyframes"]
        assert len(keyframes) > 40, f"Insufficient keyframes for {term}"

        # Monotonic timestamps & no NaNs
        last_t = -1.0
        for kf in keyframes:
            t = kf["timestamp_ms"]
            assert t > last_t, f"Non-monotonic timestamp in {term}: {t} <= {last_t}"
            last_t = t

            # Verify arm rotation floats are finite
            r_arm = kf.get("right_arm_rotation", {})
            for axis in ["x", "y", "z"]:
                val = r_arm.get(axis, 0.0)
                assert not math.isnan(val) and not math.isinf(val), f"NaN/Inf in {term} right_arm"

            # Verify hand phalanges
            rh = kf.get("right_hand", {})
            assert "thumb" in rh and "index" in rh and "middle" in rh and "ring" in rh and "pinky" in rh


# 2. Fidelity Overview API Endpoint Test
def test_avatar_fidelity_overview_endpoint():
    """Verify GET /api/v1/avatar/fidelity returns aggregate metrics across all 5 concepts."""
    res = client.get("/api/v1/avatar/fidelity")
    assert res.status_code == 200
    concepts_list = res.json()

    assert isinstance(concepts_list, list)
    assert len(concepts_list) == 5

    terms = [c["concept_term"] for c in concepts_list]
    assert "Algorithm" in terms
    assert "Frequency" in terms
    assert "Current" in terms
    assert "Beam" in terms
    assert "Torque" in terms

    # Check NMLE across all concepts (< 0.05 normalized units, i.e. <5% error)
    for c in concepts_list:
        assert c["normalized_mean_landmark_error"] < 0.05
        assert c["median_landmark_error"] < 0.05
        assert c["max_landmark_error"] < 0.10
        assert "per_body_part_error" in c
        assert "trajectory_smoothness_score" in c
        assert 0.0 <= c["trajectory_smoothness_score"] <= 1.0


# 3. Concept-Specific Fidelity Endpoint Test
def test_avatar_fidelity_concept_endpoint():
    """Verify GET /api/v1/avatar/fidelity/{concept_term} returns detailed metrics for valid and 404 for invalid."""
    # Test valid concept: Algorithm
    res = client.get("/api/v1/avatar/fidelity/Algorithm")
    assert res.status_code == 200
    data = res.json()

    assert data["concept_term"] == "Algorithm"
    assert data["total_keyframes"] > 50
    assert data["normalized_mean_landmark_error"] < 0.05
    assert data["max_landmark_error"] < 0.10
    assert "per_body_part_error" in data
    assert "head" in data["per_body_part_error"]
    assert "wrists" in data["per_body_part_error"]
    assert "fingers" in data["per_body_part_error"]
    assert "handshape_fidelity" in data
    dom_hand = data["handshape_fidelity"]["detected_dominant_handshape"]
    assert any(k in dom_hand for k in ["Handshape", "Pointing", "Fist", "Flat", "Open"])
    assert "limitations_disclaimer" in data

    # Test case insensitivity
    res_lower = client.get("/api/v1/avatar/fidelity/torque")
    assert res_lower.status_code == 200
    assert res_lower.json()["concept_term"].lower() == "torque"

    # Test 404 for non-existent concept
    res_404 = client.get("/api/v1/avatar/fidelity/NonExistentConcept99")
    assert res_404.status_code == 404


# 4. Mathematical DTW and Distance Unit Tests
def test_dtw_and_euclidean_distance_math():
    """Verify numerical behavior of DTW and Euclidean distance helpers."""
    p1 = {"x": 1.0, "y": 2.0, "z": 3.0}
    p2 = {"x": 4.0, "y": 6.0, "z": 3.0}
    # distance = sqrt(3^2 + 4^2 + 0) = 5.0
    assert math.isclose(euclidean_dist(p1, p2), 5.0, rel_tol=1e-5)

    # Identical series -> DTW distance is 0.0
    s1 = [0.1, 0.2, 0.3, 0.4, 0.5]
    assert compute_dtw_distance(s1, s1) == 0.0

    # Shifted series -> DTW distance > 0.0
    s2 = [0.2, 0.3, 0.4, 0.5, 0.6]
    assert compute_dtw_distance(s1, s2) > 0.0

    # Empty series handling
    assert compute_dtw_distance([], s1) == 0.0


# 5. Retargeting Solver Stress Tests & Clamping Limits
def test_retargeting_solver_stress_and_clamping():
    """Stress test joint clamping limits, boundary conditions, and degenerate geometry."""
    retarget_svc = MotionRetargetingService()

    # Joint limit clamping checks
    assert clamp(-5.0, JOINT_LIMITS["elbow_flexion"][0], JOINT_LIMITS["elbow_flexion"][1]) == 0.0
    assert clamp(10.0, JOINT_LIMITS["elbow_flexion"][0], JOINT_LIMITS["elbow_flexion"][1]) == JOINT_LIMITS["elbow_flexion"][1]
    assert clamp(-10.0, JOINT_LIMITS["shoulder_pitch"][0], JOINT_LIMITS["shoulder_pitch"][1]) == JOINT_LIMITS["shoulder_pitch"][0]
    assert clamp(10.0, JOINT_LIMITS["shoulder_pitch"][0], JOINT_LIMITS["shoulder_pitch"][1]) == JOINT_LIMITS["shoulder_pitch"][1]

    # Hand phalange solver with empty landmarks returns relaxed neutral hand
    relaxed_left = retarget_svc._solve_hand_phalanges([], is_left=True)
    relaxed_right = retarget_svc._solve_hand_phalanges([], is_left=False)
    assert relaxed_left.index.mcp.x == 0.25
    assert relaxed_right.index.mcp.x == 0.25

    # Hand phalange solver with full 21 landmarks
    mock_hand_landmarks = [{"x": float(i) * 0.01, "y": float(i) * 0.01, "z": 0.0} for i in range(21)]
    solved_right = retarget_svc._solve_hand_phalanges(mock_hand_landmarks, is_left=False)
    assert solved_right.thumb.mcp is not None
    assert solved_right.index.pip is not None


# 6. Zero-Fabrication Safeguard Audit: Status Clamped at PARTIALLY_VERIFIED
def test_zero_fabrication_audit_status_invariance():
    """
    Zero-Fabrication Policy:
    Animations derived from ISLRTC video mocap MUST remain PARTIALLY_VERIFIED_MOTION
    and NEVER prematurely promoted to VERIFIED_ISL_MOTION without external accredited review.
    """
    res = client.get("/api/v1/avatar/animations")
    assert res.status_code == 200
    anims = res.json()["animations"]

    for a in anims:
        if a["is_mocap"]:
            assert a["motion_status"] == MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value, (
                f"Animation {a['animation_name']} improperly promoted to {a['motion_status']}"
            )
            # Must reference authentic sign_record_id
            assert a["sign_record_id"] is not None


# 7. Sequence Generation Co-Articulation Boundary Pauses
def test_coarticulation_boundary_pause_preservation():
    """Verify that multi-concept sequence synthesis introduces rest pauses between signs."""
    anim_lib = AnimationLibraryService()
    seq = anim_lib.assemble_sequence_from_translation_plan(
        source_text="Algorithm frequency",
        detected_concepts=[
            {"id": 5, "term": "Algorithm", "category": "DIRECT_LEXICAL"},
            {"id": 8, "term": "Frequency", "category": "DIRECT_LEXICAL"}
        ],
        grammar_plan={"sentence_type": "DECLARATIVE"}
    )

    # Expected track structure: Rest Pose -> Lexical Sign 1 -> Coarticulation Rest -> Lexical Sign 2 -> Rest Pose
    track_types = [t.track_type.value for t in seq.tracks]
    assert len(seq.tracks) >= 4
    assert track_types[0] == AnimationTrackType.REST_POSE.value
    assert track_types[1] == AnimationTrackType.LEXICAL_SIGN.value
    # Pauses between signs prevent phonemic corruption
    assert AnimationTrackType.REST_POSE.value in track_types[2:]
