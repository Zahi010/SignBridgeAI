# SIGNBRIDGE AI — LIMITATIONS AND RESEARCH ROADMAP

**Document Version:** Phase 8.5 (Verified Prototype)  
**Project:** SignBridge AI — Indian Sign Language Translation for STEM Higher Education  
**Document Classification:** Academic Integrity & Technical Limitations Disclosure  
**Target Audience:** College Project Evaluation Committee, External Reviewers, Collaborating Researchers  
**Date:** 2026-11-23  

---

## 1. Principle of Academic & Scientific Honesty

In accordance with our **Zero-Fabrication Policy**, this document transparently records the boundaries of our current implementation.

SignBridge AI is an **engineering research prototype**, not a commercially certified or linguistically complete machine translation product. We explicitly distinguish between our implemented software achievements and our remaining research objectives.

---

## 2. Transparently Documented Limitations

### 2.1 Lexical Inventory Coverage
* **Current Boundary:** The platform currently indexes 5 fully retargeted benchmark engineering signs (*Algorithm*, *Frequency*, *Current*, *Beam*, *Torque*), supplemented by 4 core technical concepts (*Database*, *Computer Network*, *Machine*, *Voltage*), and structured pedagogical fallback cards for emerging terms (*Backpropagation*, *Deadlock*).
* **Limitation:** Comprehensive engineering education requires thousands of technical terms. The vocabulary must be expanded in co-design workshops with Deaf educators before full semester-long classroom deployment.

### 2.2 External Linguistic Validation Status (Gate B Locked)
* **Current Boundary:** Technical tracking confidence scores (0.942–0.971) measure MediaPipe landmark tracking stability and kinematic retargeting precision—**not linguistic naturalness or Deaf user comprehension**.
* **Limitation:** All five candidate signs remain strictly `PENDING_EXTERNAL_REVIEW`. Gate B cannot be unlocked until independent, accredited Deaf native signers and RCI-certified interpreters evaluate the signs through the Reviewer Portal.

### 2.3 Monocular Motion Capture & Depth Occlusion
* **Current Boundary:** Landmark tracking is derived from 2D monocular master signer video recordings using MediaPipe Holistic.
* **Limitation:** When one hand crosses directly in front of the other (hand-on-hand occlusion) or touches the torso, single-camera tracking exhibits minor depth ambiguity and finger jitter. While anatomical joint limit clamping and Savitzky-Golay filtering mitigate erratic movements, studio multi-camera or optical mocap is required for millimeter-level fidelity.

### 2.4 Non-Manual Markers (NMM) & Facial Animation
* **Current Boundary:** The 3D avatar rig articulates arms, shoulders, wrists, and 15 hand phalanges per hand.
* **Limitation:** Facial expressions, eye gaze shifts, mouth morphemes (mouthing of technical terms), and head tilts are not yet dynamically retargeted. In Indian Sign Language, non-manual markers carry essential grammatical and interrogative information.

### 2.5 Sentence-Level ISL Syntactic Grammar
* **Current Boundary:** The spaCy dependency transformation engine converts English SVO structures into canonical ISL Time-First and Topic-Comment order based on 28 core syntactic rules.
* **Limitation:** Complex compound-complex sentences with nested relative clauses, spatial classifier predicates, and role-shifting cannot be fully solved by rule-based grammar alone. They represent experimental hypotheses requiring extensive linguistic validation.

### 2.6 Institutional Partnerships
* **Current Boundary:** 12 premier Indian institutions are verified in the Outreach CRM with official public contacts and custom collaboration proposals prepared.
* **Limitation:** Exactly **0 formal Memoranda of Understanding (MoUs)** have been signed to date. All 12 institutions remain classified as prospective collaborators (`POTENTIAL_COLLABORATOR`).

---

## 3. Four-Phase Future Research Roadmap

```
Phase 9: External Linguistic Pilot & RCI Panel Review (Months 1–3)
├── Issue formal invitation codes to accredited Deaf signers & interpreters
├── Execute independent 5-criteria rubric scoring across 5 benchmark signs
├── Achieve sample size target (N >= 15 independent evaluations per sign)
└── Calculate inter-rater agreement (Fleiss' Kappa >= 0.60)
         │
         ▼
Phase 10: Facial Non-Manual Marker (NMM) Retargeting (Months 4–6)
├── Integrate MediaPipe 468-point Face Mesh retargeting to avatar face rig
├── Implement facial blendshapes (eyebrows raised/furrowed, eye gaze)
├── Synchronize mouth morphemes for key technical terminology
└── Conduct A/B comprehension tests with Deaf engineering students
         │
         ▼
Phase 11: Co-Design Workshops & Vocabulary Expansion (Months 7–9)
├── Partner with DEF (EduSign Academy) and ISLRTC
├── Host participatory sign co-design workshops with Deaf STEM students
├── Expand technical lexicon from 5 to 50 codified engineering signs
└── Codify structural pedagogical cards for 100 emerging concepts
         │
         ▼
Phase 12: Controlled Classroom Demonstration Pilot (Months 10–12)
├── Deploy sandbox SignBridge AI in hybrid engineering lectures
├── Measure student comprehension lift against English text captions
├── Evaluate cognitive load and avatar visual fatigue
└── Publish open-source dataset and peer-reviewed journal paper
```
