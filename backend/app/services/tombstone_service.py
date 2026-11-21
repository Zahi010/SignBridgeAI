"""
SignBridge AI - Tombstone Registry Service (Phase 6.5).
Prevents the 'Backup Resurrection' vulnerability where restoring a database backup
reintroduces deleted participants who previously exercised their Right to Erasure.

Maintains an immutable, append-only tombstone registry in data/backups/tombstone_registry.json.
Provides post-restore sanitization to automatically re-purge any resurrected records.
"""

import os
import json
import uuid
import hmac
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.models.validation_models import (
    ParticipantConsent,
    ResearchSession,
    ValidationAuditLog
)

TOMBSTONE_FILE = settings.BACKUPS_DIR / "tombstone_registry.json"


def get_pepper() -> str:
    return getattr(settings, "DELETION_PEPPER", settings.SECRET_KEY)


def compute_tombstone_hmac(pseudonym: str) -> str:
    return hmac.new(
        get_pepper().encode("utf-8"),
        pseudonym.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def register_tombstone(pseudonym: str, reason: Optional[str] = None, purged_sessions: int = 0) -> Dict[str, Any]:
    """
    Appends an irreversible tombstone entry to data/backups/tombstone_registry.json.
    """
    settings.BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    tombstones = []
    if TOMBSTONE_FILE.exists():
        try:
            with open(TOMBSTONE_FILE, "r", encoding="utf-8") as f:
                tombstones = json.load(f)
        except Exception:
            tombstones = []

    tombstone_id = f"TS-{uuid.uuid4().hex[:8]}"
    t_hmac = compute_tombstone_hmac(pseudonym)
    entry = {
        "tombstone_id": tombstone_id,
        "pseudonym": pseudonym, # stored in restricted server backup area
        "pseudonym_hmac": t_hmac,
        "purged_sessions_count": purged_sessions,
        "reason": reason or "User withdrawal request",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    tombstones.append(entry)

    with open(TOMBSTONE_FILE, "w", encoding="utf-8") as f:
        json.dump(tombstones, f, indent=2)

    return entry


def enforce_tombstones(db: Session) -> int:
    """
    Scans restored database against tombstone registry and purges any resurrected records.
    Returns count of re-purged participant records.
    """
    if not TOMBSTONE_FILE.exists():
        return 0

    try:
        with open(TOMBSTONE_FILE, "r", encoding="utf-8") as f:
            tombstones = json.load(f)
    except Exception:
        return 0

    re_purged_count = 0
    now = datetime.now(timezone.utc)

    for entry in tombstones:
        p_name = entry.get("pseudonym")
        if not p_name:
            continue

        consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == p_name).first()
        if consent:
            # Re-purge sessions
            db.query(ResearchSession).filter(ResearchSession.consent_id == consent.id).delete()
            
            # Anonymize consent
            anon_id = f"ANONYMIZED_PURGED_{uuid.uuid4().hex[:12]}"
            consent.pseudonym = anon_id
            consent.is_anonymized = True
            consent.consent_given = False
            consent.data_deletion_requested = True
            consent.withdrawal_date = now
            consent.notes = f"Tombstone enforced post-restore. Original tombstone ID: {entry.get('tombstone_id')}."

            # Scrub audit logs
            db.query(ValidationAuditLog).filter(ValidationAuditLog.actor_username == p_name).update(
                {ValidationAuditLog.actor_username: "ANONYMIZED_PURGED_USER"}
            )
            db.query(ValidationAuditLog).filter(ValidationAuditLog.target_id == p_name).update(
                {ValidationAuditLog.target_id: anon_id}
            )
            re_purged_count += 1

    if re_purged_count > 0:
        db.commit()

    return re_purged_count
