# SignBridge AI — Live Prototype Demonstration Script

This document provides the official presentation walkthrough for the **Live Prototype Demonstration Mode** in SignBridge AI. 

Use this script during live thesis defenses, technical evaluations, academic reviews, or stakeholder presentations.

---

## 🎯 1. Demonstration Setup & Pre-Flight

1. Open PowerShell and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\start_all.ps1
   ```
2. Open your web browser to: **[http://localhost:5173](http://localhost:5173)**
3. Navigate to **Text Translator** in the sidebar or top bar (`/translate`).
4. Ensure the **Live Presentation Mode** toggle in the top-right is **ON** (default).

---

## 📋 2. Three Demonstration Scenarios Overview

| Scenario | Query | Engineering Branch | Validation Verdict | Primary Educational Principle |
| :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | `"What is a database?"` | Computer Science | **`VERIFIED`** | Full accredited ISL video, Topic-Comment syntax, WH-movement. |
| **Scenario 2** | `"Explain how an operating system works with memory."` | Computer Science | **`PARTIAL`** | Multi-concept extraction; memory is verified while OS kernel mechanics need pedagogical explanation. |
| **Scenario 3** | `"What is a deadlock in operating systems?"` | Computer Science | **`UNSUPPORTED`** | **Zero-Fabrication Policy:** Transparent refusal to synthesize an unaccredited gesture. |

---

## 🎬 3. Detailed Step-by-Step Presentation Script

---

### SCENARIO 1: Supported Concept (Database)
**Objective:** Prove end-to-end operational capability with authentic ISL human video and 3D WebGL avatar.

#### Action:
- In the **Dedicated Live Prototype Demonstration Mode** banner, click the card:  
  **`Scenario 1: Fully Supported Concept ("What is a database?")`**
- *(Alternatively, type `"What is a database?"` into the text box and click "Translate to ISL".)*

#### What Happens on Screen:
1. The backend FastAPI service responds in **< 15 ms**.
2. The **Status Banner** illuminates in **Emerald Green**: `Verified ISL`.
3. The **Live Translation Pipeline Execution Trace** populates with 5 verified stages.
4. The **Multimodal Visual Stream** displays both the accredited video and the 3D avatar.

#### What to Explain to the Audience:
- **Point to the Status Banner:**
  > *"Notice the Emerald badge: 'Verified ISL'. This indicates that every concept identified in this sentence has an authenticated sign registered in the knowledge base."*
- **Point to Stage 1 (Input Preprocessing & Tokenization):**
  > *"In Stage 1, the backend tokenizes the sentence and isolates grammatical interrogatives. Here, it isolated the WH-word 'what'."*
- **Point to Stage 2 (Technical Concept Extraction):**
  > *"In Stage 2, the engine scanned our 21 registered technical concepts and matched 'Database' under Data Management, while ignoring auxiliary English syntax."*
- **Point to Stage 3 (ISL Syntactic Restructuring):**
  > *"In Stage 3, look at the generated gloss: `[TOPIC: DATABASE] -> [WHAT [NMM: Furrowed Brow]]`. Explain to the examiners: unlike English SVO, natural ISL places the topic first in 3D signing space, and moves WH-questions to the very end with a furrowed brow non-manual marker."*
- **Point to Stage 4 (Zero-Fabrication Policy Audit):**
  > *"Stage 4 verifies provenance citations. In our production architecture, signs link to institutional registries such as ISLRTC. In this prototype, our database seeds these provenance records to validate data schema integrity."*
- **Interact with the Media Stream:**
  - Click **Play** on the Human Video Player. Change playback speed to `0.75x`.
  - Explain to the evaluators:
    > *"In this demonstration prototype, the player streams benchmark MP4 test assets to validate custom controls, byte-range streaming, variable speed, and attribution cards. Certified studio recordings of human Deaf signers will be ingested in Milestone 2."*
  - Click and drag the **3D Avatar Viewer** to rotate the signer. Click **"Hands Focus"** to zoom in on the signing workspace.
  - Explain:
    > *"The 3D avatar is an interactive WebGL anatomical viewer powered by Three.js and React Three Fiber. It provides an anatomical space with camera presets, built to receive skeletal motion-capture rigs."*

---

### SCENARIO 2: Partially Supported Sentence (OS & Memory)
**Objective:** Demonstrate multi-concept concurrent extraction and transparent handling of compound terms.

#### Action:
- Click the card:  
  **`Scenario 2: Partially Supported Sentence ("Explain how an operating system works with memory.")`**

#### What Happens on Screen:
1. The backend extracts two distinct concepts: **Operating System** and **Memory**.
2. The status returns as **`Partial Sign`** / **`Pedagogical Explanation Needed`**.
3. Spatial Indexing notes appear in the ISL grammar view.

#### What to Explain to the Audience:
- **Point to Stage 2 (Concept Extraction):**
  > *"Notice that the engine successfully extracted two separate engineering entities: 'Operating System' (Systems Software) and 'Memory' (Hardware Architecture)."*
- **Point to the Linguistic Note on Operating System:**
  > *"While 'Memory' has a certified sign, 'Operating System' is flagged as 'Pedagogical Explanation Needed'. The base sign compound (COMPUTER + SYSTEM-MANAGE) exists, but specialized kernel mechanics require expanded visual diagrams. SignBridge does not overstate its confidence."*
- **Point to Dual Spatial Loci (Stage 3):**
  > *"Because two concepts interact, ISL syntax applies Spatial Indexing: assigning Operating System to Spatial Locus A on the left, and Memory to Locus B on the right, connecting them with directional predicates."*

---

### SCENARIO 3: Unsupported Technical Concept (Deadlock)
**Objective:** The defining moment of the presentation — prove the **Zero Fabricated Signs Policy**.

#### Action:
- Click the card:  
  **`Scenario 3: Unsupported Technical Concept ("What is a deadlock in operating systems?")`**

#### What Happens on Screen:
1. The backend detects **Deadlock** and **Operating System**.
2. The status banner turns **Rose Red**: **`Unsupported (Zero Fabrication)`**.
3. The video player displays an honest empty state: *"No Verified Sign Video — Awaiting Deaf Peer Validation Corpus"*.

#### What to Explain to the Audience (Key Presentation Moment):
- **Deliver this core statement:**
  > *"Here is where SignBridge AI fundamentally differs from generic translation tools. Many commercial apps would invent a synthetic hand movement or naively re-arrange words into Subject-Object-Verb, which produces incomprehensible gibberish for deaf engineers."*
- **Point to Stage 4 (Policy Audit):**
  > *"Our Zero-Fabrication Policy actively blocks synthetic generation. It transparently reports: 'No national standardized single sign currently certified for DEADLOCK in ISL. Certified deaf educators recommend fingerspelling (D-E-A-D-L-O-C-K) followed by an interactive visual resource diagram.'"*
- **Point to the Video Player:**
  > *"Instead of showing fake or irrelevant stock video footage, the player shows an honest empty state stating that peer review is pending. This preserves academic integrity and respect for deaf culture."*

---

### 4. Demonstrating the Pipeline Stepper Controls
- At the top of the **Live Pipeline Execution Trace** panel, click **`Step-by-Step`**.
- Click **`Stage 1/5`**, then click **`Stage 2/5`**, **`Stage 3/5`**, etc.
- Explain to the evaluators:
  > *"For presentation clarity, our live interface allows examiners to step through each phase of the backend pipeline individually or view the entire trace simultaneously."*

---

### 5. Demonstrating Real-Time Audit History
- Scroll to the bottom of the page to **Live Translation Session History**.
- Point out that all three demonstration queries you just submitted appear chronologically with exact timestamps, status verdicts, and verified concept counts.
- Explain:
  > *"Every transaction is persisted directly to SQLite and synced in real time without page refreshes."*

---

### 6. Demonstrating the Reset Action
- Click the **`Reset Demonstration`** button in the top demo header.
- The input clears, the active result resets, and the system returns to a clean baseline ready for audience questions or custom sentences.

---

## ❓ 7. Examiner & Evaluator Q&A Guide

**Q1: Did you train an AI model from scratch?**  
*Answer:* "No. In accordance with project architecture guidelines, training an ungrounded neural network for sign generation often leads to linguistic hallucination. Instead, we built a modular translation and knowledge-retrieval pipeline with an authentic linguistic grammar engine and an accredited provenance registry."

**Q2: How does the 3D avatar handle unverified signs?**  
*Answer:* "The 3D avatar operates in neutral anatomical posture mode with interactive WebGL camera controls. Procedural animations are only connected when accredited motion-capture datasets are certified by deaf educators."

**Q3: Can it support additional engineering branches?**  
*Answer:* "Yes. The database schema is fully relational and currently holds curriculum terms for Computer Science, Electronics, Mechanical, Civil, and Electrical Engineering. Expanding to Chemical or Aerospace engineering simply requires seeding domain concepts."

