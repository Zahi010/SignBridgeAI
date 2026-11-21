# SignBridge AI — Context-Aware Semantic Translation Engine Architecture

**Document Version:** 2.0.0  
**Effective Date:** November 20, 2026  
**Standards:** Zero Fabricated Signs Policy, Context-Aware Disambiguation, Topic-Comment ISL Grammar, Shared Translation Intermediate Representation (IR)

---

## 1. Executive Translation Pipeline Architecture

The translation engine transforms raw English technical engineering text into authentic, grammatically ordered Indian Sign Language representations through an independently verifiable 5-stage pipeline:

```
INPUT TEXT (English Technical Discourse)
                     ↓
STAGE 1: Input Preprocessing & Tokenization
  - Case normalization, punctuation stripping, interrogative/negation isolation
  - Sentence typology classification (DECLARATIVE, WH_QUESTION, POLAR_QUESTION, CONDITIONAL, COMPARATIVE)
                     ↓
STAGE 2: Semantic Concept Recognition & Disambiguation
  - Multi-word phrase matching against 100 candidate engineering concepts
  - Contextual disambiguation (e.g. electrical Current vs temporal current)
  - Semantic relationship extraction between interacting entities
  - Branch and technical domain inference
                     ↓
STAGE 3: ISL Syntactic Restructuring & Gloss Planning
  - Topic-Comment constituent ordering
  - Sentence-final WH-movement with Non-Manual Markers ([NMM: Furrowed Brow])
  - Spatial Loci assignment (LOCUS_A on Left, LOCUS_B on Right)
  - Directional agreement predicates
                     ↓
STAGE 4: Zero-Fabrication Policy & Accreditation Audit
  - Evaluates weakest concept validation status
  - Enforces UNSUPPORTED for uncodified terms (e.g. Deadlock, Pointer)
  - Generates structured pedagogical explanations and fingerspelling guidance
                     ↓
STAGE 5: Multimodal Visual Media Assembly & Unified IR Synthesis
  - Resolves verified human signing videos
  - Mounts 3D WebGL anatomical avatar
  - Emits unified JSON Translation Intermediate Representation (IR)
```

---

## 2. Contextual Disambiguation Engine

Polysemous words that hold both common and specialized engineering meanings are disambiguated using co-occurrence triggers and syntactic context:

| Term | Context 1: Common / Colloquial Meaning | Context 2: Technical Engineering Meaning | Disambiguation Engine Rule |
| :--- | :--- | :--- | :--- |
| **`Current`** | Temporal adjective: *"Current research focuses on AI."* | Electrical charge flow: *"Current flows through a resistor."* | If co-occurring with `research`, `trends`, `year`, `state` -> Filtered out. If co-occurring with `voltage`, `flow`, `resistor`, `circuit` -> Extracted as Electrical Current (`ECE/EEE`). |
| **`Stress`** | Psychological emotion: *"Exam stress affects students."* | Mechanical load per area: *"Mechanical stress on the concrete beam."* | Checked for `concrete`, `beam`, `load`, `strain`, `shear`, `MPa`. |
| **`Power`** | Political/colloquial influence. | Mechanical/Electrical energy per second ($P = VI$ or $P = \tau\omega$). | Checked for `grid`, `system`, `transmission`, `watts`, `engine`, `torque`. |
| **`Memory`** | Human cognitive recall. | Semiconductor address space (RAM / Cache). | Checked for `virtual`, `operating system`, `processor`, `cache`, `stack`. |

---

## 3. Translation Intermediate Representation (IR) Specification

The unified Translation IR is shared directly between the human video retrieval service, the 3D WebGL avatar player, and the frontend workspace:

```json
{
  "source_text": "Explain how an operating system works with memory.",
  "detected_branch": {
    "code": "cs",
    "name": "Computer Science & Engineering"
  },
  "detected_subject": {
    "code": "CS301",
    "name": "Operating Systems"
  },
  "context_domain": "Systems Software & Memory Management",
  "token_analysis": [
    {"token": "Explain", "type": "lexical"},
    {"token": "how", "type": "interrogative"},
    {"token": "operating", "type": "lexical"},
    {"token": "system", "type": "lexical"}
  ],
  "detected_concepts": [
    {
      "term": "Operating System",
      "validation_status": "explanation_needed",
      "disambiguation_rationale": "Unambiguous technical terminology matched in engineering knowledge base.",
      "dominant_hand": "Two-Handed",
      "handshape": "Open-5 hands transitioning to interlocking C-shapes"
    },
    {
      "term": "Memory",
      "validation_status": "verified",
      "disambiguation_rationale": "Hardware RAM storage indexed in systems software context.",
      "dominant_hand": "Two-Handed",
      "handshape": "Modified L-handshape indicating storage grid"
    }
  ],
  "semantic_relations": [
    {
      "source_concept": "Operating System",
      "target_concept": "Memory",
      "relation_type": "manages_allocation_of",
      "description": "The Operating System manages virtual address spaces and physical Memory allocation."
    }
  ],
  "isl_grammar_plan": {
    "sentence_type": "WH_QUESTION",
    "gloss_sequence": [
      "OPERATING-SYSTEM",
      "MEMORY",
      "EXPLAIN-CLARIFY",
      "WORK-FUNCTION",
      "HOW [NMM: Furrowed Brow]"
    ],
    "spatial_loci": [
      {"concept": "Operating System", "locus": "LOCUS_A (Left Spatial Coordinate)"},
      {"concept": "Memory", "locus": "LOCUS_B (Right Spatial Coordinate)"}
    ]
  },
  "policy_verdict": {
    "overall_status": "explanation_needed",
    "pedagogical_guidance": [
      {
        "term": "Operating System",
        "why_unsupported": "Base sign compound exists, but kernel mechanics require pedagogical explanation.",
        "recommended_isl_strategy": "Sign base compound OPERATING-SYSTEM, then visually unpack kernel layers."
      }
    ]
  },
  "asset_resolution": {
    "has_video": false,
    "has_avatar": true,
    "avatar_rig": "MediaPipe-Holistic / ReadyPlayerMe"
  }
}
```

---

## 4. 50-Sentence Benchmark Evaluation

The translation engine is continuously evaluated against an automated suite of **50 diverse engineering sentences** (`data/evaluation_set_50.json`):
- Simple definitions (6)
- Technical questions (5)
- Comparisons (5)
- Multi-concept interactions (5)
- Semantic relationships (5)
- Unsupported concepts enforcing Zero Fabrication (7)
- Contextual disambiguation challenges (4)
- Conditional statements (3)
- Complex engineering systems (10)

Benchmark test: `backend/tests/test_translation_evaluation.py` verifies 100% policy compliance, zero hallucinated signs, and sub-10ms response latency.

---

*Document certified by Lead AI Engineer & ISL Linguistics Specialist on November 20, 2026.*

