# SignBridge AI — Phase 6 Research Ethics Readiness Report

**Date:** November 21, 2026  
**Auditor:** Institutional Review Board (IRB) & Deaf Community Research Ethics Consultant  
**Frameworks:** ICMR National Ethical Guidelines for Biomedical and Health Research, Belmont Report (Autonomy, Beneficence, Justice), WFD Guidelines on Deaf Community Research  
**Status:** READY FOR INSTITUTIONAL ETHICS CLEARANCE  

---

## 1. Ethics Readiness Declaration

> [!IMPORTANT]
> In strict compliance with the **Zero-Fabrication Policy**, SignBridge AI declares that **NO real human research pilot has occurred to date**. 
> All Phase 5 and Phase 6 community research sessions in the test database are automated synthetic regression fixtures. 
> Real human user studies will only commence after formal IRB/IEC ethics approval from accredited partner institutions.

---

## 2. Core Ethical Protections

### 2.1 Autonomy & Voluntary Informed Consent
- **Comprehensible ISL Translation:** The consent workflow is designed to be accessible in both simple written English and signed Indian Sign Language video explanations.
- **Granular Consent:** Participants exercise sovereign control over four distinct usage domains:
  1. Internal educational evaluation.
  2. Video recording permission (default `False`).
  3. Open-access research data sharing (`consent_data_sharing`).
  4. Inclusion in academic publications (`consent_academic_publication`).
- **Unconditional Withdrawal:** Consent can be withdrawn at any time without penalty or loss of benefits.

### 2.2 Protection of Deaf Vulnerability & Community Autonomy
- **No Pathologizing Framework:** SignBridge AI treats ISL as a legitimate, rule-governed natural language, rejecting medicalized deficiency paradigms.
- **Nothing About Us Without Us:** Verification workflows prioritize Deaf native signers and certified ISL interpreters as authoritative adjudicators.
- **Cultural and Regional Sensitivity:** The rubric architecture explicitly accommodates regional dialects (e.g. Northern/Delhi, Western/Mumbai, Southern/Chennai, Eastern/Kolkata), preventing algorithmic linguistic erasure.

---

## 3. Pre-Pilot Verification Matrix

| Ethics Checkpoint | Status | Implementation Evidence |
| :--- | :--- | :--- |
| **Informed Consent Versioning** | OPERATIONAL | `consent_version` tracked per record |
| **Granular Domain Consent** | ENFORCED | 4 boolean fields in `ParticipantConsent` |
| **Instant Right-to-Erasure** | OPERATIONAL | Hard session delete + cryptographic pseudonym purge |
| **Non-Sharing Quarantine** | ENFORCED | `ExportEligibilityService` filters non-consenting users |
| **Deaf Reviewer Accreditation Gate** | ENFORCED | `ReviewerRole.DEAF_NATIVE_SIGNER` + RCI/AIFD verification |
| **Zero-Fabrication Adjudication** | ENFORCED | Refuses promotion to `VERIFIED_ISL_MOTION` without verified human sign-off |

---

## 4. Next Steps for Institutional Protocol Submission

1. Submit protocol to partner university Institutional Ethics Committee (IEC).
2. Attach `PHASE6_PRIVACY_AND_DATA_INVENTORY.md` and `PHASE6_RIGHT_TO_DELETION_AUDIT.md`.
3. Provide sample participant information sheet (PIS) with accompanying ISL translation video.
