# SignBridge AI — Phase 2: Authentic ISL Data Source Research Report

**Document ID:** `reports/PHASE2_ISL_DATA_SOURCE_RESEARCH.md`  
**Research Date:** November 20, 2026  
**Auditor & Research Role:** Senior AI Systems Auditor & Indian Sign Language (ISL) Linguistics Specialist  
**Investigation Scope:** Identification, legal verification, accessibility audit, and vocabulary analysis of authentic Indian Sign Language resources for STEM education.

---

## 1. Executive Summary

A critical constraint identified in Phase 1 is that **no genuine human ISL signing videos existed in the repository**, and all video assets were synthetic FFmpeg `testsrc` animations. 

In Phase 2, we conducted an exhaustive investigation into public and academic Indian Sign Language data sources across government portals, academic institutions, and open AI repositories.

### Key Linguistic & Data Findings:
1. **Language Authenticity:** Indian Sign Language (ISL) is a distinct, natural visual-gestural language with its own grammar, syntax (Topic-Comment, Time-First, terminal WH-movement), and phonology. Resources using American Sign Language (ASL) or British Sign Language (BSL) cannot be substituted for ISL.
2. **Foundational STEM vs. Advanced Engineering Vocabulary:**
   - General science and mathematics terms (*Force*, *Energy*, *Machine*, *Computer*, *Angle*, *Current*, *Voltage*, *Measure*, *Temperature*) exist in the **ISLRTC 10,000-word STEM Glossary** and school curriculum projects (DIKSHA/NCERT).
   - Advanced university engineering concepts (*Deadlock*, *Compiler Intermediate Representation*, *Quadrature Amplitude Modulation*, *Finite Element Method*, *Prestressed Concrete*, *P-Delta Effect*, *Synchronous Reactance*) **are not codified as isolated single signs in any public Indian dataset**.
3. **Deaf Community Standard for Uncodified Concepts:**
   Deaf engineering students and certified interpreters navigate unstandardized terminology through:
   - Initialized compound signs (e.g., combining *COMPUTER* + *MEMORY* for RAM).
   - Two-handed ISL fingerspelling sequences (e.g., `D-E-A-D-L-O-C-K`).
   - Pedagogical visual diagramming and conceptual classifier handshapes.
4. **Licensing & Redistribution Realities:**
   - Academic datasets (ISLTranslate, INCLUDE, CISLR) are licensed exclusively for **non-commercial academic research** under CC BY-NC 4.0 or custom institutional terms.
   - Government datasets (ISLRTC via data.gov.in / NDLI) are released under the **Government Open Data License - India (GODL-India)** or educational fair dealing.

---

## 2. In-Depth Source Evaluation Matrix

### A. ISLRTC 10,000-Word STEM Dictionary & NDLI Modules
- **Organization:** Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities (DEPwD), Ministry of Social Justice and Empowerment, Government of India.
- **Resource Name:** ISLRTC 10,000 Words ISL Dictionary & NDLI STEM Technical Modules.
- **Language:** Authentic Indian Sign Language (Standard Northern / Pan-India).
- **Available Vocabulary:** 10,000 lexical items spanning technical, academic, administrative, and daily life terms. Includes dedicated modules:
  - *Academic Terms of Science in Sign Language*
  - *Academic Terms of Mathematics in Sign Language*
  - *ISL Dictionary - Technical Terms*
- **Video / Media Formats:** MP4 video clips, 1080p and 720p H.264, standard 25/30 fps.
- **Signer Identity & Consent:** Certified Deaf master signers and licensed interpreters employed under institutional government consent protocols.
- **Annotation Format:** English gloss, Hindi translation, formal definition, parts of speech.
- **Engineering Terminology:** Strong coverage of primary and secondary STEM concepts (physics, chemistry, math, basic computing). Weak on specialized engineering branches (no *Deadlock*, *Modulation*, *Bracing*).
- **Access Procedure:** Searchable digital dictionary at `islrtc.nic.in`, mobile app *Sign Learn*, National Digital Library of India (NDLI portal), and open data mirrors on `data.gov.in`.
- **License:** Government Open Data License - India (GODL-India) / Educational Fair Use.
- **Commercial Use:** Restricted without explicit ministry authorization.
- **Modifications / Derivative Works:** Permitted for non-commercial educational integration provided attribution is preserved.
- **Attribution Requirement:** Explicit citation: *"Source: Indian Sign Language Research and Training Centre (ISLRTC), Government of India"*.

---

### B. ISLTranslate & iSign Benchmark Suite
- **Organization / Authors:** Exploration-Lab, Indian Institute of Technology Kanpur (IIT Kanpur) & Indian Institute of Technology Hyderabad (IIT Hyderabad) — Abhinav Joshi, Susmit Agrawal, Ashutosh Modi.
- **Resource Name:** `ISLTranslate: Dataset for Translating Indian Sign Language` (ACL 2023) / `iSign Benchmark`.
- **Language:** Continuous Indian Sign Language.
- **Available Vocabulary:** 31,000+ continuous ISL-English sentence/phrase pairs; over 118,000 video-phrase instances in iSign.
- **Video / Media Formats:** High-definition MP4 videos, 25 fps, accompanied by pre-extracted 2D/3D MediaPipe holistic pose landmark arrays.
- **Signer Identity & Consent:** Multiple native Deaf signers recorded under signed institutional ethics approval and academic participant consent.
- **Annotation Format:** Full-sentence English translations, sentence-level gloss annotations, spatial landmark coordinates (`.npy` / `.npz`).
- **Engineering Terminology:** General conversational, educational narratives, current affairs; limited specialized tertiary engineering terms.
- **Access Procedure:** GitHub repository (`Exploration-Lab/ISLTranslate`) and Hugging Face Dataset Hub (`Exploration-Lab/iSign` — gated, requires accepting usage terms).
- **License:** Creative Commons Attribution-NonCommercial 4.0 International (**CC BY-NC 4.0**).
- **Commercial Use:** **Strictly Prohibited**.
- **Modifications / Derivative Works:** Permitted for research and non-commercial educational tools.
- **Attribution Requirement:** Mandatory academic citation of the ACL 2023 publication.

---

### C. INCLUDE Dataset (AI4Bharat / IIT Madras)
- **Organization / Authors:** AI4Bharat, Indian Institute of Technology Madras (IIT Madras) — Advaith Sridhar, Rohith Gandhi Ganesan, Pratyush Kumar, Mitesh M. Khapra (ACM MM 2020).
- **Resource Name:** `INCLUDE: A Large Scale Dataset for Indian Sign Language Recognition`.
- **Language:** Indian Sign Language (Word-level isolated signs).
- **Available Vocabulary:** 263 word signs spanning 15 categories (4,287+ video clips); benchmark subset *INCLUDE-50* (50 classes).
- **Video / Media Formats:** MP4 video clips recorded under natural lighting.
- **Signer Identity & Consent:** Native deaf student signers from the **St. Louis School for the Deaf (Adyar, Chennai)**. Explicit parental and institutional consent protocols recorded.
- **Annotation Format:** Word-level CSV labels, class index mappings, bounding boxes.
- **Engineering Terminology:** General vocabulary (numbers, colors, family, education, everyday actions). Very limited engineering coverage.
- **Access Procedure:** Download script via `github.com/AI4Bharat/INCLUDE` and AI4Bharat ISL research portal.
- **License:** Code under MIT License; dataset under academic/research non-commercial evaluation terms prioritizing participant dignity.
- **Commercial Use:** Prohibited without written agreement.
- **Modifications:** Permitted for non-commercial benchmark evaluations.

---

### D. CISLR: Corpus for Indian Sign Language Recognition
- **Organization / Authors:** Exploration-Lab (IIT Kanpur / IIT Hyderabad).
- **Resource Name:** `Exploration-Lab/CISLR` (Hugging Face).
- **Language:** Word-level Indian Sign Language.
- **Available Vocabulary:** ~4,700 distinct words/signs.
- **Video / Media Formats:** MP4 video files.
- **Signer Identity & Consent:** Recorded with Deaf native signers and licensed interpreters.
- **Annotation Format:** Word-level JSON metadata, one-shot ASL-proxy alignment embeddings.
- **Engineering Terminology:** Broad academic vocabulary including foundational physics, math, and electrical terms.
- **Access Procedure:** Hugging Face Datasets (`Exploration-Lab/CISLR`).
- **License:** Academic Free License v3.0 (**AFL-3.0**).
- **Commercial Use:** Permitted under AFL-3.0 conditions (with disclaimer of warranty and patent grant terms).

---

### E. Sign Dictionary ISL (Bridge Connectivity Solutions)
- **Organization:** Bridge Connectivity Solutions (`bridgeconn`).
- **Resource Name:** `bridgeconn/sign-dictionary-isl` (Hugging Face).
- **Language:** Indian Sign Language (Isolated lexical signs).
- **Available Vocabulary:** 3,077 lexical items / glosses (~2.5 hours total footage).
- **Video / Media Formats:** High-quality MP4 (one gloss per video) + pre-extracted pose features (`pose-dwpose.npz` and `pose-mediapipe.pose`).
- **Signer Identity & Consent:** Professional ISL signers recorded against neutral studio backgrounds.
- **Annotation Format:** JSON metadata (`filename`, `transcripts`, `glosses`, `pose_features`).
- **Engineering Terminology:** General vocabulary, everyday concepts, basic science and IT words (*Computer*, *Internet*, *Phone*, *Write*, *Read*).
- **Access Procedure:** Hugging Face WebDataset format (`https://huggingface.co/datasets/bridgeconn/sign-dictionary-isl`).
- **License:** Creative Commons Attribution-ShareAlike 4.0 International (**CC BY-SA 4.0**).
- **Commercial Use:** Permitted under ShareAlike conditions.
- **Redistribution / Derivative Works:** Permitted with attribution and under the same CC BY-SA 4.0 license.

---

## 3. Organizations & Deaf Community Networks in India

To establish authorized recording and validation partnerships:

1. **ISLRTC (New Delhi):** Autonomous government centre under DEPwD; the statutory standard-setting body for ISL in India.
2. **All India Federation of the Deaf (AIFD, New Delhi):** Apex national federation of Deaf associations representing Deaf individuals nationwide.
3. **Deaf Enabled Foundation (DEF, Hyderabad/Chennai):** Major non-profit providing vocational, technical, and educational courses for Deaf youth with extensive digital ISL resources.
4. **Kerala Federation of the Deaf (KFD, Thiruvananthapuram):** Regional authority on Malayalam-ISL linguistic variations and vernacular Deaf education.
5. **National Association of the Deaf (NAD India):** Advocacy organization focusing on accessible higher education and legal recognition of ISL.

---

## 4. Legal, Ethical, and Provenance Architecture for SignBridge AI

To ensure compliance with non-negotiable rules:
- **No Scraping Without Rights:** We refuse to scrape copyrighted or restricted video platforms.
- **Consent Documentation Protocol:** Every newly recorded sign video must be linked to a `RecordingSession` record storing signer consent ID, date, recording conditions, and explicit educational license terms.
- **Separation of Verified Corpus from Candidate Dictionary:**
  - A concept is marked **`VERIFIED`** ONLY when an authentic video from an approved source (e.g., ISLRTC GODL-India or certified studio recording) is validated by an authorized ISL expert.
  - Concepts awaiting authorized video recordings are retained as **`NEEDS_REVIEW`** or **`UNSUPPORTED`**.

