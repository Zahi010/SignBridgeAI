# SignBridge AI — Phase 5.1: Validation Architecture & Linguistic Rubric

**Author:** Senior ISL Linguistics Specialist & Systems Architect  
**Milestone:** Phase 5 — ISL Community Review, Expert Validation & Academic Evaluation Framework  
**Project:** SignBridge AI (`E:\SignBridgeAi`)  

---

## 1. Architectural Philosophy: Linguistic Correctness vs. Software Functionality

Phase 4.5 established technical motion fidelity (Normalized Mean Landmark Error $< 3.9\%$, 60 FPS WebGL rendering, One-Euro adaptive jitter reduction). However, **software correctness and kinematic smoothness do not establish linguistic validity**. A 3D avatar executing an impossible or corrupted sign smoothly remains linguistically invalid.

Phase 5 establishes the formal architecture to evaluate whether signs generated or retargeted by SignBridge AI are:
1. **Linguistically Correct:** Conforming to the phonological parameters of Indian Sign Language (Handshape, Orientation, Location, Movement, Non-Manual Features).
2. **Understandable:** Free from polysemic confusion or syntactic distortion.
3. **Natural:** Exhibiting human-like rhythm, acceleration, and ease of perception for native Deaf signers.
4. **Culturally Appropriate:** Respecting Deaf community conventions and regional dialectal variations.

```
+-----------------------------------------------------------------------------------+
|                           EVIDENCE HIERARCHY GATEWAY                              |
+-----------------------------------------------------------------------------------+
| Level 1: Code Exists            --> Solvers, Rig, WebGL, APIs in Repository        |
| Level 2: Code Executes          --> 93/93 Pytest passing, Vite build clean        |
| Level 3: Feature Works          --> Dual-engine synchronized comparison functional|
| Level 4: Technically Accurate   --> NMLE < 3.9%, Joint Clamping, Smoothing        |
+-----------------------------------------------------------------------------------+
| >>> STRICT LINGUISTIC GATE (Requires Qualified Accredited Human Review) <<<       |
+-----------------------------------------------------------------------------------+
| Level 5: Linguistically Valid   --> Certified Deaf ISL Expert & RCI Interpreter  |
|                                     Sign-Off via Structured 12-Criterion Rubric   |
+-----------------------------------------------------------------------------------+
```

---

## 2. The 12-Criterion Linguistic Evaluation Rubric

SignBridge AI implements a configurable, multi-dimensional evaluation rubric capturing the full phonological and grammatical matrix of Indian Sign Language:

| # | Criterion | Linguistic Focus | Evaluation Scope |
| :-: | :--- | :--- | :--- |
| **1** | **Lexical Sign Correctness** | Core Vocabulary | Confirms whether the lexical base sign corresponds to standard Indian Sign Language vocabulary rather than ASL, BSL, or an invented gesture. |
| **2** | **Handshape** | Phonological Primaries | Evaluates finger extension, knuckle flexion (MCP, PIP, DIP), thumb opposition, and adherence to canonical ISL handshape inventories (e.g., Open-B, S-Fist, 1-Index, C-Hand). |
| **3** | **Palm & Finger Orientation** | Spatial Orientation | Evaluates the anatomical direction faced by the palm and fingers relative to the signer's torso, head, and interacting hand. |
| **4** | **Signing Location** | Spatial Anchor | Checks that the sign is produced in the appropriate signing space (neutral chest space, chin, temple, forehead, or base non-dominant hand). |
| **5** | **Movement Trajectory** | Kinematic Stroke | Audits the stroke trajectory, repetition (single vs. iterated strokes for nouns vs. verbs), acceleration, and boundary deceleration. |
| **6** | **Dominant / Non-Dominant Coordination** | Bimanual Phonotactics | In two-handed signs, validates symmetry conditions (both active) or dominance conditions (base hand passive, dominant hand articulating). |
| **7** | **Non-Manual Facial Markers (NMM)** | Affective & Grammatical | Inspects eyebrow position (furrowed for WH-questions, raised for Polar questions), mouth morphemes, eye aperture, and head tilts. |
| **8** | **Grammatical Correctness** | Syntactic Structure | In multi-sign sequences, validates Topic-Comment word order, temporal anchoring, spatial agreement, and directional verb inflection. |
| **9** | **Contextual Engineering Meaning** | Semantic Precision | Ensures specialized STEM concepts (e.g., electrical *Current* vs. temporal *current*, structural *Beam* vs. optical *beam*) are disambiguated without polysemic confusion. |
| **10** | **Naturalness & Fluidity** | Perceptual Ergonomics | Assesses whether the animation feels human and comfortable to perceive over sustained educational lectures without visual fatigue. |
| **11** | **Regional / Community Variation** | Sociolinguistic Scope | Notes whether the sign follows Delhi/Northern ISLRTC standards, Western (Mumbai/Pune), Southern (Chennai/Bengaluru), or Eastern dialectal variants. |
| **12** | **Ambiguity & Alternative Interpretations** | Misperception Risk | Identifies whether the sign could be misread as an unrelated everyday gesture or an inappropriate homophenic sign. |

---

## 3. Standardized Rating Scales

Every criterion is evaluated using a 6-point standardized ordinal scale:

1. **`PASS`**: The criterion fully complies with ISL phonological and grammatical standards. No communicative impediment.
2. **`MINOR_ISSUE`**: Slight cosmetic or timing imperfection that does not compromise intelligibility or alter meaning (e.g., slight stiffness in deceleration).
3. **`MAJOR_ISSUE`**: Phonological defect that renders the sign non-standard or difficult to perceive (e.g., thumb tucked instead of opposed).
4. **`INCORRECT`**: Phonemic corruption that changes the meaning to a different concept or produces an illegal ISL sign.
5. **`NOT_APPLICABLE`**: The criterion does not apply to this sign (e.g., base-hand coordination for a one-handed sign).
6. **`UNABLE_TO_ASSESS`**: The reviewer cannot reach a determination due to occlusion, camera perspective, or missing contextual evidence.

---

## 4. The Critical Phonological Error Gate

A naive weighted average score (e.g., averaging 11 "Pass" scores with 1 "Incorrect" score to yield a 92% pass) is fundamentally unscientific in sign language linguistics. In phonology, **a single incorrect handshape or inverted palm orientation completely corrupts a sign**, just as substituting a single consonant in spoken language turns "pat" into "bat".

### Enforced Algorithmic Safeguard
In `backend/app/services/validation_service.py`:
```python
# If any criterion is rated MAJOR_ISSUE or INCORRECT, recommendation cannot be 'accept'
if has_critical_error and overall_recommendation.lower() == "accept":
    evaluation.overall_recommendation = "needs_revision"
```
- If a reviewer flags any criterion as `MAJOR_ISSUE` or `INCORRECT`, the system **programmatically locks the overall recommendation** to `NEEDS_REVISION` or `REJECT`.
- An evaluation with critical phonological errors can **never** approve an animation as representative ISL.

---

## 5. Timestamped Annotation Architecture

To bridge the gap between high-level critique and engineering retargeting fixes, reviewers can anchor feedback to exact millisecond timestamps on the synchronized player:

```json
{
  "task_id": 5,
  "timestamp_ms": 1420,
  "duration_ms": 300,
  "target_type": "comparison",
  "category": "handshape_error",
  "comment": "Index finger collapses into palm at inflection peak; must remain extended."
}
```

Categories supported:
- `handshape_error`: Knuckle or finger flexion discrepancy.
- `movement_jerk`: Unnatural velocity spike or filter lag.
- `orientation_flaw`: Inverted wrist pitch or roll.
- `expression_missing`: Missing brow raise or mouth morpheme.
- `timing_lag`: Depth foreshortening discrepancy.
- `general`: Broad pedagogical or linguistic commentary.
