# SignBridge AI — Phase 3 Document Translation Report

**Module:** `backend/app/services/document_parser.py` & `backend/app/api/endpoints/documents.py`  
**Lead AI Systems Architect:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Status:** IMPLEMENTED, TESTED & INTEGRATED

---

## 1. Architectural Overview

Engineering course materials are distributed across multi-page PDF textbooks, Microsoft Word lecture notes (`.docx`), and PowerPoint presentations (`.pptx`).

Previously, document ingestion collapsed the entire file into a single truncated string. Phase 3 upgrades the architecture to **Section-by-Section Granular Document Translation**:
1. **Structural Segmentation:** Detects logical chapter headings, slide numbers (`[Slide X]`), numbered lists, and paragraph breaks.
2. **Per-Section Concept Extraction:** Identifies engineering concepts and semantic relations within each section independently.
3. **Curricular Coverage Analysis:** Calculates overall document concept coverage percentage ($\frac{\text{Supported} + \text{Pedagogical}}{\text{Total Concepts}} \times 100\%$).
4. **Interactive Section Navigator:** Allows students to navigate between sections, inspect translation status per paragraph, and view ISL video outputs.

---

## 2. Document Processing Pipeline

```
                     +---------------------------------------+
                     | UPLOADED DOCUMENT (PDF / DOCX / PPTX)  |
                     +---------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     | 1. PyMuPDF / python-docx / pptx Parser|
                     |    - Text & slide extraction          |
                     |    - Sanitization & size audit        |
                     +---------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     | 2. Section Structural Segmenter       |
                     |    - Slide markers [Slide 1, 2...]    |
                     |    - Thematic headings & paragraphs   |
                     +---------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     | 3. Concept Extraction & Disambiguation|
                     |    Per Section (Supported vs Unsup)   |
                     +---------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     | 4. Document-Level Coverage Summary    |
                     |    & Granular Section Navigator View  |
                     +---------------------------------------+
```

---

## 3. Schemas & Data Structures

### 3.1 `DocumentSectionTranslation`
```python
class DocumentSectionTranslation(BaseModel):
  section_index: int
  heading: str
  text_preview: str
  sentence_count: int
  detected_concepts: List[str] = []
  supported_count: int = 0
  explanation_count: int = 0
  unsupported_count: int = 0
  status: str  # "supported", "explanation_required", "unsupported", "neutral"
  isl_gloss_summary: str
```

### 3.2 `DocumentAnalysisSummary`
```python
class DocumentAnalysisSummary(BaseModel):
  total_sections: int
  total_concepts_found: int
  supported_concepts_count: int
  explanation_required_count: int
  unsupported_concepts_count: int
  overall_status: str
  coverage_percentage: float  # e.g., 85.5%
```

---

## 4. Verification Evidence

- `test_document_upload_pdf`: Uploads genuine PyMuPDF generated document, parses concepts, returns HTTP 200. (**PASS**)
- `test_document_upload_validation_invalid_ext`: Rejects unauthorized `.exe` binary. (**PASS**)
- `test_document_section_by_section_analysis`: Validates multi-section segmentation, per-section concept mapping, and document analysis coverage metrics. (**PASS**)

