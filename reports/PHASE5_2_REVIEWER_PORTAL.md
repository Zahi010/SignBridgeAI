# SignBridge AI — Phase 5.2: Expert Reviewer Portal

**Author:** Senior Front-End Engineer & ISL Evaluation Specialist  
**Milestone:** Phase 5 — ISL Community Review, Expert Validation & Academic Evaluation Framework  
**Project:** SignBridge AI (`E:\SignBridgeAi`)  

---

## 1. Overview and Operational Role

The **Expert Reviewer Portal** (`/expert-review`) is a professional workspace engineered specifically for certified Indian Sign Language interpreters, Deaf master signers, and academic linguists. It operationalizes the linguistic validation architecture designed in Phase 5.1.

Unlike general consumer interfaces, this portal provides precise synchrony between 1080p human signer reference videos and the 3D WebGL avatar, single-frame temporal stepping ($\pm 33\text{ms}$), multi-speed scrubbing, timestamped flaw annotation, and a 12-criterion evaluation rubric with critical phonological error protection.

---

## 2. Reviewer Identity, Roles and Accreditation Tiers

SignBridge AI enforces an explicit administrative accreditation gate:

```
[Registration] ---> Status: UNVERIFIED
      |
      v
[Submit Credential] (RCI Registration Number, Deaf Association Membership)
      |
      v
Status: VERIFICATION_PENDING
      |
      v
[Administrative Audit] (Verification against central RCI / association register)
      |
      +---> [Approved] ---> Status: VERIFIED (Authorized to certify signs)
      +---> [Rejected] ---> Status: REJECTED (Reason documented in audit log)
```

### Reviewer Roles Supported:
1. **`deaf_native_signer`**: Native Deaf individuals whose primary language is ISL. Primary authority on naturalness, ease of perception, and community acceptance.
2. **`certified_interpreter`**: Certified by the Rehabilitation Council of India (RCI) or State Deaf Associations. Authority on pedagogical clarity, grammatical adherence, and lexical precision.
3. **`expert_reviewer`**: Academic linguist, university professor, or sign lexicographer. Authority on syntactic rules, phonological taxonomy, and cross-linguistic disambiguation.
4. **`admin`**: System administrator responsible for auditing credentials, managing validation projects, and resolving inter-reviewer disagreements.
5. **`reviewer`**: General candidate reviewer. Permitted to submit exploratory feedback and draft notes; cannot certify signs as `VERIFIED_ISL_MOTION`.

---

## 3. Portal Frontend Capabilities

### 3.1 Reviewer Authentication & Credential Modal (`ReviewerAuthModal.tsx`)
- Reviewer login and registration with explicit role selection and qualifications logging.
- Credential submission dialog supporting RCI certificates, AIFD registration numbers, and university diplomas.
- Prominent verification status badges:
  - `UNVERIFIED` (Gray): Candidate account, draft permissions only.
  - `VERIFICATION_PENDING` (Amber): Awaiting administrative review.
  - `VERIFIED` (Emerald): Formally accredited expert with certification authority.
  - `REJECTED` (Rose): Inadequate or unverified documentation.

### 3.2 Candidate Signs Queue
- Left-hand navigation queue displaying all active validation tasks.
- Task status indicators:
  - `PENDING_REVIEW`: Awaiting initial evaluation.
  - `UNDER_REVIEW`: One review submitted.
  - `REVIEWED`: Multiple reviews completed.
  - `DISAGREEMENT_DETECTED`: Conflicting reviews flagged for adjudication.
- Review count badges and conflict alerts.

### 3.3 Synchronized Dual-Engine Comparison Player
- **Left Panel (Reference):** Authentic ISLRTC 1080p reference video player displaying current playback timestamp, signer attribution, and resolution tags.
- **Right Panel (Avatar):** Interactive Three.js WebGL 54-joint articulated avatar executing the identical retargeted motion capture track.
- **Master Transport Controls:**
  - Synchronized Play / Pause.
  - Reset to start ($0\text{ms}$).
  - Single-frame step controls ($\pm 33\text{ms}$).
  - Smooth seek slider with millisecond readout.
  - Multi-speed playback ($0.25\times, 0.5\times, 1.0\times, 1.5\times$).

### 3.4 Interactive Timestamp Annotation
- Allows reviewers to pause at an exact millisecond and tag a specific flaw (e.g. collapsed knuckle, velocity jitter, inverted palm).
- Real-time annotation feed displaying timestamps and categorization.
- Anchors qualitative observations directly to skeletal animation timelines.

### 3.5 12-Criterion Rubric & Decision Submission (`EvaluationRubricForm.tsx`)
- Intuitive rating buttons for each criterion (`Pass`, `Minor Issue`, `Major Issue`, `Incorrect`, `Unable to Assess`).
- Critical error lock: if a major phonological error is flagged, the overall recommendation is prevented from selecting "Accept".
- Actions: **Save Review Draft** (persists without affecting task status) and **Submit Final Evaluation** (triggers disagreement detection and status advancement).
