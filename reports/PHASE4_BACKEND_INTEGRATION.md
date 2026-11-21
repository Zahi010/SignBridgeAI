# Phase 4 Backend Integration & API Specification

**Service:** Avatar Subsystem REST Endpoints  
**Router Path:** `backend/app/api/endpoints/avatar.py`  
**Base URL:** `/api/v1/avatar`  
**Test Suite:** `backend/tests/test_phase4_avatar.py`  

---

## 1. REST Endpoint Reference

### 1.1 `GET /api/v1/avatar/status`
Returns real-time status of the 3D avatar rig, motion capture library, and Zero-Fabrication safeguards.
- **Response Model:** `AvatarStatusResponse`
- **Payload Sample:**
  ```json
  {
    "avatar_name": "SignBridge Signer-01",
    "rig_standard": "SignBridge-Articulated-54",
    "total_joints_count": 54,
    "finger_joints_count_per_hand": 15,
    "supported_facial_morph_targets": [
      "brow_furrow_left", "brow_furrow_right",
      "brow_raise_left", "brow_raise_right",
      "mouth_open", "mouth_wide",
      "eye_blink_left", "eye_blink_right",
      "head_pitch", "head_yaw", "head_roll"
    ],
    "motion_capture_pipeline_available": true,
    "active_mocap_animations_count": 5,
    "status_breakdown": {
      "partial": 5,
      "not_implemented": 1
    },
    "zero_fabrication_policy_enforced": true,
    "disclaimer": "All motions are governed by the Zero-Fabrication Policy..."
  }
  ```

### 1.2 `GET /api/v1/avatar/animations`
Lists all registered animations with optional filtering by status query parameter (`?status=partial`).
- **Response Structure:** `{ "total_count": int, "animations": [...] }`

### 1.3 `GET /api/v1/avatar/animations/{animation_id}`
Retrieves full keyframe tracks, joint angles, duration, and linguistic disclaimer for a specific animation.

### 1.4 `GET /api/v1/avatar/animations/concept/{concept_id}`
Retrieves animation metadata and phonological parameters for a concept ID.

### 1.5 `POST /api/v1/avatar/sequence`
Assembles a complete multi-concept continuous signing sequence from source text and translation plan.
- **Request Body:**
  ```json
  {
    "source_text": "Algorithm computes frequency",
    "detected_concepts": [{"term": "Algorithm", "category": "DIRECT_LEXICAL"}],
    "grammar_plan": {"sentence_type": "DECLARATIVE"}
  }
  ```
- **Response Model:** `AvatarSequencePayload`

### 1.6 `POST /api/v1/avatar/retarget`
Accepts raw landmark frames on the fly and retargets them to avatar bone Euler keyframes.

---

## 2. Backward-Compatibility Preservation

The Phase 4 upgrade preserves all legacy endpoints without breaking changes:
- `GET /api/v1/avatar/retrieve/{concept_id}` (Legacy metadata resolver)
- `POST /api/v1/avatar/timeline` (Legacy IR timeline generator)
- `POST /api/v1/avatar/upload` (Asset upload handler)

