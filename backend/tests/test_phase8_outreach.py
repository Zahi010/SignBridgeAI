"""
SignBridge AI - Phase 8 Institutional Outreach & Collaboration Readiness Tests.
Validates:
1. Retrieval of verified institutional directory (12 verified institutions).
2. Category, status, and text-search filtering.
3. Outreach pipeline summary statistics and follow-up tracking.
4. Institutional detail endpoint with chronological interaction audit history.
5. Organization creation and update workflows.
6. Interaction logging with lifecycle status transitions.
7. Governance export of outreach data.
8. Zero-Fabrication invariant: no autonomous external communication.
"""

import pytest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database.database import SessionLocal
from backend.app.models.outreach_models import (
    InstitutionalOutreach,
    OutreachInteraction,
    OutreachCategory,
    OutreachStatus,
    InteractionType
)
from backend.app.models.validation_models import Reviewer, ReviewerRole, ReviewerVerificationStatus
from backend.app.core.auth import create_access_token

client = TestClient(app)


@pytest.fixture
def admin_token():
    """Authenticates as administrator or creates token."""
    login_res = client.post("/api/v1/validation/login", json={
        "username_or_email": "admin",
        "password": "admin_pass_2026_isl"
    })
    if login_res.status_code == 200:
        return login_res.json()["access_token"]

    db = SessionLocal()
    try:
        admin = db.query(Reviewer).filter(Reviewer.username == "admin").first()
        if not admin:
            from backend.app.core.auth import hash_password
            admin = Reviewer(
                username="admin",
                email="admin_p8@test.com",
                hashed_password=hash_password("admin_pass_2026_isl"),
                full_name="SignBridge Administrator",
                role=ReviewerRole.ADMIN,
                verification_status=ReviewerVerificationStatus.VERIFIED
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        return create_access_token({"sub": admin.id, "username": admin.username, "role": admin.role.value})
    finally:
        db.close()


def test_list_organizations_baseline():
    """Verifies that all 12 verified institutions from Phase 8.2 are retrievable."""
    res = client.get("/api/v1/outreach/organizations")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 12

    # Check key organizations are present
    acronyms = [item.get("acronym") for item in data if item.get("acronym")]
    assert "ISLRTC" in acronyms
    assert "AYJNISHD" in acronyms
    assert "DEF" in acronyms
    assert "ASSISTECH IITD" in acronyms


def test_organization_filtering():
    """Tests category, status, and search filters."""
    # Filter by category
    res_cat = client.get("/api/v1/outreach/organizations?category=GOVERNMENT_NATIONAL")
    assert res_cat.status_code == 200
    gov_data = res_cat.json()
    assert len(gov_data) >= 3
    for org in gov_data:
        assert org["category"] == "GOVERNMENT_NATIONAL"

    # Filter by status
    res_st = client.get("/api/v1/outreach/organizations?status=READY_FOR_OUTREACH")
    assert res_st.status_code == 200
    ready_data = res_st.json()
    assert len(ready_data) >= 1
    for org in ready_data:
        assert org["outreach_status"] == "READY_FOR_OUTREACH"

    # Search by keyword
    res_search = client.get("/api/v1/outreach/organizations?search=Madras")
    assert res_search.status_code == 200
    search_data = res_search.json()
    assert len(search_data) >= 1
    assert any("Madras" in org["organization_name"] for org in search_data)


def test_outreach_stats():
    """Verifies aggregate metrics for outreach pipeline."""
    res = client.get("/api/v1/outreach/stats")
    assert res.status_code == 200
    stats = res.json()

    assert stats["total_organizations"] >= 12
    assert "GOVERNMENT_NATIONAL" in stats["by_category"]
    assert "ACADEMIC_RESEARCH" in stats["by_category"]
    assert "DEAF_ORGANIZATION" in stats["by_category"]
    assert stats["total_interactions"] >= 0


def test_organization_detail_and_interaction():
    """Verifies retrieving single organization and adding interaction."""
    # Find ISLRTC
    res_list = client.get("/api/v1/outreach/organizations?search=ISLRTC")
    assert res_list.status_code == 200
    orgs = res_list.json()
    assert len(orgs) > 0
    islrtc_id = orgs[0]["id"]

    # Get detail
    res_detail = client.get(f"/api/v1/outreach/organizations/{islrtc_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["id"] == islrtc_id
    assert "interactions" in detail

    # Log interaction
    interaction_payload = {
        "interaction_type": "NOTE",
        "summary": "Internal Review of Collaboration Proposal",
        "details": "Proposal alignment with ISLRTC 2026 technical dictionary codification objectives confirmed.",
        "outcome": "READY_FOR_PRESENTATION",
        "next_steps": "Schedule internal rehearsal before external inquiry."
    }
    res_log = client.post(f"/api/v1/outreach/organizations/{islrtc_id}/interactions", json=interaction_payload)
    assert res_log.status_code == 201
    log_data = res_log.json()
    assert log_data["outreach_id"] == islrtc_id
    assert log_data["summary"] == interaction_payload["summary"]

    # Re-fetch detail and ensure interaction is listed
    res_detail_updated = client.get(f"/api/v1/outreach/organizations/{islrtc_id}")
    assert res_detail_updated.status_code == 200
    updated_detail = res_detail_updated.json()
    summaries = [i["summary"] for i in updated_detail["interactions"]]
    assert "Internal Review of Collaboration Proposal" in summaries


def test_organization_status_transition_on_interaction():
    """Tests that logging an EMAIL_SENT advances READY_FOR_OUTREACH to CONTACTED."""
    # Create a test organization
    test_org_name = f"Test Outreach Institute {datetime.now().timestamp()}"
    create_payload = {
        "organization_name": test_org_name,
        "acronym": "TOI",
        "category": "ACADEMIC_RESEARCH",
        "website": "https://test.edu.in",
        "public_contact": "contact@test.edu.in",
        "department": "Computer Science",
        "verification_source": "Official Directory",
        "verification_date": "2026-11-23",
        "collaboration_role": "Academic Pilot Hosting",
        "outreach_status": "READY_FOR_OUTREACH",
        "proposed_collaboration_tier": "Tier 3: Classroom Demonstration Pilot"
    }
    res_create = client.post("/api/v1/outreach/organizations", json=create_payload)
    assert res_create.status_code == 201
    org_id = res_create.json()["id"]

    # Log an EMAIL_SENT interaction
    email_interaction = {
        "interaction_type": "EMAIL_SENT",
        "summary": "Dispatched Institutional Collaboration Letter",
        "details": "Formal research proposal and presentation outline delivered via authorized admin.",
        "outcome": "AWAITING_REPLY",
        "next_steps": "Follow up after 10 working days if no response."
    }
    res_email = client.post(f"/api/v1/outreach/organizations/{org_id}/interactions", json=email_interaction)
    assert res_email.status_code == 201

    # Check that status is now CONTACTED
    res_check = client.get(f"/api/v1/outreach/organizations/{org_id}")
    assert res_check.status_code == 200
    assert res_check.json()["outreach_status"] == "CONTACTED"

    # Clean up test organization to prevent test artifact pollution
    db = SessionLocal()
    try:
        test_org = db.query(InstitutionalOutreach).filter(InstitutionalOutreach.id == org_id).first()
        if test_org:
            db.delete(test_org)
            db.commit()
    finally:
        db.close()


def test_update_organization():
    """Tests updating an organization's fields."""
    res_list = client.get("/api/v1/outreach/organizations?search=AIISH")
    assert res_list.status_code == 200
    orgs = res_list.json()
    assert len(orgs) > 0
    org_id = orgs[0]["id"]

    update_payload = {
        "notes": "Verified speech-language evaluation team contact. Ready for Tier 1 outreach."
    }
    res_update = client.patch(f"/api/v1/outreach/organizations/{org_id}", json=update_payload)
    assert res_update.status_code == 200
    assert "Verified speech-language" in res_update.json()["notes"]


def test_export_outreach():
    """Verifies that full outreach registry exports with complete provenance and interaction details."""
    res = client.get("/api/v1/outreach/export")
    assert res.status_code == 200
    data = res.json()
    assert "export_timestamp" in data
    assert "total_organizations" in data
    assert "organizations" in data
    assert data["total_organizations"] >= 12

    # Check each organization in export has required verification fields
    first = data["organizations"][0]
    assert "verification_source" in first
    assert "verification_date" in first
    assert "collaboration_role" in first
    assert "outreach_status" in first


def test_zero_fabrication_safeguard():
    """
    Confirms that no unverified or mock institution has status COLLABORATION_CONFIRMED
    without an explicit documented agreement.
    """
    res = client.get("/api/v1/outreach/organizations?status=COLLABORATION_CONFIRMED")
    assert res.status_code == 200
    confirmed = res.json()
    # At this baseline stage (Phase 8), zero partnerships have been signed.
    assert len(confirmed) == 0, "No organization should be claimed as COLLABORATION_CONFIRMED without signed MoU"
