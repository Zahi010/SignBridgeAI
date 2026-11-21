import io
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.models.entities import ValidationStatus

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"]["status"] == "connected"
    assert data["zero_fabrication_policy"] == "enforced"

def test_get_branches():
    response = client.get("/api/v1/branches")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    branch_codes = [b["code"] for b in data]
    assert "cs" in branch_codes
    assert "ece" in branch_codes
    assert "mech" in branch_codes
    assert "civil" in branch_codes
    assert "eee" in branch_codes

def test_get_subjects():
    response = client.get("/api/v1/subjects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10
    names = [s["name"] for s in data]
    assert "Operating Systems" in names
    assert "Database Management Systems" in names

def test_vocabulary_retrieval():
    response = client.get("/api/v1/vocabulary")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 20
    assert data["verified_count"] > 0
    terms = [item["term"] for item in data["items"]]
    assert "Database" in terms
    assert "Operating System" in terms
    assert "Deadlock" in terms

def test_vocabulary_search_and_filter():
    response = client.get("/api/v1/vocabulary?search=database")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1
    assert data["items"][0]["term"] == "Database"

def test_concept_detail_by_id():
    # Fetch all vocabulary to get Database id
    vocab_res = client.get("/api/v1/vocabulary?search=database")
    db_id = vocab_res.json()["items"][0]["id"]

    response = client.get(f"/api/v1/vocabulary/{db_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["term"] == "Database"
    assert data["validation_status"] == "verified"
    assert len(data["signs"]) > 0
    assert data["signs"][0]["is_authentic"] is True
    assert data["signs"][0]["has_video"] is True

def test_translate_verified_concept_database():
    response = client.post(
        "/api/v1/translate",
        json={"text": "What is a database?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "verified"
    assert len(data["extracted_concepts"]) >= 1
    assert data["extracted_concepts"][0]["term"] == "Database"
    assert data["video_output"]["available"] is True
    assert data["video_output"]["video_url"] is not None
    assert "DATABASE" in data["isl_gloss_sequence"]
    assert any("WHAT" in g for g in data["isl_gloss_sequence"])

def test_translate_unsupported_concept_deadlock():
    response = client.post(
        "/api/v1/translate",
        json={"text": "What is a deadlock in operating systems?"}
    )
    assert response.status_code == 200
    data = response.json()
    # Deadlock triggers unsupported status under Zero Fabrication Policy
    assert data["status"] == ValidationStatus.UNSUPPORTED.value
    terms = [c["term"] for c in data["extracted_concepts"]]
    assert "Deadlock" in terms
    assert "Zero Fabricated Signs Policy" in data["status_reason"] or "lacks standardized" in data["status_reason"] or "Deadlock" in data["status_reason"]

def test_translate_explanation_needed():
    response = client.post(
        "/api/v1/translate",
        json={"text": "Explain how an operating system works."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "explanation_needed"
    terms = [c["term"] for c in data["extracted_concepts"]]
    assert "Operating System" in terms
    assert len(data["grammar_notes"]) > 0

def test_translate_unsupported_random_input():
    response = client.post(
        "/api/v1/translate",
        json={"text": "Random sentence with no engineering keywords."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "unsupported"
    assert len(data["extracted_concepts"]) == 0
    assert data["video_output"]["available"] is False

def test_translation_history():
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_document_upload_validation_invalid_ext():
    file_bytes = b"fake executable binary"
    files = {"file": ("malicious.exe", io.BytesIO(file_bytes), "application/octet-stream")}
    response = client.post("/api/v1/documents/upload", files=files)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_document_upload_pdf():
    # Create simple valid PDF bytes using pymupdf
    import pymupdf
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Explain computer networks and database architecture.")
    pdf_bytes = doc.tobytes()
    doc.close()

    files = {"file": ("test_lecture.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    response = client.post("/api/v1/documents/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_lecture.pdf"
    assert data["file_type"] == "PDF"
    assert data["page_or_slide_count"] >= 1
    assert data["detected_concepts_count"] >= 1


def test_pipeline_stages_trace():
    response = client.post(
        "/api/v1/translate",
        json={"text": "What is a database?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "pipeline_stages" in data
    assert len(data["pipeline_stages"]) == 5
    stage_ids = [s["stage_id"] for s in data["pipeline_stages"]]
    assert "stage_1_tokenization" in stage_ids
    assert "stage_2_concept_extraction" in stage_ids
    assert "stage_3_grammar_restructuring" in stage_ids
    assert "stage_4_policy_audit" in stage_ids
    assert "stage_5_media_assembly" in stage_ids
    assert data["total_pipeline_duration_ms"] > 0
    # Check details inside stage 1
    s1 = next(s for s in data["pipeline_stages"] if s["stage_id"] == "stage_1_tokenization")
    assert s1["details"]["token_count"] >= 3
    # Check details inside stage 2
    s2 = next(s for s in data["pipeline_stages"] if s["stage_id"] == "stage_2_concept_extraction")
    assert s2["details"]["matched_count"] >= 1
