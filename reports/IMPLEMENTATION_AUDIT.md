# SignBridge AI — Independent Implementation & Codebase Audit Report

**Auditor:** Senior AI Systems Auditor, ISL Linguistics Specialist & Full-Stack Architect  
**Audit Date:** November 20, 2026  
**Repository Directory:** `E:\SignBridgeAi`  
**Execution Context:** Evidence-driven inspection of actual source code, database tables, binary assets, and test runs.

---

## 1. Executive Summary & Core Verdict

The SignBridge AI application has established **impressive software engineering infrastructure**:
- FastAPI REST APIs, SQLAlchemy models, Pydantic schemas, and Vite React frontend compile and execute cleanly.
- Multi-word technical concept extraction, regex-based tokenization, and polysemy disambiguation function deterministically in Python.
- Pedagogical explanations for unsupported concepts and authentic two-handed fingerspelling sequence generation work as designed.
- Document parsing via PyMuPDF and python-docx extracts curriculum text without error.

**HOWEVER, from a linguistic and empirical sign language perspective:**
1. **Zero Real Human ISL Signing Videos:** Every video in `data/sign_videos/` is a synthetic FFmpeg `testsrc` animation showing digital clock digits and color bars. No human signers exist in the project.
2. **Zero Validated 3D Avatar Mocap Assets:** The 3D avatar is a procedural Three.js mannequin oscillating with sine waves. It has no articulated fingers, no thumb opposition, no facial blendshapes, and no motion-capture files. `data/avatar_animations/neutral_avatar.glb` does not exist on disk.
3. **Misrepresented Provenance in Database:** 4 video clips were falsely listed in SQLite as performed by a `Certified ISL Specialist` under `ISLRTC STEM Open Reference Pilot` with `VERIFIED` status. 40 concepts were marked `VERIFIED` despite having no empirical Deaf educator sign-off or video assets.
4. **Heuristic Grammar Approximation:** The translation engine uses a keyword-reordering heuristic (Topic-Comment rule, hardcoded verb lookup table, WH-word final positioning). It does not perform full syntactic dependency parsing or 3D spatial discourse modeling.
5. **Software Correctness != Linguistic Correctness:** The 50/50 passing test suite verified that software outputs matched hardcoded assertions, but does not prove genuine ISL translation accuracy.

---

## 2. Component-by-Component Audit Findings

| Component | Claimed Functionality | Actual Implementation | Concrete Evidence | Status |
|:---|:---|:---|:---|:---:|
| **Candidate Concepts** (`engineering_100_candidates.json`) | 100 genuine engineering ISL signs across 5 disciplines | 100 curated dictionary entries with candidate phonological descriptions; 40 marked verified without video or external review | Inspected JSON and DB: 40 marked `verified` with no accredited external review; only local test reviewer accounts exist | **`NEEDS_REVIEW`** |
| **50-Sentence Benchmark** (`evaluation_set_50.json`) | Proven 100% translation accuracy across engineering curricula | 50 test sentences testing software pipeline assertions (concept presence, status checks, IR schema) | `test_translation_evaluation.py` passes software assertions; does not evaluate human linguistic quality | **`PARTIAL`** |
| **Database Models & Tables** (`entities.py`, SQLite) | Certified ISL registry with provenance, videos, and reviewer audits | SQLite schema with branches, subjects, concepts, sign records, videos, animations, and reviews | `concepts` has 100 rows; `sign_records` has 100 rows; `reviewer_validations` has 1 test row; `sign_videos` has 5 rows | **`PASS`** (Schema) / **`DEMO_ONLY`** (Data) |
| **Semantic Analyzer** (`semantic_analyzer.py`) | Disambiguates polysemous words (e.g. electrical Current vs temporal current) | Keyword and regex matching with context-window scoring | Successfully disambiguates "Current flows" vs "Current research" in sentence test #35 | **`PASS`** |
| **Concept Explainer** (`concept_explainer.py`) | Pedagogical explanations and ISL fingerspelling for unsupported terms | Generates structured advice, diagram guidance, and letter-by-letter two-handed ISL fingerspelling arrays | Generates `['D', 'E', 'A', 'D', 'L', 'O', 'C', 'K']` for uncodified terms; verified in tests | **`PASS`** |
| **Grammar Transformer** (`isl_grammar.py`) | Genuine ISL syntactic transformation | Rule-based template heuristic: moves temporal words to front, matched concepts to Topic, hardcoded 10-verb lookup, appends WH-word to end | Lines 30-120 of `isl_grammar.py`: contains dictionary of 10 English verbs (`work`, `flow`, etc.); not a neural or dependency translation model | **`PARTIAL`** |
| **Translation Engine** (`engine.py`) | End-to-end ISL translation with 5-stage trace | Orchestrates tokenizer, semantic analyzer, DB lookup, grammar transformer, and IR assembler | Emits 5 pipeline stages and unified IR. Correctly tags unsupported terms, but previously served synthetic video for verified terms | **`PASS`** (Engine) / **`PARTIAL`** (Translation) |
| **Translation IR** (`intermediate_representation.py`) | Standardized JSON IR linking tokens, phonology, and media | Pydantic model constructing tokens, spatial loci, facial NMMs, and provenance | Produces compliant JSON schema consumed by frontend | **`PASS`** |
| **Video Ingestion** (`video_ingestion.py`) | Multi-parameter video ingestion and validation | Uses `ffprobe` to extract duration, fps, resolution, and `ffmpeg` for thumbnail creation; forces status to `NEEDS_REVIEW` | Functionally executed; generated thumbnail for test upload | **`PASS`** |
| **Video Retrieval** (`video_retrieval.py`) | Single-sign exact/contextual retrieval; blocks sentence concatenation | Queries `sign_videos`; returns exact match or contextual match; refuses to concatenate sentences | Correctly returned `available: False` for Deadlock; enforced non-concatenation policy | **`PASS`** (Logic) / **`DEMO_ONLY`** (Assets) |
| **Sign Video Assets** (`data/sign_videos/*.mp4`) | Real human Deaf signers demonstrating ISL | 5 synthetic FFmpeg `testsrc` animations showing a clock counter and SMPTE color bars | Probed with `ffprobe` and frame extraction: 0 human signers; 100% test patterns | **`DEMO_ONLY`** |
| **Avatar Sequencer** (`avatar_animation.py`) | Dynamic timeline sequencer with mocap blending | Generates timeline data structure with rest-pose blend metadata | DB points to `/data/avatar_animations/neutral_avatar.glb` which does NOT exist on disk | **`PARTIAL`** |
| **3D Avatar Viewer** (`AvatarViewer.tsx`) | 3D signing avatar reproducing ISL signs | Procedural Three.js box/cylinder model oscillating with sine waves (`Math.sin(t*2.0)*0.08`) | No finger joints, no thumb opposition, no morph targets; cannot sign any ISL sign | **`DEMO_ONLY`** |
| **Expert Validation API** (`endpoints/validation.py`) | Multi-signature Deaf educator accreditation workflow | Full CRUD API for pending reviews, submission, and audit trails | Endpoints functional, but database only holds test reviews from local developer scripts | **`PASS`** (API) / **`NEEDS_REVIEW`** (Community) |
| **Frontend Translator** (`TranslatorPage.tsx`) | Live pipeline view, phonological accordion, semantic relations, IR inspector | Fully wired React UI displaying backend response data | Displays stages, relations, explanations, IR; previously showed green "Verified" badge for synthetic videos | **`PASS`** |
| **Document Translator** (`DocumentTranslatorPage.tsx`) | Translates PDF, DOCX, and PPTX textbooks | Parses documents using PyMuPDF / python-docx; extracts concepts and generates summary | Successfully extracted concepts from `sample_lecture.pdf` | **`PASS`** |
| **Vocabulary Explorer** (`VocabularyExplorerPage.tsx`) | Explores STEM concepts with 6 phonological parameters | Modal displays dominant hand, handshape, movement, location, orientation, NMMs, and provenance | Fully operational; displays candidate phonological data | **`PASS`** |

---

## 3. Discovered Vulnerabilities & Misrepresentations

1. **Synthetic Video Misrepresentation:**
   In `sign_videos`, rows 1-4 were recorded with `signer_name = 'Certified ISL Specialist'`, `license = 'GODL-India'`, and `validation_status = 'VERIFIED'`. Independent frame inspection proved all 4 clips are FFmpeg synthetic test patterns.
   *Remediation Required:* Update database records and API schemas to relabel these assets as `DEMO_ONLY (Synthetic Testsrc)`. Never present them as authentic Deaf signers.

2. **Phantom 3D Avatar Asset:**
   In `avatar_animations`, row 1 points to `/data/avatar_animations/neutral_avatar.glb`. This file does not exist on disk.
   *Remediation Required:* Relabel avatar status as `NOT_IMPLEMENTED`. Update `AvatarViewer.tsx` to display an explicit notice: *"Procedural Mannequin Preview — Validated 3D Motion-Capture Awaiting Studio Recording"*, and halt fake arm flapping during sign translation.

3. **Unearned `VERIFIED` Statuses on 40 Concepts:**
   40 concepts were seeded as `VERIFIED` without external review from certified Deaf organizations.
   *Remediation Required:* Downgrade all 40 unverified concepts in SQLite to `NEEDS_REVIEW`.

4. **Alias Matching Gap for Inflected Words:**
   In audit sentence 29 (*"The database system is deadlocked"*), the concept *Deadlock* was not recognized because the inflected form *"deadlocked"* was not in aliases. The sentence fell back to matching *Database*, falsely marking the sentence `VERIFIED`.
   *Remediation Required:* Add stem/inflection matching or common technical inflections to aliases.

