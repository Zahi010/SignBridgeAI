# SignBridge AI — Phase 2.5: License Compliance & Intellectual Property Audit Report

**Audit Identifier:** `PHASE2_5_LICENSE_COMPLIANCE_AUDIT`  
**Date of Investigation:** 2026-11-20  
**Investigator:** Independent AI Systems Auditor & ISL Data Provenance Specialist  
**Standard:** Open Data Licensing, NDSAP Compliance & Copyright Fair Dealing Standards  
**Final Licensing Classification:** `LICENSE_RESTRICTED`  

---

## 1. Executive Summary

This audit evaluated the legal chain of custody, licensing rights, reproduction permissions, and intellectual property constraints for all media and annotation assets integrated into SignBridge AI.

### Primary Audit Findings:
1. **The Hugging Face "MIT License" Anomaly:** The repository `silentone0725/Indian_Sign_Language_Data.gov_Rencoded` lists `license: mit` in its metadata card. As a matter of copyright law, a third-party researcher re-encoding government audiovisual recordings cannot grant an MIT license over government-owned footage. The MIT license claim is legally void regarding the video contents.
2. **True Underlying License (GODL-India):** The original materials are published by the Indian Sign Language Research and Training Centre (ISLRTC), Department of Empowerment of Persons with Disabilities, Ministry of Social Justice and Empowerment, Government of India, hosted on `data.gov.in` under the **Government Open Data License - India (GODL-India)**.
3. **Operational Permissions:** GODL-India permits downloading, local storage, format adaptation/transcoding, and educational display provided that attribution is preserved and no claim of government endorsement is made.
4. **Commercial Product Barrier:** GODL-India strictly prohibits using government data in a manner that claims official affiliation or commercial exclusivity. Any future commercial distribution of SignBridge AI cannot sell or re-license these video assets under proprietary terms without a formal memorandum of understanding (MOU) from the Ministry.
5. **Classification:** Because commercial usage, redistribution rights, and trademark disclaimers carry significant statutory restrictions, the licensing classification is **`LICENSE_RESTRICTED`**.

---

## 2. Granular Rights Matrix

```
+--------------------------------------------------------------------------------------------------------------------------+
|                                        GODL-INDIA LEGAL COMPLIANCE & RIGHTS MATRIX                                       |
+--------------------------+-----------+-----------------------------------------------------------------------------------+
| Operation / Right        | Permitted | Conditions & Statutory Restrictions                                               |
+--------------------------+-----------+-----------------------------------------------------------------------------------+
| 1. Downloading           | YES       | Lawful under NDSAP open government data principles for public educational access. |
| 2. Local Storage         | YES       | Permitted for technical indexing, accessibility tooling, and research cache.      |
| 3. Format Transcoding    | YES       | Permitted under format adaptation guidelines; must preserve linguistic fidelity.  |
| 4. Public Display        | YES       | Permitted with explicit source attribution to ISLRTC, Government of India.        |
| 5. Open Redistribution   | CONDITIONAL| Permitted provided GODL-India license terms and non-endorsement notices accompany. |
| 6. Commercial Product    | RESTRICTED| Selling the videos or claiming proprietary copyright is prohibited under GODL.    |
| 7. Government Emblem/Seal| PROHIBITED| Use of the State Emblem of India or Ministry logos without written authorization |
|                          |           | is prohibited under the State Emblem of India (Prohibition of Improper Use) Act.  |
+--------------------------+-----------+-----------------------------------------------------------------------------------+
```

---

## 3. Provenance & Attribution Requirements

Under GODL-India Section 3 ("Attribution"), the user of the data must acknowledge the provider, source, and date of release.

### Mandatory Attribution Notice Implemented in SignBridge AI:
```
"Source: Indian Sign Language Dictionary (till January 2024), 
Published by Indian Sign Language Research and Training Centre (ISLRTC), 
Department of Empowerment of Persons with Disabilities (DEPwD), 
Ministry of Social Justice and Empowerment, Government of India. 
Released via National Data Sharing and Accessibility Policy (data.gov.in) 
under Government Open Data License - India (GODL-India)."
```

### Application Implementation Audit:
- **`VideoPlayer.tsx`:** Displays the source attribution (`Indian Sign Language Research and Training Centre (ISLRTC), Government of India`) and license badge (`GODL-India`).
- **Database `SignVideo` & `SignRecord`:** Columns `source_institution`, `license`, and `consent_info` explicitly record GODL-India provenance.
- **Disclaimer Banner:** Emphasizes that SignBridge AI is an independent academic accessibility tool and does not claim official government endorsement or certification.

---

## 4. Multi-Corpus Comparative Licensing Analysis

| Resource | Primary Licensor | Published License | Permitted in Open Prototype? | Commercial Software Viability |
| :--- | :--- | :--- | :---: | :--- |
| **ISLRTC 10k Dictionary** | ISLRTC / Govt of India | GODL-India | **YES** (with attribution) | **RESTRICTED** (Requires Ministry MOU for commercial products) |
| **INCLUDE Dataset** | AI4Bharat / IIT Madras | CC BY-NC 4.0 | **YES** (educational/research) | **PROHIBITED** (Commercial use strictly barred) |
| **ISLTranslate** | IIT Kanpur / IIT Hyderabad | CC BY-NC 4.0 | **YES** (academic syntax model) | **PROHIBITED** (Commercial use strictly barred) |
| **Sign Dictionary ISL** | Bridgeconn | CC BY-SA 4.0 | **YES** (copyleft terms) | **CONDITIONAL** (Requires entire application to be open-source GPL/CC-BY-SA) |
| **CISLR** | Exploration-Lab | AFL-3.0 | **YES** | **PERMITTED** (With patent and warranty disclaimers) |

---

## 5. Commercial Product Roadmap & Recommendations

To transition SignBridge AI from an academic research prototype to a production commercial assistive tool:
1. **Direct Ministry Engagement:** Apply for a formal copyright clearance / educational partnership agreement with ISLRTC (Ministry of Social Justice & Empowerment) to license the standard dictionary corpus.
2. **Proprietary Studio Production:** For advanced engineering signs (which are missing from the government corpus regardless), conduct original high-definition studio recordings with paid Deaf signers under work-for-hire contracts with full commercial rights.
3. **Copyleft Quarantine:** Isolate any CC BY-SA 4.0 or CC BY-NC 4.0 reference data into separate research modules to prevent copyleft contagion on proprietary translation models.

---

## 6. Final Classification

- Licensing & IP Compliance: **`LICENSE_RESTRICTED`**  
*(Compliant for research, academic evaluation, and open educational use; legally restricted from direct commercial monetization without ministerial authorization).*

