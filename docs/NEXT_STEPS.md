# SignBridge AI — Next Steps & Future Roadmap

This document outlines the strategic engineering roadmap to transition SignBridge AI from a validated technological prototype into a full-scale educational deployment platform.

---

## 1. Multilingual Expansion: Malayalam & Hindi Support

While English is the primary medium of engineering instruction in India, vernacular explanations play a critical role in student comprehension. The next phase introduces dual vernacular pipelines:

### A. Malayalam ISL Translation Pipeline
- **Morphosyntactic Differences:** Malayalam follows Subject-Object-Verb (SOV) order with extensive agglutinative case markers (accusative, dative, instrumental, locative).
- **Linguistic Strategy:**
  - Tokenizer and lemmatizer using MLMorph or IndicNLP for Malayalam root word extraction.
  - Mapping case markers to ISL spatial loci (e.g., `-il` [in/at] mapped to locative spatial indices).
  - Integration with Kerala Federation of the Deaf (KFD) regional dialectal variations.

### B. Hindi ISL Translation Pipeline
- **Linguistic Characteristics:** Hindi is an SOV language with postpositions (*ne*, *ko*, *se*, *ke liye*) and grammatical gender.
- **Linguistic Strategy:**
  - Postposition stripping during ISL semantic tokenization.
  - Alignment with standard northern ISL dialects codified by ISLRTC New Delhi.
  - Disambiguation of Hindi engineering loanwords (e.g., *vidyut* vs. *bijli* for electricity).

---

## 2. Certified Deaf Signer Studio Recording Protocol

To replace sample video clips with certified reference recordings:

### A. Studio Environment & Setup
- **Background:** High-contrast neutral chroma key (green screen #00FF00) or 18% neutral gray.
- **Lighting:** Three-point softbox lighting (key, fill, backlight) calibrated to eliminate harsh facial shadows and hand motion blur.
- **Camera Configuration:**
  - 4K resolution at 60 frames per second (fps) to capture rapid finger articulations.
  - Framing: High-waist to top of head, with 20% margin around lateral signing perimeter.
  - Synchronized frontal and 45-degree lateral cameras for 3D spatial reconstruction.

### B. Signer Accreditation & Ethics
- Certified Deaf master signers and licensed ISL interpreters recruited through ISLRTC or national Deaf associations.
- Explicit informed consent forms covering open educational licensing (Creative Commons BY-NC-SA).
- Peer review committee verifying signing clarity before publishing to the registry.

---

## 3. High-Density 54-Keypoint Motion Capture Ingestion

To advance the 3D avatar from keyframe tracks to natural signing reproduction:

### A. Ingestion Pipeline Architecture
```
[Video Footage (60fps)]
        │
        ▼
[MediaPipe Holistic / OpenPose]
  - 33 Pose Landmarker Keypoints (torso, arms, shoulders)
  - 21 Left Hand Keypoints + 21 Right Hand Keypoints
  - 468 Dense Facial Mesh Keypoints
        │
        ▼
[Spatial Normalization & Depth Solver]
  - Temporal smoothing via 1-Euro Filter or Savitzky-Golay filter
  - Kinematic bone length constraints preventing joint hyper-extension
        │
        ▼
[BVH / glTF Skeletal Rig & Blendshape Exporter]
  - Skeletal bone rotation quaternions (Mixamo humanoid compatible)
  - 52 ARKit-compatible facial blendshapes
```

### B. Co-articulation & Blend Optimization
- Automated calculation of transition curves between sequential signs.
- Dynamic hand-transition speed scaling based on phonological distance between consecutive handshapes.
- Facial Non-Manual Marker synchronization with lexical sign peaks.

---

## 4. Community Co-Design & Pilot Deployment

1. **Academic Advisory Board:** Form formal partnership with Deaf engineering graduates and certified ISLRTC researchers.
2. **Classroom Beta Testing:** Deploy SignBridge AI in live classrooms across selected engineering colleges in India.
3. **Continuous Feedback Loop:** Enable Deaf students to rate sign clarity and flag ambiguous translations directly in the UI.

