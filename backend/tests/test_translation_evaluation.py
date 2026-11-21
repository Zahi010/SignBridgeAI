"""
SignBridge AI - 50-Sentence Translation Evaluation Benchmark.
Evaluates:
- Technical concept extraction across 5 engineering branches
- Context-aware disambiguation (e.g. electrical Current vs temporal current)
- Semantic relationship extraction between interacting entities
- Zero-Fabrication Policy compliance (unsupported terms must return UNSUPPORTED)
"""

import json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_50_sentence_benchmark_suite():
    eval_file = Path("data/evaluation_set_50.json")
    assert eval_file.exists(), f"Evaluation dataset {eval_file} missing."

    with open(eval_file, "r", encoding="utf-8") as f:
        sentences = json.load(f)

    assert len(sentences) >= 50, f"Expected at least 50 benchmark sentences, found {len(sentences)}."

    passed_count = 0
    disambiguation_checks_passed = 0
    unsupported_enforcements_passed = 0
    semantic_relations_extracted = 0

    print(f"\n[Benchmark] Executing {len(sentences)} engineering sentence evaluations...")

    for item in sentences:
        s_id = item["id"]
        sentence = item["sentence"]
        expected_concepts = item["expected_concepts"]
        expected_status = item["expected_status"]

        response = client.post("/api/v1/translate", json={"text": sentence})
        assert response.status_code == 200, f"Sentence #{s_id} failed with HTTP {response.status_code}"

        data = response.json()
        extracted_terms = [c["term"] for c in data["extracted_concepts"]]
        status_returned = data["status"]

        # 1. Concept extraction check: at least one expected concept must be extracted
        matched_expected = [c for c in expected_concepts if c in extracted_terms]
        assert len(matched_expected) > 0, f"Sentence #{s_id} ('{sentence}') extracted no expected concepts from {expected_concepts}. Extracted: {extracted_terms}"

        # 2. Status check for unsupported items
        if expected_status == "unsupported":
            assert status_returned == "unsupported", f"Sentence #{s_id} expected UNSUPPORTED, got {status_returned}"
            unsupported_enforcements_passed += 1

        # 3. Disambiguation check for item 35 ("Current research focuses on AI")
        if s_id == 35:
            assert "Current" not in extracted_terms, "Disambiguation failed: 'Current research' extracted electrical Current."
            assert "Algorithm" in extracted_terms, "Algorithm was not extracted from sentence 35."
            disambiguation_checks_passed += 1

        # 4. Semantic relations check
        if data.get("semantic_relations"):
            semantic_relations_extracted += len(data["semantic_relations"])

        # 5. IR structure check
        ir = data.get("intermediate_representation")
        assert ir is not None, f"Intermediate Representation missing in response for sentence #{s_id}"
        assert "isl_grammar_plan" in ir, "isl_grammar_plan missing in IR"
        assert "policy_verdict" in ir, "policy_verdict missing in IR"

        passed_count += 1

    print(f"[Benchmark] Completed: {passed_count}/{len(sentences)} passed.")
    print(f"[Benchmark] Unsupported policy enforcements: {unsupported_enforcements_passed}")
    print(f"[Benchmark] Disambiguation tests passed: {disambiguation_checks_passed}")
    print(f"[Benchmark] Total semantic relationships identified: {semantic_relations_extracted}")

    assert passed_count == len(sentences)

