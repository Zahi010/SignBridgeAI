# SignBridge AI — Phase 3 3D Avatar Foundation Specification

**Components:** `frontend/src/components/avatar/AvatarViewer.tsx` & `backend/app/services/avatar_animation.py`  
**Lead 3D Animation & Computer Vision Engineer:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Status:** SPECIFIED, CODED (THREE.JS / REACT THREE FIBER) & ZERO-FABRICATION VERIFIED

---

## 1. Objective & Ethical Posture

Generating arbitrary procedural gestures that resemble sign language but lack phonological correctness is a widespread defect in sign language software. For deaf engineering students, synthetic hand movements that lack authentic handshapes, orientation, and non-manual markers are unintelligible.

SignBridge AI strictly enforces the **Zero-Fabrication Policy** for 3D animation:
1. **Neutral Resting Posture by Default:** In the absence of validated motion capture (mocap) data, the 3D humanoid avatar maintains an attentive neutral posture with natural idle breathing and eye contact.
2. **Prohibition of Procedural Invention:** The system never synthesizes fake random signing motions.
3. **54-Keypoint Mocap Compatibility:** The underlying animation sequencer and rigged mesh are engineered to consume genuine 54-keypoint motion capture data (33 pose keypoints, 21 hand keypoints, and facial landmark blendshapes) once authentic studio recordings are acquired.

---

## 2. 3D Humanoid Architecture

```
                                  +-----------------------+
                                  | React Three Fiber     |
                                  | WebGL Canvas (60 FPS) |
                                  +-----------------------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
        +-------------------------+                       +-------------------------+
        | Articulated Upper-Body  |                       | Studio Environment      |
        | Mesh Standard Materials |                       | - Directional keylight  |
        | - Head / Eyes / Cranium |                       | - Ambient fill light    |
        | - Torso / Academic Shirt|                       | - Ground contact shadow |
        | - Dual Arm Assemblies   |                       | - Metric reference grid |
        +-------------------------+                       +-------------------------+
                     |
                     v
        +-------------------------------------------------------+
        | Zero-Fabrication Resting State:                       |
        | - Breathing frequency: 1.5 rad/s, amplitude: 0.015m   |
        | - Head attentive micro-movements: 0.8 rad/s           |
        | - Arms: -0.35 rad (x), ±0.22 rad (z) resting posture  |
        | - Synthetic signing gestures: STRICTLY BLOCKED        |
        +-------------------------------------------------------+
```

---

## 3. 54-Keypoint Data Ingestion Roadmap

Once studio recording sessions commence under certified Deaf signer consent protocols:
1. **Pose (33 Keypoints):** MediaPipe Holistic / ReadyPlayerMe standard format for shoulder, elbow, and wrist kinematics.
2. **Hands (21 Keypoints per Hand):** Full distal, intermediate, and proximal phalange joint rotations for ISL handshapes (Open-B, C-handshape, Index extended, Fist).
3. **Face (468 Mesh Blendshapes):** Non-Manual Markers (furrowed brow for WH-questions, raised brow for conditionals, headshake for sentence-final negation).

---

## 4. UI Controls & Disclaimers

In `AvatarViewer.tsx`:
- **Interactive Camera Angles:** Front View, Side View, Close-up (Face/NMM inspection).
- **Speed Controls:** 0.75x, 1.0x, 1.25x pacing.
- **Transparency Pill:** `3D Signing Avatar Preview — Zero Fabrication Policy active (Non-verified gestures are not fabricated)`.
- **Rig Badge:** `Rig: MediaPipe / ReadyPlayerMe Compatible`.

