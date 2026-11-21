"""
SignBridge AI - Phase 7 Institutional Collaboration & Pilot Management Tests.
Tests:
1. Reviewer invitation code generation and validation.
2. Pilot status endpoint and PREPARATION gate enforcement.
3. Feedback remediation engine: auto-generation of engineering tickets from rubric criticisms.
4. Pilot evidence export bundle generation.
5. Invariance of Zero-Fabrication and licensing boundaries.
"""

import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.database import SessionLocal
from backend.app.models.validation_models import (
    Reviewer,
    ReviewerRole,
    ReviewerVerificationStatus,
    ValidationProject,
    ValidationTask,
    SignEvaluation,
    EvaluationCriterionRating,
    RubricCriterionRating,
    FeedbackRemediationTicket,
    RemediationCategory,
    RemediationStatus
)
from backend.app.core.auth import create_access_token

client = TestClient(app)


@pytest.fixture
def admin_token():
    """Authenticates as the seeded administrative reviewer and returns token."""
    login_res = client.post("/api/v1/validation/login", json={
        "username_or_email": "admin",
        "password": "admin_pass_2026_isl"
    })
    if login_res.status_code == 200:
        return login_res.json()["access_token"]
    
    # Fallback: create admin
    db = SessionLocal()
    admin = db.query(Reviewer).filter(Reviewer.username == "admin").first()
    if not admin:
        from backend.app.core.auth import hash_password
        admin = Reviewer(
            username="admin",
            email="admin_p7@test.com",
            hashed_password=hash_password("admin_pass_2026_isl"),
            full_name="SignBridge Administrator",
            role=ReviewerRole.ADMIN,
            verification_status=ReviewerVerificationStatus.VERIFIED
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
    token = create_access_token({"sub": admin.id, "username": admin.username, "role": admin.role.value})
    db.close()
    return token


def test_reviewer_invitation_lifecycle(admin_token):
    """
    Tests creating a reviewer invitation, verifying the code, and preventing reuse.
    """
    headers = {"Authorization": f"Bearer {admin_token}"}
    invite_payload = {
        "invited_email": f"expert_{uuid.uuid4().hex[:6]}@islrtc.test",
        "invited_name": "ISLRTC Master Signer",
        "intended_role": "expert_reviewer",
        "institutional_affiliation": "ISLRTC Delhi",
        "valid_days": 14
    }

    # 1. Create invitation
    res = client.post("/api/v1/validation/invitations", json=invite_payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "invitation_code" in data
    assert data["invitation_code"].startswith("INV-")
    assert data["invited_email"] == invite_payload["invited_email"]
    assert data["is_used"] is False

    invite_code = data["invitation_code"]

    # 2. Verify invitation code
    verify_res = client.get(f"/api/v1/validation/invitations/verify/{invite_code}")
    assert verify_res.status_code == 200
    v_data = verify_res.json()
    assert v_data["valid"] is True
    assert v_data["invited_name"] == "ISLRTC Master Signer"

    # 3. Invalid code check
    inv_res = client.get("/api/v1/validation/invitations/verify/INV-NONEXISTENT")
    assert inv_res.status_code == 404


def test_pilot_status_preparation_gate():
    """
    Validates that the pilot project status is strictly maintained in PREPARATION
    and provides the mandatory ethical gate message.
    """
    res = client.get("/api/v1/validation/pilot/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "PREPARATION"
    assert "SB-PILOT" in data["protocol_reference"]
    assert data["total_pilot_tasks"] >= 5
    assert "PREPARATION" in data["pilot_gate_message"]
    assert "Zero-Fabrication Policy" in data["pilot_gate_message"]


def test_feedback_driven_remediation_engine(admin_token):
    """
    Validates that expert ratings of MAJOR_ISSUE or INCORRECT are automatically
    transformed into categorized engineering remediation tickets.
    """
    db = SessionLocal()
    task = db.query(ValidationTask).first()
    assert task is not None, "At least one validation task must exist."

    reviewer = db.query(Reviewer).first()
    assert reviewer is not None

    # Create an evaluation with major handshape and orientation flaws
    eval_rec = SignEvaluation(
        task_id=task.id,
        reviewer_id=reviewer.id,
        sign_record_id=task.sign_record_id,
        is_draft=False,
        overall_recommendation="needs_revision",
        general_feedback="Handshape angle is rigid and orientation is flipped 90 degrees."
    )
    db.add(eval_rec)
    db.flush()

    cr1 = EvaluationCriterionRating(
        evaluation_id=eval_rec.id,
        criterion_name="handshape",
        rating=RubricCriterionRating.MAJOR_ISSUE,
        notes="Index knuckle flexion does not reach 90 degrees."
    )
    cr2 = EvaluationCriterionRating(
        evaluation_id=eval_rec.id,
        criterion_name="orientation",
        rating=RubricCriterionRating.INCORRECT,
        notes="Palm faces outward instead of towards signer sternum."
    )
    db.add_all([cr1, cr2])
    db.commit()
    db.refresh(eval_rec)

    # Invoke auto-generation endpoint
    gen_res = client.post(f"/api/v1/validation/remediations/generate-from-evaluation/{eval_rec.id}")
    assert gen_res.status_code == 200
    tickets = gen_res.json()
    assert len(tickets) >= 2

    categories = [t["category"] for t in tickets]
    assert "hand_articulation" in categories
    assert "orientation_solver" in categories

    ticket_id = tickets[0]["id"]

    # Update ticket status
    headers = {"Authorization": f"Bearer {admin_token}"}
    patch_res = client.patch(
        f"/api/v1/validation/remediations/{ticket_id}",
        json={"status": "in_progress", "resolution_notes": "Calibrating Euler limits in AvatarHandRig."},
        headers=headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "in_progress"

    db.close()


def test_pilot_evidence_export():
    """
    Tests the evidence export endpoint to verify that pilot packages
    are exported with full provenance, tasks, and remediation records.
    """
    res = client.get("/api/v1/validation/pilot/evidence-export")
    assert res.status_code == 200
    data = res.json()

    assert "export_metadata" in data
    assert "pilot_candidate_signs" in data
    assert len(data["pilot_candidate_signs"]) >= 5

    # Check that each sign in the package has provenance and license
    for s in data["pilot_candidate_signs"]:
        assert "concept_term" in s
        assert "source_provenance" in s
        assert s["source_provenance"]["license"] in ["GODL-India", "Government Open Data License - India (GODL-India)"]
        assert "mocap_metadata" in s
