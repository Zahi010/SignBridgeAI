# SignBridge AI — Known Limitations & Technical Roadmap

**Audit & Document Date:** November 19, 2026  
**Auditor Roles:** Senior Full-Stack Engineer, QA Engineer, AI/ML Engineer, Accessibility Specialist & Technical Auditor  
**Policy Standard:** In adherence to the **Zero Fabricated Signs Policy** and rigorous engineering transparency, this document catalogs the exact operational boundaries, prototype limitations, and planned development milestones.

---

## 1. Prototype Operational State & Feature Boundaries

| System Component | Prototype Operational State | Exact Technical Limitation & Scope |
| :--- | :--- | :--- |
| **Concept Extraction Engine** | **Operational (Rule-Based)** | Employs multi-word regex phrase matching and alias dictionary lookup filtered by branch/subject. Limited to 21 registered technical concepts. Semantic vector similarity is planned for Milestone 2. |
| **ISL Syntactic Restructuring** | **Operational (Rule-Based)** | Applies deterministic grammar transformation rules: Topic-Comment reordering, sentence-final WH-movement with Non-Manual Markers (`[NMM: Furrowed Brow]`), and dual spatial loci assignment. Does not use an end-to-end trained neural sequence-to-sequence model. |
| **Zero-Fabrication Policy Engine** | **Fully Operational** | Categorizes submitted queries into `verified`, `partial`, `explanation_needed`, `needs_review`, or `unsupported`. Transparently reports unverified concepts (e.g. `Deadlock`) rather than synthesizing fake signs. |
| **Sign Language Video Player** | **Operational (Demo Media)** | The custom HTML5 video player, byte-range streaming, replay, timeline scrubber, and variable playback speed (0.5x–1.25x) are fully operational. However, the media files (`data/sign_videos/*.mp4`) are **synthetic FFmpeg test pattern clips (`testsrc`)** used to validate streaming architecture. They do not contain human Deaf signers. |
| **3D Avatar Viewer** | **Operational (Preview Only)** | Renders an articulated procedural humanoid mesh in WebGL via Three.js / React Three Fiber with interactive OrbitControls and camera presets. The avatar executes a subtle idle breathing loop. It **does NOT synthesize sign language gestures**, and the asset `neutral_avatar.glb` does not exist on disk. |
| **Document Translator** | **Fully Operational** | PyMuPDF (PDF), python-docx (DOCX), and python-pptx (PPTX) extract text and analyze domain concepts. Includes 15MB file-size limits, format validation, and sanitized filenames to prevent path traversal (CWE-22). |
| **Live Lecture Interface** | **Simulated Demo Only** | The live lecture view is an interactive client-side prototype demonstration. It does not capture microphone audio or run `faster-whisper`. It displays an animated SVG waveform (`Math.random()`) and steps through pre-scripted demo sentences every 6 seconds. |
| **Dataset Provenance & Reviewers** | **Demo Seed Data** | While the Indian Sign Language Research and Training Centre (ISLRTC) is an authentic statutory body, the specific pilot URLs, "DTEI Peer Registry", and reviewer personas ("Prof. Rajesh Sharma", "Ananya Menon, M.Tech") are **synthetic demo seed records** authored in `backend/app/database/seed.py`. |
| **Student Dashboard & Explorer** | **Fully Operational** | Connected to live FastAPI endpoints; displays genuine SQLite database counts with live search and branch/status filtering. |
| **Translation Audit History** | **Fully Operational** | Real-time SQLite persistence; logs every translation request with timestamp, concept counts, and validation status. |

---

## 2. Linguistic & Lexical Limitations

1. **Initial Vocabulary Coverage (21 Concepts):**
   The initial prototype seeds 21 foundational technical concepts across Computer Science, Electronics, Mechanical, Civil, and Electrical engineering. Concepts outside this registry are reported as `unsupported`.
2. **ISL Regional Dialects:**
   The vocabulary reflects standard pan-Indian ISL conventions accredited by the Indian Sign Language Research and Training Centre (ISLRTC). Regional dialectal variations (e.g. Kerala, Maharashtra, Tamil Nadu) are flagged for future milestone harmonization.
3. **Complex Sentence Concurrency:**
   While simple to moderately complex engineering queries are handled (e.g. *"What is a database?"*, *"Explain the difference between voltage and current"*), highly nested compound sentences with subordinate clauses require human deaf interpreter supervision.

---

## 3. Multimedia & 3D Avatar Roadmap

- **Milestone 1 (Current Prototype):**
  - Custom React video player with byte-range streaming and speed controls.
  - Three.js WebGL procedural avatar with OrbitControls, zoom, and camera angle presets.
  - Transparent Zero-Fabrication fallback messaging.
- **Milestone 2 (Q2 2027):**
  - Studio video recording of certified Deaf master signers for foundational STEM concepts.
  - 3D skeletal avatar rigged with 54 MediaPipe-Holistic motion-capture keypoints.
  - Ingestion of `.glb` animations for verified vocabulary terms.

---

## 4. Multilingual & Speech Recognition Roadmap

- **Milestone 1 (Current Prototype):** English technical text and document inputs. Simulated live lecture demonstration.
- **Milestone 2 (Q3 2027):** Malayalam technical terminology integration for polytechnics in Kerala.
- **Milestone 3 (Q4 2027):** Hindi technical terminology harmonization in collaboration with national deaf institutes.
- **Milestone 4 (2028):** Real-time server-side `faster-whisper` speech transcription with on-device microphone streaming via WebSockets on GPU-accelerated infrastructure.

---

*Document certified by Technical Auditor on November 19, 2026.*
