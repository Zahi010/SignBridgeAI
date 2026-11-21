# SignBridge AI — Phase 3 Translation Intermediate Representation (IR) Specification

**Module:** `backend/app/schemas/intermediate_representation.py`  
**Lead AI Systems Architect:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Status:** SPECIFIED, CODED (PYDANTIC V2) & INTEGRATED

---

## 1. Specification Objective

The **Translation Intermediate Representation (IR)** is the central linguistic and multimodal contract for SignBridge AI. It decouples the upstream Natural Language Processing (NLP) stage from the downstream rendering engines:
1. **Authentic Human Signing Video Player**
2. **Interactive 3D WebGL Avatar Engine**
3. **Structured Classroom Pedagogical View**

By decoupling analysis from rendering, the IR guarantees that multimodal outputs reflect identical linguistic constraints, spatial loci, and zero-fabrication policies.

---

## 2. Pydantic Schema Architecture

```
                               +-----------------------------+
                               | IntermediateRepresentation  |
                               +-----------------------------+
                                              |
        +------------------+------------------+------------------+------------------+
        |                  |                  |                  |                  |
        v                  v                  v                  v                  v
+---------------+  +---------------+  +---------------+  +---------------+  +---------------+
| Tokens & POS  |  |   Concepts    |  | Relationships |  |   Discourse   |  |  Translation  |
|   (Syntax)    |  | (Phonology/KB)|  |   (Triples)   |  |   (Grammar)   |  |     Plan      |
+---------------+  +---------------+  +---------------+  +---------------+  +---------------+
```

### 2.1 Core Sub-Schemas

1. **`SemanticConceptIR`:**
   - `id`: Optional concept database primary key.
   - `term`: Canonical English term (e.g., `"Operating System"`, `"Deadlock"`).
   - `category`: Engineering discipline (e.g., `"Computer Systems Architecture"`).
   - `domain`: Contextual domain (e.g., `"Systems Software & Concurrency"`).
   - `canonical_gloss`: Standardized uppercase gloss string (e.g., `"OPERATING-SYSTEM"`).
   - `validation_status`: `VERIFIED`, `PARTIAL`, `EXPLANATION_REQUIRED`, `UNSUPPORTED`.
   - `confidence`: Extraction confidence score (0.0 to 1.0).
   - `disambiguation_rationale`: Human-readable context justification.
   - `phonology`: Optional `PhonologyIR` (dominant hand, handshape, movement, location, orientation, non-manual markers).
   - `has_video`: Boolean flag indicating video asset presence.
   - `video_url`: Video stream path if available.
   - `source_attribution`: Provenance citation (e.g., `"ISLRTC Open STEM Reference"`).

2. **`ConceptRelationshipIR`:**
   - `source_concept`: Subject entity (e.g., `"Processor"`).
   - `target_concept`: Object entity (e.g., `"Memory"`).
   - `relation_type`: Semantic predicate (e.g., `"fetches_instructions_from"`, `"executes"`).
   - `description`: Plain text relationship summary.
   - `triple_string`: Visual representation (`[Processor] -> [executes] -> [Instruction]`).
   - `confidence`: Extraction confidence.

3. **`DiscourseContextIR`:**
   - `sentence_type`: `DECLARATIVE`, `WH_QUESTION`, `POLAR_QUESTION`, `CONDITIONAL`, `COMPARATIVE`.
   - `modality`: `neutral`, `obligation`, `possibility`, `capability`.
   - `temporal_frame`: `present`, `past`, `future`, `general_principle`.
   - `polarity`: `positive` or `negative`.

4. **`NegationMarkerIR`:**
   - `is_negated`: Boolean indicating clause negation.
   - `marker_token`: English negation token (`"not"`, `"never"`, `"cannot"`).
   - `isl_position`: Obligatory `"sentence_final"`.
   - `non_manual_marker`: Mandatory `"Headshake"`.

5. **`InterrogativeIR`:**
   - `is_interrogative`: Boolean indicating question clause.
   - `question_type`: `"WH_QUESTION"` or `"POLAR_QUESTION"`.
   - `wh_word`: Interrogative token (`"what"`, `"how"`, `"why"`).
   - `isl_position`: Obligatory `"sentence_final"`.
   - `non_manual_marker`: Mandatory `"Furrowed Brow"`.

6. **`TemporalMarkerIR`:**
   - `has_temporal`: Boolean indicating time reference.
   - `marker_token`: Time token (`"today"`, `"yesterday"`, `"initially"`).
   - `isl_position`: Obligatory `"sentence_initial"` (Time-First principle).

7. **`SpatialAnchorIR`:**
   - `concept_term`: Concept assigned to signing locus.
   - `locus_id`: `"LOCUS_A"`, `"LOCUS_B"`, `"NEUTRAL_CENTER"`.
   - `spatial_coordinate`: `"left"`, `"right"`, `"center"`.
   - `contrastive_role`: `"agent"`, `"target"`, `"comparator"`.

8. **`TranslationPlanIR`:**
   - `translation_units`: List of planned multimodal sequence units (`TranslationUnitIR`).
   - `total_units`: Integer count.
   - `lexical_count`: Direct video sign count.
   - `explanation_count`: Multi-step pedagogical explanation count.
   - `unsupported_count`: Two-handed fingerspelling fallback count.
   - `overall_strategy_summary`: Descriptive summary string.

---

## 3. JSON Sample Serialization

```json
{
  "source_text": "What is an algorithm?",
  "engineering_branch": {
    "code": "cs",
    "name": "Computer Science & Engineering"
  },
  "context_domain": "Algorithms & Data Structures",
  "tokens": [
    {"index": 0, "text": "What", "lemma": "what", "pos": "PRON", "is_stop": true},
    {"index": 1, "text": "is", "lemma": "be", "pos": "AUX", "is_stop": true},
    {"index": 2, "text": "an", "lemma": "an", "pos": "DET", "is_stop": true},
    {"index": 3, "text": "algorithm", "lemma": "algorithm", "pos": "NOUN", "is_stop": false}
  ],
  "detected_concepts": [
    {
      "id": 5,
      "term": "Algorithm",
      "canonical_gloss": "ALGORITHM",
      "validation_status": "partial",
      "has_video": true,
      "video_url": "/data/sign_videos/islrtc_algorithm.mp4",
      "source_attribution": "ISLRTC Open Educational Release"
    }
  ],
  "discourse_context": {
    "sentence_type": "WH_QUESTION",
    "modality": "neutral",
    "temporal_frame": "present",
    "polarity": "positive"
  },
  "interrogative": {
    "is_interrogative": true,
    "question_type": "WH_QUESTION",
    "wh_word": "what",
    "isl_position": "sentence_final",
    "non_manual_marker": "Furrowed Brow"
  },
  "translation_plan": {
    "total_units": 2,
    "lexical_count": 1,
    "explanation_count": 0,
    "unsupported_count": 0,
    "translation_units": [
      {
        "unit_id": 1,
        "source_segment": "Algorithm",
        "strategy": "LEXICAL_SIGN_DIRECT",
        "assigned_gloss": "ALGORITHM",
        "video_resource_ref": "/data/sign_videos/islrtc_algorithm.mp4",
        "rationale": "Authentic ISL sign video available (PARTIAL). Sourced from ISLRTC Open Educational Release."
      },
      {
        "unit_id": 2,
        "source_segment": "what",
        "strategy": "LEXICAL_SIGN_DIRECT",
        "assigned_gloss": "WHAT [NMM: Furrowed Brow]",
        "rationale": "ISL positions interrogatives at sentence-final position, synchronized with furrowed eyebrows."
      }
    ]
  }
}
```

