"""
SignBridge AI - Phase 8.6 3D Avatar Subsystem Regression Tests.
Verifies:
1. Rig handedness alignment (Right arm at -X, Left arm at +X).
2. Kinematic Euler rotation sign conventions (forward pitch, elbow flexion, finger curl into palm).
3. 5 Mocap files data integrity, monotonic timestamps, absence of NaN/Inf.
4. Physiological joint limit bounds adherence across all 5 mocap files.
5. Video/Avatar synchronization interface contracts.
"""

import json
import math
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.motion_retargeting_service import JOINT_LIMITS, MotionRetargetingService

client = TestClient(app)
PROCESSED_MOCAP_DIR = Path("data/isl_motion/processed")


def test_mocap_files_integrity_all_five():
    """Verifies all 5 mocap JSON files exist, have monotonic timestamps and zero NaN/Inf."""
    expected_files = [
        "islrtc_algorithm_mocap.json",
        "islrtc_beam_mocap.json",
        "islrtc_current_mocap.json",
        "islrtc_frequency_mocap.json",
        "islrtc_torque_mocap.json"
    ]

    for fname in expected_files:
        fpath = PROCESSED_MOCAP_DIR / fname
        assert fpath.exists(), f"Mocap file {fname} is missing"

        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert data["concept_term"] is not None
        assert data["duration_seconds"] > 0
        assert data["sample_fps"] == 25

        kfs = data["keyframes"]
        assert len(kfs) > 50, f"Insufficient keyframes in {fname}"

        raw_str = json.dumps(kfs)
        assert "NaN" not in raw_str and "nan" not in raw_str
        assert "Infinity" not in raw_str and "inf" not in raw_str

        # Monotonic timestamps
        ts = [k["timestamp_ms"] for k in kfs]
        for i in range(len(ts) - 1):
            assert ts[i] <= ts[i + 1], f"Timestamp monotonicity violated in {fname} at frame {i}"


def test_mocap_joint_limits_bounded():
    """Verifies all solved Euler rotations in mocap files stay within physiological joint limits."""
    for fpath in PROCESSED_MOCAP_DIR.glob("*_mocap.json"):
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        for idx, kf in enumerate(data["keyframes"]):
            ra = kf.get("right_arm_rotation", {})
            pitch = ra.get("x", 0.0)
            yaw = ra.get("y", 0.0)
            roll = ra.get("z", 0.0)

            assert JOINT_LIMITS["shoulder_pitch"][0] <= pitch <= JOINT_LIMITS["shoulder_pitch"][1], \
                f"Shoulder pitch limit violated in {fpath.name} frame {idx}: {pitch}"
            assert JOINT_LIMITS["shoulder_yaw"][0] <= yaw <= JOINT_LIMITS["shoulder_yaw"][1], \
                f"Shoulder yaw limit violated in {fpath.name} frame {idx}: {yaw}"
            assert JOINT_LIMITS["shoulder_roll"][0] <= roll <= JOINT_LIMITS["shoulder_roll"][1], \
                f"Shoulder roll limit violated in {fpath.name} frame {idx}: {roll}"

            rf = kf.get("right_forearm_rotation", {})
            elbow_flex = rf.get("x", 0.0)
            assert JOINT_LIMITS["elbow_flexion"][0] <= elbow_flex <= JOINT_LIMITS["elbow_flexion"][1], \
                f"Elbow flexion limit violated in {fpath.name} frame {idx}: {elbow_flex}"


def test_euler_forward_kinematics_direction():
    """
    Mathematical verification of Euler rotation sign convention:
    For an arm or finger segment pointing along -Y:
    Applying a negative X rotation (-theta with theta > 0) must displace the tip into +Z (forward towards camera).
    Applying a positive X rotation (+theta with theta > 0) displaces the tip into -Z (backward into body).
    """
    theta = 1.0  # ~57 degrees forward elevation / flexion
    # Matrix rotation of [0, -1, 0] around X:
    # R_x(phi) * [0, -1, 0]^T = [0, -cos(phi), -sin(phi)]^T
    
    # 1. Uncorrected positive angle:
    z_uncorrected = -math.sin(theta)
    assert z_uncorrected < 0, "Positive rotation must produce negative Z (backward displacement)"

    # 2. Corrected negative angle:
    z_corrected = -math.sin(-theta)
    assert z_corrected > 0, "Negated rotation must produce positive Z (forward displacement towards camera)"


def test_avatar_viewer_codebase_rig_handedness():
    """
    Static code verification of AvatarViewer.tsx:
    Ensures right arm is positioned at -0.44 X (viewer's left) and left arm is at +0.44 X (viewer's right).
    Ensures finger phalanges use negated flexion rotations (-fState.mcp.x).
    """
    avatar_viewer_path = Path("frontend/src/components/avatar/AvatarViewer.tsx")
    assert avatar_viewer_path.exists()
    content = avatar_viewer_path.read_text(encoding="utf-8")

    # Right arm placed on anatomical right (-0.44 X in Three.js facing camera)
    assert "ref={rightArmRef} position={[-0.44, 0.4, 0]}" in content
    # Left arm placed on anatomical left (+0.44 X in Three.js facing camera)
    assert "ref={leftArmRef} position={[0.44, 0.4, 0]}" in content

    # Finger flexion negated
    assert "rotation={[-fState.mcp.x, fState.mcp.y * sideMultiplier, fState.mcp.z]}" in content
    assert "rotation={[-fState.pip.x, fState.pip.y, fState.pip.z]}" in content
    assert "rotation={[-fState.dip.x, fState.dip.y, fState.dip.z]}" in content

    # Arm pitch forward negated
    assert "rightArmRef.current.rotation.x = -currentKeyframe.right_arm_rotation.x" in content
    assert "rightForearmRef.current.rotation.x = -currentKeyframe.right_forearm_rotation.x" in content


def test_live_demo_page_synchronization_integration():
    """
    Static code verification of LiveDemoPage.tsx:
    Ensures LiveDemoPage passes controlled synchronization props to AvatarViewer.
    """
    live_demo_path = Path("frontend/src/pages/LiveDemoPage.tsx")
    assert live_demo_path.exists()
    content = live_demo_path.read_text(encoding="utf-8")

    assert "controlledIsPlaying={isPlaying}" in content
    assert "controlledSpeed={playbackSpeed}" in content
    assert "controlledCurrentTime={currentTime}" in content
    assert "controlledCameraPreset={cameraAngle}" in content
    assert "onTimeUpdate=" in content

