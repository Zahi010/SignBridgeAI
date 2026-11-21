# SignBridge AI — Phase 6.5: Research Ethics Gap Analysis

**Date:** 2026-11-21  
**Auditor:** Human Subjects Research Ethics & Linguistic Governance Specialist  
**Reference Frameworks:** Declaration of Helsinki, ICMR Ethical Guidelines for Biomedical Research (India), Deaf Studies Research Ethics Protocols  

---

## 1. Executive Summary

Conducting research with the Deaf signing community requires specialized ethical governance beyond standard software testing. Deaf signers represent a linguistic minority with a documented history of exploitative, non-consensual linguistic extraction and uncredited data harvesting.

This gap analysis evaluated SignBridge AI against institutional review board (IRB) requirements and identified operational prerequisites before real human participants are invited to evaluate signs.

---

## 2. Completed Ethical Infrastructure (Current Baseline)

The following governance safeguards are fully implemented and verified in code:
1. **Granular Informed Consent:** The consent model (`ParticipantConsent`) captures independent consent flags:
   - General research participation
   - Video recording authorization (opt-in only)
   - Cross-institutional data sharing
   - Academic publication permissions
   - Explicit confirmation that consent may be withdrawn at any time without penalty.
2. **Right to Erasure:** Complete hard-purge of research sessions, anonymization of consent, audit log sanitization, and tombstone persistence to prevent resurrection.
3. **Low-Entropy Protection:** Keyed HMAC-SHA256 pseudonym hashing preventing dictionary attacks.
4. **Zero-Fabrication Safeguard:** Absolute refusal to simulate reviewer responses or synthesize Deaf community feedback.

---

## 3. Pre-Pilot Ethical Gaps & Operational Prerequisites

Before launching live community research sessions with real Deaf signers, the following operational gaps must be closed:

### 3.1 IRB / Institutional Ethics Committee (IEC) Formal Protocol
* **Current Status:** Ethical architecture is technically ready, but formal Institutional Ethics Committee protocol approval has not been submitted to an affiliated university or hospital review board.
* **Remediation Required:** Prepare participant information sheets (PIS) and informed consent forms (ICF) in written English, Hindi, and pre-recorded ISL video formats. Submit formal application to an accredited Indian Ethics Committee.

### 3.2 ISL Video-Based Consent Protocol
* **Gap:** Written consent forms are inaccessible to signers with limited English or Hindi literacy.
* **Remediation Required:** Produce professional ISL video translations of every consent clause. Embed an interactive video consent viewer in the frontend where Deaf signers view each clause signed in ISL before providing electronic consent.

### 3.3 Signer Compensation & Attribution Policy
* **Gap:** No codified financial remuneration or formal academic co-authorship policy exists in the repository documentation.
* **Remediation Required:** Establish standard honoraria for Deaf signers and expert reviewers per session in compliance with ICMR fair compensation guidelines. Explicitly document academic contributor accreditation agreements.

---

## 4. Ethical Readiness Verdict
The technical infrastructure for ethical research data governance is complete and certified. Field recruitment of Deaf participants remains on hold pending formal IRB protocol approval and ISL video consent media creation.
