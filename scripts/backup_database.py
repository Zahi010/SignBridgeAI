"""
SignBridge AI - Automated Database Disaster Recovery Backup Script (Phase 6).
Creates an atomic, online SQLite backup of signbridge.db, computes SHA-256 checksums,
and records the backup entry in the disaster recovery manifest.
"""

import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "backend" / "signbridge.db"
BACKUPS_DIR = ROOT_DIR / "data" / "backups"
MANIFEST_PATH = BACKUPS_DIR / "backup_manifest.json"


def compute_sha256(file_path: Path) -> str:
    """Computes SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def run_backup() -> Path:
    if not DB_PATH.exists():
        print(f"[ERROR] Database file not found at: {DB_PATH}", file=sys.stderr)
        sys.exit(1)

    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_filename = f"signbridge_backup_{timestamp_str}.db"
    backup_path = BACKUPS_DIR / backup_filename
    sha256_path = BACKUPS_DIR / f"{backup_filename}.sha256"

    print(f"[SignBridge DR] Initiating atomic online backup of {DB_PATH.name}...")
    source_conn = sqlite3.connect(DB_PATH)
    dest_conn = sqlite3.connect(backup_path)
    
    with dest_conn:
        source_conn.backup(dest_conn, pages=100)
    
    source_conn.close()
    dest_conn.close()

    # Compute checksum
    backup_hash = compute_sha256(backup_path)
    backup_size = backup_path.stat().st_size

    # Write sidecar .sha256 file
    with open(sha256_path, "w", encoding="utf-8") as f:
        f.write(f"{backup_hash} *{backup_filename}\n")

    # Read tables count for validation
    v_conn = sqlite3.connect(backup_path)
    cursor = v_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cursor.fetchall()]
    v_conn.close()

    # Update manifest.json
    manifest_data = []
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
        except Exception:
            manifest_data = []

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "backup_file": backup_filename,
        "sha256": backup_hash,
        "size_bytes": backup_size,
        "tables_count": len(tables),
        "tables": tables
    }
    manifest_data.append(record)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    print(f"[SignBridge DR] Backup complete: {backup_path.name}")
    print(f"[SignBridge DR] SHA-256: {backup_hash}")
    print(f"[SignBridge DR] Size: {backup_size} bytes, Tables: {len(tables)}")
    return backup_path


if __name__ == "__main__":
    run_backup()

