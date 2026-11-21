"""
SignBridge AI - Motion Retargeting Service (Phase 4).
Converts normalized 3D landmarks into skeletal bone rotations (Euler angles / Quaternions)
for the SignBridge-Articulated-54 rig, with physiological joint limit clamping,
finger phalange kinematics, and Non-Manual Marker blendshape calculation.
"""

import math
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from backend.app.schemas.avatar import (
    MotionVerificationStatus,
    EulerAngles,
    HandPoseState,
    FingerJointState,
    FacialBlendshapes,
    AvatarKeyframe,
    AvatarAnimationTrack,
    AnimationTrackType
)


# Anatomical rotation limits (min_rad, max_rad) for stability
JOINT_LIMITS = {
    "shoulder_pitch": (-1.57, 2.35),
    "shoulder_yaw": (-1.57, 1.57),
    "shoulder_roll": (-1.75, 1.75),
    "elbow_flexion": (0.0, 2.62),
    "wrist_pitch": (-1.22, 1.22),
    "wrist_yaw": (-0.70, 0.70),
    "wrist_roll": (-1.57, 1.57),
    "finger_mcp_flexion": (0.0, 1.60),
    "finger_pip_flexion": (0.0, 1.80),
    "finger_dip_flexion": (0.0, 1.30),
    "thumb_cmc_abduction": (0.0, 0.85),
    "thumb_mcp_flexion": (0.0, 1.10),
    "thumb_ip_flexion": (0.0, 1.40),
}


def clamp(val: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(max_val, val))


def vector_sub(v1: Dict[str, float], v2: Dict[str, float]) -> Dict[str, float]:
    return {"x": v1["x"] - v2["x"], "y": v1["y"] - v2["y"], "z": v1["z"] - v2["z"]}


def vector_len(v: Dict[str, float]) -> float:
    return math.sqrt(v["x"] * v["x"] + v["y"] * v["y"] + v["z"] * v["z"]) or 1e-6


def vector_norm(v: Dict[str, float]) -> Dict[str, float]:
    length = vector_len(v)
    return {"x": v["x"] / length, "y": v["y"] / length, "z": v["z"] / length}


def angle_between_vectors(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    """Computes the unsigned angle in radians between two 3D vectors."""
    n1 = vector_norm(v1)
    n2 = vector_norm(v2)
    dot = n1["x"] * n2["x"] + n1["y"] * n2["y"] + n1["z"] * n2["z"]
    dot = max(-1.0, min(1.0, dot))
    return math.acos(dot)


class MotionRetargetingService:
    """
    Solves kinematics from 3D point cloud landmarks to avatar bone Euler rotations.
    """

    def retarget_frames_to_keyframes(
        self,
        frames_data: List[Dict[str, Any]]
    ) -> List[AvatarKeyframe]:
        """
        Processes normalized landmark frames into avatar skeletal keyframes.
        """
        keyframes = []
        for f in frames_data:
            kf = self._retarget_single_frame(f)
            keyframes.append(kf)
        return keyframes

    def _retarget_single_frame(self, frame_entry: Dict[str, Any]) -> AvatarKeyframe:
        timestamp_ms = frame_entry.get("timestamp_ms", 0)
        pose_lms = frame_entry.get("pose", [])
        left_hand_lms = frame_entry.get("left_hand", [])
        right_hand_lms = frame_entry.get("right_hand", [])
        facial_nmm = frame_entry.get("facial_nmm", {})

        # Default neutral poses
        left_arm_rot = EulerAngles(x=-0.35, y=0.0, z=0.22)
        left_forearm_rot = EulerAngles(x=0.0, y=0.0, z=0.0)
        right_arm_rot = EulerAngles(x=-0.35, y=0.0, z=-0.22)
        right_forearm_rot = EulerAngles(x=0.0, y=0.0, z=0.0)

        chest_rot = EulerAngles(x=0.0, y=0.0, z=0.0)
        neck_rot = EulerAngles(x=0.0, y=0.0, z=0.0)
        head_rot = EulerAngles(
            x=facial_nmm.get("head_pitch", 0.0),
            y=facial_nmm.get("head_yaw", 0.0),
            z=facial_nmm.get("head_roll", 0.0)
        )

        # Pose landmarks mapping:
        # 11: L Shoulder, 12: R Shoulder, 13: L Elbow, 14: R Elbow, 15: L Wrist, 16: R Wrist
        if len(pose_lms) >= 17:
            ls = pose_lms[11]
            rs = pose_lms[12]
            le = pose_lms[13]
            re = pose_lms[14]
            lw = pose_lms[15]
            rw = pose_lms[16]

            # Solve Right Arm (Dominant hand in most ISL signs)
            r_upper = vector_sub(re, rs)
            r_fore = vector_sub(rw, re)
            right_arm_rot, right_forearm_rot = self._solve_arm_kinematics(r_upper, r_fore, is_left=False)

            # Solve Left Arm
            l_upper = vector_sub(le, ls)
            l_fore = vector_sub(lw, le)
            left_arm_rot, left_forearm_rot = self._solve_arm_kinematics(l_upper, l_fore, is_left=True)

        # Solve Left Hand Finger Joints
        left_hand_pose = self._solve_hand_phalanges(left_hand_lms, is_left=True)

        # Solve Right Hand Finger Joints
        right_hand_pose = self._solve_hand_phalanges(right_hand_lms, is_left=False)

        # Build blendshapes
        blendshapes = FacialBlendshapes(
            brow_furrow_left=facial_nmm.get("brow_furrow_left", 0.0),
            brow_furrow_right=facial_nmm.get("brow_furrow_right", 0.0),
            brow_raise_left=facial_nmm.get("brow_raise_left", 0.0),
            brow_raise_right=facial_nmm.get("brow_raise_right", 0.0),
            mouth_open=facial_nmm.get("mouth_open", 0.0),
            mouth_wide=facial_nmm.get("mouth_wide", 0.0),
            eye_blink_left=0.0,
            eye_blink_right=0.0,
            head_pitch=head_rot.x,
            head_yaw=head_rot.y,
            head_roll=head_rot.z
        )

        return AvatarKeyframe(
            timestamp_ms=timestamp_ms,
            chest_rotation=chest_rot,
            neck_rotation=neck_rot,
            head_rotation=head_rot,
            left_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
            left_arm_rotation=left_arm_rot,
            left_forearm_rotation=left_forearm_rot,
            left_hand=left_hand_pose,
            right_shoulder_rotation=EulerAngles(x=0.0, y=0.0, z=0.0),
            right_arm_rotation=right_arm_rot,
            right_forearm_rotation=right_forearm_rot,
            right_hand=right_hand_pose,
            facial_blendshapes=blendshapes
        )

    def _solve_arm_kinematics(
        self,
        upper_vec: Dict[str, float],
        fore_vec: Dict[str, float],
        is_left: bool
    ) -> Tuple[EulerAngles, EulerAngles]:
        """
        Solves shoulder Euler angles and elbow flexion with limit clamping.
        """
        nu = vector_norm(upper_vec)

        # Upper arm pitch (forward/back), yaw (in/out), roll
        # In neutral: arm points down (0, -1, 0)
        pitch = math.atan2(nu["z"], -nu["y"])  # Forward/back elevation
        yaw = math.atan2(nu["x"], -nu["y"])    # Abduction / lateral spread
        roll = 0.0

        pitch = clamp(pitch, JOINT_LIMITS["shoulder_pitch"][0], JOINT_LIMITS["shoulder_pitch"][1])
        yaw = clamp(yaw, JOINT_LIMITS["shoulder_yaw"][0], JOINT_LIMITS["shoulder_yaw"][1])

        arm_rot = EulerAngles(x=round(pitch, 3), y=round(yaw, 3), z=round(roll, 3))

        # Elbow flexion: angle between upper arm and forearm vectors
        elbow_angle = angle_between_vectors(upper_vec, fore_vec)
        elbow_flexion = clamp(elbow_angle, JOINT_LIMITS["elbow_flexion"][0], JOINT_LIMITS["elbow_flexion"][1])

        # Elbow bends primarily around local X axis
        forearm_rot = EulerAngles(x=round(elbow_flexion, 3), y=0.0, z=0.0)

        return arm_rot, forearm_rot

    def _solve_hand_phalanges(
        self,
        hand_lms: List[Dict[str, float]],
        is_left: bool
    ) -> HandPoseState:
        """
        Solves 15 individual finger phalange joint angles from 21 MediaPipe hand landmarks.
        0: Wrist
        Thumb:  1: CMC, 2: MCP, 3: IP, 4: TIP
        Index:  5: MCP, 6: PIP, 7: DIP, 8: TIP
        Middle: 9: MCP, 10: PIP, 11: DIP, 12: TIP
        Ring:   13: MCP, 14: PIP, 15: DIP, 16: TIP
        Pinky:  17: MCP, 18: PIP, 19: DIP, 20: TIP
        """
        # If no hand detected, return relaxed resting handshape
        if not hand_lms or len(hand_lms) < 21:
            relaxed_finger = FingerJointState(
                mcp=EulerAngles(x=0.25, y=0.0, z=0.0),
                pip=EulerAngles(x=0.35, y=0.0, z=0.0),
                dip=EulerAngles(x=0.20, y=0.0, z=0.0)
            )
            return HandPoseState(
                wrist=EulerAngles(x=0.0, y=0.0, z=0.0),
                thumb=FingerJointState(
                    mcp=EulerAngles(x=0.2, y=0.3, z=0.0),
                    pip=EulerAngles(x=0.2, y=0.0, z=0.0),
                    dip=EulerAngles(x=0.1, y=0.0, z=0.0)
                ),
                index=relaxed_finger,
                middle=relaxed_finger,
                ring=relaxed_finger,
                pinky=relaxed_finger
            )

        w = hand_lms[0]

        def get_finger_state(base_idx: int) -> FingerJointState:
            mcp_pt = hand_lms[base_idx]
            pip_pt = hand_lms[base_idx + 1]
            dip_pt = hand_lms[base_idx + 2]
            tip_pt = hand_lms[base_idx + 3]

            v_palm_to_mcp = vector_sub(mcp_pt, w)
            v_mcp_to_pip = vector_sub(pip_pt, mcp_pt)
            v_pip_to_dip = vector_sub(dip_pt, pip_pt)
            v_dip_to_tip = vector_sub(tip_pt, dip_pt)

            mcp_angle = angle_between_vectors(v_palm_to_mcp, v_mcp_to_pip)
            pip_angle = angle_between_vectors(v_mcp_to_pip, v_pip_to_dip)
            dip_angle = angle_between_vectors(v_pip_to_dip, v_dip_to_tip)

            mcp_clamped = clamp(mcp_angle, JOINT_LIMITS["finger_mcp_flexion"][0], JOINT_LIMITS["finger_mcp_flexion"][1])
            pip_clamped = clamp(pip_angle, JOINT_LIMITS["finger_pip_flexion"][0], JOINT_LIMITS["finger_pip_flexion"][1])
            dip_clamped = clamp(dip_angle, JOINT_LIMITS["finger_dip_flexion"][0], JOINT_LIMITS["finger_dip_flexion"][1])

            return FingerJointState(
                mcp=EulerAngles(x=round(mcp_clamped, 3), y=0.0, z=0.0),
                pip=EulerAngles(x=round(pip_clamped, 3), y=0.0, z=0.0),
                dip=EulerAngles(x=round(dip_clamped, 3), y=0.0, z=0.0)
            )

        # Thumb calculation
        cmc = hand_lms[1]
        mcp = hand_lms[2]
        ip = hand_lms[3]
        tip = hand_lms[4]

        v_w_cmc = vector_sub(cmc, w)
        v_cmc_mcp = vector_sub(mcp, cmc)
        v_mcp_ip = vector_sub(ip, mcp)
        v_ip_tip = vector_sub(tip, ip)

        thumb_abd = clamp(angle_between_vectors(v_w_cmc, v_cmc_mcp), 0.0, 0.85)
        thumb_mcp = clamp(angle_between_vectors(v_cmc_mcp, v_mcp_ip), 0.0, 1.10)
        thumb_ip = clamp(angle_between_vectors(v_mcp_ip, v_ip_tip), 0.0, 1.40)

        thumb_state = FingerJointState(
            mcp=EulerAngles(x=round(thumb_abd, 3), y=round(0.3 if not is_left else -0.3, 3), z=0.0),
            pip=EulerAngles(x=round(thumb_mcp, 3), y=0.0, z=0.0),
            dip=EulerAngles(x=round(thumb_ip, 3), y=0.0, z=0.0)
        )

        return HandPoseState(
            wrist=EulerAngles(x=0.0, y=0.0, z=0.0),
            thumb=thumb_state,
            index=get_finger_state(5),
            middle=get_finger_state(9),
            ring=get_finger_state(13),
            pinky=get_finger_state(17)
        )

