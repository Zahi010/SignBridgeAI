# SignBridge AI — Expert Validation & Peer Review Workflow

**Document Version:** 1.0.0  
**Effective Date:** November 19, 2026  
**Standards:** Deaf Community Accountability, Multi-Tiered Sign Validation, Immutable Audit Trails

---

## 1. Objectives & Principles

The Expert Validation Workflow guarantees that no sign is marked `VERIFIED` without independent review by certified deaf educators, ISL master interpreters, or academic sign linguists.

### Core Rules:
1. **Zero Synthetic Reviews:** Synthetic or fabricated reviewer identities are strictly prohibited from active production records.
2. **Reviewer Role Classification:**
   - `certified_interpreter`: Government or nationally accredited sign interpreter.
   - `deaf_educator`: Deaf school or college lecturer actively teaching technical subjects.
   - `linguist_researcher`: Academic linguist specializing in Indian Sign Language phonology and syntax.
   - `test_reviewer_local`: Development account clearly designated for automated integration and local test suites.
3. **Immutable Decision Trail:** Every review decision is permanently stored in the `reviewer_validations` table with timestamp, corrections, comments, and accuracy rating (1.0 to 5.0 scale).

---

## 2. Review Decision Taxonomy

When evaluating a candidate sign in the validation queue, a reviewer submits one of four formal decisions:

| Decision Code | Semantic Meaning | Resulting Validation Status |
| :--- | :--- | :--- |
| **`approved`** | The sign accurately reflects established ISL usage and convey technical meaning without ambiguity. | Updated to **`VERIFIED`** |
| **`rejected`** | The proposed sign violates ISL phonological rules or represents an invented/inaccurate gesture. | Set to **`UNSUPPORTED`** |
| **`requires_correction`** | The core concept is understood, but handshape, orientation, or movement needs adjustment. | Maintained at **`NEEDS_REVIEW`** with reviewer feedback logged |
| **`status_modified`** | The reviewer changes the classification (e.g. flagging that a concept requires diagrammatic expansion). | Set to **`EXPLANATION_REQUIRED`** or **`PARTIAL`** |

---

## 3. End-to-End Validation Protocol

```
Candidate Sign Ingested (e.g. from Syllabus or Video)
                     ↓
Status set to: NEEDS_REVIEW (Default)
                     ↓
Enters Queue: GET /api/v1/validation/pending
                     ↓
Qualified Reviewer inspects:
  - Concept definition and technical context
  - Phonological parameters (Handshape, Movement, Location, Orientation, NMMs)
  - Video recording or 3D skeletal preview
  - Proposed regional dialect
                     ↓
Reviewer submits Decision via:
  POST /api/v1/validation/submit
                     ↓
System updates SignRecord & appends entry to:
  GET /api/v1/validation/audit-trail/{sign_record_id}
```

---

## 4. API Endpoints for Expert Reviewers

### 4.1 Queue Retrieval
- **Endpoint:** `GET /api/v1/validation/pending`
- **Parameters:** `branch_code` (optional), `validation_status` (default: `needs_review`), `limit` (default: 50).
- **Response:** List of pending validation records with concept names, subjects, video indicators, and review counts.

### 4.2 Sign Inspection
- **Endpoint:** `GET /api/v1/validation/signs/{sign_record_id}`
- **Response:** Comprehensive phonological parameters, provenance citations, regional variations, and past review history.

### 4.3 Decision Submission
- **Endpoint:** `POST /api/v1/validation/submit`
- **Request Body:**
  ```json
  {
    "sign_record_id": 5,
    "reviewer_name": "Certified Deaf Educator #401",
    "reviewer_role": "certified_interpreter",
    "affiliation": "National ISL Technical Working Group",
    "decision": "approved",
    "assigned_status": "verified",
    "corrections": null,
    "suggested_regional_variation": "Standard Pan-India",
    "comments": "Sign accurately captures sequential logic.",
    "accuracy_rating": 4.8
  }
  ```

### 4.4 Audit Trail
- **Endpoint:** `GET /api/v1/validation/audit-trail/{sign_record_id}`
- **Response:** Chronological ledger of all reviewer decisions, timestamps, ratings, and corrections.

---

*Document certified by Lead AI Engineer & ISL Linguistics Specialist on November 19, 2026.*
