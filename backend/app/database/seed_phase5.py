"""
SignBridge AI - Phase 5 Database Seeding Script.
Initializes Phase 5 tables, default validation project, tasks for authentic ISL signs,
and an administrative governance account.
Strict Zero-Fabrication: All signs are marked PENDING_EXTERNAL_REVIEW.
No fake validation reviews or simulated accreditations are seeded.
"""

from backend.app.database.database import SessionLocal, Base, engine
from backend.app.models.entities import SignRecord, Concept
from backend.app.models.validation_models import (
    Reviewer,
    ReviewerRole,
    ReviewerVerificationStatus,
    ValidationProject,
    ValidationTask,
    ValidationTaskStatus
)
from backend.app.core.auth import hash_password


def seed_phase5_database():
    print("[Seed Phase 5] Ensuring all validation & community tables exist...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Default Validation Project
        project = db.query(ValidationProject).first()
        if not project:
            print("[Seed Phase 5] Creating default Validation Project...")
            project = ValidationProject(
                name="ISLRTC STEM Engineering Terminology Validation Pilot 2026",
                description="Linguistic and phonological validation of engineering signs across Indian Sign Language Deaf cohorts.",
                target_domain="Engineering & Computer Science",
                rubric_config_json="12_criteria_rubric_v1",
                is_active=True
            )
            db.add(project)
            db.flush()

        # 2. Seed Default Administrative Governance Reviewer
        admin = db.query(Reviewer).filter(Reviewer.username == "admin").first()
        if not admin:
            print("[Seed Phase 5] Creating default Administrative Reviewer...")
            admin = Reviewer(
                username="admin",
                email="governance@signbridge.ai",
                hashed_password=hash_password("admin_pass_2026_isl"),
                full_name="SignBridge System Administrator",
                is_deaf_native_signer=False,
                is_certified_interpreter=False,
                years_of_experience=5,
                institution_affiliation="SignBridge AI Research Governance Secretariat",
                role=ReviewerRole.ADMIN,
                verification_status=ReviewerVerificationStatus.VERIFIED,
                verification_notes="Root system administrative account authorized for credential audits.",
                is_active=True
            )
            db.add(admin)
            db.flush()

        # 3. Seed ValidationTasks for the 5 authentic ISLRTC signs
        authentic_terms = ["Algorithm", "Frequency", "Current", "Beam", "Torque"]
        for term in authentic_terms:
            concept = db.query(Concept).filter(Concept.term == term).first()
            if not concept:
                continue

            sign = db.query(SignRecord).filter(SignRecord.concept_id == concept.id).first()
            if not sign:
                continue

            existing_task = db.query(ValidationTask).filter(ValidationTask.sign_record_id == sign.id).first()
            if not existing_task:
                print(f"[Seed Phase 5] Creating ValidationTask for '{term}'...")
                task = ValidationTask(
                    project_id=project.id,
                    sign_record_id=sign.id,
                    concept_id=concept.id,
                    status=ValidationTaskStatus.PENDING_REVIEW,
                    assigned_reviewers_count=0,
                    completed_reviews_count=0
                )
                db.add(task)

        db.commit()
        print("[Seed Phase 5] Phase 5 database initialization complete.")
    except Exception as e:
        db.rollback()
        print(f"[Seed Phase 5] Error during seeding: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_phase5_database()
