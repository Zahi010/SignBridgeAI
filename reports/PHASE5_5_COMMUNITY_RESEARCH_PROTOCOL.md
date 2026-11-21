# SignBridge AI — Phase 5.5: Deaf Community Research Protocol & Ethics

**Author:** Deaf Community Research Liaison & Research Ethics Specialist  
**Milestone:** Phase 5 — ISL Community Review, Expert Validation & Academic Evaluation Framework  
**Project:** SignBridge AI (`E:\SignBridgeAi`)  

---

## 1. Ethical Governance & Research Principles

Conducting research with Deaf community members requires strict adherence to international and Indian biomedical/behavioral research guidelines (ICMR Ethical Guidelines for Biomedical Research Involving Human Participants):

1. **Cultural Respect & Deaf Epistemology:** Recognizing Indian Sign Language as a complete natural language and Deaf signers as a linguistic minority, not clinical subjects requiring correction.
2. **Voluntary Informed Consent:** Clear explanation of research objectives in accessible ISL and English.
3. **Zero Personally Identifiable Information (PII):** No names, phone numbers, email addresses, or facial camera recordings are collected.
4. **Pseudonymization:** Participants operate under anonymous research codes (e.g., `DEAF-PARTICIPANT-83A`).
5. **Right to Withdraw (Right to be Forgotten):** Participants may withdraw at any time. An automated data deletion workflow permanently purges all survey responses.
6. **Zero-Fabrication:** Never fabricate participant cohorts, survey scores, or community acceptance claims without real human trials.

---

## 2. Participant Information Sheet & Consent Workflow

Before entering any evaluation survey, participants review an electronic information sheet:

```
+-------------------------------------------------------------------------------+
|                    DEAF COMMUNITY RESEARCH CONSENT PROTOCOL                   |
+-------------------------------------------------------------------------------+
| Study Title: SignBridge AI STEM Sign Comprehension & Naturalness Pilot 2026   |
| Purpose: Evaluate whether 3D animated signs are clear, accurate, and natural. |
| Risks: None beyond visual screen reading.                                     |
| Data Collected: Anonymous comprehension choices, 1-5 naturalness star rating, |
|                 regional dialect commentary.                                  |
| Privacy: Data linked strictly to your pseudonym.                              |
+-------------------------------------------------------------------------------+
```

Participants check `[x] I have read the information sheet and give voluntary consent`, which issues a timestamped `ParticipantConsent` database record via `POST /api/v1/community/consent`.

---

## 3. Comprehension Assessment Protocol

A sign language translation tool is useless if Deaf students cannot understand the technical concepts conveyed. The portal tests **true semantic comprehension**:

1. **Avatar Video Playback:** The participant watches the avatar sign an engineering concept without English text captions.
2. **Multiple-Choice Meaning Verification:** The participant is asked: *"What concept is being signed?"* and chooses among 4 plausible technical options.
3. **Objective Comprehension Scoring:** A binary accuracy score ($1.0$ for correct, $0.0$ for incorrect) is computed and stored.

---

## 4. Naturalness & Perceptual Ergonomics

Even if a sign is comprehensible, it may be unnatural, abrupt, or fatiguing to watch during a 45-minute engineering lecture. The portal measures:

- **1–5 Star Likert Rating:** From $1$ ("Robotic / Awkward") to $5$ ("Highly Fluid & Natural").
- **Facial Expression Evaluation:** Whether the presence or absence of non-manual markers hinders comprehension.
- **Regional Dialect Tagging:** Reviewers document whether their local community (e.g., Kerala, West Bengal, Maharashtra) uses an alternate lexical sign.

---

## 5. Right to be Forgotten / Automated Data Deletion

Under `POST /api/v1/community/delete-data`, participants can withdraw at any time:

```python
# Purges all research sessions and feedback notes
deleted_sessions_count = db.query(ResearchSession).filter(ResearchSession.consent_id == consent.id).delete()
consent.consent_given = False
consent.data_deletion_requested = True
consent.withdrawal_date = datetime.utcnow()
```

- Instantly deletes all session records from the database.
- Marks consent as withdrawn.
- Prevents subsequent recording under that pseudonym.
- Logs the deletion event in the immutable audit log for compliance.

---

## 6. Open Academic Research Dataset Export

To support open science, anonymized evaluation records can be exported via `GET /api/v1/community/export`:
- Format: JSON / CSV.
- License: Open Data Commons Attribution License (ODC-By).
- Compliance: Automatically excludes withdrawn participants.
