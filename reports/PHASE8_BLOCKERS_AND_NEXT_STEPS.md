# SIGNBRIDGE AI — PHASE 8: BLOCKERS AND NEXT STEPS (PHASE 9 ROADMAP)

**Phase:** Phase 8 — Institutional Outreach, Live Demonstration, External ISL Expert Recruitment & Collaboration Readiness  
**Date:** 2026-11-23  
**Document Classification:** Operational Roadmap & Transition Plan  

---

## 1. Current Blockers & Institutional Dependencies

SignBridge AI's software, security, live demonstration, and documentation systems are fully completed and tested. However, transitioning from **Gate A (Presentation Readiness)** to **Gate B (External Linguistic Pilot & Sign Promotion)** is intentionally gated by real-world institutional dependencies:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     GATE B TRANSITION PREREQUISITES                     │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│ Prerequisite             │ Current Status           │ Required Action  │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ 1. Signed Institutional  │ 0 signed agreements;     │ Admin outreach   │
│    MoU / Agreement       │ 12 potential partners    │ and presentation │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ 2. External IRB/Ethics   │ Data governance ready;   │ Submit joint     │
│    Committee Approval    │ pending institutional PI │ ethics proposal  │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ 3. Accredited External   │ 0 external reviewers;    │ Issue invitation │
│    Reviewer Onboarding   │ portal ready on /review  │ codes to experts │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ 4. Independent Review    │ 0 completed reviews;     │ Conduct 5-sign   │
│    Evaluations (N>=15)   │ 5 dossiers ready         │ evaluation study │
└──────────────────────────┴──────────────────────────┴──────────────────┘
```

These are **not software defects**; they are genuine institutional and scientific prerequisites mandated by our Zero-Fabrication Policy.

---

## 2. Immediate Operational Steps for Research Administrators

Now that Gate A is passed, human research administrators can execute the following real-world actions:

1. **Conduct Internal Rehearsal:**
   - Execute the 6-step `/demo` walkthrough with internal researchers using the presentation outline (`reports/PHASE8_3_PRESENTATION_OUTLINE.md`).
   - Review defense questions in `reports/PHASE8_8_INSTITUTIONAL_QA.md`.
2. **Initiate First-Wave Institutional Inquiries:**
   - Review the 4 primary institutions in `/outreach` with status `READY_FOR_OUTREACH`:
     1. ISLRTC (Apex ISL authority)
     2. AYJNISHD (National hearing institute)
     3. ASSISTECH IIT Delhi (Assistive HCI)
     4. Deaf Enabled Foundation (Deaf community NGO)
   - Disseminate customized collaboration letters (`reports/PHASE8_3_INSTITUTIONAL_LETTER.md`) and one-page briefs (`SIGNBRIDGE_ONE_PAGE_BRIEF.md`) via official public email channels.
   - Log email dispatches in `/outreach` to transition status to `CONTACTED`.
3. **Schedule Live Demonstrations:**
   - Upon receiving institutional response, schedule virtual or campus presentations.
   - Demonstrate `/demo` using local or sandbox deployment.

---

## 3. Phase 9 Roadmap: Collaborative External Linguistic Pilot Execution

Upon securing the first signed institutional collaboration agreement, Phase 9 will execute the formal validation pilot:

### Phase 9.1: Onboarding of Accredited External Reviewers
* Generate official invitation codes (`/api/v1/validation/invitations`) for nominated ISL faculty, certified interpreters, and Deaf educators.
* Verify reviewer credentials against CRR numbers (RCI) or institutional rosters.
* Guide reviewers through onboarding using `reports/PHASE8_6_REVIEWER_GUIDE.md`.

### Phase 9.2: Controlled Five-Sign Linguistic Evaluation
* Execute independent evaluations across *Algorithm*, *Frequency*, *Current*, *Beam*, and *Torque*.
* Compute real-time statistical metrics (Cohen's $\kappa$, Fleiss' $\kappa$, inter-rater agreement percentage, Wilson score confidence intervals).
* Enforce sample size gating: retain `PENDING_EXTERNAL_REVIEW` status until $N \ge 15$ evaluations per sign are achieved.

### Phase 9.3: Automated Remediation of Rubric Criticisms
* Route flagged critical errors directly to the Feedback Remediation Engine (`FeedbackRemediationTicket`).
* Retarget 3D animations to address joint angle, speed, or orientation criticisms.

### Phase 9.4: Co-Design Workshops for Technical Vocabulary Expansion
* Host participatory workshops with Deaf engineering students to co-design and validate 20 additional STEM concepts.
* Advance facial Non-Manual Marker (NMM) retargeting research in partnership with computer vision collaborators.
