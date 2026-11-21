# SignBridge AI — Phase 3 Translation Planner Specification

**Module:** `backend/app/services/translation_planner.py`  
**Lead AI Systems Architect:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Status:** FULLY INTEGRATED & OPERATIONAL

---

## 1. Objective & Philosophy

The **Engineering Translation Planner** resolves the fundamental limitation of naive sign language prototypes: blind word-for-word string replacement or arbitrary procedural gesture generation.

In engineering education, technical concepts fall into distinct linguistic and resource categories:
1. **Lexical Signs:** Concepts possessing authentic, standardized ISL signs (e.g., *Algorithm*, *Current*, *Frequency*, *Beam*, *Torque*).
2. **Pedagogical Explanations:** Abstract, composite mechanisms lacking single atomic dictionary signs but well-supported through structured visual classifier sequences (e.g., *Deadlock*, *Compiler*, *Modulation*, *Finite Element Analysis*).
3. **Unsupported Non-Codified Terms:** Specialized terms with no established ISL representation that must honestly fall back to two-handed ISL fingerspelling without fabricating artificial gestures.

The Translation Planner evaluates the Structured Intermediate Representation (IR), inspects asset availability in the database, and builds an explicit, multi-unit multimodal execution plan.

---

## 2. Translation Planning Pipeline

```
                                 +-----------------------+
                                 |  INPUT: Structured IR  |
                                 +-----------------------+
                                             |
                 +---------------------------+---------------------------+
                 |                           |                           |
                 v                           v                           v
      +---------------------+     +---------------------+     +---------------------+
      | 1. TEMPORAL PRIMACY |     | 2. TOPIC CONCEPTS   |     | 3. SPATIAL RELATIONS|
      | Prepend time words  |     | Classify into:      |     | Assign LOCUS A/B    |
      | (Time-First rule)   |     | - Direct Lexical    |     | Map directional     |
      |                     |     | - Pedagogical Plan  |     | relational verbs    |
      |                     |     | - Fingerspelling    |     |                     |
      +---------------------+     +---------------------+     +---------------------+
                 |                           |                           |
                 +---------------------------+---------------------------+
                                             |
                 +---------------------------+---------------------------+
                 |                                                       |
                 v                                                       v
      +---------------------+                                 +---------------------+
      | 4. FINAL NEGATION   |                                 | 5. FINAL WH-QUESTION|
      | Append NOT + NMM    |                                 | Append WH + Furrow  |
      | (Negative headshake)|                                 | eyebrow marker      |
      +---------------------+                                 +---------------------+
                                             |
                                             v
                           +-----------------------------------+
                           | OUTPUT: TranslationPlanIR         |
                           | Transparent, audited unit stream  |
                           +-----------------------------------+
```

---

## 3. Translation Strategies Defined

### 3.1 `LEXICAL_SIGN_DIRECT`
- **When Applied:** Concept possesses an authentic human signing video (`validation_status` in `VERIFIED` or `PARTIAL`).
- **Output:** Assigns canonical ISL gloss, binds video file path, and specifies source attribution.
- **Example:** `"Algorithm"` $\rightarrow$ `ALGORITHM` (`islrtc_algorithm.mp4`).

### 3.2 `PEDAGOGICAL_EXPLANATION`
- **When Applied:** Concept is abstract or composite with `validation_status` in `EXPLANATION_REQUIRED` or `EXPLANATION_NEEDED` (e.g., *Modulation*, *Compiler*, *FEA*).
- **Output:** Binds a 4-step pedagogical sequence:
  1. Two-handed ISL fingerspelling of the English term.
  2. Spatial locus establishment.
  3. Visual classifier demonstration (e.g., carrier sinusoidal wave combined with audio envelope).
  4. Pedagogical text explanation for deaf engineering students.

### 3.3 `UNSUPPORTED_FINGERSPELLING`
- **When Applied:** Concept has no codified sign and no video asset (`validation_status == UNSUPPORTED`).
- **Output:** Explicitly flags uncodified status, generates two-handed ISL fingerspelling letter sequence, and disables video playback to prevent misleading concatenation.
- **Zero-Fabrication Guarantee:** Never invents synthetic procedural gestures.

### 3.4 `RELATIONAL_SPATIAL_INDEX`
- **When Applied:** Interacting concept pairs detected in Subject-Predicate-Object triples.
- **Output:** Positions `Concept 1` at `LOCUS_A` (left), `Concept 2` at `LOCUS_B` (right), and plans directional movement between loci.

---

## 4. Verification Evidence

- `backend/tests/test_phase3_translation.py::test_translation_plan_generation_multi_concept`: **PASS**
- Unit breakdown generated for multi-concept queries:
  - Lexical signs, pedagogical units, and fingerspelling units accurately counted and surfaced in API response and frontend UI card.

