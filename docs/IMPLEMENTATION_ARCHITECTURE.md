# SignBridge AI — System Architecture & Implementation Design

## 1. Executive Overview

SignBridge AI is an AI-powered Indian Sign Language (ISL) educational translation platform built specifically for deaf and hard-of-hearing engineering students. The system transforms technical curriculum materials (spoken lectures, typed text, PDF textbooks, and PPTX presentation slides) into grammatically structured Indian Sign Language representations while adhering strictly to a **Zero-Fabricated Signs Policy**.

### Core Tenet: Zero-Fabrication Policy
SignBridge AI never synthesizes or invents sign gestures, videos, or avatar animations for concepts that lack formal linguistic codification or Deaf community validation. Unsupported or partially supported concepts are categorized with transparent linguistic statuses (`VERIFIED`, `PARTIAL`, `NEEDS_REVIEW`, `EXPLANATION_REQUIRED`, or `UNSUPPORTED`) and supported with pedagogical definitions, ISL fingerspelling sequences, and conceptual diagrams.

---

## 2. Architecture Diagram

```
+--------------------------------------------------------------------------------------------------+
|                                    SignBridge AI Architecture                                    |
+--------------------------------------------------------------------------------------------------+

[User Inputs]
   │
   ├─► Plain Text / Engineering Sentences ──┐
   ├─► Live Spoken Audio (Whisper Pipeline) ┼──► [FastAPI API Gateway]
   └─► PDF / DOCX / PPTX Documents ─────────┘           │
                                                        ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             Context-Aware Semantic Translation Engine                            │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Text Normalization & Tokenization                                                             │
│    - Regex tokenization, stop-word filtering, technical multi-word compounding                   │
│                                                                                                  │
│ 2. Concept Extraction & Knowledge Base Retrieval                                                 │
│    - Multi-word exact and alias matching against curated STEM dictionary                         │
│    - Database lookup in SQLite `concepts` & `sign_records`                                        │
│                                                                                                  │
│ 3. Semantic Analysis & Disambiguation (e.g. Electrical Current vs Temporal current)              │
│    - Context window scoring, branch attribution (CSE, ECE, ME, CE, EEE)                          │
│    - Semantic relationship extraction: [Voltage] --(drives_flow_of)--> [Current]                 │
│                                                                                                  │
│ 4. ISL Linguistic Restructuring                                                                  │
│    - Topic-Comment ordering: Object + Subject + Verb                                             │
│    - Non-Manual Markers (NMMs): WH-questions -> brow_furrowed, Yes/No -> brow_raised           │
│    - Spatial indexing and temporal marker fronting                                               │
│                                                                                                  │
│ 5. Zero-Fabrication Policy Enforcement & Pedagogical Explainer                                    │
│    - Uncodified terms routed to Pedagogical Explainer                                            │
│    - Two-handed ISL fingerspelling sequence generation (D-E-A-D-L-O-C-K)                            │
│    - Pedagogical diagram description & educator technical advice                                 │
│                                                                                                  │
│ 6. Translation Intermediate Representation (IR) Emission                                        │
│    - Unified JSON schema linking tokens, phonology, semantic relations, and media anchors        │
└────────────────────────────────────────┬─────────────────────────────────────────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
┌──────────────────────────────────┐            ┌──────────────────────────────────┐
│      Human Video Pipeline        │            │    3D Signing Avatar Pipeline    │
├──────────────────────────────────┤            ├──────────────────────────────────┤
│ - Strict non-concatenation policy│            │ - SignSequenceTimeline builder   │
│ - Exact & contextual retrieval   │            │ - Rest-pose blend interpolation  │
│ - Provenance verification        │            │ - Facial blendshapes (NMMs)      │
│ - FFmpeg metadata & thumbnails   │            │ - Three.js WebGL rendering       │
└──────────────────────────────────┘            └──────────────────────────────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   React + TypeScript Frontend                                    │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ - Text Translator with Live Pipeline Stages & Intermediate Representation Inspector              │
│ - Document Translator (PDF / DOCX / PPTX) with curriculum concept breakdown                      │
│ - ISL Vocabulary Explorer with 6-parameter phonological grid (Handshape, Movement, Location, etc)│
│ - Expert Reviewer Validation Portal for Deaf Community accreditation & audit trails              │
│ - Dual-track Presentation Display: Human Sign Video Player & 3D WebGL Avatar                     │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Details

### A. Backend (`FastAPI`, `SQLAlchemy`, `SQLite`)
- **API Endpoints (`backend/app/api/endpoints/`):**
  - `/translate`: Context-aware text translation returning structured IR, semantic relations, and pedagogical explanations.
  - `/vocabulary`: Filtering, searching, and phonological retrieval across 100 STEM concepts and 23 subjects.
  - `/validation`: Expert Deaf educator review submission, status updating, and multi-signature audit trails.
  - `/videos`: Single-sign video retrieval and multi-parameter metadata validation via FFmpeg/ffprobe.
  - `/avatar`: Dynamic `SignSequenceTimeline` generation with neutral blend transitions and facial blend shapes.
  - `/documents`: Document parsing for PDF, DOCX, and PPTX extracting engineering concepts.

### B. Context-Aware Semantic Translation Engine (`backend/app/translation/`)
- **`semantic_analyzer.py`**: Disambiguates polysemous words (e.g. distinguishing electrical `Current` from chronological `current`; mechanical `Stress` from psychological `stress`). Calculates relationship graphs between detected terms.
- **`concept_explainer.py`**: Formulates structured pedagogical guidance for uncodified terms, including authentic two-handed ISL fingerspelling arrays and conceptual diagram descriptions.
- **`intermediate_representation.py`**: Generates a standardized JSON IR encapsulating tokens, syntactic roles, spatial coordinates, facial NMM blendshapes, and provenance metadata.

### C. Human Video Pipeline (`backend/app/services/`)
- **`video_ingestion.py`**: Validates uploaded video files, extracts frame rates, resolutions, and codecs using `ffprobe`, and generates preview thumbnails. Sets new uploads to `NEEDS_REVIEW`.
- **`video_retrieval.py`**: Resolves videos based on concept IDs. Categorizes matches as `EXACT_MATCH`, `CONTEXTUAL_MATCH`, `PARTIAL_MATCH`, or `NO_MATCH`. Strictly rejects synthesizing continuous sign sentences by stitching discrete video files.

### D. 3D Signing Avatar Engine (`backend/app/services/avatar_animation.py` & Three.js)
- **`SignSequenceTimeline`**: Compiles sign tracks separated by transition blends (`blend_duration: 0.25s`) back to a neutral rest pose (`hands_down_relaxed`).
- **Facial Blendshapes for NMMs**: Drives facial expressions (`brow_down_furrowed` for WH-questions, `brow_up_raised` for polar questions, `cheeks_puffed` for intensive qualifiers).
- **Three.js Renderer**: WebGL rendering with OrbitControls and realistic joint lighting.

### E. Frontend Application (`React`, `TypeScript`, `Tailwind CSS`, `Vite`)
- **Linguistic Transparency**: Every view features status badges (`VERIFIED`, `PARTIAL`, `NEEDS_REVIEW`, `EXPLANATION_REQUIRED`, `UNSUPPORTED`) and tooltips explaining provenance.
- **Phonological Inspector**: Displays dominant hand, handshape, movement, location, orientation, and non-manual markers for each sign.
- **Interactive Validation Portal**: Enables certified Deaf reviewers to submit accreditation decisions, suggest dialectal variations, and record phonological corrections.

