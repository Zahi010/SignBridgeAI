"""
SignBridge AI - Media Disaster Recovery Backup Script (Phase 6.5).
Creates a compressed .tar.gz archive of signing videos, thumbnails, and mocap data.
Computes SHA-256 checksums and records the entry in data/backups/media_manifest.json.
"""

import os
import sys
import json
import tarfile
import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
BACKUPS_DIR = DATA_DIR / "backups" / "media_backups"
MANIFEST_PATH = DATA_DIR / "backups" / "media_manifest.json"

MEDIA_DIRECTORIES = [
    DATA_DIR / "sign_videos",
    DATA_DIR / "isl_motion" / "processed",
]


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def run_media_backup() -> Path:
    start_time = time.time()
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    archive_filename = f"signbridge_media_{timestamp_str}.tar.gz"
    archive_path = BACKUPS_DIR / archive_filename
    sha256_path = BACKUPS_DIR / f"{archive_filename}.sha256"

    print(f"[SignBridge DR] Initiating media backup to {archive_filename}...")
    archived_files = []
    total_uncompressed_bytes = 0

    with tarfile.open(archive_path, "w:gz") as tar:
        for media_dir in MEDIA_DIRECTORIES:
            if media_dir.exists():
                for file_path in media_dir.rglob("*"):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(DATA_DIR)
                        tar.add(file_path, arcname=str(rel_path).replace("\\", "/"))
                        archived_files.append(str(rel_path).replace("\\", "/"))
                        total_uncompressed_bytes += file_path.stat().st_size

    if not archived_files:
        print("[WARNING] No media files found to archive.", file=sys.stderr)

    compressed_size = archive_path.stat().st_size
    sha256_hash = compute_sha256(archive_path)

    with open(sha256_path, "w", encoding="utf-8") as f_sha:
        f_sha.write(f"{sha256_hash}  {archive_filename}\n")

    duration = time.time() - start_time

    # Update manifest
    manifest_entries = []
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f_m:
                manifest_entries = json.load(f_m)
        except Exception:
            manifest_entries = []

    manifest_entries.append({
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "filename": archive_filename,
        "compressed_bytes": compressed_size,
        "uncompressed_bytes": total_uncompressed_bytes,
        "file_count": len(archived_files),
        "sha256": sha256_hash,
        "backup_duration_seconds": round(duration, 3)
    })

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f_m:
        json.dump(manifest_entries, f_m, indent=2)

    print(f"[SignBridge DR] Media backup completed in {duration:.3f}s:")
    print(f"  Archive: {archive_path}")
    print(f"  Files: {len(archived_files)}")
    print(f"  Compressed size: {compressed_size / (1024*1024):.2f} MB")
    print(f"  SHA-256: {sha256_hash}")
    return archive_path


if __name__ == "__main__":
    run_media_backup()

