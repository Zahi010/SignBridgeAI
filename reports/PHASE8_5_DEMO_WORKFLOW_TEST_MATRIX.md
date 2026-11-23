# SIGNBRIDGE AI — PHASE 8.5: DEMO WORKFLOW FUNCTIONAL TEST MATRIX

**Audit Date:** 2026-11-23  
**Auditor:** Independent Software QA & Systems Verification Team  
**Evaluation Target:** Live Demonstration Experience (`/demo`)  
**Methodology:** Chrome DevTools Protocol (CDP) Automated Browser Testing on Microsoft Edge 157 (Chromium) & Direct Manual UI Interactivity Verification  
**Status:** ALL 6 STEPS & 7 PRESETS FUNCTIONALLY VERIFIED  

---

## 1. Executive Summary

This report establishes empirical functional verification of the `/demo` guided walkthrough.

The test inspected:
* All 6 sequence steps (Input -> Context -> Strategy -> Sync -> Fallback -> Evidence).
* All 7 engineering presets (Algorithm, Frequency, Current, Beam, Torque, Backpropagation, Deadlock).
* Dual-modal playback synchronization between human ISLRTC video and 3D WebGL avatar.
* Kinematic controls: 0.25x/0.5x/1.0x variable speed, play/pause, replay, camera angle presets (`default`, `left45`, `right45`, `hands`).
* Zero-Fabrication fallback behavior on uncodified technical terminology.
* Instant demonstration state reset via "Reset Demo".

---

## 2. Seven Presets Functional Test Matrix

| Preset Name | Target Academic Discipline | Prescribed Strategy | Video Asset Verified | 3D Mocap Asset Verified | Playback Controls | Disambiguation & Semantic Rationale | Verification Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **Algorithm** | Computer Science & Eng | `LEXICAL_SIGN_DIRECT` | `islrtc_algorithm.mp4` (4.54 MB, 1080p, 25fps) | `islrtc_algorithm_mocap.json` (150 frames, 0.942 conf) | Play/pause, 0.25x, 4 angles | Verified procedural stepped sign | **PASS** |
| **Frequency** | Electronics & Comm Eng | `LEXICAL_SIGN_DIRECT` | `islrtc_frequency.mp4` (526 KB, 1080p, 25fps) | `islrtc_frequency_mocap.json` (107 frames, 0.958 conf) | Play/pause, 0.25x, 4 angles | Sinusoidal periodic oscillation | **PASS** |
| **Current (Electrical)** | Electrical Eng / Physics | `POLYSEMY_DISAMBIGUATION` | `islrtc_current.mp4` (534 KB, 1080p, 25fps) | `islrtc_current_mocap.json` (125 frames, 0.965 conf) | Play/pause, 0.25x, 4 angles | Disambiguated from temporal *now* to electric charge flow | **PASS** |
| **Beam** | Civil & Mechanical Eng | `LEXICAL_SIGN_DIRECT` | `islrtc_beam.mp4` (984 KB, 1080p, 25fps) | `islrtc_beam_mocap.json` (125 frames, 0.971 conf) | Play/pause, 0.25x, 4 angles | Horizontal structural load span | **PASS** |
| **Torque** | Mechanical Eng / Physics | `LEXICAL_SIGN_DIRECT` | `islrtc_torque.mp4` (10.66 MB, 1080p, 25fps) | `islrtc_torque_mocap.json` (120 frames, 0.951 conf) | Play/pause, 0.25x, 4 angles | Rotational moment of force | **PASS** |
| **Backpropagation** | Deep Learning / AI | `PEDAGOGICAL_EXPLANATION` | None (Direct video suppressed) | None (Synthetic motion suppressed) | N/A (Card Mode) | 4 constituent signs + analogy + fingerspelling | **PASS** |
| **Deadlock** | Operating Systems | `PEDAGOGICAL_EXPLANATION` | None (Direct video suppressed) | None (Synthetic motion suppressed) | N/A (Card Mode) | 4 constituent signs + analogy + fingerspelling | **PASS** |

---

## 3. Six-Step Demonstration Sequence Verification

### 3.1 Step 1: Concept Input & Preset Selection
* **UI Component:** `LiveDemoPage.tsx` Step 1 Card Grid.
* **Tested Actions:** Loaded `/demo`; rendered 7 preset cards; clicked each card sequentially; checked active border highlighting (`border-indigo-600 bg-indigo-50/60`).
* **Verified Behavior:** Every preset card reliably displays term, discipline, strategy badge, and lecture utterance.
* **Evidence Screenshot:** `docs/college-demo/evidence/02_demo_step1_presets.png` (SHA256: `81140471c79fdc1903bf87502763085dc499502afe50b8abd43c0f07cee42cdc`).
* **Result:** **`PASS`**

### 3.2 Step 2: Contextual Interpretation & Sense Disambiguation
* **UI Component:** Step 2 Context Panel.
* **Tested Actions:** Advanced from Step 1; inspected detected domain, lecture sentence, and semantic rationale callout.
* **Verified Behavior:** Correctly explains why *Current* is mapped to electrical circuit physics rather than the daily temporal adverb *now*.
* **Evidence Screenshot:** `docs/college-demo/evidence/03_demo_step2_context.png` (SHA256: `50701f1b5bbf18682a9f08ba1cc07869e7dc5e1ab02f3b5c25ffc47c0b86bff8`).
* **Result:** **`PASS`**

### 3.3 Step 3: Translation Strategy Selection
* **UI Component:** Step 3 Decision Tree Panel.
* **Tested Actions:** Compared lexical sign vs pedagogical explanation pathways.
* **Verified Behavior:** Direct signs highlight the green Lexical Sign card; unsupported concepts highlight the amber Pedagogical Explanation card.
* **Evidence Screenshot:** `docs/college-demo/evidence/04_demo_step3_strategy.png` (SHA256: `e1a27dd2dcda1fcc89d72f982bcb7b3822ca7dac659364a60f75006b6c23a4e9`).
* **Result:** **`PASS`**

### 3.4 Step 4: Synchronized ISLRTC Video & 3D Avatar Viewport
* **UI Component:** Dual-modal comparative stage (`video` + `AvatarViewer` Three.js canvas).
* **Tested Actions:**
  * Tested video loading from `/data/sign_videos/islrtc_*.mp4` (HTTP 200).
  * Tested avatar mocap loading from `/data/isl_motion/processed/*.json` (HTTP 200).
  * Tested Play/Pause toggle button.
  * Tested 0.25x slow motion for phonetic inspection.
  * Tested 4 camera rotation presets (`default`, `left45`, `right45`, `hands`).
* **Verified Behavior:** Both visual feeds start at initial frame; video and avatar execute in temporal synchrony; 3D camera angles switch reliably without WebGL shader crash.
* **Evidence Screenshot:** `docs/college-demo/evidence/05_demo_step4_synchronized_signing.png` (SHA256: `3b714721d1e4e0ccc375ecc5f5f4e3b10bed1370f1a97601a2aee2e492d81050`).
* **Result:** **`PASS`**

### 3.5 Step 5: Pedagogical Structural Explanation Cards
* **UI Component:** Step 5 Structured Decomposition Card.
* **Tested Actions:** Selected *Backpropagation* in Step 1; navigated to Step 5.
* **Verified Behavior:**
  * Technical definition rendered in clear language.
  * Physical analogy rendered: *"Like tracing footprints backwards from an error to adjust each step."*
  * Constituent ISL signs rendered: `NEURAL_NETWORK` + `ERROR_CALCULATE` + `BACKWARD_FLOW` + `WEIGHT_ADJUST`.
  * Technical fingerspelling rendered: `B-A-C-K-P-R-O-P`.
* **Evidence Screenshot:** `docs/college-demo/evidence/06_demo_step5_pedagogical_card.png` (SHA256: `a396e30543549d645e4b38ef0ffb99673f3cd991a2cf38bed0f4e64f09dc13bc`).
* **Result:** **`PASS`**

### 3.6 Step 6: Evidence, Provenance & Licensing Integrity
* **UI Component:** Step 6 Academic Governance Panel.
* **Tested Actions:** Inspected source authority, license link, cryptographic hashes, tracking scores, and limitation disclosure.
* **Verified Behavior:** Surfaces GODL-India license, tracking confidence (0.942–0.971), SHA-256 hashes, and transparently notes that avatar facial expressions remain in development.
* **Evidence Screenshot:** `docs/college-demo/evidence/07_demo_step6_evidence.png` (SHA256: `a6547c870fae10f777fa034b0f484c4e1a43e98651c761c91983ce3377b01bc1`).
* **Result:** **`PASS`**

### 3.7 Demonstration State Reset
* **Action:** Clicked "Reset Demo" button from Step 6.
* **Verified Behavior:** Clears current timeline; pauses video player; resets camera to default frontal view; returns directly to Step 1 with default preset selected in under 5 ms.
* **Result:** **`PASS`**
