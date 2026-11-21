# SignBridge AI — 3D ISL Signing Avatar Animation Architecture

**Document Version:** 2.0.0  
**Effective Date:** November 20, 2026  
**Standards:** Zero Fabricated Signs Policy, Three.js WebGL Articulation, Skeletal Motion Retargeting, Non-Manual Marker Synchronization

---

## 1. Overview & Architectural Principles

The 3D Signing Avatar provides an interactive, accessible 3D visualization modality for Deaf engineering students who prefer 3D spatial rendering with customizable camera angles.

### Non-Negotiable Directives:
1. **Zero Random Hand Waves:** Arbitrary procedural hand movements or synthetic ragdoll motions must never be represented as Indian Sign Language.
2. **Skeletal Articulation Standards:** The humanoid avatar is modeled to support full anatomical degrees of freedom:
   - Complete 5-finger articulation (thumb 3 joints, index, middle, ring, pinky).
   - Wrist flex and pronation/supination.
   - Elbow and shoulder 3D rotational ball joints.
   - Head nod, turn, and facial blend shapes for non-manual markers.
3. **Shared Translation IR:** The avatar sequencer consumes the exact same Translation Intermediate Representation (IR) as the human video player, preserving absolute linguistic consistency.

---

## 2. Avatar Animation Sequencing Pipeline

```
Translation Intermediate Representation (IR)
                      ↓
POST /api/v1/avatar/timeline
                      ↓
Timeline Construction:
  - Neutral Rest Pose (0.5s baseline)
  - Sequential Sign Keyframe Lookup per concept
  - Locus Allocation (LOCUS_A on Left, LOCUS_B on Right)
  - Facial Non-Manual Marker Track (Furrowed brow for WH-questions)
  - Neutral Rest Pose (0.5s termination)
                      ↓
Frontend Three.js / React Three Fiber Renderer:
  - AnimationMixer plays validated tracks
  - Camera Presets: Front View, Hands Focus, Face Focus, Side View
  - Variable Playback Speed: 0.5x, 0.75x, 1.0x, 1.5x
  - Transparent Pause Notice if animation is unverified
```

---

## 3. Supported Rigging & Data Formats

- **Target Rig Standards:**
  - **MediaPipe Holistic (54 keypoints):** Standardized landmark format matching the open iSign benchmark.
  - **ReadyPlayerMe / Mixamo Humanoid Standard:** Standardized humanoid bone naming conventions (`LeftHandThumb1`, `LeftHandIndex1`, `Neck`, `Head`).
- **File Containers:** `.glb` (glTF binary format) and `.json` keyframe coordinate arrays.

---

## 4. API Endpoints

### 4.1 Concept Animation Retrieval
- **Endpoint:** `GET /api/v1/avatar/retrieve/{concept_id}`
- **Response:**
  ```json
  {
    "available": false,
    "concept_term": "Deadlock",
    "sign_gloss": "DEADLOCK",
    "validation_status": "unsupported",
    "phonological_parameters": {
      "dominant_hand": null,
      "handshape": null,
      "movement": null
    },
    "message": "Zero-Fabrication Policy: No validated 3D skeletal animation exists for 'Deadlock'. Arbitrary avatar gestures are prohibited."
  }
  ```

### 4.2 Timeline Generation
- **Endpoint:** `POST /api/v1/avatar/timeline`
- **Request:** Translation Intermediate Representation (IR) JSON payload.
- **Response:** Synchronized timeline with sign tracks, start/duration timestamps, spatial loci, and facial blend shape triggers.

### 4.3 Animation Asset Ingestion
- **Endpoint:** `POST /api/v1/avatar/upload`
- **Fields:** `sign_record_id` (int), `animation_name` (str), `rig_standard` (str), `is_mocap` (bool), `file` (UploadFile `.glb`/`.json`).
- **Default Status:** Defaults to `NEEDS_REVIEW` until certified by deaf educators.

---

*Document certified by 3D Animation Engineer & Computer Vision Specialist on November 20, 2026.*

