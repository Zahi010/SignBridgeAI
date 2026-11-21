"""
SignBridge AI - Media Disaster Recovery Restore Script (Phase 6.5).
Verifies SHA-256 cryptographic checksums before restoring media assets.
Extracts videos, thumbnails, and mocap files to data/ safely.
"""

import os
import sys
import json
import time
import tarfile
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
BACKUPS_DIR = DATA_DIR / "backups" / "media_backups"
MANIFEST_PATH = DATA_DIR / "backups" / "media_manifest.json"


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def restore_media(target_backup: Optional[Path] = None) -> float:
    start_time = time.time()
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    if target_backup is None:
        archives = sorted(list(BACKUPS_DIR.glob("signbridge_media_*.tar.gz")), key=lambda p: p.stat().st_mtime)
        if not archives:
            print("[ERROR] No media archives found in data/backups/media_backups/", file=sys.stderr)
            sys.exit(1)
        target_backup = archives[-1]

    if not target_backup.exists():
        print(f"[ERROR] Specified media backup does not exist: {target_backup}", file=sys.stderr)
        sys.exit(1)

    print(f"[SignBridge DR] Selected media backup for restore: {target_backup.name}")
    actual_hash = compute_sha256(target_backup)

    # Check sidecar checksum if present
    sidecar_path = target_backup.parent / f"{target_backup.name}.sha256"
    if sidecar_path.exists():
        expected_hash = sidecar_path.read_text(encoding="utf-8").strip().split()[0]
        if actual_hash != expected_hash:
            print(f"[CRITICAL CHECKSUM MISMATCH] Expected: {expected_hash}, Actual: {actual_hash}", file=sys.stderr)
            sys.exit(1)
        print("[SignBridge DR] SHA-256 verification against sidecar: VALID")
    else:
        print("[SignBridge DR] Warning: No sidecar checksum file found. Proceeding with caution.")

    # Extract archive into DATA_DIR
    print(f"[SignBridge DR] Extracting media files to {DATA_DIR}...")
    extracted_count = 0
    with tarfile.open(target_backup, "r:gz") as tar:
        # Validate member paths to prevent directory traversal
        for member in tar.getmembers():
            member_path = DATA_DIR / member.name
            try:
                member_path.resolve().relative_to(DATA_DIR.resolve())
            except ValueError:
                print(f"[SECURITY ALERT] Malicious tar member path detected: {member.name}", file=sys.stderr)
                sys.exit(1)
        if hasattr(tarfile, 'data_filter'):
            tar.extractall(DATA_DIR, filter='data')
        else:
            tar.extractall(DATA_DIR)
        extracted_count = len(tar.getmembers())

    duration = time.time() - start_time
    print(f"[SignBridge DR] Media restoration complete in {duration:.3f} seconds.")
    print(f"  Restored files: {extracted_count}")
    print(f"  Recovery Time Objective (RTO): {duration:.3f}s")
    return duration


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    restore_media(target)
