# SignBridge AI — Phase 7: Blockers, External Approvals & Next Steps

**Date:** 2026-11-21  
**Project:** SignBridge AI  
**Workspace:** `E:\SignBridgeAi`  
**Milestone:** Phase 7  

---

## 1. External Approvals & Prerequisite Blockers

The software platform is technically ready for external engagement. However, before the pilot can transition from `PREPARATION` to `ACTIVE` with real human signers, the following external real-world blockers must be resolved:

### 1.1 Formal Institutional Ethics Committee (IEC / IRB) Clearance
* **Description:** Research involving Deaf participants (a linguistic minority) requires formal review by an accredited Indian Institutional Ethics Committee (under ICMR guidelines).
* **Current Status:** Ethical architecture (consent models, HMAC pseudonymization, GDPR Article 17 erasure) is implemented in software. Formal human protocol submission to a partner university/hospital review board is pending.
* **Resolution Pathway:** Submit `SIGNBRIDGE_RESEARCH_PROPOSAL.md` and `SIGNBRIDGE_PILOT_METHODOLOGY.md` to the target partner university's Ethics Committee.

### 1.2 Institutional Collaboration Agreements (MoU)
* **Description:** Collaborating with national bodies like ISLRTC, AYJNISHD, or Deaf Enabled Foundation requires formal administrative authorization.
* **Current Status:** Contact directory and research proposals are prepared. In compliance with Rule 6, no unsolicited messages have been dispatched.
* **Resolution Pathway:** Project leadership executes authorized outreach to identified liaisons, leading to formal bilateral research MoUs.

### 1.3 Professional ISL Video Consent Filming
* **Description:** Written English/Hindi consent forms are legally insufficient for signers with limited written English literacy. Every consent clause must be signed in ISL on video.
* **Current Status:** Video consent viewer architecture is operational; recorded video media for the consent clauses must be filmed with a certified Deaf master signer.
* **Resolution Pathway:** Commission a certified Deaf signer to record standard consent videos and place them in `data/consent_videos/`.

---

## 2. Technical Next Steps (Phase 8 Preparation)

1. **Host Infrastructure Deployment:**
   - Deploy Docker containers to an institutional Linux server with public HTTPS and automated domain routing.
   - Configure automated nightly disaster recovery backups (`backup_database.py` and `backup_media.py`).

2. **Expert Reviewer Onboarding Cohort:**
   - Issue the first batch of invitation codes (`INV-XXXXXXXX`) to 5 accredited ISL interpreters and Deaf educators under the pilot MoU.
   - Monitor reviewer registrations and verify credentials via `POST /api/v1/validation/credentials/{id}/verify`.

3. **Execution of First Pilot Review:**
   - Track completion of the 5 baseline signs (Algorithm, Frequency, Current, Beam, Torque).
   - Review live Fleiss' Kappa inter-rater agreement on the academic dashboard.
   - Review and triage auto-generated remediation tickets via `FeedbackRemediationService`.

4. **Multi-Center Lexicon Expansion:**
   - Following validation of the 5 baseline signs, progressively ingest authentic signing videos for the remaining 95 engineering concepts in the candidate lexicon.

