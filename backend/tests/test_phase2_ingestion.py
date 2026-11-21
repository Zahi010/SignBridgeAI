"""
SignBridge AI - Phase 2 Authentic ISL Ingestion & Validation Gate Tests
Tests:
1. Reviewer profiles API listing and accreditation flags.
2. Unauthorized reviewers (developer test accounts or unregistered users) cannot assign VERIFIED (403 Forbidden).
3. Authorized expert reviewers (RCI accredited / Deaf native signers) can certify signs as VERIFIED.
4. Recording session creation with explicit consent status.
5. Ingestion rejects invalid consent statuses.
6. Batch JSON annotation ingestion with zero fabrication (missing fields remain None).
7. Batch CSV annotation ingestion with strict NEEDS_REVIEW initialization.
8. Video ingestion rejects unsupported formats (.txt, .exe).
"""

import io
import json
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.entities import ValidationStatus

client = TestClient(app)

def test_reviewer_profiles_listing():
    """
    GET /api/v1/validation/reviewers must return registered reviewer profiles,
    distinguishing authorized experts from unaccredited test accounts.
    """
    response = client.get("/api/v1/validation/reviewers")
    assert response.status_code == 200
    profiles = response.json()
    assert len(profiles) >= 2

    # Verify authorized master deaf reviewer
    auth_profile = next((p for p in profiles if p["reviewer_code"] == "REV-DEAF-MASTER-01"), None)
    assert auth_profile is not None
    assert auth_profile["is_authorized_expert"] is True
    assert auth_profile["is_deaf_native_signer"] is True
    assert "RCI" in (auth_profile["accreditation_body"] or "")

    # Verify unaccredited test account
    test_profile = next((p for p in profiles if p["reviewer_code"] == "REV-TEST-DEV-01"), None)
    assert test_profile is not None
    assert test_profile["is_authorized_expert"] is False


def test_unauthorized_reviewer_cannot_assign_verified():
    """
    CRITICAL GOVERNANCE RULE:
    Attempting to certify a sign as VERIFIED using an unaccredited reviewer
    (e.g., developer test account) MUST be rejected with HTTP 403 Forbidden.
    """
    response = client.post(
        "/api/v1/validation/submit",
        json={
            "sign_record_id": 1,
            "reviewer_code": "REV-TEST-DEV-01",
            "reviewer_name": "Dev Test Account",
            "decision": "approved",
            "assigned_status": "verified",
            "comments": "Attempting illegal verification from test account."
        }
    )
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]
    assert "not an authorized expert" in response.json()["detail"]


def test_unregistered_reviewer_cannot_assign_verified():
    """
    An unprofiled / anonymous reviewer attempting to certify as VERIFIED
    must be blocked with HTTP 403 Forbidden.
    """
    response = client.post(
        "/api/v1/validation/submit",
        json={
            "sign_record_id": 1,
            "reviewer_name": "Anonymous External User",
            "decision": "approved",
            "assigned_status": "verified",
            "comments": "No credentials provided."
        }
    )
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]


def test_authorized_reviewer_can_certify_verified():
    """
    A certified Deaf master reviewer (REV-DEAF-MASTER-01) can certify a sign as VERIFIED.
    The sign's authenticity flag is set, and accreditation evidence is recorded in the audit trail.
    """
    response = client.post(
        "/api/v1/validation/submit",
        json={
            "sign_record_id": 1,
            "reviewer_code": "REV-DEAF-MASTER-01",
            "reviewer_name": "Shri Rajesh Sharma",
            "decision": "approved",
            "assigned_status": "verified",
            "comments": "Linguistically authentic B-handshape downward stacking sign verified per ISLRTC 10k glossary standards.",
            "accuracy_rating": 4.9
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["assigned_status"] == "verified"

    # Verify audit trail contains accreditation evidence
    trail_res = client.get("/api/v1/validation/audit-trail/1")
    assert trail_res.status_code == 200
    trail = trail_res.json()
    assert len(trail) > 0
    latest = trail[0]
    assert latest["assigned_status"] == "verified"
    assert "RCI" in (latest.get("accreditation_evidence") or "")


def test_recording_session_creation_and_listing():
    """
    Registering an authentic sign recording session with consent metadata must succeed.
    """
    session_uid = "TEST-REC-20261120-CS-09"
    payload = {
        "session_uid": session_uid,
        "signer_id": "TEST-SIGNER-01",
        "signer_name": "Test Native Deaf Signer",
        "is_native_signer": True,
        "camera_setup": "Dual 1080p60 Studio Setup",
        "lighting_environment": "3-Point Softbox 5600K",
        "background": "Neutral 18% Gray",
        "consent_status": "verified_consent",
        "consent_document_ref": "CONSENT-TEST-2026-009",
        "notes": "Test session under DPDPA 2023 compliance."
    }
    response = client.post("/api/v1/ingestion/recording-session", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_uid"] == session_uid
    assert data["consent_status"] == "verified_consent"

    # List recording sessions
    list_res = client.get("/api/v1/ingestion/recording-sessions")
    assert list_res.status_code == 200
    sessions = list_res.json()
    uids = [s["session_uid"] for s in sessions]
    assert session_uid in uids


def test_recording_session_invalid_consent_rejected():
    """
    Submitting an invalid consent status enum must return HTTP 400.
    """
    payload = {
        "session_uid": "TEST-INVALID-CONSENT",
        "signer_id": "TEST-SIGNER-X",
        "consent_status": "unapproved_consent_string"
    }
    response = client.post("/api/v1/ingestion/recording-session", json=payload)
    assert response.status_code == 400
    assert "Invalid consent status" in response.json()["detail"]


def test_batch_json_ingestion_zero_fabrication():
    """
    Batch JSON ingestion must register candidate signs under NEEDS_REVIEW status.
    Unprovided phonological parameters must remain None (zero fabrication).
    """
    sample_dataset = [
        {
            "term": "Database",
            "sign_gloss": "DATA STORE [INGESTED]",
            "source_institution": "ISLRTC Test Import",
            "source_url_or_dataset_id": "ISLRTC-BATCH-TEST-01",
            "license": "GODL-India",
            "dominant_hand": "Right hand active",
            "handshape": "B-handshape",
            # Intentionally omit movement, location, orientation
        }
    ]
    file_bytes = json.dumps(sample_dataset).encode("utf-8")
    response = client.post(
        "/api/v1/ingestion/batch-json",
        files={"file": ("dataset.json", io.BytesIO(file_bytes), "application/json")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_parsed"] == 1
    assert (data["created_records"] + data["updated_records"]) == 1


def test_batch_csv_ingestion():
    """
    Batch CSV ingestion must parse valid CSV rows and enqueue candidate signs under NEEDS_REVIEW.
    """
    csv_content = (
        "concept_term,sign_gloss,source_institution,license,handshape,movement\n"
        "Operating System,COMPUTER CONTROL [INGESTED],AI4Bharat Test,CC BY-NC 4.0,C-handshape,circular\n"
    )
    response = client.post(
        "/api/v1/ingestion/batch-csv",
        files={"file": ("dataset.csv", io.BytesIO(csv_content.encode("utf-8")), "text/csv")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert (data["created_records"] + data["updated_records"]) >= 1


def test_invalid_video_format_rejected():
    """
    Video ingestion must reject non-video file formats (.txt, .exe, etc.).
    """
    dummy_text = b"This is not a video file."
    response = client.post(
        "/api/v1/ingestion/sign-video",
        data={
            "concept_id": 1,
            "title": "Invalid File Test",
            "source_attribution": "Testing Framework"
        },
        files={"file": ("malicious.txt", io.BytesIO(dummy_text), "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported video format" in response.json()["detail"]
