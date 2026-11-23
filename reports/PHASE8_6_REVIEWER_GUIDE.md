# SIGNBRIDGE AI — PHASE 8.6: STEP-BY-STEP REVIEWER ONBOARDING & EVALUATION GUIDE

**Phase:** Phase 8 — Institutional Outreach, Live Demonstration, External ISL Expert Recruitment & Collaboration Readiness  
**Target Audience:** External ISL Expert Reviewers, Deaf Native Signers, Certified Interpreters  
**Portal Route:** `/expert-review`  
**Version:** 1.0.0  
**Date:** 2026-11-23  

---

## 1. Introduction & Welcome

Welcome to the SignBridge AI Expert Reviewer Portal!

Your expertise as a Deaf native signer, certified interpreter, or sign language linguist is essential to determining whether our 3D avatar accurately and naturally conveys technical engineering concepts in Indian Sign Language.

We adhere strictly to our **Zero-Fabrication Policy**: your ratings directly govern whether a sign motion is approved, revised, or rejected. We never alter reviewer feedback.

---

## 2. Step 1: Account Registration & Verification

1. Navigate to the **Expert Review Portal** at `http://localhost:5173/expert-review` (or institutional URL).
2. Click **"Register as Reviewer"**.
3. Fill in your basic details:
   * **Full Name** and **Email Address**.
   * **Linguistic Background:** Indicate whether you are a Deaf native signer and/or certified interpreter.
   * **Years of Experience** and **Institutional Affiliation** (e.g. ISLRTC, AYJNISHD, University).
4. Enter your single-use **Invitation Code** (provided in your official invitation letter, format: `INV-XXXX-2026-XXXXXX`).
5. Choose a secure password and submit.
6. Upon registration, your profile will be active in the evaluation system.

---

## 3. Step 2: Accessing Assigned Validation Tasks

1. Log in with your credentials on `/expert-review`.
2. The dashboard displays your **Assigned Evaluation Tasks**:
   * *Algorithm* (Computer Science)
   * *Frequency* (Electronics)
   * *Current (Electrical)* (Electrical Engineering)
   * *Beam* (Civil / Mechanical Engineering)
   * *Torque* (Mechanical Engineering)
3. Click **"Start Evaluation"** on any sign task.

---

## 4. Step 3: Navigating the Comparative Inspection Interface

The evaluation interface provides synchronized comparative tools:

```
┌───────────────────────────────────────┬───────────────────────────────────────┐
│     AUTHENTIC ISLRTC REFERENCE        │         3D RETARGETED AVATAR          │
│                                       │                                       │
│   [Video Player: 1080p Master Signer] │     [Three.js Interactive Canvas]     │
│                                       │                                       │
│   • Loop playback                     │   • 15-joint articulated fingers      │
│   • 0.25x / 0.5x / 1.0x slow motion   │   • Rotate: Front, 45° Left, Right    │
│   • Scrub bar with frame stepping     │   • Zoom in on hands and facial area  │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

### Pro Tips for Inspection:
* **Check at 0.25x speed:** Watch the initiation and termination of hand movements closely to verify finger configuration.
* **Rotate the 3D Avatar:** Use the camera angle buttons (`Front`, `Left 45°`, `Right 45°`, `Hands`) to view depth and hand orientation that may be obscured in the 2D video.
* **Compare Handshapes:** Compare the thumb and finger curvature of the avatar against the master signer.

---

## 5. Step 4: Completing the Multi-Criteria Rubric

For each sign, evaluate the avatar against five phonological criteria using the standardized scale:

| Rating | Definition | When to Select |
| :--- | :--- | :--- |
| **Excellent / Natural** (4) | Completely accurate, fluent, and culturally authentic. | Matches master signer; immediately understandable. |
| **Acceptable** (3) | Minor stylistic or speed flaws, but clear and understandable. | Slight finger stiffness, but phonologically correct. |
| **Partially Distorted** (2) | Distorted trajectory or handshape; impairs comprehension. | Significant joint misplacement; requires effort to read. |
| **Unacceptable** (1) | Incorrect sign, changed meaning, or non-ISL motion. | Violates ISL grammar or represents a completely different sign. |

### Criteria Breakdown:
1. **Handshape:** Are the active and passive hand configurations correct? Are all fingers in proper extension/flexion?
2. **Location:** Does the sign occur in the correct spatial location (neutral signing space, chest level, chin, etc.)?
3. **Movement:** Is the trajectory (linear, arc, circular), repetition, and speed dynamics accurate?
4. **Orientation:** Are the palms and wrists facing the correct direction?
5. **Non-Manual Features (NMM):** Are head tilt, eye gaze, and facial expressions adequate? *(Note: Avatar NMM retargeting is in early stages; please evaluate whether the lack of facial expression impedes comprehension).*

---

## 6. Step 5: Flagging Critical Errors & Annotations

If the avatar makes a severe error that changes the meaning or renders the sign unrecognizable:
1. Check the box **"Flag as Critical Error"**.
2. Specify the timestamp (in seconds or frames) where the flaw occurs.
3. Provide a clear, actionable explanation (e.g., *"Right index finger extends too early at 1.8s; should remain bent until contact"*).
4. Critical error flags automatically generate an engineering remediation ticket for our 3D animation team.

---

## 7. Step 6: Submitting Your Evaluation

1. Review your ratings across all criteria.
2. Add any general pedagogical recommendations for Deaf engineering students.
3. Click **"Submit Evaluation & Complete Task"**.
4. Repeat for the remaining assigned signs.
5. Once all 5 signs are completed, an automatic certificate of evaluation and honorarium receipt will be generated.

*Thank you for contributing your vital expertise to making STEM education accessible to Deaf students across India!*
