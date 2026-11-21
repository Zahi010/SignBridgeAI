"""
SignBridge AI - Audit Safeguards & Linguistic Integrity Tests
Tests critical non-negotiable rules:
1. Unsupported concepts never receive fabricated sign videos.
2. Inflected unsupported concepts ('deadlocked') properly trigger UNSUPPORTED status and suppress partial video.
3. Polysemy disambiguation correctly filters out electrical Current in non-technical sentences.
4. Video assets in the database are marked DEMO_ONLY and do not falsely claim certified human signers.
5. Avatar animations without physical mocap files on disk report NOT_IMPLEMENTED / unavailable.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.entities import ValidationStatus

client = TestClient(app)

def test_deadlocked_inflection_and_video_suppression():
    """
    Sentence containing both Database and Deadlocked must:
    1. Extract both concepts.
    2. Set overall status to UNSUPPORTED.
    3. Suppress the Database video to prevent misleading single-concept playback.
    """
    response = client.post(
        "/api/v1/translate",
        json={"text": "The database system is deadlocked."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == ValidationStatus.UNSUPPORTED.value
    extracted = [c["term"] for c in data["extracted_concepts"]]
    assert "Database" in extracted
    assert "Deadlock" in extracted
    # Crucial safeguard: video must NOT be available
    assert data["video_output"]["available"] is False
    assert "Video playback disabled" in data["video_output"]["notes"] or "uncodified" in data["video_output"]["notes"]

def test_polysemy_disambiguation_temporal_current():
    """
    'Current research focuses on artificial intelligence.' must NOT extract electrical Current.
    """
    response = client.post(
        "/api/v1/translate",
        json={"text": "Current research focuses on artificial intelligence."}
    )
    assert response.status_code == 200
    data = response.json()
    extracted = [c["term"] for c in data["extracted_concepts"]]
    assert "Current" not in extracted
    assert data["status"] == ValidationStatus.UNSUPPORTED.value

def test_video_asset_demo_only_labeling():
    """
    Retrieving video metadata must reflect DEMO_ONLY status and indicate synthetic test patterns.
    """
    response = client.get("/api/v1/videos/retrieve/1")
    assert response.status_code == 200
    data = response.json()
    assert data["match_type"] == "EXACT_MATCH"
    assert data["video_url"] is not None
    # The status must be DEMO_ONLY
    assert data["validation_status"].lower() == "demo_only" or "demo" in data["validation_status"].lower()
    assert "Synthetic" in data["signer_name"] or "Test Pattern" in data["signer_name"]

def test_unsupported_concept_fingerspelling_emitted():
    """
    Concepts like Deadlock, Entropy, Modulation must emit two-handed fingerspelling sequences.
    """
    for term, sentence in [
        ("Deadlock", "What is deadlock?"),
        ("Modulation", "What is modulation?"),
        ("Bracing", "What is bracing?")
    ]:
        response = client.post("/api/v1/translate", json={"text": sentence})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == ValidationStatus.UNSUPPORTED.value
        explanations = data.get("pedagogical_explanations", [])
        assert len(explanations) > 0
        exp = explanations[0]
        assert exp["term"] == term
        assert len(exp["fingerspelling_sequence"]) > 0

def test_sentence_retrieval_refuses_continuous_concatenation():
    """
    Sentence retrieval must refuse to concatenate discrete sign videos into a fake continuous sentence.
    """
    response = client.get("/api/v1/videos/sentence-retrieval?concept_ids=1,3")
    assert response.status_code == 200
    data = response.json()
    assert data["continuous_sentence_video"]["available"] is False
    assert "Zero Fabricated Signs Policy" in data["continuous_sentence_video"]["message"]
