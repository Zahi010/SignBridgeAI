# SignBridge AI — Indian Sign Language (ISL) Dataset & Linguistic Resource Research

**Document Version:** 1.0.0  
**Research Date:** November 19, 2026  
**Lead Researchers:** Lead AI Engineer & ISL Linguistics Specialist  
**Standard Adherence:** Zero Fabricated Signs Policy, Ethical Signer Consent, Indian DPDP Act 2023, and Fair Dealing Provisions.

---

## 1. Executive Research Summary

SignBridge AI requires verified, culturally authenticated, and legally compliant Indian Sign Language (ISL) linguistic datasets to serve Deaf engineering students. To adhere strictly to our **Non-Negotiable Zero-Fabrication Policy**, this investigation evaluates legitimate academic, government, and open-source ISL resources.

We investigated:
1. **Indian Sign Language Research and Training Centre (ISLRTC)** — Statutory Government Authority.
2. **ISLTranslate** — Continuous ISL Machine Translation Dataset (ACL Findings 2023, IIT Kanpur / IIT Hyderabad).
3. **iSign Benchmark** — Large-Scale Continuous Multimodal ISL Benchmark (Exploration Lab, Hugging Face).
4. **SignBank / Global Sign Repositories** — International Lexical Databases.

---

## 2. Detailed Dataset & Resource Investigation

### 2.1 Indian Sign Language Research and Training Centre (ISLRTC)
- **Official Portal:** [https://islrtc.nic.in/](https://islrtc.nic.in/)
- **Institutional Authority:** Autonomous body under the Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice & Empowerment, Government of India.
- **Resource Scope:**
  - **10,000-Word ISL Digital Dictionary:** Comprehensive video repository containing everyday terms, legal terminology, agricultural terms, and foundational STEM/technical terms.
  - **NCERT Textbooks in ISL:** Integration of school curricula (Grades 1–12) into ISL videos, hosted across the national DIKSHA platform and the National Digital Library of India (NDLI).
- **Linguistic Authenticity:** **100% Genuine ISL**. Codified and validated by deaf master signers, certified ISL interpreters, and deaf education specialists.
- **Copyright & Ownership:** Copyright owned by DEPwD, Ministry of Social Justice & Empowerment, Government of India.
- **Reproduction & Licensing Policy:**
  - Standard government portal terms permit free reproduction for non-commercial educational and accessibility purposes.
  - **Mandatory Requirements:**
    1. Content must be reproduced accurately without altering signs or contextual meaning.
    2. Material cannot be used in a derogatory or misleading context.
    3. Prominent credit and source acknowledgement to ISLRTC, DEPwD, and the Ministry of Social Justice & Empowerment is mandatory.
  - **Commercial & Bulk Scraping Restrictions:** Bulk automated scraping, commercial redistribution, or training proprietary commercial neural networks without explicit authorization is prohibited.
  - **Official Access Pathway:** Formal institutional communication via `islrtcnewdelhi@gmail.com` to secure research/educational data-sharing Memoranda of Understanding (MOUs).

### 2.2 ISLTranslate Dataset
- **Academic Citation:** Joshi, A., Agrawal, S., & Modi, A. (2023). *ISLTranslate: A Dataset for Translating Indian Sign Language into English and Hindi*. Findings of the Association for Computational Linguistics: ACL 2023, pp. 10452–10468.
- **Repository:** [https://github.com/Exploration-Lab/ISLTranslate](https://github.com/Exploration-Lab/ISLTranslate)
- **Resource Scope:**
  - Approximately **31,000 sentence/phrase pairs** pairing continuous ISL video with English and Hindi parallel text.
  - Covers news broadcasts, informational announcements, and educational discourse.
- **Linguistic Authenticity:** **Genuine Continuous ISL**. Signed by native and proficient deaf signers.
- **Technical Format:** Video recordings paired with sentence-level text annotations and gloss references.
- **Licensing & Usage Constraints:**
  - Available for non-commercial academic research under the Research Community License.
  - Redistribution of raw video bytes requires attribution to IIT Kanpur Exploration Lab.
  - Model training: Permitted for academic benchmark replication.

### 2.3 iSign Continuous Multimodal Benchmark
- **Academic Citation:** Exploration Lab (2024). *iSign: A Benchmark for Indian Sign Language Processing*.
- **Dataset Hosting:** [https://huggingface.co/datasets/Exploration-Lab/iSign](https://huggingface.co/datasets/Exploration-Lab/iSign)
- **Project Page:** [https://exploration-lab.github.io/iSign/](https://exploration-lab.github.io/iSign/)
- **Resource Scope:**
  - Over **118,000+ ISL video-sentence/phrase pairs**.
  - Benchmarked tasks: `SignVideo2Text`, `SignPose2Text`, `Text2Pose`, `Word Prediction`, and `Sign Semantics`.
  - Extracted skeletal motion capture data using Google MediaPipe Holistic (54 keypoints: hands, pose, face).
- **Technical Format:**
  - Hosted on Hugging Face as multipart split archives (`iSign-videos_v1.1_part_aa`, `ab`, etc.).
  - Poses formatted in standardized `pose-format` binary structures.
- **Licensing & Access Constraints:**
  - Gated dataset: Requires Hugging Face user registration and explicit agreement to academic research terms.
  - Prohibits commercial redistribution.
  - Signer consent: Deaf participants consented to academic AI research and educational benchmarking.

---

## 3. Comparative Resource Analysis

| Resource | Scope / Size | Domain Focus | Modality | Redistribution Permitted? | Commercial Use? | Accessibility Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **ISLRTC Dictionary** | 10,000 signs | Everyday + STEM foundations | Studio Video | No (Attributed embed only) | No (Requires MOU) | **Gated / Official Request** |
| **ISLTranslate** | 31,000 pairs | General & Informational | Continuous Video + Text | Academic Research Only | No | **Open Research (GitHub)** |
| **iSign Benchmark** | 118,000 pairs | Conversational & Broad Domain | Video + MediaPipe 3D Poses | Gated Academic Only | No | **Gated (Hugging Face)** |
| **DIKSHA NCERT ISL** | Hundreds of hours | K-12 STEM & Humanities | Lecture Video | No (Streaming on DIKSHA) | No | **Public Streaming** |

---

## 4. Legal, Ethical & Privacy Framework

### 4.1 Signer Consent & Biometric Protection
- In sign language recordings, a signer's face, hands, and body morphology are visible. Under the **Digital Personal Data Protection (DPDP) Act 2023 (India)** and global biometric data protection standards, facial geometry and video recordings constitute personally identifiable biometric information.
- **Ethical Mandate:** SignBridge AI must never scrape private Deaf individuals from social media, YouTube personal vlogs, or private messaging channels. All media must carry verified informed consent documentation.

### 4.2 Handling Unsupported STEM Terminology
- **Crucial Finding:** While ISLRTC has standardized thousands of basic and secondary-school concepts, advanced tertiary engineering terms (e.g. *Deadlock*, *Pipelining*, *Eigenvalues*, *Shear Strain*, *Substation Busbar*) lack nationwide single-sign codification.
- **Linguistic Principle:** In natural Deaf engineering communication, concepts without a standardized single sign are communicated using:
  1. Two-handed fingerspelling for technical initial introduction (e.g., `D-E-A-D-L-O-C-K`).
  2. Depicting classifiers and spatial indexing to model dynamic behavior.
  3. Contextual compound expansions (e.g., `COMPUTER + LOCK + PROCESS + WAIT`).
- **Policy Enforcement:** SignBridge AI must never synthesize a fake arbitrary hand movement for an uncodified term. It must transparently report `UNSUPPORTED` or `EXPLANATION_REQUIRED`, provide fingerspelling guidance, and request deaf educator review.

---

## 5. Architectural Data Ingestion Strategy

SignBridge AI implements a decoupled **Dataset Importer Architecture**:
1. **Schema Grounding:** The database stores authoritative source identifiers, licenses, and phonological parameters.
2. **Authorized Ingestion Scripts:** Reusable CLI scripts in `scripts/` ingest validated datasets from approved CSV/JSON/Media bundles without hardcoding.
3. **Pending Validation Queue:** All newly ingested candidate terms enter the state `NEEDS_REVIEW` and must be approved by a verified reviewer before achieving `VERIFIED` status.

---

*Document certified by Lead AI Engineer & ISL Linguistics Specialist on November 19, 2026.*
