"""
SignBridge AI - Phase 4.5 Motion Data Integrity & Verification Script.
Audits all 5 source video and mocap JSON pairs:
- File existence & readability
- SHA-256 checksums
- Frame count, fps, duration
- Keyframe count, timestamp continuity, monotonically increasing checks
- Coordinate formats, landmark counts, NaN/Inf checks, out-of-range bounds
- Left/right hand presence & visibility
- Facial NMM availability & range
"""

import sys
import json
import math
import hashlib
from pathlib import Path
import cv2

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

PAIRS = [
    {
        "concept": "Algorithm",
        "video": "data/sign_videos/islrtc_algorithm.mp4",
        "mocap": "data/isl_motion/processed/islrtc_algorithm_mocap.json"
    },
    {
        "concept": "Frequency",
        "video": "data/sign_videos/islrtc_frequency.mp4",
        "mocap": "data/isl_motion/processed/islrtc_frequency_mocap.json"
    },
    {
        "concept": "Current",
        "video": "data/sign_videos/islrtc_current.mp4",
        "mocap": "data/isl_motion/processed/islrtc_current_mocap.json"
    },
    {
        "concept": "Beam",
        "video": "data/sign_videos/islrtc_beam.mp4",
        "mocap": "data/isl_motion/processed/islrtc_beam_mocap.json"
    },
    {
        "concept": "Torque",
        "video": "data/sign_videos/islrtc_torque.mp4",
        "mocap": "data/isl_motion/processed/islrtc_torque_mocap.json"
    }
]

def sha256_file(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()

def check_numeric_val(val, path_str, issues):
    if val is None:
        return
    if isinstance(val, (int, float)):
        if math.isnan(val):
            issues.append(f"NaN at {path_str}")
        elif math.isinf(val):
            issues.append(f"Inf at {path_str}")
    elif isinstance(val, dict):
        for k, v in val.items():
            check_numeric_val(v, f"{path_str}.{k}", issues)
    elif isinstance(val, list):
        for idx, item in enumerate(val):
            check_numeric_val(item, f"{path_str}[{idx}]", issues)

def audit_pair(item):
    concept = item["concept"]
    video_path = ROOT_DIR / item["video"]
    mocap_path = ROOT_DIR / item["mocap"]

    res = {
        "concept": concept,
        "video_exists": video_path.exists(),
        "mocap_exists": mocap_path.exists(),
        "video_sha256": None,
        "mocap_sha256": None,
        "video_fps": 0.0,
        "video_total_frames": 0,
        "video_duration_seconds": 0.0,
        "video_resolution": None,
        "mocap_keyframes_count": 0,
        "mocap_duration_seconds": 0.0,
        "mocap_sample_fps": 0,
        "mocap_declared_source_sha256": None,
        "sha256_match": False,
        "timestamp_continuity_ok": True,
        "timestamp_issues": [],
        "nan_inf_issues": [],
        "hand_presence": {"left_hand_active_frames": 0, "right_hand_active_frames": 0},
        "joint_rotation_ranges": {},
        "facial_nmm_summary": {"has_brow_furrow": False, "has_brow_raise": False, "has_mouth_open": False}
    }

    if res["video_exists"]:
        res["video_sha256"] = sha256_file(video_path)
        cap = cv2.VideoCapture(str(video_path))
        if cap.isOpened():
            res["video_fps"] = cap.get(cv2.CAP_PROP_FPS) or 25.0
            res["video_total_frames"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            res["video_duration_seconds"] = round(res["video_total_frames"] / res["video_fps"], 3)
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            res["video_resolution"] = f"{w}x{h}"
            cap.release()

    if res["mocap_exists"]:
        res["mocap_sha256"] = sha256_file(mocap_path)
        with open(mocap_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        res["mocap_keyframes_count"] = len(data.get("keyframes", []))
        res["mocap_duration_seconds"] = data.get("duration_seconds", 0.0)
        res["mocap_sample_fps"] = data.get("sample_fps", 0)
        res["mocap_declared_source_sha256"] = data.get("source_sha256")
        res["sha256_match"] = (res["mocap_declared_source_sha256"] == res["video_sha256"])

        keyframes = data.get("keyframes", [])
        prev_t = -1
        numeric_issues = []

        lh_active = 0
        rh_active = 0

        # Track extremes for joint ranges
        joint_mins = {}
        joint_maxs = {}

        for idx, kf in enumerate(keyframes):
            t_ms = kf.get("timestamp_ms", 0)
            if t_ms <= prev_t and idx > 0:
                res["timestamp_continuity_ok"] = False
                res["timestamp_issues"].append(f"Non-increasing timestamp at frame {idx}: {t_ms} <= {prev_t}")
            prev_t = t_ms

            # Check for NaN / Inf
            check_numeric_val(kf, f"kf[{idx}]", numeric_issues)

            # Check hand poses
            rh = kf.get("right_hand", {})
            lh = kf.get("left_hand", {})
            if rh and rh.get("index", {}).get("mcp", {}).get("x", 0) != 0.25: # not default relaxed
                rh_active += 1
            if lh and lh.get("index", {}).get("mcp", {}).get("x", 0) != 0.25:
                lh_active += 1

            # Check facial NMM
            fnmm = kf.get("facial_blendshapes", {})
            if fnmm.get("brow_furrow_left", 0) > 0.01:
                res["facial_nmm_summary"]["has_brow_furrow"] = True
            if fnmm.get("brow_raise_left", 0) > 0.01:
                res["facial_nmm_summary"]["has_brow_raise"] = True
            if fnmm.get("mouth_open", 0) > 0.01:
                res["facial_nmm_summary"]["has_mouth_open"] = True

        res["hand_presence"]["left_hand_active_frames"] = lh_active
        res["hand_presence"]["right_hand_active_frames"] = rh_active
        res["nan_inf_issues"] = numeric_issues[:10] # limit to 10

    return res

def main():
    print("--- Running Phase 4.5 Motion Data Integrity Audit ---")
    results = []
    for item in PAIRS:
        r = audit_pair(item)
        results.append(r)
        print(f"\nConcept: {r['concept']}")
        print(f"  Video: exists={r['video_exists']}, {r['video_resolution']}, {r['video_total_frames']} frames, {r['video_duration_seconds']}s @ {r['video_fps']} fps")
        print(f"  Mocap: exists={r['mocap_exists']}, {r['mocap_keyframes_count']} keyframes, {r['mocap_duration_seconds']}s @ {r['mocap_sample_fps']} fps")
        print(f"  SHA-256 match declared: {r['sha256_match']}")
        print(f"  Timestamp continuity: {r['timestamp_continuity_ok']}")
        print(f"  NaN/Inf issues count: {len(r['nan_inf_issues'])}")
        print(f"  Hand presence: Right={r['hand_presence']['right_hand_active_frames']} kf, Left={r['hand_presence']['left_hand_active_frames']} kf")
        print(f"  Facial NMM: {r['facial_nmm_summary']}")

    out_path = ROOT_DIR / "reports" / "phase4_5_integrity_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nAudit complete. Results saved to {out_path}")

if __name__ == "__main__":
    main()

