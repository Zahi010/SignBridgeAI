"""
SignBridge AI - Batch Motion Capture Extraction Script (Phase 4).
Runs MediaPipe landmark extraction, normalization, temporal smoothing,
and skeletal retargeting on acquired ISLRTC videos.
Outputs processed mocap JSON keyframes to data/isl_motion/processed/.
"""

import sys
import json
import hashlib
from pathlib import Path

# Add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.services.motion_capture_service import MotionCaptureService
from backend.app.services.motion_retargeting_service import MotionRetargetingService
from backend.app.schemas.avatar import MotionVerificationStatus


VIDEOS_TO_PROCESS = [
    {
        "term": "Algorithm",
        "gloss": "ALGORITHM",
        "concept_id": 1,
        "video_file": "islrtc_algorithm.mp4",
        "max_duration": 6.0
    },
    {
        "term": "Frequency",
        "gloss": "FREQUENCY",
        "concept_id": 21,
        "video_file": "islrtc_frequency.mp4",
        "max_duration": 5.0
    },
    {
        "term": "Current",
        "gloss": "CURRENT",
        "concept_id": 41,
        "video_file": "islrtc_current.mp4",
        "max_duration": 5.0
    },
    {
        "term": "Beam",
        "gloss": "BEAM",
        "concept_id": 61,
        "video_file": "islrtc_beam.mp4",
        "max_duration": 5.0
    },
    {
        "term": "Torque",
        "gloss": "TORQUE",
        "concept_id": 81,
        "video_file": "islrtc_torque.mp4",
        "max_duration": 6.0
    }
]


def compute_sha256(filepath: Path) -> str:
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def run_batch_extraction():
    data_dir = ROOT_DIR / "data"
    videos_dir = data_dir / "sign_videos"
    motion_dir = data_dir / "isl_motion"
    processed_dir = motion_dir / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    mocap_svc = MotionCaptureService(models_dir=motion_dir)
    retarget_svc = MotionRetargetingService()

    print(f"--- Starting ISL Motion Capture Pipeline ---")
    print(f"MediaPipe Pipeline Available: {mocap_svc.is_pipeline_available()}")

    for item in VIDEOS_TO_PROCESS:
        v_path = videos_dir / item["video_file"]
        if not v_path.exists():
            print(f"Skipping {item['term']}: video not found at {v_path}")
            continue

        sha256_hash = compute_sha256(v_path)
        print(f"\nProcessing '{item['term']}' ({item['video_file']})...")
        print(f"  SHA-256: {sha256_hash}")

        # Extract landmarks with CV pipeline
        raw_res = mocap_svc.extract_landmarks_from_video(
            video_path=v_path,
            max_duration_seconds=item["max_duration"],
            sample_fps=25
        )
        print(f"  Extracted {raw_res['total_extracted_frames']} smoothed frames ({raw_res['duration_seconds']}s).")

        # Retarget to avatar skeleton
        keyframes = retarget_svc.retarget_frames_to_keyframes(raw_res["frames"])
        print(f"  Retargeted {len(keyframes)} keyframes to SignBridge-Articulated-54 rig.")

        # Serialize to JSON payload
        output_data = {
            "concept_id": item["concept_id"],
            "concept_term": item["term"],
            "sign_gloss": item["gloss"],
            "source_video_file": item["video_file"],
            "source_sha256": sha256_hash,
            "source_organization": "ISLRTC",
            "license": "Government Open Data License - India (GODL-India)",
            "motion_status": MotionVerificationStatus.PARTIALLY_VERIFIED_MOTION.value,
            "linguistic_disclaimer": (
                "Authentic motion extracted from official ISLRTC video via MediaPipe Holistic. "
                "Classified as PARTIALLY_VERIFIED_MOTION pending formal linguistic sign-accuracy review "
                "by an accredited Deaf ISL expert reviewer. Zero-Fabrication Policy strictly enforced."
            ),
            "rig_standard": "SignBridge-Articulated-54",
            "sample_fps": raw_res["sample_fps"],
            "duration_seconds": raw_res["duration_seconds"],
            "keyframes_count": len(keyframes),
            "keyframes": [kf.model_dump() for kf in keyframes]
        }

        stem = v_path.stem
        out_file = processed_dir / f"{stem}_mocap.json"
        with open(out_file, "w", encoding="utf-8") as f_out:
            json.dump(output_data, f_out, indent=2)

        print(f"  Successfully saved mocap data: {out_file.relative_to(ROOT_DIR)} ({out_file.stat().st_size} bytes)")

    print("\n--- Batch Motion Capture Extraction Complete ---")


if __name__ == "__main__":
    run_batch_extraction()

