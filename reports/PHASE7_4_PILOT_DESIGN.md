# SignBridge AI — Phase 7.4: First Pilot Design & Sign Evaluation Package

**Date:** 2026-11-21  
**Project:** SignBridge AI  
**Workspace:** `E:\SignBridgeAi`  
**Milestone:** Phase 7.4  

---

## 1. Scope & Objective

Phase 7.4 established the evaluation package for the initial controlled validation pilot. Rather than prematurely expanding the vocabulary into unverified terrain, the pilot is deliberately restricted to the five candidate engineering signs currently backed by genuine ISLRTC master recordings.

---

## 2. The Five Pilot Candidate Signs

The complete technical and linguistic dossier was authored at `data/pilot/pilot_five_signs_package.json`:

| Sign Gloss | Discipline | Concept ID | Video Path | Tracking Conf. | Dominant Hand | Movement Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Algorithm** | Computer Science | 1 | `/data/sign_videos/islrtc_algorithm.mp4` | 0.942 | Right | Sequential planar step translation (left-to-right). |
| **Frequency** | Electronics & Comm. | 13 | `/data/sign_videos/islrtc_frequency.mp4` | 0.958 | Right | Oscillatory sinusoidal wave trajectory. |
| **Current** | Electrical & Electronics | 25 | `/data/sign_videos/islrtc_current.mp4` | 0.965 | Two-Handed | Directional forward flow along forearm conduit. |
| **Beam** | Civil Engineering | 37 | `/data/sign_videos/islrtc_beam.mp4` | 0.971 | Two-Handed | Horizontal flat palm across vertical columns. |
| **Torque** | Mechanical Eng. | 49 | `/data/sign_videos/islrtc_torque.mp4` | 0.951 | Two-Handed | Torsional twisting stroke around central axis. |

---

## 3. Evaluation Package Structure

For each of the five signs, the package includes:
1. **Provenance & Legal Clearance:** Official attribution to ISLRTC / DEPwD, Government Open Data License - India (GODL-India), and SHA-256 integrity checksums.
2. **Mocap Tracking Metadata:** Total frame count, tracking confidence score, and joint trajectory characteristics.
3. **Known Technical Limitations:** Fully disclosed to reviewers (e.g., subtle wrist stiffness in *Frequency*, DIP smoothing in *Algorithm*).
4. **12-Factor Phonological Rubric:** Standardized evaluation of Lexical Accuracy, Handshape, Orientation, Location, Movement, Coordination, Facial NMM, Syntax, Technical Context, Fluidity, Regional Dialect, and Semantic Ambiguity.
5. **Reviewer Guidance:** Explicit instructions prompting the reviewer to determine whether the sign conveys the technical engineering concept in ISL without relying on English subtitles.

---

## 4. Phase 7.4 Status Verdict: **PASS**
The five-sign evaluation package is fully compiled, validated against database records, and available as an exportable JSON artifact.

