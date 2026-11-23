# SignBridge AI — Phase 8.3: Research Presentation Outline

**Structure:** 12-Slide Academic Presentation  
**Target Duration:** 15–20 minutes with interactive live demonstration  
**Audience:** Faculty, Academic Supervisors, Accessibility Committees, Deaf Community Leaders  

---

### Slide 1: Title & Vision
- **Header:** SignBridge AI: Accessible STEM Higher Education in Indian Sign Language
- **Sub-header:** A Linguistically Governed NLP Translation, 3D Kinematic Retargeting, and Community Validation Platform
- **Presenter Info:** SignBridge AI Research Working Group
- **Key Visual:** Split image showing Deaf engineering student in a lecture hall alongside the 3D WebGL avatar.

### Slide 2: The STEM Accessibility Crisis in Higher Education
- **Key Statistics:** 1.8M+ Deaf individuals in India; < 1% enrollment in B.Tech/B.E. programs.
- **The Core Problem:** Technical lectures delivered in dense spoken English; lip-reading captures only ~30% of phonemes; high interpreter fatigue from continuous fingerspelling.
- **The Gap:** Lack of standardized, codified technical ISL vocabulary in Indian universities.

### Slide 3: Why Naive Machine Learning Models Fail for ISL
- **The Pitfalls of Off-the-Shelf AI:**
  1. *ASL/BSL Transference:* Imposing Western sign languages onto Indian students.
  2. *Naive Direct Concatenation:* Word-for-word SVO string substitution destroying ISL syntax.
  3. *The Hallucination Crisis:* Generative models inventing artificial, anatomically plausible but linguistically meaningless hand gestures.

### Slide 4: SignBridge AI Architecture: The Modular Monolith
- **System Diagram:** Multi-stage flow from input text/PDF/speech to NLP intermediate representation, Zero-Fabrication gate, mocap retargeting, and WebGL avatar.
- **Core Principle:** Strict separation between technical motion fidelity and linguistic validity.

### Slide 5: Domain-Aware Technical NLP & ISL Grammar Planning
- **Lexical Recognizer:** 100 candidate engineering terms across Computer Science, Electronics, Electrical, Civil, and Mechanical engineering.
- **Contextual Disambiguation:** Resolving polysemy (e.g., *current* in circuits vs. *current* in time).
- **Grammatical Transformer:** Converting linear English to ISL Topic-Comment order, Time-First aspect, and end-of-sentence interrogatives/negation.

### Slide 6: Authentic Motion Capture & 3D WebGL Avatar Engine
- **MediaPipe Holistic Kinematics:** Extracting 33 pose landmarks, 42 hand joints (21 per hand), and 468 facial mesh points from 1080p broadcast signing.
- **Skeletal Retargeting:** Normalizing against anthropometric shoulder width; Euler rotation clamping; cubic Hermite spline smoothing at 60 FPS in Three.js.

### Slide 7: The Zero-Fabrication Safeguard & Pedagogical Decomposition
- **Architectural Policy:** When a concept is not codified or authenticated, the avatar **refuses to fabricate**.
- **Pedagogical Alternative:** Presenting structured conceptual analogies, root sign combinations, and fingerspelling tokens.
- **Status Badges:** Clear visual labeling (`PARTIALLY_VERIFIED` vs `UNSUPPORTED`).

### Slide 8: The Five Candidate Pilot Signs (Initial Benchmark)
- **Table:** Algorithm (`ISL-CS-001`), Frequency (`ISL-ECE-013`), Current (`ISL-EEE-025`), Beam (`ISL-CIV-037`), Torque (`ISL-MEC-049`).
- **Data Provenance:** Official ISLRTC master recordings licensed under GODL-India with SHA-256 integrity verification.
- **Honest Baseline:** High tracking confidence (0.942–0.971) confirmed, but explicitly designated **UNREVIEWED** pending external pilot review.

### Slide 9: Live Product Demonstration (5-Minute Interactive Session)
- **Demonstration SOP (`/demo`):**
  1. Enter authenticated term (*Algorithm*) $\rightarrow$ See NLP parse, verified badge, and 3D avatar execution.
  2. Enter uncodified term (*Backpropagation*) $\rightarrow$ See Zero-Fabrication refusal and pedagogical breakdown.
  3. Open Synchronized Expert Portal $\rightarrow$ Show split-screen video/avatar player and millisecond annotation timeline.

### Slide 10: Independent Linguistic Review & Adjudication Infrastructure
- **12-Factor Phonological Rubric:** Handshape, orientation, location, movement dynamics, coordination, non-manual markers, regional variation, and technical ambiguity.
- **Statistical Reliability:** Live calculation of exact Fleiss' Kappa ($\kappa$), Cohen's Kappa, and 95% Wilson Score Confidence Intervals.
- **Disagreement Adjudication:** Automated ticket escalation when independent raters conflict.

### Slide 11: Proposed Institutional Collaboration Framework
- **Three-Tier Partnership:**
  - *Tier 1: Academic & Linguistic Review:* Faculty and interpreters evaluate the 5 baseline signs.
  - *Tier 2: Classroom Usability Pilot:* Controlled, IRB-approved evaluation with 15–30 DHH engineering students.
  - *Tier 3: Joint Publication & Lexicon Expansion:* Co-authored research papers in peer-reviewed accessibility conferences.
- **Guarantees:** 100% open-source, student honoraria funded, on-premise privacy deployment.

### Slide 12: Next Steps & Discussion
- **Immediate Milestones:** Collaborative protocol submission to Institutional Ethics Committees (IEC).
- **Contact:** Research Working Group directory and GitHub repository link.
- **Open Q&A:** Transition to discussion.
