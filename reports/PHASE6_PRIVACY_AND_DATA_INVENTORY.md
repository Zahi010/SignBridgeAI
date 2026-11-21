# SignBridge AI — Phase 6 Privacy & Data Inventory Audit

**Date:** November 21, 2026  
**Auditor:** Research Ethics & Privacy Compliance Officer  
**Scope:** Data Classification, PII Minimization, Participant Pseudonymization, Storage Safeguards, Regulatory Compliance (DPDP Act 2023 / GDPR)  
**Status:** PASS  

---

## 1. Data Classification Schema

SignBridge AI categorizes all project data into five strict sensitivity tiers:

| Tier | Category | Description | Storage Location | Retention / Deletion Policy |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Participant PII** | Direct real-world identifiers (names, phone numbers, Aadhaar, email of participants) | **NEVER STORED** | Zero-PII policy: participants are registered under client-generated pseudonyms only. |
| **Tier 2** | **Reviewer Credentials** | Reviewer legal names, emails, institutional affiliation, RCI certificate numbers | `phase5_reviewers`, `phase5_reviewer_credentials` | Retained during active participation. Hard delete on account closure. |
| **Tier 3** | **Linguistic Research Data** | Comprehension scores, naturalness ratings, rubric annotations, dialect notes | `phase5_research_sessions`, `phase5_sign_evaluations` | Pseudonymized; immediately purged upon right-to-erasure invocation. |
| **Tier 4** | **3D Avatar & Kinematics** | Keyframed bone rotations, MediaPipe landmarks, joint angles | `data/avatar_animations/`, `avatar_animations` | Retained as CC-BY-4.0 open research assets. Contains no human biometric face geometry. |
| **Tier 5** | **Government Reference Media** | Authentic ISLRTC signing recordings (5 official signs) | `data/sign_videos/`, `sign_videos` | Read-only reference pointers. Non-redistributable under GODL-India. |

---

## 2. Participant Pseudonymization Architecture

In compliance with India's **Digital Personal Data Protection (DPDP) Act 2023** and ethical research standards for Deaf communities:
1. **Zero Direct Identification:** Participants in comprehension surveys and naturalness studies are identified solely by synthetic alphanumeric pseudonyms (e.g. `DEAF-PARTICIPANT-83A`).
2. **Decoupled Registration:** No phone numbers, residential addresses, biometric facial geometry, or identity documents are collected from Deaf community participants.
3. **Cryptographic One-Way Hashing on Withdrawal:** When a participant withdraws and requests data deletion:
   - All session records are permanently deleted (`DELETE FROM phase5_research_sessions WHERE consent_id = ?`).
   - The original pseudonym is irreversibly hashed using SHA-256 (`ANONYMIZED_PURGED_<sha256[:12]>`).
   - The consent table retains only the proof that withdrawal was honored, with `is_anonymized = True` and `consent_given = False`.
   - Historical audit logs are scrubbed to replace the original pseudonym with `ANONYMIZED_PURGED_USER`.

---

## 3. Reviewer Data Inventory & Credential Protection

Certified ISL interpreters and Deaf educators who register as peer reviewers provide credentials for administrative verification.
- Passwords are encrypted with PBKDF2-HMAC-SHA256 (100,000 rounds).
- Credential verification documents (RCI certificates, diplomas) are stored in restricted paths and accessible solely by administrative accounts (`ReviewerRole.ADMIN`).
- Reviewer evaluations submitted to the public dashboard display only verified full names and accreditation status; contact emails and hashed passwords are excluded from API serializers (`ReviewerProfileResponse`).

---

## 4. Consent Inventory & Granular Control

Phase 6 introduced four independent, granular consent flags to `ParticipantConsent`:
1. `consent_general_research` (Boolean): Participation in comprehension surveys.
2. `consent_video_recording` (Boolean): Default `False`.
3. `consent_data_sharing` (Boolean): Distribution in open-access academic repositories.
4. `consent_academic_publication` (Boolean): Inclusion in peer-reviewed journal datasets.

If a participant grants consent for research participation but disables `consent_data_sharing`, the `ExportEligibilityService` strictly omits their records from public dataset exports.

