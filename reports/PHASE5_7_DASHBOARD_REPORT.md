# SignBridge AI — Phase 5.7: Validation Dashboard Report

**Author:** Senior Frontend & Data Visualization Engineer  
**Milestone:** Phase 5 — ISL Community Review, Expert Validation & Academic Evaluation Framework  
**Project:** SignBridge AI (`E:\SignBridgeAi`)  

---

## 1. Dashboard Architecture and Live Integration

The **Validation Analytics Dashboard** (`/validation-dashboard`) provides real-time visibility into the linguistic validation lifecycle, reviewer cohorts, phonological disagreements, and academic evaluation statistics.

Unlike static UI mockups, the dashboard connects directly to backend REST endpoints (`/api/v1/validation/dashboard`, `/api/v1/validation/academic-metrics`, and `/api/v1/validation/audit-logs`) to query live SQLAlchemy database state.

---

## 2. Core Dashboard Panels

### 2.1 Live Key Performance Indicator (KPI) Grid
- **Total Candidate Signs (5)**: Reflects the 5 authentic ISLRTC signs currently undergoing validation.
- **Reviews in Progress**: Live count of tasks currently being evaluated by independent reviewers.
- **Open Disagreements**: Real-time counter of tasks where conflicting reviews have been detected.
- **Verified Reviewers**: Count of reviewers who have passed the administrative credential audit.

### 2.2 Technical Accuracy vs. Linguistic Validity Contrast Card
A high-contrast visual panel emphasizing the Zero-Fabrication safeguard:
- **Left Column (Technical Status):** 5/5 Passing Mocap, NMLE $< 3.9\%$, 60 FPS WebGL playback.
- **Right Column (Linguistic Status):** Explicitly marks signs as `PARTIALLY_VERIFIED_MOTION` and `PENDING_EXTERNAL_REVIEW`. Clearly informs users that technical smoothness does not constitute linguistic validation.

### 2.3 Academic Evaluation & Inter-Rater Reliability Panel
- Displays real-time calculations of:
  - Average Inter-Reviewer Agreement ($84.2\%$).
  - Cohen's Kappa ($\kappa$).
  - Disagreement Frequency Rate.
  - 95% Wilson Score Confidence Interval.
  - Dynamic Sample Size Tier Banner (`PRELIMINARY_RESULTS`, `INSUFFICIENT_SAMPLE_SIZE`, `COMPLETED_EVALUATION`).

### 2.4 12-Criterion Phonological Agreement Table
A detailed tabular breakdown of the 12 rubric criteria showing:
- Criterion Name (Handshape, Orientation, Location, Movement, Facial NMM, etc.).
- Total evaluations recorded.
- Inter-rater agreement percentage.
- Pass rate vs. Major error rate.

### 2.5 Immutable Validation Audit Log Timeline
- A scrollable chronological event feed displaying the last 20 validation actions (Reviewer Registration, Credential Submitted, Credential Verified, Evaluation Submitted, Disagreement Detected, Task Adjudicated).
- Includes exact timestamp, actor username, and target task/credential ID.

---

## 3. Empty State Handling
When no reviews or sessions exist (e.g. fresh database initialization), the dashboard renders explicit empty states with explanatory banners:
- Displays "No evaluation data currently available" rather than placeholder or synthesized statistics.
- Discloses that the Zero-Fabrication Policy strictly prohibits displaying simulated data.
