# Phase 4.5F Facial Non-Manual Marker (NMM) Audit Report

**Auditor:** ISL Linguistics Researcher & 3D Character Technical Artist  
**Date:** 2026-11-21  
**Subsystem:** Facial Blendshape Rig & Grammatical Non-Manual Marker Synthesis  
**Target Rig:** SignBridge-Articulated-54 Character Mesh  

---

## 1. Executive Summary

In Indian Sign Language, non-manual markers—including movements of the eyebrows, eyes, cheeks, lips, and head orientation—are integral grammatical morphemes that convey syntactic structure, question types, negation, and topicalization.

This audit evaluates the technical implementation and linguistic claims surrounding SignBridge AI's facial animation subsystem.

---

## 2. Technical Blendshape Verification

| Blendshape Target | Rig Implementation | Dynamic Weight Range | Observable Visual Effect | Technical Status |
| :--- | :--- | :--- | :--- | :--- |
| `brow_furrow_left/right` | Vertical translation & inward contraction of eyebrow meshes | $0.00$ to $1.00$ | Eyebrows lower by up to $0.025\text{ units}$ toward nasion | **VERIFIED** |
| `brow_raise_left/right` | Upward vertical elevation of eyebrow meshes | $0.00$ to $1.00$ | Eyebrows raise by up to $0.025\text{ units}$ above rest position | **VERIFIED** |
| `mouth_open` | Vertical scaling of mouth cavity mesh (`scale.y`) | $1.00$ to $3.50$ | Mandible depression simulating open vowel/morpheme mouthing | **VERIFIED** |
| `mouth_wide` | Lateral horizontal scaling of mouth mesh (`scale.x`) | $1.00$ to $2.50$ | Lateral lip retraction (commissure spread) | **VERIFIED** |
| `head_pitch` | Euler X rotation of head transform group | $-0.52$ to $0.60\text{ rad}$ | Head nod forward (affirmation) / backward | **VERIFIED** |
| `head_yaw` | Euler Y rotation of head transform group | $-0.78$ to $0.78\text{ rad}$ | Head turn left/right (spatial referencing) | **VERIFIED** |
| `head_roll` | Euler Z rotation of head transform group | $-0.44$ to $0.44\text{ rad}$ | Lateral head tilt (topic demarcation) | **VERIFIED** |

---

## 3. Seven Mandatory Verification Checks

1. **Blendshape Targets Exist:**
   - Both the backend schema (`FacialBlendshapes` in `backend/app/schemas/avatar.py`) and frontend mesh hooks (`leftEyebrowRef`, `rightEyebrowRef`, `mouthRef` in `AvatarViewer.tsx`) explicitly declare and manipulate these targets.
2. **Blendshape Weights Actually Change:**
   - In `islrtc_algorithm_mocap.json`, mouth opening varies dynamically from $0.00$ to $0.22$, and brow furrow varies up to $0.18$.
   - In `islrtc_beam_mocap.json`, brow furrow rises to $0.32$ during the structural emphasis phase.
3. **Facial Animation Plays at Correct Timestamps:**
   - Facial blendshapes are embedded directly within `AvatarKeyframe` objects, synchronizing frame-for-frame with arm and finger joint transforms.
4. **Facial Motion is Synchronized with Hand Motion:**
   - In question-sentence translation (`assemble_sequence_from_translation_plan`), non-manual markers are applied specifically during the terminal question sign and question particle interval.
5. **Facial Expressions are Not Permanently Active:**
   - At the beginning and end of every animation sequence, resting keyframes (`create_neutral_rest_track`) explicitly reset all blendshape weights to $0.00$.
6. **Facial Movements Do Not Distort Expressions:**
   - Geometric clamping bounds eyebrow translation to a maximum of $\pm 0.025\text{ units}$, preventing mesh clipping into the cranium or eyes.
7. **Missing Facial Data Handling:**
   - When facial landmarks cannot be detected (e.g. low video contrast or partial profile), the system defaults safely to $0.00$ neutral without synthesizing arbitrary grimaces.

---

## 4. Linguistic Grounding & Experimental Boundary

> [!CRITICAL]
> **Experimental Linguistic Hypothesis:**
> The association of:
> - `brow_furrow` with WH-Questions (WHAT, WHERE, WHY, HOW)
> - `brow_raise` with Polar Questions (Yes/No questions and topic markers)
> 
> is grounded in established sign language linguistics literature (Zeshan 2004; Sagara 2014; ISLRTC grammar notes). However, in SignBridge AI, these procedural mappings are **explicitly classified as unvalidated linguistic hypotheses**, not certified ISL grammar rules.
>
> Simple eyebrow animation must never be misrepresented as comprehensive Indian Sign Language Non-Manual Marker proficiency. Native ISL signing incorporates intricate co-occurring mouthings, eye gazes, and body shifts that require extensive native Deaf educator curation.

