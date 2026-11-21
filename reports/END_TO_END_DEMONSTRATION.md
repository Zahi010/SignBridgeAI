# SignBridge AI — End-to-End Technical Demonstration Walkthrough

**Document:** `reports/END_TO_END_DEMONSTRATION.md`  
**Purpose:** Documents the smallest genuinely achievable end-to-end educational translation workflows, tracing exact execution paths from raw input to pedagogical and visual output without fabricating unaccredited ISL signs.

---

## 1. Demonstration Philosophy: Absolute Linguistic Transparency

In accordance with our **Zero-Fabricated Signs Policy**:
- We demonstrate the complete, functioning software translation pipeline up to the actual external data boundary.
- When an authentic, peer-reviewed human sign video is unavailable, the system displays an honest unavailable or demo notice. It **never** substitutes a fake sign video or synthetic continuous video.
- When an avatar motion-capture file is unavailable, the 3D viewer displays an attentive resting mannequin and blocks fake procedural gestures.
- When an engineering term lacks certified ISL codification (e.g., *Deadlock*, *Modulation*, *Bracing*), the engine returns `UNSUPPORTED` with two-handed ISL fingerspelling sequences and pedagogical diagram descriptions.

---

## 2. Walkthrough Scenarios

### Scenario A: Uncodified Technical Concept & Pedagogical Explainer
**Input Sentence:**
```
The database system is deadlocked.
```

#### Step-by-Step Execution Path:
1. **Input Preprocessing & Tokenization (`Stage 1`):**
   - Normalized Tokens: `['the', 'database', 'system', 'is', 'deadlocked']`
   - Sentence Type: `DECLARATIVE`
2. **Concept Extraction & Polysemy Disambiguation (`Stage 2`):**
   - Extracted Concepts:
     - `Database` (Category: Data Management, Domain: Database Systems)
     - `Deadlock` (Category: Systems Software, Domain: Concurrency & Synchronization)
   - Disambiguation: Both terms validated as technical entities within Computer Science & Engineering.
3. **ISL Syntactic Restructuring & Gloss Planning (`Stage 3`):**
   - ISL Gloss Sequence: `['DATABASE', 'DEADLOCK']`
   - Topic-Comment Structure: Prioritizes establishing physical entities before state descriptions.
4. **Zero-Fabrication Policy Enforcement (`Stage 4`):**
   - Status Verdict: **`UNSUPPORTED`**
   - Policy Rule Applied: *Sentence contains uncodified engineering concept (`Deadlock`). The system strictly suppresses `VERIFIED` labels and refuses to synthesize non-standard gestures.*
   - Pedagogical Explainer Generated:
     - **Why Unsupported:** No certified single-sign ISL equivalent has been codified by ISLRTC or national Deaf associations.
     - **Recommended Strategy:** Letter-by-letter two-handed ISL fingerspelling:  
       `['D', 'E', 'A', 'D', 'L', 'O', 'C', 'K']`
     - **Conceptual Diagram Description:** Draw two competing process nodes in circular wait holding locks on resource boxes $R_1$ and $R_2$.
5. **Multimodal Media Output Control (`Stage 5`):**
   - **Video Output:** `available: False`. Crucial fix: The video for *Database* is intentionally suppressed so the learner is not misled by an incomplete single-sign playback.
   - **3D Avatar Viewer:** Mannequin remains in an attentive resting posture. Explicit alert displayed: *"Procedural arm gestures blocked under Zero-Fabrication Policy."*

---

### Scenario B: Contextual Polysemy Disambiguation
**Pair of Input Sentences:**
1. *"Explain how current flows through a circuit."* (Technical electrical context)
2. *"Current research focuses on artificial intelligence."* (Chronological / modern context)

#### Execution Results & Linguistic Justification:
- **Sentence 1 (Electrical Circuit):**
  - **Extracted Concepts:** `Current` (EEE) and `Circuit` (ECE/EEE)
  - **Disambiguation Confidence:** 0.95
  - **Semantic Relation:** `[Current] --(flows_through)--> [Circuit]`
  - **Gloss Sequence:** `['CURRENT', 'CIRCUIT', 'FLOW-MOVE']`
  - **Linguistic Justification:** Electrical *Current* represents directional movement of electrons through a physical conductor.
- **Sentence 2 (Temporal Adjective):**
  - **Extracted Concepts:** None (0 concepts)
  - **Disambiguation Rationale:** *Current* is identified as a temporal marker modifying *research*, not an electrical charge.
  - **Status Verdict:** `UNSUPPORTED` (General query without engineering concepts)
  - **Linguistic Justification:** The system successfully prevents misattributing the electrical sign for *Current* in non-technical sentences.

---

### Scenario C: Curated Candidate STEM Concept with 6-Parameter Phonology
**Input Sentence:**
```
What is voltage?
```

#### Step-by-Step Execution Path:
1. **Concept Extraction:** `Voltage` (Discipline: Electrical & Electronics Engineering, Code: `ISL-EEE-001`)
2. **ISL Syntactic Restructuring:**
   - Topic: `VOLTAGE`
   - Interrogative Movement: Terminal `WHAT` with non-manual marker:
   - Gloss Sequence: `['VOLTAGE', 'WHAT [NMM: Furrowed Brow]']`
   - Linguistic Rule: In natural ISL, WH-questions are obligatorily placed at the end of the sentence synchronized with furrowed eyebrows.
3. **Phonological Parameter Display (Vocabulary Explorer & Translator Card):**
   - **Dominant Hand:** Right (Two-Handed Contact)
   - **Handshape:** Modified V-handshape depicting electric potential difference
   - **Movement:** Quick tapping contact between index and middle fingertips and non-dominant palm
   - **Location:** Chest level neutral space
   - **Orientation:** Palm facing inward towards body
   - **Non-Manual Markers:** Focused gaze, slight forward head tilt during lexical peak
4. **Media Asset Provenance Status:**
   - **Sign Video Player:** Serves `voltage_sign.mp4` with prominent amber badge: **`DEMO MEDIA ONLY`** (*FFmpeg synthetic benchmark test pattern; authentic studio recording scheduled for Phase 2*).
   - **3D Avatar:** Displays 3D WebGL mannequin with notice: *Attentive resting posture. 54-keypoint mocap ingestion pending studio recording.*

---

## 3. Verification Commands to Reproduce Live Demonstration

```powershell
# 1. Start Backend API
cd E:\SignBridgeAi
.\backend\venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

# 2. Start Frontend Dev Server
cd E:\SignBridgeAi\frontend
npm run dev

# 3. Open Web Translator
# Navigate to: http://127.0.0.1:5173/translate
# Select 'Unsupported Concept (Deadlock)' or enter: 'The database system is deadlocked.'
# Inspect: Live Pipeline Trace, Fingerspelling Array, Pedagogical Diagram, Media Disclaimers.
```

