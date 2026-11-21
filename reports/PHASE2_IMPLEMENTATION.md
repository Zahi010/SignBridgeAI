# SignBridge AI — Phase 2: Authentic ISL Data Acquisition & Dataset Ingestion Architecture

**Milestone:** Phase 2: Authentic ISL Data Acquisition & Signing Dataset Development  
**Date:** 2026-11-20  
**Lead AI Systems Auditor & Technical Architect:** Senior AI Systems Auditor & ISL Research Team  
**Status:** IMPLEMENTED, MIGRATED, AND VERIFIED  

---

## 1. Architectural Overview & Design Philosophy

Phase 2 transitions SignBridge AI from an exploratory prototype into an **accreditation-governed, ethically grounded platform** designed to ingest, validate, and serve authentic Indian Sign Language data.

```
+---------------------------------------------------------------------------------------------------+
|                                  SIGNBRIDGE AI PHASE 2 ARCHITECTURE                               |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Authentic Video / CSV / JSON]                                                                   |
|                |                                                                                  |
|                v                                                                                  |
|  +-----------------------------+       +------------------------------------+                     |
|  |   Dataset Ingestion Engine  | ----> | Recording Session & Consent Check  |                     |
|  | - Format: MP4, MOV, WebM    |       | - DPDPA 2023 Consent Verification  |                     |
|  | - FFprobe stream metadata   |       | - Camera / Lighting / Backdrop     |                     |
|  | - FFmpeg thumbnail extract  |       +------------------------------------+                     |
|  +-----------------------------+                         |                                        |
|                |                                         v                                        |
|                v                             +-----------------------+                            |
|  +-----------------------------+             |  SignRecord Database  |                            |
|  |  Batch Ingestion Pipeline   | ----------> | - Status: NEEDS_REVIEW| (Strict initial state;     |
|  | - Zero fabrication policy   |             | - Phonological params |  never auto-verified)      |
|  | - Missing fields kept NULL  |             +-----------------------+                            |
|  +-----------------------------+                         |                                        |
|                                                          v                                        |
|                                       +--------------------------------------+                    |
|                                       |     Expert ISL Peer Review Gate      |                    |
|                                       |  - Requires ReviewerProfile          |                    |
|                                       |  - is_authorized_expert == True      |                    |
|                                       +--------------------------------------+                    |
|                                               /                      \                            |
|                       (Authorized Expert)    /                        \   (Unaccredited / Dev)    |
|                                             v                          v                          |
|                               +-------------------------+     +------------------------+          |
|                               | Status -> VERIFIED      |     | HTTP 403 FORBIDDEN     |          |
|                               | Sign Marked Authentic   |     | Rejection of VERIFIED; |          |
|                               | Audit Trail Appended    |     | Review / Notes only    |          |
|                               +-------------------------+     +------------------------+          |
|                                             |                                                     |
|                                             v                                                     |
|                               +-------------------------+                                         |
|                               |   Translation Runtime   |                                         |
|                               | - Serves verified video |                                         |
|                               | - Avatar: Neutral rest  |                                         |
|                               |   (pending 3D mocap)    |                                         |
|                               +-------------------------+                                         |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Database Schema Extensions & Migration

The Phase 2 schema was migrated directly into SQLite (`backend/signbridge.db`) with zero data loss using `scripts/migrate_phase2_schema.py`.

### 2.1 New Entity: `RecordingSession`
Stores studio recording parameters and legal consent verification:
```python
class RecordingSession(Base):
    __tablename__ = "recording_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_uid = Column(String(100), unique=True, index=True, nullable=False)
    signer_id = Column(String(100), nullable=False)
    signer_name = Column(String(150), nullable=True)
    is_native_signer = Column(Boolean, default=True)
    camera_setup = Column(String(150), default="Frontal 1080p60 Studio Setup")
    lighting_environment = Column(String(150), default="Three-point softbox, zero harsh shadows")
    background = Column(String(150), default="Neutral 18% Gray / Chroma Green")
    consent_status = Column(Enum(ConsentStatus), default=ConsentStatus.PENDING_CONSENT, nullable=False)
    consent_document_ref = Column(String(200), nullable=True)
    consent_date = Column(DateTime, nullable=True)
    recording_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 2.2 New Entity: `ReviewerProfile`
Enforces accreditation checks on sign certification:
```python
class ReviewerProfile(Base):
    __tablename__ = "reviewer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    reviewer_code = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    is_certified_interpreter = Column(Boolean, default=False)
    is_deaf_native_signer = Column(Boolean, default=False)
    accreditation_body = Column(String(150), nullable=True)
    accreditation_number = Column(String(100), nullable=True)
    institution_affiliation = Column(String(150), nullable=True)
    qualifications = Column(Text, nullable=True)
    is_authorized_expert = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 2.3 Extended Existing Entities
- **`SignRecord`**: Added `recording_session_id`, `recording_filename`, `recording_metadata_json`, `regional_variation_notes`.
- **`SignVideo`**: Added `recording_session_id`.
- **`ReviewerValidation`**: Added `reviewer_profile_id` and `accreditation_evidence`.

---

## 3. Authentic Dataset Ingestion Engine (`backend/app/services/dataset_ingestion.py`)

### 3.1 Media Probing & Stream Validation
1. **Container Whitelist:** `.mp4`, `.mov`, `.webm`.
2. **Technical Probing via FFprobe:** Automatically queries video width, height, framerate, duration, bitrate, and codec without external network calls.
3. **Automated Thumbnail Extraction via FFmpeg:** Generates high-resolution PNG keyframes at `t=0.5s` stored in `data/sign_videos/thumbnails/`.
4. **Size Bounds:** Enforces 100MB per-video upload limits to prevent resource exhaustion.

### 3.2 Batch Annotation Ingestion (CSV / JSON)
- Parses external metadata tables into `SignRecord` database rows.
- **Zero Fabrication Rule:** If external datasets do not document non-manual markers, dominant hand, or spatial locations, those fields remain strictly `None`.
- All batch-ingested candidate signs are initialized with status `NEEDS_REVIEW`.

---

## 4. Expert Review Workflow & Rejection of Unauthorized Reviewers

### 4.1 Strict Authorization Rule on `POST /api/v1/validation/submit`
The system strictly prevents unaccredited developers or automated tests from self-approving candidate signs:
```python
if req.assigned_status == ValidationStatus.VERIFIED:
    if not profile or not profile.is_authorized_expert:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                f"Forbidden: Reviewer '{req.reviewer_name}' is not an authorized expert. "
                "Only certified Deaf native signers or licensed RCI ISL interpreters can certify a sign as VERIFIED."
            )
        )
```

### 4.2 Immutable Audit Trail
Every review action generates a timestamped `ReviewerValidation` entry containing:
- `reviewer_profile_id` linking to official accreditation credentials.
- `accreditation_evidence` (e.g. `Rehabilitation Council of India (RCI) (Ref: RCI-CRR-A12345)`).
- Accuracy rating (1.0 to 5.0) and phonological correction notes.

---

## 5. API Endpoints Registered (`/api/v1`)

| Method | Endpoint | Description | Phase 2 Governance |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/ingestion/recording-session` | Register new recording session | Mandates consent status & equipment metadata |
| `GET` | `/api/v1/ingestion/recording-sessions` | List registered recording sessions | Displays consent status and signer ID |
| `POST` | `/api/v1/ingestion/sign-video` | Ingest human signing video | FFprobe metadata extraction + FFmpeg thumbnail |
| `POST` | `/api/v1/ingestion/batch-json` | Batch-ingest JSON sign annotations | Zero-fabrication ingestion; enqueues `NEEDS_REVIEW` |
| `POST` | `/api/v1/ingestion/batch-csv` | Batch-ingest CSV sign annotations | Zero-fabrication ingestion; enqueues `NEEDS_REVIEW` |
| `GET` | `/api/v1/validation/reviewers` | List registered reviewer profiles | Differentiates accredited experts from test accounts |
| `POST` | `/api/v1/validation/submit` | Submit sign validation decision | Blocks unaccredited accounts from assigning `VERIFIED` |
| `GET` | `/api/v1/validation/audit-trail/{id}` | Complete audit log for sign | Shows credentials, accreditation, and decisions |

---

## 6. Avatar Non-Concatenation & Resting State Integrity

To prevent ungrammatical synthetic avatar animations from misleading students:
1. All avatar entries without laboratory-grade 54-keypoint mocap are stored with `asset_path = 'UNAVAILABLE_PENDING_MOCAP'`.
2. The 3D avatar viewer displays an **Authentic ISL Mocap Pending** advisory and maintains a neutral anatomical resting posture.
3. The translation pipeline outputs:
   - `verified_signs_count` vs `unsupported_signs_count`.
   - Clear grammar and pedagogical advisory for educator-led delivery.

