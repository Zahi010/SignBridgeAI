# SignBridge AI: Controlled Pilot Methodology & Evaluation Protocol
## Formal Framework for the First Multi-Center ISL Technical Sign Validation Pilot

**Protocol Reference:** SB-PILOT-2026-v1.0  
**Target Milestone:** Phase 7 Controlled Pilot  
**Ethics Governance:** ICMR Ethical Guidelines (India), Declaration of Helsinki, Deaf Community Research Protocols  
**Status:** **IN PREPARATION** (Awaiting formal Institutional Ethics Committee clearance)  

---

## 1. Research Objectives & Hypotheses

### Primary Objectives:
1. **Linguistic Fidelity:** Evaluate whether 3D retargeted avatar animations preserve the phonological parameters (handshape, orientation, location, movement) of original ISLRTC signing recordings with $\ge 85\%$ expert consensus.
2. **Pedagogical Comprehensibility:** Measure whether Deaf engineering students understand technical concepts presented via SignBridge AI avatar + pedagogical explanations significantly better than text captions alone.
3. **Inter-Rater Convergence:** Assess statistical agreement among certified ISL interpreters and Deaf native signers using Fleiss' Kappa ($\kappa \ge 0.60$ threshold for substantial agreement).

### Core Hypotheses:
- **$H_1$:** Retargeted 3D avatar animations generated from authentic mocap data achieve $\ge 80\%$ acceptance on phonological accuracy from certified ISL reviewers.
- **$H_2$:** Technical comprehension scores among Deaf engineering students improve by $\ge 25\%$ when concepts are presented with Topic-Comment ISL avatar animations compared to verbatim English captions.
- **$H_3$:** The Zero-Fabrication safeguard eliminates false sign adoption compared to uncontrolled generative AI baselines.

---

## 2. Participant Cohorts & Eligibility Criteria

```
                        [Pilot Participant Pool]
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
      [Cohort A: Expert Reviewers]         [Cohort B: Student Learners]
      (N = 5 to 10 Qualified)             (N = 20 to 30 DHH Students)
                 │                                   │
   - Certified ISL Interpreters (RCI)   - Enrolled in B.Tech / Diploma
   - Deaf Master Signers / Educators    - ISL as Primary Language
   - $\ge 3$ Years Professional Exp.     - Age $\ge 18$, Voluntary Consent
```

### Cohort A: Expert Evaluators
* **Inclusion Criteria:**
  1. Certified Indian Sign Language Interpreter with Rehabilitation Council of India (RCI) registration; OR
  2. Deaf native signer with $\ge 3$ years experience as an ISL educator/trainer in a recognized Deaf school or NGO; OR
  3. Academic researcher in sign language linguistics or Deaf studies.
* **Exclusion Criteria:** Individuals without demonstrable ISL fluency; commercial vendors with competing sign software.

### Cohort B: Deaf Engineering Students
* **Inclusion Criteria:**
  1. Enrolled in an undergraduate engineering (B.Tech/B.E.), polytechnic diploma, or computer applications (BCA/MCA) degree program in India.
  2. Proficient in Indian Sign Language as a primary or preferred mode of communication.
  3. Age 18 or older.
  4. Active informed consent.

---

## 3. Evaluation Rubric & Psychometric Instrument

Expert reviewers evaluate each candidate sign across **12 standardized phonological & communicative dimensions**:

| # | Dimension | Evaluation Question | Scale |
| :--- | :--- | :--- | :--- |
| **1** | **Lexical Accuracy** | Is this the canonical ISL sign for the intended engineering concept? | Pass / Minor / Major / Incorrect |
| **2** | **Handshape** | Are finger configurations, knuckle extensions, and thumb oppositions accurate? | Pass / Minor / Major / Incorrect |
| **3** | **Orientation** | Is the palm and finger orientation anatomically and linguistically correct? | Pass / Minor / Major / Incorrect |
| **4** | **Location** | Is the sign produced in the correct signing space (neutral chest, head, chin)? | Pass / Minor / Major / Incorrect |
| **5** | **Movement** | Is the trajectory, velocity, repetition, and path shape authentic? | Pass / Minor / Major / Incorrect |
| **6** | **Coordination** | In two-handed signs, do the dominant and non-dominant hands coordinate properly? | Pass / Minor / Major / Incorrect |
| **7** | **Facial NMM** | Are required non-manual markers (eyebrow, mouth morphemes, head tilt) present? | Pass / Minor / Major / Incorrect |
| **8** | **Grammar** | Does the utterance follow ISL Topic-Comment structure rather than English SVO? | Pass / Minor / Major / Incorrect |
| **9** | **Contextual Meaning**| Does the sign distinguish the technical meaning from everyday polysemic senses? | Pass / Minor / Major / Incorrect |
| **10**| **Naturalness** | Does the avatar motion feel fluid and human rather than robotic or abrupt? | Pass / Minor / Major / Incorrect |
| **11**| **Regional Dialect** | Is this sign recognized pan-India (ISLRTC standard) or regional (Delhi/Mumbai/etc.)?| Standard / Regional Variant |
| **12**| **Ambiguity** | Is there potential for misinterpretation as an unrelated everyday word? | Low / Medium / High Risk |

---

## 4. Ethical Safeguards & Participant Protection

1. **Dual-Format Informed Consent:** Consent must be provided in both written English/Hindi and accessible ISL video format before any session commences.
2. **Participant Pseudonymization:** Every participant is assigned a cryptographic pseudonym (e.g. `DEAF-PARTICIPANT-83A`). Real names and email addresses are never linked to evaluation data in the public dataset.
3. **Right to Erasure (GDPR Art. 17 / DPDP Act):** Participants can withdraw at any time. Invoking the deletion API immediately hard-deletes research sessions and logs an immutable tombstone to prevent backup resurrection.
4. **Fair Compensation:** Participating Deaf signers and student evaluators receive institutional honoraria in compliance with ICMR fair compensation guidelines.

---

## 5. Statistical Analysis Plan

1. **Inter-Rater Reliability:** Computed per criterion using **exact Fleiss' Kappa**:
   - $\kappa < 0.20$: Poor agreement $\rightarrow$ Requires rubric refinement.
   - $0.21 \le \kappa \le 0.40$: Fair agreement.
   - $0.41 \le \kappa \le 0.60$: Moderate agreement.
   - $0.61 \le \kappa \le 0.80$: Substantial agreement $\rightarrow$ Prerequisite for sign verification.
   - $\kappa > 0.80$: Almost perfect agreement.
2. **Wilson Score Confidence Intervals:** All acceptance and pass percentages are reported with 95% Wilson score confidence bounds to account for sample size variance.
3. **Disagreement Adjudication:** Any task where reviewers disagree on pass/fail triggers an adjudication task assigned to a designated Deaf master reviewer.

---

## 6. Pilot Governance Status: PREPARATION GATE

In accordance with SignBridge AI's Non-Negotiable Governance Rules:
* **The pilot is officially designated as `IN_PREPARATION`.**
* No participant recruitment or data collection will occur until formal Institutional Ethics Committee (IEC) clearance is granted and formal institutional collaboration agreements are executed.
