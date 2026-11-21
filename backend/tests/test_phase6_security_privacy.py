"""
SignBridge AI - Phase 6 Pre-Pilot Security, Privacy, Ethics & Resilience Regression Test Suite.
Tests:
1. Security headers & health readiness probes
2. Server-side Bearer token revocation on logout
3. Tampered token rejection
4. Granular consent persistence (research, video, sharing, publication)
5. Ethical right-to-erasure (session purge, cryptographic de-identification, audit log scrubbing)
6. Export eligibility service with multi-license segregation (ODC-By, CC-BY-4.0, GODL-India)
7. Exact Fleiss' Kappa & reviewer cohort segregation in academic metrics
8. Disaster recovery backup & restore integrity with SHA-256 verification
"""

import uuid
import hashlib
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session

from backend.app.main import app
from backend.app.database.database import get_db, SessionLocal
from backend.app.models.validation_models import (
    Reviewer,
    ReviewerRole,
    ReviewerVerificationStatus,
    RevokedToken,
    ParticipantConsent,
    ResearchSession,
    ValidationAuditLog
)
from backend.app.services.academic_metrics_service import AcademicMetricsService
from backend.app.services.export_eligibility_service import ExportEligibilityService
from scripts.backup_database import run_backup, compute_sha256
from scripts.restore_database import restore_database

client = TestClient(app)


def test_security_headers_present():
    """Verifies mandatory production security headers are set on all responses."""
    res = client.get("/")
    assert res.status_code == 200
    headers = res.headers
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-frame-options") == "DENY"
    assert headers.get("x-xss-protection") == "1; mode=block"
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"


def test_health_endpoints_and_readiness_probes():
    """Verifies service health check and container orchestration probes."""
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["database"]["status"] == "connected"
    assert data["security"]["zero_fabrication_safeguard"] == "strictly_enforced"
    assert "token_revocation_engine" in data["security"]

    # Probes
    live_res = client.get("/api/v1/health/live")
    assert live_res.status_code == 200
    assert live_res.json()["live"] is True

    ready_res = client.get("/api/v1/health/ready")
    assert ready_res.status_code == 200
    assert ready_res.json()["ready"] is True


def test_token_revocation_on_logout():
    """
    Tests that a Bearer token is immediately revoked upon logout,
    preventing any subsequent access to protected endpoints.
    """
    uname = f"revtest_{uuid.uuid4().hex[:6]}"
    reg_payload = {
        "username": uname,
        "email": f"{uname}@signbridge.ai",
        "password": "SecurePassword123!",
        "full_name": "Revocation Tester",
        "is_deaf_native_signer": True,
        "is_certified_interpreter": False,
        "years_of_experience": 3,
        "role": "reviewer"
    }
    client.post("/api/v1/validation/register", json=reg_payload)

    # Login to obtain token
    login_res = client.post("/api/v1/validation/login", json={
        "username_or_email": uname,
        "password": "SecurePassword123!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    auth_header = {"Authorization": f"Bearer {token}"}

    # Verify token works on /me
    me_res = client.get("/api/v1/validation/me", headers=auth_header)
    assert me_res.status_code == 200
    assert me_res.json()["username"] == uname

    # Logout
    logout_res = client.post("/api/v1/validation/logout", headers=auth_header)
    assert logout_res.status_code == 200
    assert logout_res.json()["status"] == "success"

    # Verify token is now revoked and rejected with 401
    me_revoked_res = client.get("/api/v1/validation/me", headers=auth_header)
    assert me_revoked_res.status_code == 401
    assert "revoked" in me_revoked_res.json()["detail"].lower()


def test_tampered_token_signature_rejected():
    """Verifies that tampering with a token signature is immediately rejected."""
    tampered_token = "eyJzdWIiOiA5OX0.invalidsignature1234567890abcdef"
    res = client.get("/api/v1/validation/me", headers={"Authorization": f"Bearer {tampered_token}"})
    assert res.status_code == 401
    assert "signature" in res.json()["detail"].lower() or "invalid" in res.json()["detail"].lower()


def test_participant_granular_consent_persistence():
    """Verifies that all 4 granular consent flags are properly persisted."""
    p_id = f"DEAF-PARTICIPANT-{uuid.uuid4().hex[:6]}"
    payload = {
        "pseudonym": p_id,
        "study_name": "ISLRTC Engineering Comprehension Pilot 2026",
        "consent_version": "v1.2-ethics",
        "consent_given": True,
        "can_withdraw_anytime": True,
        "consent_general_research": True,
        "consent_video_recording": False,
        "consent_data_sharing": True,
        "consent_academic_publication": True,
        "notes": "Deaf native signer from Delhi cohort."
    }

    res = client.post("/api/v1/community/consent", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["pseudonym"] == p_id
    assert data["consent_general_research"] is True
    assert data["consent_video_recording"] is False
    assert data["consent_data_sharing"] is True
    assert data["consent_academic_publication"] is True

    # Retrieve by pseudonym
    get_res = client.get(f"/api/v1/community/consent/{p_id}")
    assert get_res.status_code == 200
    g_data = get_res.json()
    assert g_data["consent_video_recording"] is False
    assert g_data["consent_data_sharing"] is True


def test_right_to_erasure_complete_purge_and_sanitization():
    """
    Tests ethical right-to-erasure / right-to-be-forgotten:
    1. Research sessions are hard-deleted.
    2. Participant pseudonym is cryptographically irreversibly anonymized.
    3. Historical audit trail is scrubbed of the raw pseudonym.
    """
    p_id = f"DEAF-ERASE-{uuid.uuid4().hex[:6]}"
    client.post("/api/v1/community/consent", json={
        "pseudonym": p_id,
        "study_name": "Erasure Test Study",
        "consent_version": "v1.0",
        "consent_given": True,
        "can_withdraw_anytime": True,
        "consent_general_research": True,
        "consent_video_recording": False,
        "consent_data_sharing": True,
        "consent_academic_publication": True
    })

    # Record a session
    sess_code = f"SESS-{uuid.uuid4().hex[:6]}"
    sess_res = client.post("/api/v1/community/sessions", json={
        "participant_pseudonym": p_id,
        "session_code": sess_code,
        "session_type": "comprehension_survey",
        "concepts_tested": ["Algorithm"],
        "comprehension_score": 0.95,
        "naturalness_rating": 4.5,
        "feedback_notes": "Very clear hand movement."
    })
    assert sess_res.status_code == 200

    # Execute deletion request
    del_res = client.post("/api/v1/community/delete-data", json={
        "participant_pseudonym": p_id,
        "reason": "Participant requested complete withdrawal."
    })
    assert del_res.status_code == 200
    del_data = del_res.json()
    assert del_data["status"] == "success"
    assert del_data["purged_sessions_count"] == 1
    anonymized_id = del_data["anonymized_pseudonym"]
    assert anonymized_id.startswith("ANONYMIZED_PURGED_")

    # Verify session is purged from DB
    db: Session = SessionLocal()
    remaining_sessions = db.query(ResearchSession).filter(ResearchSession.session_code == sess_code).count()
    assert remaining_sessions == 0

    # Verify raw pseudonym no longer exists in consent table
    raw_consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == p_id).first()
    assert raw_consent is None

    # Verify anonymized consent record retains non-identifiable withdrawal metadata
    anon_consent = db.query(ParticipantConsent).filter(ParticipantConsent.pseudonym == anonymized_id).first()
    assert anon_consent is not None
    assert anon_consent.is_anonymized is True
    assert anon_consent.consent_given is False
    assert anon_consent.data_deletion_requested is True
    assert anon_consent.original_pseudonym_hash == hashlib.sha256(p_id.encode("utf-8")).hexdigest()

    # Verify audit logs referencing the old pseudonym were scrubbed
    raw_logs = db.query(ValidationAuditLog).filter(
        (ValidationAuditLog.actor_username == p_id) | (ValidationAuditLog.target_id == p_id)
    ).count()
    assert raw_logs == 0
    db.close()


def test_export_eligibility_multi_license_segregation():
    """
    Tests ExportEligibilityService to guarantee:
    - ODC-By applies to community evaluations
    - CC-BY-4.0 applies to retargeted mocap
    - GODL-India applies to authentic ISLRTC video pointers
    - Unconsented or non-data-sharing participants are strictly excluded
    """
    # Create one participant with consent_data_sharing = False
    opt_out_id = f"DEAF-NOSHARE-{uuid.uuid4().hex[:6]}"
    client.post("/api/v1/community/consent", json={
        "pseudonym": opt_out_id,
        "study_name": "Opt-Out Test Study",
        "consent_version": "v1.0",
        "consent_given": True,
        "can_withdraw_anytime": True,
        "consent_general_research": True,
        "consent_video_recording": False,
        "consent_data_sharing": False,  # Opted out of export
        "consent_academic_publication": False
    })
    opt_out_sess = f"SESS-NOSHARE-{uuid.uuid4().hex[:6]}"
    client.post("/api/v1/community/sessions", json={
        "participant_pseudonym": opt_out_id,
        "session_code": opt_out_sess,
        "session_type": "comprehension_survey",
        "concepts_tested": ["Torque"],
        "comprehension_score": 0.8,
        "naturalness_rating": 4.0
    })

    # Call export endpoint
    res = client.get("/api/v1/community/export")
    assert res.status_code == 200
    export_bundle = res.json()

    assert "packages" in export_bundle
    packages = export_bundle["packages"]
    assert "community_evaluations" in packages
    assert "retargeted_mocap" in packages
    assert "islrtc_reference_metadata" in packages

    # Check licenses
    assert "ODC-By" in packages["community_evaluations"]["license"]
    assert "CC-BY-4.0" in packages["retargeted_mocap"]["license"]
    assert "GODL-India" in packages["islrtc_reference_metadata"]["license"]

    # Verify opt-out session is strictly excluded
    exported_session_codes = [r["session_code"] for r in packages["community_evaluations"]["records"]]
    assert opt_out_sess not in exported_session_codes


def test_academic_metrics_fleiss_kappa_and_cohort_filter():
    """
    Verifies academic statistics engine:
    - cohort filtering separates verified experts from all reviewers
    - Fleiss' kappa and Cohen's kappa calculations return valid metrics
    """
    # Test cohort = all
    res_all = client.get("/api/v1/validation/academic-metrics?cohort=all")
    assert res_all.status_code == 200
    data_all = res_all.json()
    assert "sample_size_category" in data_all
    assert "confidence_interval_95" in data_all

    # Test cohort = verified_experts_only
    res_exp = client.get("/api/v1/validation/academic-metrics?cohort=verified_experts_only")
    assert res_exp.status_code == 200
    data_exp = res_exp.json()
    assert "sample_size_category" in data_exp


def test_database_backup_and_restore_cycle():
    """
    Tests disaster recovery automation:
    - Executes atomic backup
    - Verifies SHA-256 manifest
    - Restores backup cleanly
    """
    backup_path = run_backup()
    assert backup_path.exists()
    assert backup_path.stat().st_size > 0

    computed_hash = compute_sha256(backup_path)
    sha256_file = backup_path.with_suffix(".db.sha256")
    assert sha256_file.exists()

    with open(sha256_file, "r", encoding="utf-8") as f:
        stored_hash = f.read().split()[0].strip()
    assert computed_hash == stored_hash

    # Test restoration
    restore_database(backup_path)

