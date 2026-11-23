# SIGNBRIDGE AI — COLLEGE BACKUP DEMONSTRATION CHECKLIST

**Document Version:** Phase 8.5 (College Presentation Readiness)  
**Classification:** Operational Contingency & Offline Demonstration Manual  
**Project:** SignBridge AI  
**Date:** 2026-11-23  

---

## 1. Purpose & Risk Management

Academic presentations and project defenses often encounter unexpected classroom disruptions: loss of internet connectivity, projector resolution mismatches, microphone driver issues, or port blocking.

This checklist provides a bulletproof contingency plan to ensure a flawless live demonstration under any technical condition.

---

## 2. Pre-Presentation Preparation (15 Minutes Before Defense)

### 2.1 Hardware & Environment Check
* [ ] Laptop plugged into AC power (do not rely on battery power during 3D WebGL rendering).
* [ ] Display resolution set to 1920x1080 (16:9 ratio) for optimal projector rendering.
* [ ] Close heavy background software (virtual machines, video editors, gaming clients) to reserve memory.
* [ ] Open terminal in `E:\SignBridgeAi`.

### 2.2 Local Server Cold Boot
Open two separate terminal windows or run the background commands:
1. **Terminal 1 (Backend Server):**
   ```powershell
   cd E:\SignBridgeAi
   .\backend\venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
   ```
   *Expected output:* `Uvicorn running on http://127.0.0.1:8000`
2. **Terminal 2 (Frontend Server):**
   ```powershell
   cd E:\SignBridgeAi\frontend
   cmd /c npm run dev
   ```
   *Expected output:* `VITE ready ... Local: http://localhost:5173/`

### 2.3 Browser Tab Pre-loading
Open your browser (Edge or Chrome) and pre-open these 4 tabs:
* **Tab 1 (Primary Demo):** `http://localhost:5173/demo` (Live Demo walkthrough).
* **Tab 2 (Outreach CRM):** `http://localhost:5173/outreach` (Institutional Directory).
* **Tab 3 (Text Translator):** `http://localhost:5173/translate` (Text translation & disambiguation).
* **Tab 4 (Validation Analytics):** `http://localhost:5173/validation-dashboard` (Metrics & Fleiss Kappa).

---

## 3. Zero-Internet Demonstration Mode (Offline Failsafe)

SignBridge AI is **100% self-contained locally**:
* **Database:** Runs on local SQLite (`backend/signbridge.db`).
* **Media Assets:** All 5 authentic ISLRTC videos reside locally in `data/sign_videos/`.
* **Motion Capture:** All 5 mocap landmark JSON files reside locally in `data/isl_motion/processed/`.
* **NLP Models:** Uses local spaCy parser; requires zero external cloud API calls.
* **3D Engine:** Three.js and WebGL libraries are bundled locally in `frontend/node_modules/`.

*If the college Wi-Fi disconnects, the demonstration continues with zero degradation.*

---

## 4. Emergency Contingency Actions

| Potential Issue | Root Cause | Immediate Recovery Action |
| :--- | :--- | :--- |
| **Port 8000 Already in Use** | Previous orphan python process | Run: `netstat -ano \| findstr :8000` then `taskkill /F /PID <PID>` and restart backend. |
| **Port 5173 Already in Use** | Previous vite daemon | Run: `netstat -ano \| findstr :5173` then `taskkill /F /PID <PID>` and restart frontend. |
| **Microphone Recognition Fails** | Browser mic permissions blocked | Do not panic. Explain that the Web Speech API requires HTTPS or mic permissions, then immediately click **Scenario 1** or **Scenario 2** presets on `/translate`. |
| **3D Avatar Appears Black/Blank** | WebGL context lost | Press `Ctrl+F5` to perform a hard refresh, or click **"Reset Demo"** on `/demo`. |
| **Projector Cuts Video Display** | Projector HDMI handshake issue | Disconnect and reconnect HDMI; system state will remain intact on `/demo`. |

---

## 5. Offline Evidence Screenshot Fallback

In the unlikely event of total laptop hardware failure, all demonstration screens have been pre-captured and stored with cryptographic SHA-256 integrity hashes in:  
`docs/college-demo/evidence/`

1. `01_landing_page.png` — Main landing page & Zero-Fabrication badge.
2. `02_demo_step1_presets.png` — 7 concept presets rendered.
3. `03_demo_step2_context.png` — Contextual sense disambiguation card.
4. `04_demo_step3_strategy.png` — Translation decision tree.
5. `05_demo_step4_synchronized_signing.png` — Side-by-side ISLRTC video & 3D avatar viewport.
6. `06_demo_step5_pedagogical_card.png` — Backpropagation pedagogical fallback card.
7. `07_demo_step6_evidence.png` — GODL license & audit evidence card.
8. `08_outreach_crm.png` — 12 verified institutions directory.
9. `09_outreach_modal.png` — ISLRTC detail slide-over modal.
10. `10_expert_review_portal.png` — Expert Review Portal.
11. `11_validation_dashboard.png` — Validation analytics & agreement metrics.
12. `12_community_evaluation.png` — Community research portal.
13. `13_text_translator.png` — Engineering text translator.

*Keep a copy of this folder on a USB flash drive as an ultimate fallback.*
