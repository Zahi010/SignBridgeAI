# SignBridge AI — Phase 6.5: License & Provenance Verification

**Date:** 2026-11-21  
**Auditor:** Open Source Licensing & Research Data Governance Specialist  
**Subject:** Provenance Verification, GODL-India Licensing, Academic Export Filtering  

---

## 1. Overview & Audit Objectives

Phase 2.6 and Phase 6 established the initial provenance framework for SignBridge AI. The Phase 6.5 audit independently inspected all multimedia assets, vocabulary definitions, and export pipelines to guarantee:
1. No unverified third-party copyrighted material is redistributed.
2. Official Indian Sign Language Research and Training Centre (ISLRTC) videos are properly attributed under Government Open Data License - India (GODL-India).
3. The Zero-Fabrication Policy is strictly enforced at the export boundary: unverified, synthetic, or non-mocap assets cannot be exported as verified signs.

---

## 2. Asset Provenance Matrix

The repository hosts five authentic ISLRTC sign videos downloaded from official government sources (data.gov.in / DEPwD):

| Asset ID | Concept | Source Attribution | License | Local File | Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ISL-CS-001** | Algorithm | ISLRTC Official Dictionary / DEPwD | GODL-India | `data/sign_videos/islrtc_algorithm.mp4` | **PARTIALLY_VERIFIED** (Awaiting formal external pilot sign-off) |
| **ISL-ECE-013**| Frequency | ISLRTC Official Dictionary / DEPwD | GODL-India | `data/sign_videos/islrtc_frequency.mp4` | **PARTIALLY_VERIFIED** |
| **ISL-EEE-025**| Current | ISLRTC Official Dictionary / DEPwD | GODL-India | `data/sign_videos/islrtc_current.mp4` | **PARTIALLY_VERIFIED** |
| **ISL-CIV-037**| Beam | ISLRTC Official Dictionary / DEPwD | GODL-India | `data/sign_videos/islrtc_beam.mp4` | **PARTIALLY_VERIFIED** |
| **ISL-MEC-049**| Torque | ISLRTC Official Dictionary / DEPwD | GODL-India | `data/sign_videos/islrtc_torque.mp4` | **PARTIALLY_VERIFIED** |

### 2.1 GODL-India Compliance Checklist
- [x] **Attribution Provided:** `source_attribution` explicitly names "ISLRTC, Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India".
- [x] **Integrity Preserved:** Transcoding to H.264 (yuv420p) preserved exact frame sequence, signer movement, and timing without alterations.
- [x] **Non-Endorsement Disclaimer:** Export bundles state that redistribution does not imply government endorsement of SignBridge AI.

---

## 3. Asset-Level Export Eligibility Enforcement

Prior to Phase 6.5, the export eligibility service performed cohort-level validation without inspecting asset-level provenance flags. 

### Remediated Architecture (`export_eligibility_service.py`):
The export eligibility service was updated to evaluate individual asset provenance tags:

1. **Authentic Government Videos:**
   - Evaluated for explicit government attribution and GODL-India license.
   - Assigned status: `ELIGIBLE_FOR_RESEARCH_EXPORT`.
   - Lacking verified attribution $\rightarrow$ Downgraded to `RIGHTS_UNCONFIRMED` and blocked from public distribution.
2. **Avatar Animations:**
   - Real mocap retargeting from authentic ISLRTC videos $\rightarrow$ `ELIGIBLE_FOR_RESEARCH_EXPORT`.
   - Procedural/Neutral preview animations $\rightarrow$ Flagged as `RESTRICTED_RESEARCH_ONLY` to prevent representation as verified ISL motion.
3. **Community Evaluations:**
   - Released under `Open Data Commons Attribution License (ODC-By)` provided participant consent for academic publication is confirmed.

---

## 4. Verification Verdict
All assets in the SignBridge AI repository are accounted for, correctly licensed, and shielded by programmatic export guards. No unlicensed or fabricated assets can escape into academic export packages.

