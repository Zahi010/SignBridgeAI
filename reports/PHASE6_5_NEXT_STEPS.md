# SignBridge AI — Phase 6.5: Next Steps & Pilot Execution Roadmap

**Date:** 2026-11-21  
**Target Milestone:** Phase 7 — External Deaf Community Pilot & Multimodal Field Evaluation  
**Prerequisites Completed:** Phase 6.5 Independent Verification & Remediation  

---

## 1. High-Priority Next Steps

Following the successful completion of Phase 6.5, the immediate path forward focuses on non-technical research clearance, container hosting, and accredited participant recruitment.

### Step 1: Formal Institutional Review Board (IRB) Submission
- Prepare formal study protocol document using the validated parameters in `reports/PHASE6_5_RESEARCH_ETHICS_GAP_ANALYSIS.md`.
- Finalize participant information sheets (PIS) and consent documents.
- Submit to university or partner hospital ethics committee for formal clearance.

### Step 2: Production Staging on Docker/Cloud Host
- Deploy the verified `Dockerfile` and `docker-compose.yml` to a Linux cloud host (e.g. AWS, GCP, or institutional server with Docker installed).
- Configure automated HTTPS via Let's Encrypt / reverse proxy.
- Verify that automated backup cron jobs execute `backup_database.py` and `backup_media.py` daily.

### Step 3: Production of ISL Video-Based Consent Media
- Film a certified Deaf master signer reciting each informed consent clause in standard Indian Sign Language.
- Store videos in `data/consent_videos/` and link to the frontend informed consent workflow.

### Step 4: Expert Reviewer Onboarding
- Invite accredited ISLRTC / Rehabilitation Council of India (RCI) certified sign language interpreters.
- Conduct onboarding review sessions using the Phase 5 evaluation rubrics.
- Monitor Fleiss' Kappa in real time via the academic dashboard as independent evaluations accumulate.

---

## 2. Maintenance & Hygiene Schedule

- **Weekly:** Execute `scripts/backup_database.py` and `scripts/backup_media.py`.
- **Monthly:** Execute disaster recovery dry runs (`scripts/restore_database.py` and `scripts/restore_media.py`) into an isolated test environment.
- **Continuous:** Ensure 107/107 automated tests pass on all pull requests. Maintain zero application deprecation warnings.

