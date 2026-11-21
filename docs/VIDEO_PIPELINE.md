# SignBridge AI — Human ISL Signing Video Pipeline Architecture

**Document Version:** 2.0.0  
**Effective Date:** November 20, 2026  
**Standards:** Zero Fabricated Signs Policy, FFmpeg Probe & Thumbnail Automation, Strict Attribution, Isolated Retrieval

---

## 1. Overview & Architecture

The SignBridge AI Human Video Pipeline is engineered to ingest, validate, store, and serve authentic recordings of Deaf signers and certified Indian Sign Language (ISL) interpreters.

### Non-Negotiable Policy Directives:
1. **Zero Concatenation Rule:** The system strictly **prohibits** stringing isolated sign video clips together to fabricate a pseudo-continuous sentence video. Natural ISL requires fluent transitions, co-articulation, and continuous non-manual markers that cannot be faked by naive video concatenation.
2. **Mandatory Metadata & Provenance:** Every video record maintains signer attribution, native signer status, license terms, duration, resolution, frame rate, and validation status.
3. **Validation Default:** All newly uploaded videos default to `NEEDS_REVIEW` until approved by a qualified reviewer.

---

## 2. Ingestion Pipeline Execution Flow

```
Raw Media File (MP4, WebM) Uploaded
                ↓
File Format & Size Guard (< 50MB, MIME verification)
                ↓
ffprobe Metadata Extraction:
  - Exact duration in seconds
  - Width x Height & Resolution Label (1080p, 720p, etc.)
  - Codec (H.264, VP9) & Framerate (FPS)
                ↓
ffmpeg Automated Thumbnail Generation:
  - High-clarity JPEG frame extracted at 1.0s timestamp
  - Stored in data/sign_videos/thumbnails/
                ↓
Sanitized Storage on Disk:
  - Saved to data/sign_videos/{slug}_{timestamp}.mp4
                ↓
Database Persistence:
  - Created under table sign_videos with status: NEEDS_REVIEW
```

---

## 3. Video Retrieval Engine

The video retrieval service (`backend/app/services/video_retrieval.py`) resolves video assets for translated sentences using strict match categorization:

| Match Category | Criteria | Presentation Behavior |
| :--- | :--- | :--- |
| **`EXACT_MATCH`** | Concept has an authenticated, peer-reviewed ISL video (`VERIFIED`). | Full video player rendered with playback controls and green badge. |
| **`CONTEXTUAL_MATCH`**| Candidate video exists but is currently undergoing validation (`NEEDS_REVIEW`). | Video displayed with amber review disclaimer badge. |
| **`PARTIAL_MATCH`** | Multi-concept sentence has video for some terms, but others lack video. | Verified concept videos displayed individually; missing terms clearly noted. |
| **`NO_MATCH`** | Concept has no authenticated sign recording. | Transparent empty state displayed; zero playback of irrelevant videos. |

---

## 4. API Specification

### 4.1 Video Ingestion
- **Endpoint:** `POST /api/v1/videos/upload`
- **Content-Type:** `multipart/form-data`
- **Fields:** `sign_record_id` (int), `title` (str), `signer_name` (str), `source_attribution` (str), `license_type` (str), `is_native_signer` (bool), `notes` (str), `file` (UploadFile).
- **Response:**
  ```json
  {
    "status": "success",
    "video_id": 5,
    "sign_record_id": 5,
    "title": "Algorithm - Candidate Sign Recording",
    "video_path": "/data/sign_videos/algorithm_20261120_060226.mp4",
    "thumbnail_path": "/data/sign_videos/thumbnails/algorithm_20261120_060226_thumb.jpg",
    "duration_seconds": 2.0,
    "resolution": "640x360 (25.0 fps, h264)",
    "validation_status": "needs_review",
    "message": "Video successfully ingested and placed in expert validation queue."
  }
  ```

### 4.2 Concept Video Retrieval
- **Endpoint:** `GET /api/v1/videos/retrieve/{concept_id}`
- **Response:** Match classification (`EXACT_MATCH`, `NO_MATCH`), video URL, duration, resolution, license, and validation status.

### 4.3 Multi-Concept Sentence Retrieval
- **Endpoint:** `GET /api/v1/videos/sentence-retrieval?concept_ids=1,4`
- **Response:** Granular per-concept matches with explicit policy notice rejecting synthetic concatenation.

---

*Document certified by Computer Vision Engineer & Full-Stack Architect on November 20, 2026.*
