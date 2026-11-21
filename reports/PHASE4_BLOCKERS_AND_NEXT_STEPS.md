# Phase 4 Blockers, Linguistic Challenges & Next Steps

**Milestone:** Phase 4 Review  
**Project:** SignBridge AI  
**Next Objective:** Phase 5 — Continuous Indian Sign Language Production & Field Evaluation  

---

## 1. Technical & Linguistic Blockers Identified

1. **Depth Ambiguity in Monocular Video Mocap:**
   - Single front-facing 1080p video lacks direct depth sensor ($Z$-axis) data.
   - While MediaPipe estimates relative depth, optical self-occlusion (e.g. one hand crossing directly in front of the other or hands touching the chest) can cause transient depth uncertainty.
   - *Mitigation in Phase 4:* Temporal smoothing (EMA / One-Euro filter) and interpolation mitigate occlusion artifacts.
   - *Phase 5 Recommendation:* Incorporate multi-view studio recordings or stereoscopic capture for critical technical signs.

2. **Accredited Deaf Reviewer Ecosystem:**
   - Currently, reviewer profiles in the database are simulated fixtures (`[Demonstration Profile]`).
   - Authentic certification to `VERIFIED_ISL_MOTION` requires real partnerships with accredited Deaf ISL master instructors from organizations such as ISLRTC, National Association of the Deaf (NAD), or All India Federation of the Deaf (AIFD).
   - *Phase 5 Recommendation:* Establish formal evaluation MoUs with Deaf educational institutions.

3. **Co-Articulation Blending in Continuous Multi-Sign Sentences:**
   - Concatenating isolated lexical signs currently inserts neutral rest postures between concepts to avoid jarring teleportation.
   - Natural human signing features smooth co-articulation (e.g., dominant hand flowing directly from the terminal handshape of *Algorithm* into the onset handshape of *Current*).
   - *Phase 5 Recommendation:* Implement a Bézier curve / quaternion spherical linear interpolation (SLERP) co-articulation transition planner.

4. **Curriculum Vocabulary Coverage:**
   - 5 authentic ISLRTC signs are fully processed into 3D mocap keyframes (`Algorithm`, `Frequency`, `Current`, `Beam`, `Torque`).
   - The remaining 95 concepts in the engineering candidate pool require either additional ISLRTC video acquisition or certified pedagogical explanation classifier routines.

---

## 2. Roadmap for Phase 5

1. **Co-Articulation Transition Blending:** Develop SLERP quaternion interpolation between consecutive lexical signs to eliminate unnatural pauses.
2. **Deaf User Experience Testing:** Conduct structured usability trials with engineering students who are deaf or hard of hearing to measure comprehension rates.
3. **Advanced Facial Blendshape Synthesis:** Connect syntactic question markers directly to real-time speech prosody.
4. **Offline Mobile Package:** Bundle lightweight keyframe runtime for Android/PWA deployment in Indian engineering colleges with limited bandwidth.

