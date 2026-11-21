# Phase 4 Linguistic Validation Readiness Assessment

**Standard:** SignBridge AI ISL Linguistic Audit Protocol  
**Target Reviewers:** Accredited Deaf ISL Master Instructors & Certified Sign Interpreters  
**Scope:** Motion-Capture Retargeting Validation & 3D Avatar Evaluation Protocol  

---

## 1. Five Phonological Evaluation Parameters

To promote an avatar animation from `PARTIALLY_VERIFIED_MOTION` or `REQUIRES_LINGUISTIC_REVIEW` to `VERIFIED_ISL_MOTION`, qualified human reviewers evaluate the following five linguistic dimensions:

```
                                ┌────────────────────────────────┐
                                │   ISL Phonological Rubric      │
                                └───────────────┬────────────────┘
                                                │
        ┌───────────────┬───────────────────────┼───────────────────────┬───────────────┐
        ▼               ▼                       ▼                       ▼               ▼
┌───────────────┐┌───────────────┐      ┌───────────────┐       ┌───────────────┐┌───────────────┐
│ 1. Handshape  ││  2. Location  │      │  3. Movement  │       │4. Orientation ││    5. NMM     │
│ - 15 phalanges││ - Spatial locus│     │ - Trajectory  │       │ - Palm facing ││ - Eyebrows    │
│ - Finger curl ││ - Body contact │     │ - Speed/accel │       │ - Finger point││ - Mouthing    │
│ - Abduction   ││ - Signing box │      │ - Repetition  │       │ - Supination  ││ - Head tilt   │
└───────────────┘└───────────────┘      └───────────────┘       └───────────────┘└───────────────┘
```

---

## 2. Quantitative Scoring Rubric (1 to 5 Scale)

| Score | Rating Level | Phonological Criteria | Certification Eligibility |
| :--- | :--- | :--- | :--- |
| **5** | **Flawless Native Sign** | Handshape, location, movement, orientation, and NMM are indistinguishable from an accredited Deaf master signer. | **Eligible for `VERIFIED_ISL_MOTION`** |
| **4** | **High Comprehensibility** | Minor non-phonemic deviation in finger spread or movement speed; meaning is completely clear to native signers. | **Eligible for `VERIFIED_ISL_MOTION`** |
| **3** | **Acceptable with Reservations** | Handshape or orientation slightly awkward due to kinematic retargeting; comprehensible in context but unnatural. | Retained under `PARTIALLY_VERIFIED_MOTION` |
| **2** | **Phonemically Ambiguous** | Handshape confuses two distinct ISL minimal pairs (e.g. B vs 1); requires re-extraction. | Rejected; downgraded to `REQUIRES_LINGUISTIC_REVIEW` |
| **1** | **Unintelligible / Incorrect** | Inverted joints, incorrect signing location, or missing non-manual markers. | **Prohibited under Zero-Fabrication Policy** |

---

## 3. Human Review Workflow in Application

1. **Reviewer Authentication:** The reviewer logs into the SignBridge Validation Portal using their verified credentials.
2. **Side-by-Side Verification:** The portal displays the original authentic ISLRTC video alongside the retargeted 3D avatar.
3. **Multi-Angle Inspection:** The reviewer uses the Camera Presets (`Face NMM`, `Hands`, `45° Angles`) and frame stepping ($33\text{ms}$) to inspect hand configurations.
4. **Independent Certification:** If the reviewer awards a score $\ge 4.0$ across all five dimensions and certifies their evaluation, the status advances to `VERIFIED_ISL_MOTION`.

