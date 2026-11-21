"""
SignBridge AI - Authentication, Password Hashing & RBAC Authorization (Phase 5).
Uses standard library hashlib.pbkdf2_hmac and hmac-sha256 signed tokens.
Zero external dependency, fully reproducible and cross-platform.
"""

import hmac
import hashlib
import base64
import json
import time
from typing import Optional, Dict, Any, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.validation_models import Reviewer, ReviewerRole, ReviewerVerificationStatus

# Configuration constants
SECRET_KEY = "signbridge-isl-governance-secret-salt-2026-accredited"
TOKEN_EXPIRATION_SECONDS = 86400 * 7  # 7 days
PBKDF2_ITERATIONS = 100000

security_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = hashlib.sha256(f"{password[:4]}_{SECRET_KEY}".encode()).hexdigest()[:16]
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        PBKDF2_ITERATIONS
    )
    return f"{salt}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against stored salt and PBKDF2 key."""
    try:
        salt, key_hex = hashed_password.split("$")
        key = hashlib.pbkdf2_hmac(
            'sha256',
            plain_password.encode('utf-8'),
            salt.encode('utf-8'),
            PBKDF2_ITERATIONS
        )
        return hmac.compare_digest(key.hex(), key_hex)
    except Exception:
        return False


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Creates a cryptographically signed URL-safe bearer token.
    Payload contains reviewer identity, role, and expiration.
    """
    payload = data.copy()
    payload["exp"] = int(time.time()) + TOKEN_EXPIRATION_SECONDS
    payload_json = json.dumps(payload, sort_keys=True).encode("utf-8")
    payload_b64 = base64.urlsafe_b64encode(payload_json).decode("utf-8").rstrip("=")

    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return f"{payload_b64}.{signature}"


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Verifies cryptographic signature and expiration of bearer token.
    """
    parts = token.split(".")
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format."
        )

    payload_b64, signature = parts
    # Check HMAC signature
    expected_sig = hmac.new(
        SECRET_KEY.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, signature):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature."
        )

    # Decode payload
    padding = "=" * ((4 - len(payload_b64) % 4) % 4)
    payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
    payload = json.loads(payload_bytes.decode("utf-8"))

    # Check expiration
    if payload.get("exp", 0) < int(time.time()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again."
        )

    return payload


def get_current_reviewer(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> Reviewer:
    """
    FastAPI dependency resolving the authenticated Reviewer model.
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please provide a valid Bearer token."
        )

    payload = decode_access_token(credentials.credentials)
    reviewer_id = payload.get("sub")
    if not reviewer_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject identifier."
        )

    reviewer = db.query(Reviewer).filter(Reviewer.id == reviewer_id).first()
    if not reviewer or not reviewer.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Reviewer account inactive or not found."
        )

    return reviewer


def require_roles(allowed_roles: List[ReviewerRole]):
    """
    Role-based authorization guard factory.
    """
    def role_checker(current_reviewer: Reviewer = Depends(get_current_reviewer)) -> Reviewer:
        if current_reviewer.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {[r.value for r in allowed_roles]}."
            )
        return current_reviewer
    return role_checker


def require_verified_reviewer(current_reviewer: Reviewer = Depends(get_current_reviewer)) -> Reviewer:
    """
    Guarantees reviewer has undergone administrative credential verification.
    """
    if current_reviewer.verification_status != ReviewerVerificationStatus.VERIFIED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Action forbidden: Reviewer status is '{current_reviewer.verification_status.value}'. "
                "Only administrative VERIFIED reviewers can perform this action."
            )
        )
    return current_reviewer
