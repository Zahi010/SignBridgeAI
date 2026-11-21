# SignBridge AI — Phase 6 Remediation Log

**Date:** November 21, 2026  
**Auditor:** Lead Systems Auditor & Quality Assurance Lead  
**Scope:** Chronological Log of All Identified Defects, Root Causes, Implemented Fixes, and Verification Proofs  

---

## Remediation Inventory

### DEF-01: Server-Side Token Revocation Defect
- **Classification:** Security (Critical)
- **Component:** `backend/app/core/auth.py`, `backend/app/models/validation_models.py`
- **Issue:** Bearer tokens could not be revoked on logout; client-side logout left tokens active until 7-day expiration.
- **Fix:** Created `RevokedToken` model (`phase6_revoked_tokens` table), `is_token_revoked()`, `revoke_token()`, and `POST /api/v1/validation/logout`. Hardened `get_current_reviewer` to reject revoked tokens.
- **Verification:** `backend/tests/test_phase6_security_privacy.py::test_token_revocation_on_logout` PASSED.

---

### DEF-02: Hardcoded Cryptographic Secret Key
- **Classification:** Security (High)
- **Component:** `backend/app/core/config.py`, `backend/app/core/auth.py`
- **Issue:** Secret salt string was hardcoded in `auth.py`.
- **Fix:** Migrated secret key to `Settings` in `config.py` read from `SIGNBRIDGE_SECRET_KEY` environment variable. Added `.env.example` template.
- **Verification:** Verified via configuration overrides in test environment.

---

### DEF-03: Identifier Retention in Audit Trail on Participant Erasure
- **Classification:** Privacy / Ethics (High)
- **Component:** `backend/app/api/endpoints/community.py`
- **Issue:** Calling `/delete-data` purged research sessions but retained the raw pseudonym in `phase5_validation_audit_logs.actor_username` and `target_id`.
- **Fix:** Re-engineered `delete_participant_data` to scrub raw pseudonyms from all historical audit logs (replacing with `ANONYMIZED_PURGED_USER`), cryptographically de-identify the pseudonym (`ANONYMIZED_PURGED_<sha256[:12]>`), and record a non-identifying erasure audit entry.
- **Verification:** `backend/tests/test_phase6_security_privacy.py::test_right_to_erasure_complete_purge_and_sanitization` PASSED.

---

### DEF-04: Indiscriminate Single-License Export
- **Classification:** Legal / Licensing (High)
- **Component:** `backend/app/services/export_eligibility_service.py`, `backend/app/api/endpoints/community.py`
- **Issue:** Export endpoint applied ODC-By across all data, disregarding GODL-India restrictions on ISLRTC media.
- **Fix:** Built `ExportEligibilityService` to segregate exports into 3 distinct licensed packages (`community_evaluations` under ODC-By, `retargeted_mocap` under CC-BY-4.0, `islrtc_reference_metadata` under GODL-India). Strictly excluded unconsented and withdrawn participants.
- **Verification:** `backend/tests/test_phase6_security_privacy.py::test_export_eligibility_multi_license_segregation` PASSED.

---

### DEF-05: Missing Production HTTP Security Headers
- **Classification:** Security (Medium)
- **Component:** `backend/app/main.py`
- **Issue:** HTTP responses lacked defensive headers (nosniff, frame-options, XSS protection).
- **Fix:** Added `SecurityHeadersMiddleware` in `main.py` setting standard defensive headers on all responses.
- **Verification:** `backend/tests/test_phase6_security_privacy.py::test_security_headers_present` PASSED.

---

### DEF-06: Approximate Fleiss' Kappa & Reviewer Cohort Entanglement
- **Classification:** Academic Validity (Medium)
- **Component:** `backend/app/services/academic_metrics_service.py`
- **Issue:** Fleiss' Kappa was approximated using pairwise averages; unverified community participants were entangled with accredited interpreters.
- **Fix:** Formulated exact multi-rater multi-category Fleiss' Kappa formula and added reviewer cohort filtering (`cohort="verified_experts_only"`).
- **Verification:** `backend/tests/test_phase6_security_privacy.py::test_academic_metrics_fleiss_kappa_and_cohort_filter` PASSED.

---

### DEF-07: Absence of Automated Disaster Recovery Automation
- **Classification:** SRE / Resilience (Medium)
- **Component:** `scripts/backup_database.py`, `scripts/restore_database.py`
- **Issue:** No automated online backup or cryptographic integrity verification scripts existed.
- **Fix:** Developed `backup_database.py` and `restore_database.py` with SQLite backup API, SHA-256 sidecar checksums, and pre-restore rollback snapshots.
- **Verification:** `backend/tests/test_phase6_security_privacy.py::test_database_backup_and_restore_cycle` PASSED.
