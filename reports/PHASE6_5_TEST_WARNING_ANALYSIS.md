# SignBridge AI — Phase 6.5: Test Warning Analysis & Remediation

**Date:** 2026-11-21  
**Auditor:** Quality Assurance & Code Hygiene Engineer  
**Baseline Warning Count:** 195 warnings (Phase 6 baseline)  
**Current Warning Count:** 1 warning (Upstream Starlette deprecation)  
**Reduction:** 99.49% warning elimination (194 warnings resolved)  

---

## 1. Executive Summary

At the conclusion of Phase 6, `pytest` reported 102 passing tests, but emitted 195 deprecation warnings. Left unresolved, these warnings signaled impending failures upon upgrading Python (Python 3.13 / 3.14 deprecation of naive datetime) and Pydantic (Pydantic V2 deprecation of `class Config`).

The Phase 6.5 audit performed a complete root-cause analysis, classified all warning categories, and refactored the codebase to eliminate every application-level warning.

---

## 2. Root Cause Classification & Remediation Matrix

### 2.1 Category 1: Naive `datetime.utcnow()` Deprecation (Python 3.12+)
* **Issue:** Python 3.12 marked `datetime.datetime.utcnow()` as deprecated because it returns a naive datetime object lacking timezone awareness, leading to silent calculation bugs in UTC comparisons.
* **Warning Pattern:** `DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use datetime.datetime.now(datetime.UTC) or datetime.datetime.now(timezone.utc) instead.`
* **Occurrences:** Over 40 instances across models, endpoints, and ingestion scripts.
* **Remediation:**
  1. In `backend/app/models/entities.py` and `backend/app/models/validation_models.py`: Created helper `get_utc_now()` returning `datetime.now(timezone.utc)` and updated all SQLAlchemy column defaults.
  2. In `backend/app/schemas/`: Updated `Field(default_factory=lambda: datetime.now(timezone.utc))`.
  3. In all endpoints and services: Replaced calls to `datetime.utcnow()` with `datetime.now(timezone.utc)`.

### 2.2 Category 2: Pydantic V1 `class Config` Deprecation (Pydantic V2.0+)
* **Issue:** Pydantic V2 deprecated nested `class Config:` in favor of `model_config = ConfigDict(...)` or `SettingsConfigDict(...)`.
* **Warning Pattern:** `PydanticDeprecatedSince20: Support for class-based \`config\` is deprecated, use ConfigDict instead.`
* **Occurrences:** `backend/app/core/config.py`, `backend/app/api/endpoints/ingestion.py`.
* **Remediation:** Migrated to `SettingsConfigDict(case_sensitive=True, env_file=".env", extra="allow")` and `model_config = ConfigDict(from_attributes=True)`.

### 2.3 Category 3: FastAPI Startup Event Deprecation
* **Issue:** FastAPI `@app.on_event("startup")` is deprecated in favor of Starlette `@asynccontextmanager async def lifespan(app: FastAPI):`.
* **Occurrences:** `backend/app/main.py`.
* **Remediation:** Replaced startup event handler with `lifespan` context manager.

### 2.4 Category 4: Python 3.14 Tarfile Data Filter Deprecation
* **Issue:** Python 3.12 added a deprecation warning for `tarfile.extractall()` without explicit security filter.
* **Occurrences:** `scripts/restore_media.py`.
* **Remediation:** Added `filter='data'` feature detection:
  ```python
  if hasattr(tarfile, 'data_filter'):
      tar.extractall(DATA_DIR, filter='data')
  else:
      tar.extractall(DATA_DIR)
  ```

---

## 3. Residual Warning Analysis

Only a single warning remains in the entire test run:
```text
backend\venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: 
Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
  from starlette.testclient import TestClient as TestClient  # noqa
```

* **Origin:** Upstream FastAPI / Starlette 0.46 testclient dependency.
* **Impact:** Purely internal to `TestClient` initialization in test harness.
* **Resolution Strategy:** Upstream package update when FastAPI releases full `httpx2` client integration. Application code is 100% clean.

---

## 4. Verification Evidence
```bash
pytest backend/tests
======================= 107 passed, 1 warning in 6.98s ========================
```
Zero application warnings remain across all 107 test cases.

