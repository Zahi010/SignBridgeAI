# SignBridge AI — Phase 7.3: Controlled Expert Onboarding Report

**Date:** 2026-11-21  
**Project:** SignBridge AI  
**Workspace:** `E:\SignBridgeAi`  
**Milestone:** Phase 7.3  

---

## 1. Overview & Security Architecture

Phase 7.3 audited and enhanced the reviewer onboarding workflow to ensure that external sign language linguists, certified interpreters (RCI), and Deaf master signers can be securely invited, onboarded, and accredited without compromising data integrity or permitting unauthorized reviewers to approve signs.

---

## 2. Onboarding Workflow Implementation

```
[System Administrator]
          │
          ▼
[Generates Secure Invitation] ──► POST /api/v1/validation/invitations
(Code: INV-XXXXXXXX, Expiry: 30d)
          │
          ▼
[External Expert Receives Token]
          │
          ▼
[Token Verification & Registration] ──► GET /api/v1/validation/invitations/verify/{code}
- Pre-fills verified name, email, role, and institutional affiliation.
- Enforces strong password and identity confirmation.
          │
          ▼
[Credential Submission] ──► POST /api/v1/validation/credentials
- Submits RCI Registration Number, Deaf Association Membership, or License.
- Account Status: VERIFICATION_PENDING.
          │
          ▼
[Administrative Credential Gate] ──► POST /api/v1/validation/credentials/{id}/verify
- Administrator verifies evidence against public registry (e.g. RCI CRR).
- Upgrades status to VERIFIED.
          │
          ▼
[Task Assignment & Evaluation] ──► Access to synchronized review portal.
```

---

## 3. Key Safeguards & Audit Verifications

1. **Invitation Code Verification Endpoint (`/invitations/verify/{code}`):**
   - Validates single-use token validity.
   - Intercepts expired tokens using timezone-aware UTC datetime parsing.
   - Verified in automated regression test `test_reviewer_invitation_lifecycle`.
2. **Warning Against False Accreditation:**
   - The registration interface explicitly warns reviewers: *"Falsifying professional qualifications or RCI registration numbers violates research ethics and will result in immediate permanent suspension."*
3. **Isolation of Test Accounts:**
   - Seeded test accounts (`rev_arun_rci`, `rev_devika_1`) are clearly segregated with `test` tags and cannot be confused with live external reviewers.

---

## 4. Phase 7.3 Status Verdict: **PASS**
The controlled expert onboarding mechanism is hardened, verified with regression tests, and ready for deployment to external reviewers.

