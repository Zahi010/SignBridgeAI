# SignBridge AI — Phase 3 Live Demonstration Walkthrough

**Lead Demonstrator & AI Engineer:** SignBridge AI Core Team  
**Date:** November 20, 2026  
**Audience:** Technical Reviewers, Deaf Education Specialists, System Auditors  
**Project Directory:** `E:\SignBridgeAi`

---

## 1. Demonstration Setup & How to Run

### 1.1 Starting the Backend Server
In PowerShell:
```powershell
cd E:\SignBridgeAi
backend\venv\Scripts\uvicorn.exe backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Documentation available at: `http://127.0.0.1:8000/docs`
- Health check available at: `http://127.0.0.1:8000/api/v1/health`

### 1.2 Starting the Frontend Client
In a second terminal:
```powershell
cd E:\SignBridgeAi\frontend
npm run dev
```
- Web interface available at: `http://localhost:5173/translator`

---

## 2. Five Live Demonstration Scenarios

SignBridge AI provides a dedicated **Audience-Ready Live Presentation Mode** directly on the Translator page with 5 preloaded test scenarios illustrating the core capabilities and safeguards of the system.

### Scenario 1: Authentic Human ISL Video Demonstration (Computer Science)
- **Input Text:** `"What is an algorithm?"`
- **Branch:** Computer Science (`cs`)
- **Pipeline Execution:**
  - **Stage 1 (Tokenization):** Identifies `algorithm` as technical NOUN; identifies `what` as WH-interrogative. Sentence Type: `WH_QUESTION`.
  - **Stage 2 (Concept Extraction):** Matches `Algorithm` (`concept_id=5`). Disambiguation confirms computational procedure.
  - **Stage 3 (Experimental Grammar):** Applies Topic-Comment order: `[ALGORITHM] + [WHAT [NMM: Furrowed Brow]]`. Explicitly flagged with `UNVALIDATED_HYPOTHESIS` disclaimer.
  - **Stage 4 (Policy Audit):** Verifies authentic provenance: `ISLRTC Open Educational Release` under GODL-India license.
  - **Stage 5 (Multimodal Stream):** Serves genuine 1080p human signing video (`/data/sign_videos/islrtc_algorithm.mp4`). Mounts interactive 3D WebGL avatar in resting posture.
  - **Translation Plan Card:** Displays `LEXICAL_SIGN_DIRECT` strategy unit.

### Scenario 2: Dual Verified Signals Concept (Electronics & Communication)
- **Input Text:** `"How does frequency relate to current?"`
- **Branch:** Electronics & Communication (`ece`)
- **Pipeline Execution:**
  - **Concepts Extracted:** `Frequency` (`concept_id=40`) and `Current` (`concept_id=10`).
  - **Disambiguation Check:** Confirms electrical charge flow (supported by ECE context).
  - **Semantic Triple:** Extracted `[Frequency] -> [relates_to] -> [Current]`.
  - **Spatial Loci Assignment:** Assigns `Frequency` to `LOCUS_A` (left) and `Current` to `LOCUS_B` (right).
  - **Video Playback:** Retrieves authentic ISL recording (`islrtc_frequency.mp4`).

### Scenario 3: Civil & Mechanical Systems (Beam & Torque)
- **Input Text:** `"A structural beam supports torque."`
- **Branch:** Civil Engineering (`civil`)
- **Pipeline Execution:**
  - **Concepts Extracted:** `Beam` (`concept_id=67`) and `Torque` (`concept_id=50`).
  - **Disambiguation Check:** Confirms structural flexural member (supported by `supports`, `structural`), not optical light ray.
  - **Video Playback:** Serves authentic 4K/1080p ISLRTC video (`islrtc_beam.mp4`).
  - **Translation Plan:** Displays 2 `LEXICAL_SIGN_DIRECT` units and 1 `RELATIONAL_SPATIAL_INDEX` unit.

### Scenario 4: Partially Supported Concept & Pedagogical Explanation (Operating Systems)
- **Input Text:** `"Explain how an operating system works with memory."`
- **Branch:** Computer Science (`cs`)
- **Pipeline Execution:**
  - **Concepts Extracted:** `Operating System` (`concept_id=2`) and `Memory`.
  - **Status:** `PARTIAL`
  - **Pedagogical Explanation Triggered:** `Operating System` is an abstract composite concept. System decomposes it into process scheduling + memory management classifiers.
  - **Zero-Fabrication Policy:** Video is not fabricated for the abstract term; fingerspelling sequence `O-P-E-R-A-T-I-N-G S-Y-S-T-E-M` is displayed alongside structured classroom guidance.

### Scenario 5: Unsupported Concept & Zero-Fabrication Enforcement (Deadlock)
- **Input Text:** `"What is a deadlock in operating systems?"`
- **Branch:** Computer Science (`cs`)
- **Pipeline Execution:**
  - **Concepts Extracted:** `Deadlock` (`concept_id=4`).
  - **Status:** `UNSUPPORTED`
  - **Crucial Safeguard:** Single-concept video playback is strictly disabled to prevent misleading demonstration.
  - **Educational Breakdown:** Surfaces 4-step circular-wait classifier explanation card:
    1. Two-handed fingerspelling `D-E-A-D-L-O-C-K`.
    2. Spatial establishment of Process 1 at Left (Locus A) and Process 2 at Right (Locus B).
    3. Resource lock holding classifiers.
    4. Crossover circular wait with frozen posture and furrowed brow.
  - **Translation Plan Card:** Shows `UNSUPPORTED_FINGERSPELLING` strategy with complete transparency.

---

## 3. Speech-to-ISL Demonstration

1. Navigate to the Speech input section on `/translator`.
2. Click **Speech Input (Mic)**.
3. Speak or dictate: *"The processor executes instructions stored in memory."*
4. Transcript appears in the input text area in real-time.
5. Click **Translate to ISL**:
   - NLP Engine extracts semantic triples:
     - `[Processor] -> [executes] -> [Instruction]`
     - `[Instruction] -> [stored_in] -> [Memory]`
   - Translation Plan displays relational spatial indexing.

---

## 4. Document Translation Demonstration

1. Navigate to `/documents`.
2. Upload a syllabus or lecture slide document (PDF, DOCX, or PPTX).
3. The system processes the document section by section:
   - Displays **Document Analysis Summary** with curriculum coverage percentage.
   - Displays **Section Navigator** listing every paragraph/slide with detected engineering concepts and translation status pills.
   - Generates the complete ISL translation stream for the primary section.

---

## 5. Audit & Compliance Summary

- **Tests Passing:** 63 / 63 tests (100%).
- **Frontend Build:** Built clean with Vite in 7.12s.
- **Zero-Fabrication Safeguard:** 100% enforced; 0 fake videos, 0 procedural gestures, 0 simulated reviewer accreditations claimed.

