# SignBridge AI — Indian Sign Language Translation for Engineering

> **Accessible STEM Higher Education for Deaf and Hard-of-Hearing Students**

SignBridge AI is an AI-powered Indian Sign Language (ISL) educational translation platform designed primarily for deaf and hard-of-hearing engineering undergraduates.

The platform bridges tertiary engineering classrooms by translating:
- **Typed Technical English** into ISL syntactic structures and accredited sign references.
- **Spoken Classroom Lectures** via real-time speech capture and sentence segmentation pipelines.
- **Curriculum Documents & Slide Decks** (.PDF, .DOCX, .PPTX) directly into concept breakdowns.
- **Dual Visual Streams**: Accredited human signing videos alongside interactive 3D WebGL avatars.

---

## 🛡️ The Zero Fabricated Signs Policy

ISL is an autonomous, natural human language with independent grammatical morphology, spatial classifier predicates, and non-manual facial markers.

**SignBridge AI enforces a strict Zero Fabricated Signs Charter:**
1. **No Synthetic Signs:** We never invent artificial signs, synthetic gestures, or naive word-by-word word-order permutations.
2. **5-Tier Validation Tracking:**
   - `verified`: Certified, peer-reviewed ISL sign recorded by deaf master signers.
   - `partial`: Compound signs with validated core elements.
   - `explanation_needed`: Technical concept requiring pedagogical elaboration.
   - `needs_review`: Concepts currently in deaf educator cohort evaluation.
   - `unsupported`: Concepts (e.g. *Deadlock* in OS) lacking standardized single-sign ISL representations. We transparently recommend fingerspelling and visual diagrams rather than hallucinating false gestures.

---

## 🏗️ Architecture & Technology Stack

SignBridge AI is built as a **Modular Monolith**:

| Tier | Technologies |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Vite, Tailwind CSS, Lucide React, Axios, React Router v6 |
| **3D Engine** | Three.js, React Three Fiber (`@react-three/fiber`), Drei (`@react-three/drei`) |
| **Backend API** | Python 3.11/3.13, FastAPI, Pydantic v2, SQLAlchemy, SQLite, Alembic |
| **Document AI** | PyMuPDF (`fitz`), `python-docx`, `python-pptx` |
| **Speech Pipeline**| Web Audio API capture, audio waveform visualizer, `faster-whisper` integration ready |

---

## ⚡ Quick Start on Windows

### Prerequisites
- Python 3.11+ (Python 3.13 tested)
- Node.js 18+ (Node v24 tested)
- Windows PowerShell

### 1-Click Launch
Run the launcher from PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1
```
This initializes the SQLite database, seeds all technical engineering concepts, and launches both:
- **Frontend UI:** [http://localhost:5173](http://localhost:5173)
- **Backend API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Manual Start Commands

**Backend:**
```powershell
python -m venv backend\venv
backend\venv\Scripts\pip.exe install -r backend\requirements.txt
backend\venv\Scripts\python.exe -m backend.app.database.seed
backend\venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000
```

**Frontend:**
```powershell
npm.cmd install --prefix frontend
npm.cmd run dev --prefix frontend
```

---

## 🔬 Demonstration Guide (For Tomorrow's Review)

SignBridge AI includes pre-loaded demonstration examples in the **Text Translator** (`/translate`):
1. `"What is a database?"` → **Verified**: Loads authentic ISL human video demonstration & 3D avatar.
2. `"Explain how an operating system works."` → **Explanation Needed**: Highlights pedagogical expansion.
3. `"Explain computer networks."` → **Verified**: Shows spatial loci and classifier predicates.
4. `"What is a deadlock in operating systems?"` → **Unsupported**: Proves the Zero Fabricated Signs Policy in action!
5. `"Explain voltage and current."` → **Verified (ECE)**: Displays physics STEM signs.
6. `"What is a microprocessor?"` → **Needs Review (ECE)**: Demonstrates active peer-review workflow.

---

## 📚 Documentation Index

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Local Setup Guide](docs/SETUP_GUIDE.md)
- [Prototype Runbook](docs/PROTOTYPE_RUNBOOK.md)
- [Known Limitations & Roadmap](docs/KNOWN_LIMITATIONS.md)
- [Test Report](docs/TEST_REPORT.md)

---

## 📜 License & Provenance
SignBridge AI is developed for academic, educational, and research accessibility under open collaborative licensing. Dataset provenance citations are attributed to the Indian Sign Language Research and Training Centre (ISLRTC) STEM Reference Pilot and Deaf Technical Education Initiative (DTEI).

