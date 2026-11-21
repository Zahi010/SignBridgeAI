# SignBridge AI — Prototype Demonstration Runbook

This runbook provides a step-by-step presentation script and demonstration workflow for presenting SignBridge AI to stakeholders, academic review committees, or evaluators.

---

## 🎯 1. Demonstration Preparation Checklist

Before the presentation:
1. Ensure the backend and frontend are running:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1
   ```
2. Open the browser to [http://localhost:5173](http://localhost:5173).
3. Confirm that the top navigation status shows a green dot (`API Online`).

---

## ⏱️ 2. Presentation Flow (10-Minute Script)

### Segment 1: The Problem & Vision (1 Minute)
- **Navigate to:** Landing Page (`/`)
- **Talking Points:**
  - Deaf and hard-of-hearing students enrolled in engineering programs face extreme barriers: technical terms like *operating system*, *microprocessor*, or *concurrency deadlock* lack standardized sign glossaries.
  - Generic sign language apps either invent artificial signs or produce garbled word-for-word English translations that confuse students.
  - **SignBridge AI's Mission:** Provide authentic STEM education translation anchored in genuine Indian Sign Language (ISL) linguistics.

---

### Segment 2: Text-to-ISL Translation & The Zero Fabrication Policy (4 Minutes)
- **Navigate to:** Text Translator (`/translate`)
- **Talking Points & Actions:**

#### Demo Case A: Accredited Verified Sign
1. Click the preset button: **`"What is a database?"`**
2. Click **Translate to ISL**.
3. **Point out:**
   - **Status Banner:** Shows `Verified ISL` in emerald green.
   - **ISL Gloss Restructuring:** `[TOPIC: DATABASE] -> [WHAT [NMM: Furrowed Brow]]`. Explain how ISL moves the question word to the end with eyebrow furrowing.
   - **Human Video Stream:** Play the authentic video demonstration. Point out source attribution (*ISLRTC STEM Reference Pilot, CC-BY-NC*) and accredited reviewer (*Prof. Rajesh Sharma, Lead Deaf Master Interpreter*).
   - **3D Avatar Viewer:** Rotate the avatar with the mouse. Demonstrate the camera angle presets (*Hands Focus*, *Face / NMM*) and playback controls.

#### Demo Case B: The Zero Fabricated Signs Policy in Action
1. Click the preset button: **`"What is a deadlock in operating systems?"`**
2. Click **Translate to ISL**.
3. **Point out:**
   - **Status Banner:** Shows `Unsupported (Zero Fabrication)` in rose red.
   - **Highlight the Ethics:** Unlike generic AI, SignBridge AI **refuses to hallucinate a false sign**. 
   - The system transparently informs the student that no national standardized single sign exists for *Deadlock*, and recommends fingerspelling (`D-E-A-D-L-O-C-K`) alongside an interactive structural visual diagram.

#### Demo Case C: Pedagogical Explanation Needed
1. Click the preset button: **`"Explain how an operating system works."`**
2. **Point out:**
   - Shows `Pedagogical Explanation Needed`. 
   - A base sign for OS exists, but deeper kernel scheduling concepts require contextual visual explanation.

#### Demo Case D: Multiple Concepts & Spatial Indexing
1. Click the preset button: **`"Explain computer networks."`** or **`"Explain voltage and current."`**
2. **Point out:**
   - Demonstrates dual spatial loci assignment: entity A is established on the left, entity B on the right, and directional verbs animate interaction.

---

### Segment 3: Document & Slide Translation (2 Minutes)
- **Navigate to:** Document Translator (`/documents`)
- **Actions:**
  - Drag and drop or browse for an engineering lecture slide deck (.pptx) or PDF notes (.pdf).
  - Click **Parse & Translate Document**.
  - Show the extracted text preview, word count, slide count, and detected engineering concepts.
  - Highlight that students can upload an entire professor's presentation and immediately see which concepts have verified ISL signs.

---

### Segment 4: Live Classroom Lecture Pipeline (2 Minutes)
- **Navigate to:** Live Lecture (`/live-lecture`)
- **Actions:**
  - Click the **Microphone** button to activate streaming mode.
  - Notice the real-time audio waveform visualizer.
  - Click **Simulate Next Spoken Sentence** to progress through a live lecture on Operating Systems.
  - Show the live sentence transcript buffer and real-time ISL gloss generation.
  - Point out the honest disclaimer: the pipeline architecture is prepared for `faster-whisper` deployment.

---

### Segment 5: ISL Technical Vocabulary Explorer & Audit History (1 Minute)
- **Navigate to:** Vocabulary Explorer (`/vocabulary`)
  - Show the searchable ontology across Computer Science, Electronics, Mechanical, Civil, and Electrical engineering.
  - Filter by branch or status. Click a card to view its full linguistic handshape analysis and master reviewer rating.
- **Navigate to:** Translation History (`/history`)
  - Show that every translation performed during the session is logged with full metrics and verification audit trails.

---

## 🏆 Summary Checklist for Tomorrow
- [x] Zero login barriers — demonstration runs immediately out of the box.
- [x] Preset buttons allow 1-click execution without typing errors.
- [x] Honest status reporting with no fake accuracy percentages.
- [x] Interactive 3D WebGL avatar with camera rotation and zoom.
- [x] Video player with playback speed and source attribution.

