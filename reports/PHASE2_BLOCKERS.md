# SignBridge AI — Phase 2: Authentic ISL Data Acquisition & Technical Blockers Report

**Milestone:** Phase 2: Authentic ISL Data Acquisition & Signing Dataset Development  
**Date:** 2026-11-20  
**Lead AI Systems Auditor & Technical Architect:** Senior AI Systems Auditor & ISL Research Team  
**Status:** ACTIVE GOVERNANCE & FORMAL DEPENDENCY AUDIT  

---

## 1. Executive Summary

This report provides an uncompromised, evidence-based assessment of the foundational blockers, legal restrictions, ethical boundaries, and technical barriers that prevent off-the-shelf automated Indian Sign Language (ISL) translation for university-level engineering education.

Software systems often fabricate fluent signing by concatenating isolated dictionary clips or driving anatomical 3D mannequins with procedural inverse kinematics. In academic sign linguistics and Deaf pedagogy, **such approaches are categorically invalid**:
1. ISL is a natural visual-spatial language with its own morphology, topic-comment grammar, spatial classifiers, and non-manual markers (facial expressions, head tilts, mouth morphemes).
2. Concatenating English words translated into isolated signs yields ungrammatical "Signed English" rather than authentic ISL.
3. Over 70% of tertiary engineering terminology is currently **non-codified** as single lexical signs in Indian Sign Language.

SignBridge AI adheres to a strict **zero-fabrication principle**: when authentic signing data or validated lexical signs are unavailable, the platform reports `UNSUPPORTED` or `EXPLANATION_REQUIRED` and maintains the 3D avatar in a neutral resting pose.

---

## 2. Technical Blockers

### Blocker 2.1: The Specialized Engineering Terminology Deficit
- **Observation:** Publicly accessible Indian Sign Language corpora (ISLRTC 10,000-word glossary, NDLI, INCLUDE, CISLR, Sign Dictionary ISL) provide comprehensive coverage of daily conversational terms and foundational primary/secondary STEM concepts (*Force*, *Current*, *Voltage*, *Computer*, *Machine*, *Friction*).
- **The Deficit:** Advanced university-level engineering concepts across Computer Science, Electronics, Mechanical, Civil, and Electrical branches (*e.g., Deadlock, Compiler Intermediate Representation, Modulation Index, Finite Element Analysis, Prestressed Concrete, Synchronous Reluctance Motor*) have **never been formally codified as single lexicalized signs** in any standard ISL lexicon.
- **Classroom Reality:** In Indian Deaf engineering classrooms, educators and students negotiate meaning dynamically through:
  - Two-handed ISL fingerspelling for technical acronyms (e.g., `D-B`, `O-S`, `M-C-U`, `F-E-A`, `R-C-C`).
  - Spatial classifier predicates tracing physical mechanisms (e.g., depicting current induction or resource deadlock).
  - Bilingual whiteboard diagrams and visual schematics coupled with contextualized gestures.
- **Architectural Safeguard:** SignBridge AI rejects naive dictionary lookups. Terms without validated lexical signs are routed through the pedagogical explanation pipeline or marked `UNSUPPORTED`.

### Blocker 2.2: Absence of 54-Keypoint 3D Motion-Capture Corpora
- **Observation:** Standard 3D animation platforms drive avatars using `.bvh` or `.fbx` skeletal animation files.
- **The Deficit:** There is **zero publicly available, legally licensed 3D motion capture dataset** for Indian Sign Language that captures full-body, facial morphemes, and bilateral finger articulations (54 skeletal keypoints).
- **Failure of Monocular 2D-to-3D Lifting:**
  - Automated extraction using MediaPipe Holistic or OpenPose on monocular 2D web videos suffers from severe depth ambiguity (z-axis collapse).
  - Self-occlusion during two-handed signs (*e.g., finger contact in Database, Transformer, or Current*) results in catastrophic wrist twisting and finger swapping.
  - Facial keypoint estimation on low-framerate (24-30 fps) footage fails to capture subtle non-manual grammatical markers (eyebrow furrowing for wh-questions, lip compression for resistance).
- **Architectural Safeguard:** SignBridge AI prohibits procedural avatar animation generation for unverified signs. The 3D avatar maintains a neutral resting posture (`UNAVAILABLE_PENDING_MOCAP`) until laboratory-grade motion capture data is ingested.

---

## 3. Legal & Licensing Blockers

| Resource / Corpus | Primary Institution | Licensing Terms | Direct Commercial Software Use | Ingestion Barrier / Obligation |
| :--- | :--- | :--- | :--- | :--- |
| **ISLRTC 10k Glossary** | Ministry of Social Justice & Empowerment (MSJE), Govt of India | Government Open Data License (GODL-India) | **Restricted** (Requires attribution; cannot claim endorsement or modify government videos) | Videos cannot be resold or used in closed proprietary models without formal MOU from MSJE. |
| **INCLUDE Corpus** | AI4Bharat / IIT Madras (ACM MM 2020) | Creative Commons Non-Commercial (CC BY-NC 4.0) | **PROHIBITED** (Commercial use strictly prohibited) | Can only be utilized for non-profit academic research. Ingestion into a commercial production engine violates copyright. |
| **ISLTranslate** | Academic Consortium (ACL 2023) | CC BY-NC 4.0 | **PROHIBITED** | Limited strictly to non-commercial benchmarking and linguistic research. |
| **Sign Dictionary ISL** | Bridgeconn Community | Creative Commons ShareAlike (CC BY-SA 4.0) | **Conditional** (Requires reciprocal copyleft sharing) | Any derivative dataset or system packaging these signs must be released under identical open-source copyleft terms. |
| **Web/YouTube Scraping** | Unaffiliated Creators | Standard YouTube License / All Rights Reserved | **ILLEGAL** | Scraping videos without explicit copyright holder authorization violates copyright law and platform terms of service. |

---

## 4. Ethical, Biometric & Signer Consent Blockers

### Blocker 4.1: Biometric Privacy & DPDPA 2023 Compliance
- Indian Sign Language videos capture high-resolution imagery of the human face, eyes, dental articulation, and hand geometry.
- Under the **Digital Personal Data Protection Act (DPDPA 2023)** of India and international ethical standards (GDPR Article 9 for biometric data):
  1. Facial imagery of signers constitutes sensitive biometric personal data.
  2. Scraping or training AI models on human signing videos without explicit, informed, revocable consent is legally actionable.
  3. SignBridge AI mandates an explicit `ConsentStatus` model:
     - `verified_consent`: Signed consent form detailing educational distribution.
     - `pending_consent`: Sign recorded but quarantined until documentation clears.
     - `restricted_educational`: Permitted solely for classroom research.
     - `exempt_open_government`: Official government open data with public release mandate.

### Blocker 4.2: Exploitative Data Practices in Deaf Communities
- The Deaf community in India has historically experienced data extraction by researchers who publish papers or build tools without community benefit, attribution, or involvement.
- **Governance Requirement:**
  - Deaf native signers must be treated as co-researchers and acknowledged contributors, not merely data points.
  - Accredited Deaf educators must hold veto power over sign validation. Developer test accounts are structurally prevented from approving signs (`403 Forbidden`).

---

## 5. Standard Studio Recording Protocols (SignBridge Protocol v1.0)

To resolve data gaps lawfully and linguistically, SignBridge AI has codified the following official recording standard for future studio sessions:

```
+-----------------------------------------------------------------------------------+
|                        SIGNBRIDGE ISL STUDIO PROTOCOL                              |
+-----------------------------------------------------------------------------------+
| 1. HARDWARE SPECIFICATIONS:                                                       |
|    - Primary Camera: Frontal 4K/60fps (minimum 1080p60), global shutter.          |
|    - Secondary Camera: 45-degree oblique angle for z-axis spatial depth.          |
|    - Sensor Focal Length: 50mm equivalent (prevents wide-angle barrel distortion).|
|                                                                                   |
| 2. LIGHTING & ENVIRONMENT:                                                        |
|    - Lighting: 3-point flicker-free LED softboxes (5600K daylight balanced).      |
|    - Lux Level: Minimum 800 lux evenly distributed across face and hand zone.     |
|    - Backdrop: Matte non-reflective 18% neutral gray or studio chroma green.       |
|    - Attire: Plain matte navy/dark crewneck contrasting with signer skin tone.    |
|    - Accessories: Zero wristwatches, rings, or reflective jewelry.                |
|                                                                                   |
| 3. PERSONNEL & ACCREDITATION:                                                     |
|    - Signer: Certified Deaf native signer with STEM educational background.       |
|    - Monitor: Licensed RCI ISL Interpreter (Group A/B certified).                 |
|    - Linguistic Supervisor: Deaf educator verifying non-manual markers.           |
|                                                                                   |
| 4. METADATA & DOCUMENTATION:                                                      |
|    - Institutional Consent Form (DPDPA compliant) signed prior to session.       |
|    - 2-second neutral rest hold before and after each sign.                       |
|    - Audio/visual clapperboard with unique Session UID (e.g. REC-20261120-CS-01).  |
+-----------------------------------------------------------------------------------+
```

---

## 6. Path to Resolution: Staged Roadmap

1. **Short Term (Current Milestone):**
   - Maintain strict system honesty (`NEEDS_REVIEW`, `UNSUPPORTED`, `EXPLANATION_REQUIRED`).
   - Block developer bypass of validation.
   - Enforce ingestion validation (FFprobe stream checks, format quarantine, consent tracking).
2. **Medium Term (Phase 3 Pilot):**
   - Formalize institutional partnership with ISLRTC / Rehabilitation Council of India (RCI) for curated STEM video licensing.
   - Convene an ISL Engineering Terminology Working Group composed of Deaf STEM graduates to codify the 30 priority concepts.
3. **Long Term (Phase 4):**
   - High-density optical motion capture studio recording (Vicon/OptiTrack 54-keypoint) with certified signers.
   - Fine-tuned transformer-based ISL generation driven by true spatial grammar rather than word-for-word glossing.

