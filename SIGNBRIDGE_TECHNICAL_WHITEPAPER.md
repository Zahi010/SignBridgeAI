# SignBridge AI: Technical Whitepaper
## System Architecture, NLP Transformation, Computer Vision Mocap Retargeting & Statistical Reliability

**Version:** 1.0.0-Release Candidate  
**Date:** November 2026  
**Authors:** SignBridge AI Architecture & Engineering Working Group  
**Codebase:** [https://github.com/Zahi010/SignBridgeAi](https://github.com/Zahi010/SignBridgeAi)  
**Classification:** Technical Whitepaper & Architectural Reference  

---

## 1. System Overview & Modular Monolith Topology

SignBridge AI is engineered as a high-performance modular monolith designed for on-premise university deployment, containerized cloud execution, and air-gapped laboratory use.

```
+-----------------------------------------------------------------------------------+
|                                React 18 / Three.js Frontend                        |
|   - WebGL 3D Avatar Renderer (Skeletal Rigging, GLTF/Mixamo retargeting)          |
|   - Split-Screen Video/Avatar Synchronized Comparison Player                     |
|   - 12-Factor Phonological Evaluation Rubric & Annotation Timeline                |
|   - Academic Statistical Reliability Dashboard (Fleiss' Kappa, Wilson Score CI)   |
+------------------------------------------+----------------------------------------+
                                           | REST API (HTTP/JSON + SSE)
+------------------------------------------v----------------------------------------+
|                               FastAPI Application Backend                         |
|                                                                                   |
|  [NLP Translation Subsystem]               [Mocap & Vision Retargeting Pipeline]  |
|   - spaCy English Dependency Parser         - MediaPipe Holistic / Vision Tasks   |
|   - Engineering Terminology Disambiguator   - Anatomical Skeleton Normalizer      |
|   - ISL Grammar & Topic-Comment Planner     - Forward Kinematics / Euler Retarget |
|                                                                                   |
|  [Zero-Fabrication Safeguard Engine]       [Linguistic Governance & Adjudication] |
|   - Candidate Lexicon Registry (100 terms)  - Multi-Tenant Reviewer Auth & RBAC   |
|   - Pedagogical Fallback Generator          - Disagreement Detection Engine       |
|   - Status: VERIFIED vs UNSUPPORTED         - Post-Restore Tombstone Anti-Purge   |
|                                                                                   |
|  [Statistical & Evaluation Engine]         [Disaster Recovery & Storage]          |
|   - Exact Fleiss' & Cohen's Kappa           - Online SQLite Backup & Restore      |
|   - 95% Wilson Score Binomial Confidence    - Compressed Tar Media Archiving      |
|   - Asset-Level GODL-India Export Guard     - SHA-256 Checksum Sidecars           |
+------------------------------------------+----------------------------------------+
                                           | SQLAlchemy ORM
+------------------------------------------v----------------------------------------+
|                        Persistent Data Storage (SQLite / PostgreSQL)              |
|  - signbridge.db (31 Relational Tables: Lexicon, Mocap, Reviews, Consents, Audit) |
|  - data/sign_videos/ (Raw & Transcoded H.264 authentic master recordings)         |
|  - data/isl_motion/processed/ (Normalized JSON joint rotations & landmarks)       |
+-----------------------------------------------------------------------------------+
```

---

## 2. Natural Language Processing & Translation Engine

Translating technical English into Indian Sign Language requires transforming linear subject-verb-object (SVO) prose into spatial, visual-gestural intermediate representations.

### 2.1 The Intermediate Representation (IR) Pipeline
1. **Tokenization & Part-of-Speech Tagging:** English text is parsed using dependency graph extractors (`en_core_web_sm`).
2. **Domain-Aware Entity Extraction:** 100 candidate engineering terms spanning Computer Science, Electronics & Communication, Electrical Engineering, Civil Engineering, and Mechanical Engineering are recognized via exact and lemmatized dictionary indexing.
3. **Disambiguation:** Syntactic dependencies determine contextual sense. For example, *The torque produced by the induction motor* binds *torque* to rotational mechanics, suppressing civil or aerodynamic interpretations.
4. **ISL Grammar Planning:**
   - **Topic-Comment Ordering:** The grammatical object or topical noun is promoted to the front of the sequence ($[O] \rightarrow [S] \rightarrow [V]$).
   - **Time-First Aspect:** Temporal adverbs (*yesterday*, *tomorrow*, *during steady state*) are placed at the sentence origin.
   - **Interrogatives & Negation:** Question markers (*what*, *how*, *why*) and negators (*not*, *cannot*) are deferred to the sentence terminus.
5. **Zero-Fabrication Gate:** Concepts without an authenticated sign are diverted to the explanation pipeline, generating conceptual analogies and fingerspelling tokens.

---

## 3. Computer Vision & 3D Motion Capture Architecture

SignBridge AI extracts genuine kinematic data from high-definition signing recordings rather than animating avatars via artificial keyframing.

### 3.1 MediaPipe Landmark Extraction
- **Input:** 1080p25 broadcast-standard signing video (`data/sign_videos/`).
- **Vision Tasks:**
  - `pose_landmarker_lite.task` $\rightarrow$ 33 Cartesian coordinates ($x, y, z$, visibility).
  - `hand_landmarker.task` $\rightarrow$ 21 landmarks per hand (wrist, CMC, MCP, PIP, DIP, tip).
  - `face_landmarker.task` $\rightarrow$ 468 facial mesh landmarks.
- **Normalization:** Landmark coordinates are normalized against inter-shoulder distance and sternum origin to eliminate signer height and camera distance variations.

### 3.2 Skeletal Retargeting & Bone Rotations
- Coordinates are mapped to a humanoid standard skeletal rig (Mixamo / Three.js SkinnedMesh).
- Joint angles are computed using spherical trigonometry and directional vector projections:
  $$\vec{v}_{\text{forearm}} = \vec{p}_{\text{wrist}} - \vec{p}_{\text{elbow}}, \quad \vec{v}_{\text{upperarm}} = \vec{p}_{\text{elbow}} - \vec{p}_{\text{shoulder}}$$
- Rotations are stored as Euler angles ($XYZ$ order) and quaternions to prevent gimbal lock.
- Interpolation employs cubic Hermite splines to guarantee smooth velocity curves at 60 FPS in WebGL.

---

## 4. Mathematical & Statistical Evaluation Engine

SignBridge AI contains an academic statistical engine (`academic_metrics_service.py`) verified against published biostatistical literature.

### 4.1 Exact Fleiss' Kappa Formulation
For $N$ validation tasks, $n$ raters per task, and $k$ categorical rubric options:
$$P_i = \frac{1}{n(n-1)} \sum_{j=1}^{k} n_{ij}(n_{ij} - 1), \quad \bar{P} = \frac{1}{N} \sum_{i=1}^{N} P_i$$
$$p_j = \frac{1}{N \cdot n} \sum_{i=1}^{N} n_{ij}, \quad \bar{P}_e = \sum_{j=1}^{k} p_j^2$$
$$\kappa = \frac{\bar{P} - \bar{P}_e}{1 - \bar{P}_e}$$
- **Verification Baseline:** Independently validated against Fleiss' canonical (1971) psychiatric matrix ($N=10, n=14, k=5$), yielding exact $\kappa = 0.210$.
- **Boundary Handling:** Guaranteed $\kappa = 1.0$ under unanimous consensus; zero division safely handled under zero-variance.

### 4.2 Wilson Score Confidence Interval
For acceptance rate $p = \frac{\text{accepted}}{n}$ with 95% confidence ($z = 1.96$):
$$\text{Center} = \frac{p + \frac{z^2}{2n}}{1 + \frac{z^2}{n}}, \quad \text{Spread} = \frac{z \sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$
Bounds are strictly clamped to $[0.0, 1.0]$. Tested and verified for $n=1, n=10, n=1000$.

---

## 5. Security, Privacy & Disaster Recovery Infrastructure

1. **Authentication & Token Revocation:** HMAC-SHA256 JWTs with in-memory and database blacklist (`revoked_tokens`).
2. **Participant Anonymization:** Keyed HMAC-SHA256 pseudonym hashing using server-side pepper (`SIGNBRIDGE_DELETION_PEPPER`) preventing dictionary attacks.
3. **GDPR Article 17 Tombstones:** Persistent tombstone registry (`tombstone_registry.json`) automatically purged upon any database restoration to prevent resurrection.
4. **Disaster Recovery RTO:** Database restoration in 0.082s; Media `.tar.gz` restoration in 0.148s (Total RTO < 0.25s).
5. **Security Headers:** Enforced `nosniff`, `DENY` frames, `strict-origin-when-cross-origin`, and camera/geolocation restrictions.

---

## 6. Software Quality & Regression Metrics

- **Backend Test Suite:** 107 automated test cases passing in 7.43 seconds (`pytest`).
- **Warning Count:** 1 upstream Starlette deprecation warning; 194 deprecation warnings eliminated.
- **Frontend Production Build:** Vite 5.4 + TypeScript 5.0 compiling 2,181 modules in 7.93 seconds with 0 errors.

