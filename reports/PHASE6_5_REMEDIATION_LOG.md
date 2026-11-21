# SignBridge AI — Phase 6.5: Remediation Log

**Date:** 2026-11-21  
**Project:** SignBridge AI  
**Workspace:** `E:\SignBridgeAi`  
**Auditor & Remediation Lead:** Independent Systems Auditor & Quality Assurance Lead  

---

## 1. Summary of Remediated Defects

During the Phase 6.5 independent audit, 7 verified technical defects and architectural vulnerabilities were identified, remediated in code, and verified through regression testing.

---

## 2. Detailed Remediation Records

### REM-6.5-01: Python 3.12+ `datetime.utcnow()` Deprecation Warnings
- **Severity:** Medium (Impending breaking change in Python 3.14)
- **Files Modified:**
  - `backend/app/models/entities.py`
  - `backend/app/models/validation_models.py`
  - `backend/app/schemas/documents.py`
  - `backend/app/schemas/intermediate_representation.py`
  - `backend/app/schemas/translation.py`
  - `backend/app/services/dataset_ingestion.py`
  - `backend/app/services/video_ingestion.py`
  - `backend/app/services/validation_service.py`
  - `backend/app/api/endpoints/ingestion.py`
  - `backend/app/api/endpoints/validation.py`
  - `backend/app/api/endpoints/validation_v2.py`
  - `backend/app/api/endpoints/documents.py`
  - `scripts/backup_database.py`
  - `scripts/restore_database.py`
  - `scripts/ingest_authentic_isl_videos.py`
- **Correction:** Introduced `get_utc_now()` helper returning `datetime.now(timezone.utc)`; replaced all naive `datetime.utcnow()` occurrences.

### REM-6.5-02: Pydantic V2 Configuration Model Deprecation
- **Severity:** Medium
- **Files Modified:**
  - `backend/app/core/config.py`: Migrated `class Config:` to `model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="allow")`.
  - `backend/app/api/endpoints/ingestion.py`: Migrated to `model_config = ConfigDict(from_attributes=True)`.

### REM-6.5-03: FastAPI Startup Event Deprecation
- **Severity:** Low
- **File Modified:** `backend/app/main.py`
- **Correction:** Replaced `@app.on_event("startup")` with `@asynccontextmanager async def lifespan(app: FastAPI):`.

### REM-6.5-04: Participant Re-Identification Rainbow Table Vulnerability
- **Severity:** High (GDPR Recital 28 / DPDP Act compliance)
- **Files Modified:**
  - `backend/app/core/config.py`: Added `DELETION_PEPPER` configuration.
  - `backend/app/api/endpoints/community.py`: Replaced unsalted SHA-256 with HMAC-SHA256 keyed with server-side pepper and random UUIDv4 erasure tokens.

### REM-6.5-05: Backup Restoration Data Resurrection Vulnerability
- **Severity:** High (GDPR Article 17 Right to Erasure)
- **Files Created/Modified:**
  - Created `backend/app/services/tombstone_service.py` with `register_tombstone()` and `enforce_tombstones()`.
  - Updated `scripts/restore_database.py` to automatically execute `enforce_tombstones()` post-restore.
  - Updated `backend/app/api/endpoints/community.py` to register deletions in the persistent tombstone registry.

### REM-6.5-06: Missing Media Disaster Recovery Automation
- **Severity:** High (Data Loss Risk)
- **Files Created:**
  - `scripts/backup_media.py`: Creates timestamped `.tar.gz` archives with SHA-256 sidecars and manifest updates.
  - `scripts/restore_media.py`: Verifies SHA-256 integrity, path traversal protection, and data filters (RTO: 0.148s).

### REM-6.5-07: Unchecked Asset-Level Export Licensing
- **Severity:** Medium (Intellectual Property & Governance Risk)
- **File Modified:** `backend/app/services/export_eligibility_service.py`
- **Correction:** Added explicit asset-level provenance checks restricting unconfirmed rights and synthetic previews from research exports.

---

## 3. Test Verification
All remediations were tested with automated suites:
- **Backend Tests:** 107/107 passed (`pytest backend/tests`).
- **Deprecation Warnings:** Reduced from 195 to 1 upstream testclient warning.
- **Frontend Build:** Succeeded with 0 errors (`npm run build`).

