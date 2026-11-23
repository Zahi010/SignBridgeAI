# SignBridge AI: Live Demonstration Script & Protocol
## Standard Operating Procedure for Institutional & Expert Demonstrations

**Purpose:** Standardized walkthrough script for presenting SignBridge AI to academic faculties, Deaf educators, ISL researchers, and accessibility committees.  
**Demonstration Mode:** Live Web Application ([http://localhost:5173](http://localhost:5173)) & Local Staging Backend ([http://localhost:8000](http://localhost:8000)).  
**Estimated Duration:** 15–20 minutes.  

---

## 1. Demonstration Setup & Principles

### Golden Rules for the Presenter:
1. **Never claim full unassisted translation:** Always introduce the platform as an *academic research platform with a strict Zero-Fabrication safeguard*.
2. **Highlight the status badges:** Emphasize the visual distinction between `VERIFIED` (or `PARTIALLY_VERIFIED`), `EXPLANATION_REQUIRED`, and `UNSUPPORTED`.
3. **Acknowledge the current vocabulary size:** Be completely transparent that 5 baseline signs are currently linked to authentic ISLRTC mocap videos, while 100 engineering concepts are mapped in the candidate lexicon awaiting expert review.

---

## 2. Step-by-Step Demonstration Script

### Scene 1: The Deaf Student's Engineering Dilemma (2 mins)
* **Action:** Open the **Landing Page** (`/`). Show the hero section, the mission statement, and the Zero-Fabrication policy notice banner.
* **Spoken Narrative:**
  > "Welcome. Deaf engineering students in India face a critical hurdle: engineering lectures are delivered in high-speed technical English. Available interpreters rarely have engineering degrees and must fingerspell complex terms. Naive AI tools invent artificial signs or borrow ASL signs that make no sense to Indian Deaf students. SignBridge AI is built on one foundational principle: Never fabricate a sign, and keep Deaf experts in the loop."

### Scene 2: Translating an Authenticated Concept — "Algorithm" (4 mins)
* **Action:** Navigate to the **Translator Page** (`/translator`).
* **Input Text:** Type: `An algorithm is a step-by-step procedure to solve a problem.`
* **Select Domain:** Choose *Computer Science & Engineering* -> *Data Structures & Algorithms*.
* **Click:** `Translate to ISL`.
* **Points to Demonstrate:**
  1. **Live Pipeline Panel:** Show NLP tokenization, dependency parse, and grammatical Topic-Comment plan.
  2. **Concept Card:** Note that *Algorithm* is detected and mapped to concept code `CS-001`.
  3. **Verification Badge:** Show that *Algorithm* displays `PARTIALLY_VERIFIED (Official ISLRTC Corpus)`.
  4. **3D Avatar Playback:** The Three.js avatar executes the authentic ISLRTC motion retargeting.
  5. **Provenance Modal:** Click *View Provenance* to show the official GODL-India attribution to ISLRTC, Department of Empowerment of Persons with Disabilities, Ministry of Social Justice and Empowerment.

### Scene 3: The Zero-Fabrication Safeguard — "Backpropagation" (3 mins)
* **Action:** In the same input box, type: `The neural network is trained using backpropagation.`
* **Click:** `Translate to ISL`.
* **Points to Demonstrate:**
  1. **Detection:** The system detects *backpropagation* as an advanced technical concept.
  2. **Safeguard Enforcement:** Instead of inventing a fake sign, the avatar displays the neutral posture.
  3. **Honest Status:** Status badge displays `UNSUPPORTED / AWAITING EXPERT CODIFICATION`.
  4. **Pedagogical Explanation Card:** Show that the system presents an approved conceptual explanation (gradient descent analogy, error feedback explanation) and offers structured fingerspelling tokens.
  5. **Explain to Audience:**
     > "Notice what did NOT happen. The system did not generate a hallucinated gesture. In academic engineering, a wrong sign causes students to fail exams. SignBridge AI protects linguistic integrity by refusing to fabricate."

### Scene 4: Synchronized Split-Screen Expert Review Portal (5 mins)
* **Action:** Navigate to the **Expert Review Portal** (`/expert-review`).
* **Points to Demonstrate:**
  1. **Reviewer Login & Accreditation:** Show reviewer login modal (`ReviewerAuthModal`). Highlight the credential registration fields (RCI Registration Number, Deaf Association Membership, State Interpreter License).
  2. **Task Queue:** Select task `ISL-CS-001: Algorithm`.
  3. **Split-Screen Synchronized Player:**
     - Left window: Authentic 1080p ISLRTC master recording video.
     - Right window: 3D Three.js WebGL humanoid avatar.
     - Click **Play/Pause**: Both players play in exact lockstep.
     - Scrub Timeline / Frame Skip: Both players scrub synchronously.
     - Speed Control: Set playback to 0.5x to observe finger flexion.
  4. **12-Criteria Linguistic Rubric:**
     - Walk through the rubric: Handshape, Palm Orientation, Signing Location, Movement Dynamics, Facial Non-Manual Markers, Contextual Meaning.
     - Show millisecond-accurate timestamped annotation creation.

### Scene 5: Academic Statistical Dashboard (3 mins)
* **Action:** Navigate to the **Validation Dashboard** (`/dashboard` or `/validation-dashboard`).
* **Points to Demonstrate:**
  1. **Inter-Rater Reliability:** Show the live computation of Fleiss' Kappa and Cohen's Kappa.
  2. **Wilson Score Confidence Intervals:** Highlight that 95% confidence intervals are displayed for acceptance rates.
  3. **Sample Size Disclosure:** Point out the prominent banner: *When sample size N < 30, metrics are labeled PRELIMINARY; when N = 0, no synthetic statistics are generated.*

### Scene 6: Q&A and Institutional Collaboration Invitation (3 mins)
* **Narrative:**
  > "SignBridge AI is now ready for controlled, multi-center institutional pilots. We invite your university or center to partner with us on expert review onboarding, IRB-approved classroom evaluations, and open-source lexicon expansion."

---

## 3. Fallback & Troubleshooting Procedures
* If video fails to stream: Ensure backend is running and `/data` static mount is accessible.
* If avatar WebGL context is lost: Refresh page or toggle hardware acceleration in browser settings.

