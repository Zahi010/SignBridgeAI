"""
SignBridge AI - Phase 5 Linguistic Validation, Reviewer Accreditation & Community Evaluation Test Suite.
Validates:
- Reviewer registration, password hashing, and token authentication.
- Explicit administrative credential verification gate (unverified vs verified).
- Validation task lifecycle and 12-criterion rubric evaluation submission.
- Critical error guard: critical phonological errors prevent approval.
- Automated disagreement detection between conflicting reviewers.
- Binding administrative adjudication and Zero-Fabrication safeguard invariance.
- Ethical participant consent, research sessions, and complete data deletion.
- Academic evaluation statistics (Cohen's Kappa, confidence intervals, sample size gating).
- Dashboard real DB metrics and technical vs. linguistic status comparison.
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.validation_models import (
    ReviewerRole,
    ReviewerVerificationStatus,
    CredentialType,
    ValidationTaskStatus,
    RubricCriterionRating,
    AdjudicationDecisionEnum
)

client = TestClient(app)


# 1. Reviewer Registration & Default UNVERIFIED Status
def test_reviewer_registration_unverified():
    """Test that newly registered reviewers are strictly UNVERIFIED."""
    uid = uuid.uuid4().hex[:6]
    payload = {
        "username": f"rev_sunita_{uid}",
        "email": f"sunita_{uid}@example.org",
        "password": "SecurePassword123!",
        "full_name": "Sunita Kumari",
        "is_deaf_native_signer": True,
        "is_certified_interpreter": False,
        "years_of_experience": 8,
        "institution_affiliation": "Delhi Association of the Deaf",
        "role": ReviewerRole.DEAF_NATIVE_SIGNER.value
    }
    res = client.post("/api/v1/validation/register", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["username"] == f"rev_sunita_{uid}"
    assert data["full_name"] == "Sunita Kumari"
    assert data["verification_status"] == ReviewerVerificationStatus.UNVERIFIED.value
    assert data["is_deaf_native_signer"] is True


# 2. Reviewer Login & Authenticated Access
def test_reviewer_login_and_token():
    """Test login and JWT/Bearer token authentication."""
    # Login as admin
    login_payload = {
        "username_or_email": "admin",
        "password": "admin_pass_2026_isl"
    }
    res = client.post("/api/v1/validation/login", json=login_payload)
    assert res.status_code == 200
    token_data = res.json()

    assert "access_token" in token_data
    assert token_data["role"] == ReviewerRole.ADMIN.value
    assert token_data["verification_status"] == ReviewerVerificationStatus.VERIFIED.value

    # Access protected /me endpoint
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_res = client.get("/api/v1/validation/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["username"] == "admin"


# 3. Credential Submission & Administrative Verification Gate
def test_credential_submission_and_admin_verification():
    """Test credential submission by reviewer and administrative approval."""
    uid = uuid.uuid4().hex[:6]
    username = f"rev_arun_{uid}"
    reg_payload = {
        "username": username,
        "email": f"arun_{uid}@example.org",
        "password": "Password789!",
        "full_name": "Arun Verma",
        "is_deaf_native_signer": False,
        "is_certified_interpreter": True,
        "years_of_experience": 6,
        "institution_affiliation": "National ISL Interpreter Guild",
        "role": ReviewerRole.CERTIFIED_INTERPRETER.value
    }
    reg_res = client.post("/api/v1/validation/register", json=reg_payload)
    assert reg_res.status_code == 200

    # Login as Arun
    login_res = client.post("/api/v1/validation/login", json={"username_or_email": username, "password": "Password789!"})
    arun_token = login_res.json()["access_token"]
    arun_headers = {"Authorization": f"Bearer {arun_token}"}

    # Submit RCI credential
    cred_payload = {
        "credential_type": CredentialType.RCI_CERTIFICATE.value,
        "credential_identifier": f"RCI-ISL-2026-{uid}",
        "issuing_body": "Rehabilitation Council of India",
        "notes": "Grade-A certified ISL interpreter"
    }
    cred_res = client.post("/api/v1/validation/credentials", json=cred_payload, headers=arun_headers)
    assert cred_res.status_code == 200
    cred_id = cred_res.json()["id"]

    # Verify Arun is now VERIFICATION_PENDING
    me_res = client.get("/api/v1/validation/me", headers=arun_headers)
    assert me_res.json()["verification_status"] == ReviewerVerificationStatus.VERIFICATION_PENDING.value

    # Non-admin cannot verify credential
    unauth_res = client.post(
        f"/api/v1/validation/credentials/{cred_id}/verify",
        json={"new_status": "verified", "rationale": "Attempting self verification", "evidence_verified": True},
        headers=arun_headers
    )
    assert unauth_res.status_code == 403

    # Admin verifies credential
    admin_login = client.post("/api/v1/validation/login", json={"username_or_email": "admin", "password": "admin_pass_2026_isl"})
    admin_headers = {"Authorization": f"Bearer {admin_login.json()['access_token']}"}

    admin_verify_res = client.post(
        f"/api/v1/validation/credentials/{cred_id}/verify",
        json={"new_status": "verified", "rationale": "Verified against RCI official central register.", "evidence_verified": True},
        headers=admin_headers
    )
    assert admin_verify_res.status_code == 200
    assert admin_verify_res.json()["new_status"] == "verified"

    # Verify Arun is now VERIFIED
    arun_me_updated = client.get("/api/v1/validation/me", headers=arun_headers)
    assert arun_me_updated.json()["verification_status"] == ReviewerVerificationStatus.VERIFIED.value


# 4. Validation Tasks Listing & Detail
def test_validation_tasks_listing_and_detail():
    """Test retrieval of seeded validation tasks."""
    res = client.get("/api/v1/validation/tasks")
    assert res.status_code == 200
    tasks = res.json()

    assert len(tasks) >= 5
    terms = [t["concept_term"] for t in tasks]
    assert "Algorithm" in terms
    assert "Frequency" in terms

    # Test detailed task endpoint for first task
    task_id = tasks[0]["id"]
    detail_res = client.get(f"/api/v1/validation/tasks/{task_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()

    assert "concept" in detail
    assert "sign_record" in detail
    assert "video" in detail
    assert "avatar" in detail
    assert "annotations" in detail


# 5. Rubric Evaluation Submission & Critical Error Guard
def test_rubric_evaluation_submission_and_critical_error_guard():
    """Test submission of 12-criterion evaluation and critical error override."""
    # Login as Arun (verified reviewer)
    login_res = client.post("/api/v1/validation/login", json={"username_or_email": "rev_arun_rci", "password": "Password789!"})
    arun_headers = {"Authorization": f"Bearer {login_res.json()['access_token']}"}

    tasks = client.get("/api/v1/validation/tasks").json()
    task_id = tasks[0]["id"]

    eval_payload = {
        "task_id": task_id,
        "is_draft": False,
        "overall_recommendation": "accept", # Reviewer erroneously selected accept
        "general_feedback": "Handshape has major flaw but otherwise good.",
        "suggested_dialect": "Standard ISL Northern",
        "criteria_ratings": [
            {"criterion_name": "handshape", "rating": "major_issue", "notes": "Index finger orientation inverted", "is_critical_error": True},
            {"criterion_name": "movement", "rating": "pass", "notes": "Smooth stroke"},
            {"criterion_name": "location", "rating": "pass", "notes": "Neutral chest space"}
        ],
        "annotations": [
            {"task_id": task_id, "timestamp_ms": 1200, "duration_ms": 400, "target_type": "avatar", "category": "handshape_error", "comment": "Thumb opposition incorrect here"}
        ]
    }

    eval_res = client.post(f"/api/v1/validation/tasks/{task_id}/evaluate", json=eval_payload, headers=arun_headers)
    assert eval_res.status_code == 200
    eval_data = eval_res.json()

    # Rule: Critical error prevents 'accept' recommendation
    assert eval_data["overall_recommendation"] == "needs_revision"
    assert len(eval_data["criteria_ratings"]) == 3


# 6. Disagreement Detection on Conflicting Evaluations
def test_disagreement_detection_on_conflicting_evaluations():
    """Test that conflicting reviews trigger DISAGREEMENT_DETECTED on a task."""
    uid = uuid.uuid4().hex[:6]
    tasks = client.get("/api/v1/validation/tasks").json()
    task_id = tasks[1]["id"] # Frequency task

    # Register Reviewer 1 (Devika)
    client.post("/api/v1/validation/register", json={
        "username": f"rev_devika_{uid}",
        "email": f"devika_{uid}@example.org",
        "password": "Password123!",
        "full_name": "Devika Nair",
        "role": ReviewerRole.REVIEWER.value
    })
    token1 = client.post("/api/v1/validation/login", json={"username_or_email": f"rev_devika_{uid}", "password": "Password123!"}).json()["access_token"]

    # Register Reviewer 2 (Ramesh)
    client.post("/api/v1/validation/register", json={
        "username": f"rev_ramesh_{uid}",
        "email": f"ramesh_{uid}@example.org",
        "password": "Password123!",
        "full_name": "Ramesh Rao",
        "role": ReviewerRole.REVIEWER.value
    })
    token2 = client.post("/api/v1/validation/login", json={"username_or_email": f"rev_ramesh_{uid}", "password": "Password123!"}).json()["access_token"]

    # Devika rates Handshape as PASS, recommendation ACCEPT
    client.post(
        f"/api/v1/validation/tasks/{task_id}/evaluate",
        json={
            "task_id": task_id,
            "overall_recommendation": "accept",
            "criteria_ratings": [{"criterion_name": "handshape", "rating": "pass"}]
        },
        headers={"Authorization": f"Bearer {token1}"}
    )

    # Ramesh rates Handshape as MAJOR_ISSUE, recommendation REJECT
    client.post(
        f"/api/v1/validation/tasks/{task_id}/evaluate",
        json={
            "task_id": task_id,
            "overall_recommendation": "reject",
            "criteria_ratings": [{"criterion_name": "handshape", "rating": "major_issue", "is_critical_error": True}]
        },
        headers={"Authorization": f"Bearer {token2}"}
    )

    # Inspect task status: must be DISAGREEMENT_DETECTED
    task_detail = client.get(f"/api/v1/validation/tasks/{task_id}").json()
    assert task_detail["status"] == ValidationTaskStatus.DISAGREEMENT_DETECTED.value
    assert len(task_detail["disagreements"]) >= 1


# 7. Adjudication Requires Verified Status
def test_adjudication_requires_verified_adjudicator():
    """Test that unverified reviewers cannot issue binding adjudication decisions."""
    tasks = client.get("/api/v1/validation/tasks").json()
    task_id = tasks[1]["id"]

    # Unverified Devika attempts adjudication -> 403 Forbidden
    token_unverified = client.post("/api/v1/validation/login", json={"username_or_email": "rev_devika_1", "password": "Password123!"}).json()["access_token"]
    unauth_adj = client.post(
        f"/api/v1/validation/tasks/{task_id}/adjudicate",
        json={
            "decision": AdjudicationDecisionEnum.ACCEPTED.value,
            "resulting_motion_status": "VERIFIED_ISL_MOTION",
            "rationale": "I like this sign."
        },
        headers={"Authorization": f"Bearer {token_unverified}"}
    )
    assert unauth_adj.status_code == 403

    # Verified Admin adjudicates -> Success
    token_admin = client.post("/api/v1/validation/login", json={"username_or_email": "admin", "password": "admin_pass_2026_isl"}).json()["access_token"]
    auth_adj = client.post(
        f"/api/v1/validation/tasks/{task_id}/adjudicate",
        json={
            "decision": AdjudicationDecisionEnum.ADDITIONAL_REVIEW_REQUIRED.value,
            "resulting_motion_status": "PARTIALLY_VERIFIED_MOTION",
            "rationale": "Regional variation detected between Northern and Southern cohorts; additional expert review requested."
        },
        headers={"Authorization": f"Bearer {token_admin}"}
    )
    assert auth_adj.status_code == 200
    assert auth_adj.json()["decision"] == AdjudicationDecisionEnum.ADDITIONAL_REVIEW_REQUIRED.value


# 8. Participant Consent, Research Session, and Ethical Data Deletion
def test_participant_consent_session_and_data_deletion():
    """Test ethical research protocol: consent, session recording, and data deletion right."""
    uid = uuid.uuid4().hex[:6]
    pseudonym = f"DEAF-RESEARCH-PARTICIPANT-{uid}"

    # Record consent
    consent_payload = {
        "pseudonym": pseudonym,
        "study_name": "SignBridge AI Deaf Cohort Study 2026",
        "consent_given": True,
        "can_withdraw_anytime": True
    }
    c_res = client.post("/api/v1/community/consent", json=consent_payload)
    assert c_res.status_code == 200
    assert c_res.json()["pseudonym"] == pseudonym

    # Record research session
    sess_payload = {
        "participant_pseudonym": pseudonym,
        "session_code": f"SESS-2026-CS-{uid}",
        "session_type": "comprehension_survey",
        "concepts_tested": [{"concept": "Algorithm", "user_selected_meaning": "Step-by-step procedure"}],
        "comprehension_score": 0.90,
        "naturalness_rating": 4.5,
        "feedback_notes": "Very clear sign, matches Delhi educational usage."
    }
    sess_res = client.post("/api/v1/community/sessions", json=sess_payload)
    assert sess_res.status_code == 200
    assert sess_res.json()["comprehension_score"] == 0.90

    # Execute Data Deletion (Participant Withdrawal)
    del_res = client.post("/api/v1/community/delete-data", json={"participant_pseudonym": pseudonym, "reason": "Participant withdrew consent"})
    assert del_res.status_code == 200
    assert del_res.json()["purged_sessions_count"] == 1

    # Subsequent attempt to record session for withdrawn participant fails
    sess_res2 = client.post("/api/v1/community/sessions", json=sess_payload)
    assert sess_res2.status_code == 403


# 9. Academic Metrics & Sample Size Gating
def test_academic_metrics_sample_size_gating():
    """Test academic statistical analysis and small sample size disclaimers."""
    res = client.get("/api/v1/validation/academic-metrics")
    assert res.status_code == 200
    metrics = res.json()

    assert "sample_size_category" in metrics
    assert metrics["sample_size_category"] in ["INSUFFICIENT_SAMPLE_SIZE", "PRELIMINARY_RESULTS", "NO_DATA"]
    assert "average_inter_reviewer_agreement_percent" in metrics
    assert "confidence_interval_95" in metrics
    assert any(w in metrics["academic_disclaimer"].lower() for w in ["cohort", "sample size", "zero-fabrication", "publication", "evaluation"])


# 10. Validation Dashboard Live Statistics
def test_validation_dashboard_statistics():
    """Test dashboard endpoint returns live database-backed metrics."""
    res = client.get("/api/v1/validation/dashboard")
    assert res.status_code == 200
    data = res.json()

    assert data["total_validation_tasks"] >= 5
    assert "technical_vs_linguistic_status" in data
    assert data["technical_vs_linguistic_status"]["technical_fidelity_passing_count"] == 5
    assert data["verified_reviewers_count"] >= 1
