# SignBridge AI — Phase 3 Translation Trace & Pipeline Observability Specification

**Components:** `frontend/src/components/translator/LivePipelinePanel.tsx` & `backend/app/translation/engine.py`  
**Lead AI Systems Auditor:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Status:** SPECIFIED, CODED & AUDITED

---

## 1. Specification Objective

To guarantee complete auditability, SignBridge AI surfaces an expandable, interactive **5-Stage Pipeline Execution Trace** directly in the user interface. Every translation query executes sequentially through five instrumented stages, recording execution latency in milliseconds, state summaries, and structured diagnostic payloads.

---

## 2. Five Instrumented Pipeline Stages

```
+-----------------------------------------------------------------------------------------------------+
| STAGE 1: Input Preprocessing & Linguistic Tokenization                                              |
| - Normalizes raw text and strips extraneous punctuation                                              |
| - Identifies grammatical sentence type (WH_QUESTION, POLAR_QUESTION, DECLARATIVE, COMPARATIVE)      |
| - Detects interrogative tokens (what, how, why) and negation markers (not, never, cannot)           |
| - Produces structured tokens with universal POS and lemmatization                                    |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| STAGE 2: Semantic Concept Recognition & Disambiguation                                              |
| - Scans technical terms against 111 knowledge base concepts                                         |
| - Executes Contextual Polysemy Disambiguation across 8 engineering terms                            |
| - Infers primary engineering branch and subdomain context                                            |
| - Extracts Subject-Predicate-Object semantic triples                                                |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| STAGE 3: Experimental ISL Syntactic Restructuring & Gloss Planning                                 |
| - Applies rule-based linguistic hypotheses (Topic-Comment order, WH-terminal placement, loci)       |
| - Labels transformations explicitly with linguistic disclaimer and UNVALIDATED_HYPOTHESIS status    |
| - Generates standardized ISL gloss sequence with Non-Manual Markers ([NMM: Furrowed Brow])           |
| - Binds multi-unit Translation Plan (Lexical, Pedagogical, Unsupported)                             |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| STAGE 4: Zero-Fabrication Policy & Accreditation Audit                                              |
| - Audits concept accreditation against deaf master registries and national corpora                  |
| - Prevents synthetic video concatenation for unsupported concepts                                   |
| - Generates pedagogical explanation payload for uncodified tertiary terms                           |
| - Returns final policy verdict (VERIFIED, PARTIAL, EXPLANATION_REQUIRED, UNSUPPORTED)               |
+-----------------------------------------------------------------------------------------------------+
                                                  |
                                                  v
+-----------------------------------------------------------------------------------------------------+
| STAGE 5: Multimodal Visual Media Assembly                                                           |
| - Resolves verified/partially-verified authentic human signing video stream                         |
| - Mounts 3D WebGL anatomical avatar in attentive neutral posture                                    |
| - Calculates total end-to-end pipeline latency (typically 4-15ms)                                   |
+-----------------------------------------------------------------------------------------------------+
```

---

## 3. UI Stepper & Trace Capabilities

In `LivePipelinePanel.tsx`:
- **Interactive Step Navigation:** Allows stepping through stages one by one (Step 1 $\rightarrow$ Step 5) to inspect incremental transformations.
- **Microsecond Precision Timers:** Shows duration of each stage (e.g., `0.35ms`, `1.20ms`).
- **Expandable Diagnostic Payload:** One-click JSON viewer revealing raw token arrays, disambiguation rationales, semantic triples, and spatial loci assignments.
- **Accreditation Audit Card:** Transparently displays cited dataset provenances (`ISLRTC Open Educational Release`) and reviewer credentials.

