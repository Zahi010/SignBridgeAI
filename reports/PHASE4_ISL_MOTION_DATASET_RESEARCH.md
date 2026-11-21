# Phase 4 ISL Motion Dataset Research & Provenance Report

**Date:** 2026-11-21  
**Project:** SignBridge AI  
**Focus:** Indian Sign Language (ISL) 3D Motion Capture Datasets & Authentic Video Repositories

---

## 1. Survey of Public Indian Sign Language Datasets

To establish a legally sound, linguistically authentic motion foundation for SignBridge AI, public research datasets and official government archives were investigated:

### 1.1 ISLRTC (Indian Sign Language Research and Training Centre) Digital Collection
- **Source:** Official YouTube Channel & Website (`https://www.islrtc.nic.in/`)
- **Institution:** Ministry of Social Justice and Empowerment, Government of India.
- **Content:** Standardized ISL dictionary signs recorded by native Deaf signers and certified ISL master instructors.
- **Format:** 1080p MP4 videos, front-facing, neutral green/blue studio background, high-contrast attire.
- **Acquired Assets (5 Concepts):**
  - `Algorithm` (`islrtc_algorithm.mp4`, SHA-256: `6eef46df...`)
  - `Frequency` (`islrtc_frequency.mp4`, SHA-256: `67a6d859...`)
  - `Current` (`islrtc_current.mp4`, SHA-256: `2b137d6e...`)
  - `Beam` (`islrtc_beam.mp4`, SHA-256: `c8d20836...`)
  - `Torque` (`islrtc_torque.mp4`, SHA-256: `a9359e87...`)
- **Licensing & Terms:** Published by Government of India under the **Government Open Data License (GODL-India)**. Permits lawful commercial and non-commercial utilization with proper attribution and non-endorsement disclaimers.
- **SignBridge Role:** Primary benchmark for extracting authentic 3D signing landmarks.

### 1.2 INCLUDE Dataset (AI4Bharat / IIT Madras)
- **Institution:** Indian Institute of Technology Madras & AI4Bharat.
- **Publication:** "INCLUDE: A Large Scale Dataset for Indian Sign Language Recognition" (ACM Multimedia 2020).
- **Scale:** 4,292 videos spanning 263 isolated signs recorded across 7 signers.
- **Format:** Video recordings with variable lighting, mobile camera viewpoints.
- **Relevance:** While extensive for basic vocabulary (fruits, common actions, greetings), technical engineering concepts are largely absent. SignBridge AI can utilize its spatial landmark distribution as an anatomical sanity-check for retargeting.

### 1.3 CISLR (Continuous Indian Sign Language Recognition)
- **Institution:** Various Indian academic research groups (e.g. IIIT-Hyderabad, IIT Bombay).
- **Scale:** Small-vocabulary sentence-level recordings (100-300 sentences).
- **Relevance:** Useful for studying continuous signing co-articulation, but lacks verified technical curriculum terms.

---

## 2. Directory Layout for Phase 4 Motion Assets

The following directory hierarchy is established in `data/isl_motion/`:
- `data/isl_motion/raw/`: Original uncompressed video assets and raw landmark extractions.
- `data/isl_motion/processed/`: Normalized, smoothed 3D keyframe streams (`*_mocap.json`) ready for skeletal retargeting.
- `data/isl_motion/annotations/`: Linguistic annotations, phonological parameter sheets, and reviewer validation records.
- `data/isl_motion/metadata/`: Dataset provenance, SHA-256 integrity hashes, and licensing documentation.

---

## 3. Legal & Provenance Summary

All motion assets generated in Phase 4 originate directly from the 5 official ISLRTC recordings acquired in Phase 2. No synthetic or third-party foreign sign language motions (ASL, BSL, Auslan) are introduced into the ISL library. Under the Zero-Fabrication Policy, all extracted motions are tagged as `PARTIALLY_VERIFIED_MOTION` until reviewed and certified by an accredited Deaf linguistic reviewer.

