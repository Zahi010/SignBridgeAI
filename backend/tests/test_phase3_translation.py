"""
SignBridge AI - Phase 3 Translation Engine & Multimodal Verification Tests
Validates:
1. Modular Engineering NLP Engine (tokenization, lemmatization, POS tagging)
2. Polysemy Disambiguation across 8 engineering terms (Current, Class, Stress, Resistance, Beam, Java, Bus, Port)
3. Semantic Relationship & Triple Extraction (e.g. Processor -> executes -> Instructions -> stored_in -> Memory)
4. Structured Intermediate Representation (IR) Schema and Translation Planner
5. Educational Explanation System for uncodified/abstract terms (Deadlock, Compiler, Modulation, etc.)
6. Authentic Resource Retriever with graceful degradation
7. Speech-to-ISL API endpoints (/api/v1/speech/transcribe and /api/v1/speech/translate)
8. Document-to-ISL section-by-section analysis and summary
"""

import io
import wave
import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.nlp_engine import EngineeringNLPEngine
from backend.app.services.explanation_service import EducationalExplanationService
from backend.app.services.resource_retriever import AuthenticResourceRetriever
from backend.app.database.database import SessionLocal
from backend.app.models.entities import Concept, ValidationStatus

client = TestClient(app)

# Helper to create valid in-memory WAV audio bytes
def create_dummy_wav_bytes(duration_seconds: float = 1.0, sample_rate: int = 16000) -> bytes:
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sample_rate)
        num_frames = int(duration_seconds * sample_rate)
        # 16-bit silent samples
        wf.writeframes(b"\x00\x00" * num_frames)
    buffer.seek(0)
    return buffer.read()

# -----------------------------------------------------------------------------
# 1. NLP Engine: Tokenization, Lemmatization & POS Tagging
# -----------------------------------------------------------------------------

def test_nlp_engine_tokenization_and_lemmatization():
    text = "Processors execute instructions stored in memory circuits."
    tokens = EngineeringNLPEngine.tokenize(text)
    assert len(tokens) >= 7

    # Check plural noun lemmatization
    proc_tok = next((t for t in tokens if t["text"].lower().startswith("processor")), None)
    assert proc_tok is not None
    assert proc_tok["lemma"] == "processor"

    inst_tok = next((t for t in tokens if t["text"].lower().startswith("instruction")), None)
    assert inst_tok is not None
    assert inst_tok["lemma"] == "instruction"

    # Check verb inflection reduction
    exec_tok = next((t for t in tokens if t["text"].lower().startswith("execute")), None)
    assert exec_tok is not None
    assert exec_tok["lemma"] == "execute"
    assert exec_tok["pos"] in ("VERB", "NOUN")

    store_tok = next((t for t in tokens if t["text"].lower().startswith("store")), None)
    assert store_tok is not None
    assert store_tok["lemma"] == "store"

# -----------------------------------------------------------------------------
# 2. Contextual Polysemy Disambiguation Tests
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("sentence,term,expected_valid", [
    # Current
    ("Current research focuses on deep learning architectures.", "Current", False),
    ("Alternating current flows through the copper inductor.", "Current", True),
    # Class
    ("Students gathered in the classroom for the morning class.", "Class", False),
    ("The Java class defines object attributes and methods.", "Class", True),
    # Stress
    ("Final exam stress produces severe anxiety in university students.", "Stress", False),
    ("Tensile stress exceeds allowable yield strength in the steel beam.", "Stress", True),
    # Resistance
    ("Bacterial antibiotic resistance threatens global healthcare policies.", "Resistance", False),
    ("Ohmic resistance in the wire opposes electrical charge flow.", "Resistance", True),
    # Beam
    ("A laser beam directs coherent light photons into the optical lens.", "Beam", False),
    ("A reinforced concrete beam transfers horizontal load to columns.", "Beam", True),
    # Java
    ("I ordered a warm cup of roasted java beans at the cafe.", "Java", False),
    ("The developer compiled the Java application into executable bytecode.", "Java", True),
    # Bus
    ("Passengers waited at the central bus terminal for the transit coach.", "Bus", False),
    ("The CPU transfers data to RAM across the high-speed system bus.", "Bus", True),
    # Port
    ("Cargo ships docked at the international shipping port.", "Port", False),
    ("Connect the serial communication cable to the hardware I/O port.", "Port", True),
])
def test_polysemy_disambiguation_rules(sentence: str, term: str, expected_valid: bool):
    is_valid, rationale, confidence = EngineeringNLPEngine.disambiguate_term(term, sentence)
    assert is_valid == expected_valid, (
        f"Failed disambiguation for '{term}' in '{sentence}'. "
        f"Expected {expected_valid}, got {is_valid}. Rationale: {rationale}"
    )
    assert confidence > 0.70

# -----------------------------------------------------------------------------
# 3. Semantic Relationship & Triple Extraction
# -----------------------------------------------------------------------------

def test_semantic_triple_extraction_processor_memory():
    sentence = "The processor executes instructions stored in memory."
    detected_concepts = ["Processor", "Instruction", "Memory"]
    triples = EngineeringNLPEngine.extract_semantic_triples(sentence, detected_concepts)

    assert len(triples) >= 1
    # Check for presence of key triples
    triple_strings = [t["triple_string"] for t in triples]
    assert any("executes" in s for s in triple_strings)
    assert any("stored_in" in s for s in triple_strings)

def test_semantic_triple_extraction_voltage_current():
    sentence = "Voltage drives the flow of current through the resistor."
    detected_concepts = ["Voltage", "Current", "Resistor"]
    triples = EngineeringNLPEngine.extract_semantic_triples(sentence, detected_concepts)

    assert len(triples) >= 1
    triple_strings = [t["triple_string"] for t in triples]
    assert any("drives" in s or "drives_flow_of" in s for s in triple_strings)

# -----------------------------------------------------------------------------
# 4. Translation Plan & Intermediate Representation Integration
# -----------------------------------------------------------------------------

def test_translation_plan_generation_multi_concept():
    # Sentence with authentic concept (Algorithm), uncodified concept (Deadlock), and question
    text = "What is the algorithm for deadlock detection in memory?"
    response = client.post("/api/v1/translate", json={"text": text})
    assert response.status_code == 200
    data = response.json()

    assert data["status"] in ("unsupported", "partial", "explanation_needed")
    assert "intermediate_representation" in data
    ir = data["intermediate_representation"]

    # Verify structured IR components
    assert "tokens" in ir
    assert "detected_concepts" in ir
    assert "concept_relationships" in ir
    assert "translation_plan" in ir
    assert "discourse_context" in ir

    plan = data.get("translation_plan")
    assert plan is not None
    assert plan["total_units"] >= 2
    assert "overall_strategy_summary" in plan

    # Check translation units
    units = plan["translation_units"]
    assert any(u["strategy"] in ("LEXICAL_SIGN_DIRECT", "PEDAGOGICAL_EXPLANATION", "UNSUPPORTED_FINGERSPELLING") for u in units)

# -----------------------------------------------------------------------------
# 5. Educational Explanation Service
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("concept_term", [
    "Deadlock", "Compiler", "Modulation", "Electromagnetic Induction",
    "Shear Stress", "Finite Element Analysis", "Prestressed Concrete", "Synchronous Motor"
])
def test_educational_explanation_service(concept_term: str):
    explanation = EducationalExplanationService.get_explanation(concept_term)
    assert explanation is not None, f"Educational explanation missing for {concept_term}"
    assert explanation["term"].lower() == concept_term.lower()
    assert len(explanation["fingerspelling_sequence"]) > 0
    assert len(explanation["isl_representation_plan"]) >= 3
    assert len(explanation["codified_related_concepts"]) > 0
    assert len(explanation["student_explanation"]) > 30

# -----------------------------------------------------------------------------
# 6. Authentic Resource Retriever
# -----------------------------------------------------------------------------

def test_authentic_resource_retriever_for_algorithm():
    db = SessionLocal()
    try:
        concept = db.query(Concept).filter(Concept.term == "Algorithm").first()
        assert concept is not None

        res = AuthenticResourceRetriever.retrieve_by_concept_id(concept.id, db)
        assert res["found"] is True
        assert res["term"] == "Algorithm"
        assert res["has_video"] is True
        assert res["video_asset"] is not None
        assert "islrtc_algorithm" in res["video_asset"]["video_url"]
        assert res["video_asset"]["validation_status"] in ("partial", "verified")
    finally:
        db.close()

def test_authentic_resource_retriever_for_unsupported():
    db = SessionLocal()
    try:
        res = AuthenticResourceRetriever.retrieve_by_term("Quantum Computing QuBit", db)
        assert res["found"] is False
        assert res["has_video"] is False
        assert len(res["fingerspelling_sequence"]) > 0
        assert "Zero-Fabrication Policy" in res["notice"]
    finally:
        db.close()

# -----------------------------------------------------------------------------
# 7. Speech-to-ISL Integration
# -----------------------------------------------------------------------------

def test_speech_transcribe_endpoint():
    wav_bytes = create_dummy_wav_bytes(duration_seconds=2.0)
    response = client.post(
        "/api/v1/speech/transcribe",
        files={"file": ("lecture.wav", io.BytesIO(wav_bytes), "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "transcription" in data
    assert data["confidence"] > 0.90
    assert data["duration_seconds"] > 0
    assert data["words_detected"] > 0
    assert data["status"] == "success"

def test_speech_translate_endpoint():
    wav_bytes = create_dummy_wav_bytes(duration_seconds=2.5)
    response = client.post(
        "/api/v1/speech/translate",
        data={"custom_hint": "The processor executes instructions stored in memory."},
        files={"file": ("lecture.wav", io.BytesIO(wav_bytes), "audio/wav")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "transcription" in data
    assert "translation" in data
    assert data["transcription"]["transcription"] == "The processor executes instructions stored in memory."
    trans = data["translation"]
    assert len(trans["extracted_concepts"]) >= 1
    assert "intermediate_representation" in trans

def test_speech_invalid_format_rejected():
    dummy_text = b"Not audio data."
    response = client.post(
        "/api/v1/speech/transcribe",
        files={"file": ("speech.txt", io.BytesIO(dummy_text), "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported audio format" in response.json()["detail"]

# -----------------------------------------------------------------------------
# 8. Document-to-ISL Section-by-Section Translation
# -----------------------------------------------------------------------------

def test_document_section_by_section_analysis():
    import pymupdf
    pdf_text = (
        "Operating System Overview\n\n"
        "An operating system manages computer memory and processor execution threads.\n\n"
        "Memory and Deadlock Conditions\n\n"
        "When concurrent processes wait indefinitely on circular resources, a deadlock condition arises."
    )
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((50, 50), pdf_text)
    pdf_bytes = doc.tobytes()
    doc.close()

    res = client.post(
        "/api/v1/documents/upload",
        files={"file": ("syllabus.pdf", io.BytesIO(pdf_bytes), "application/pdf")}
    )
    assert res.status_code == 200
    data = res.json()
    assert "sections" in data
    assert len(data["sections"]) >= 1
    sec = data["sections"][0]
    assert "heading" in sec
    assert "status" in sec
    assert "document_analysis" in data
    summary = data["document_analysis"]
    assert summary["total_sections"] >= 1
    assert summary["coverage_percentage"] >= 0.0
