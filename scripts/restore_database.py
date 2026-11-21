"""
SignBridge AI - Database Disaster Recovery Restore Script (Phase 6).
Verifies SHA-256 cryptographic checksums before performing atomic restoration.
Creates a pre-restore safety rollback snapshot of the existing database.
"""

import os
import sys
import json
import shutil
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "backend" / "signbridge.db"
BACKUPS_DIR = ROOT_DIR / "data" / "backups"
MANIFEST_PATH = BACKUPS_DIR / "backup_manifest.json"


def compute_sha256(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def restore_database(target_backup: Optional[Path] = None):
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    
    if target_backup is None:
        # Find latest .db in backups
        backups = sorted(list(BACKUPS_DIR.glob("signbridge_backup_*.db")), key=lambda p: p.stat().st_mtime)
        if not backups:
            print("[ERROR] No database backups found in data/backups/", file=sys.stderr)
            sys.exit(1)
        target_backup = backups[-1]

    if not target_backup.exists():
        print(f"[ERROR] Specified backup does not exist: {target_backup}", file=sys.stderr)
        sys.exit(1)

    print(f"[SignBridge DR] Selected backup for restore: {target_backup.name}")
    actual_hash = compute_sha256(target_backup)

    # Verify checksum
    sha256_file = target_backup.with_suffix(".db.sha256")
    expected_hash = None
    if sha256_file.exists():
        with open(sha256_file, "r", encoding="utf-8") as f:
            expected_hash = f.read().split()[0].strip()

    if expected_hash and actual_hash != expected_hash:
        print(f"[CRITICAL ERROR] SHA-256 verification failed!", file=sys.stderr)
        print(f"  Expected: {expected_hash}", file=sys.stderr)
        print(f"  Actual:   {actual_hash}", file=sys.stderr)
        sys.exit(2)
    elif expected_hash:
        print(f"[SignBridge DR] Cryptographic integrity verified: {actual_hash}")

    # Check sqlite integrity
    test_conn = sqlite3.connect(target_backup)
    cursor = test_conn.cursor()
    cursor.execute("PRAGMA integrity_check;")
    check_res = cursor.fetchone()[0]
    test_conn.close()

    if check_res != "ok":
        print(f"[CRITICAL ERROR] SQLite integrity check failed: {check_res}", file=sys.stderr)
        sys.exit(3)
    print("[SignBridge DR] SQLite integrity check passed: OK")

    # Create safety rollback snapshot of existing db
    if DB_PATH.exists():
        safety_path = BACKUPS_DIR / f"pre_restore_safety_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_PATH, safety_path)
        print(f"[SignBridge DR] Pre-restore safety snapshot created: {safety_path.name}")

    # Restore via atomic file copy or sqlite backup API
    dest_conn = sqlite3.connect(DB_PATH)
    src_conn = sqlite3.connect(target_backup)
    with dest_conn:
        src_conn.backup(dest_conn, pages=100)
    dest_conn.close()
    src_conn.close()

    print(f"[SignBridge DR] SUCCESS: Database restored to {DB_PATH.name}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    restore_database(target)

