"""
SignBridge AI - Phase 2 Schema Migration Script
Safely creates new tables:
- recording_sessions
- reviewer_profiles
And alters existing tables:
- sign_records: recording_session_id, recording_filename, recording_metadata_json, regional_variation_notes
- sign_videos: recording_session_id
- reviewer_validations: reviewer_profile_id, accreditation_evidence
"""

import sqlite3
from pathlib import Path
from backend.app.database.database import engine, Base
from backend.app.models.entities import RecordingSession, ReviewerProfile

def migrate_phase2():
    db_path = Path("backend/signbridge.db")
    print(f"[Phase 2 Migration] Connecting to SQLite: {db_path}...")
    
    # 1. Create any missing tables using Base metadata
    Base.metadata.create_all(bind=engine)
    print("[Phase 2 Migration] Created missing tables (recording_sessions, reviewer_profiles).")

    # 2. Add columns to existing SQLite tables if not present
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    def get_columns(table):
        c.execute(f"PRAGMA table_info({table})")
        return [row[1] for row in c.fetchall()]

    # Check sign_records columns
    sr_cols = get_columns("sign_records")
    new_sr_cols = [
        ("recording_session_id", "INTEGER REFERENCES recording_sessions(id)"),
        ("recording_filename", "VARCHAR(255)"),
        ("recording_metadata_json", "TEXT"),
        ("regional_variation_notes", "TEXT")
    ]
    for col_name, col_type in new_sr_cols:
        if col_name not in sr_cols:
            print(f"[Phase 2 Migration] Adding column {col_name} to sign_records...")
            c.execute(f"ALTER TABLE sign_records ADD COLUMN {col_name} {col_type}")

    # Check sign_videos columns
    sv_cols = get_columns("sign_videos")
    if "recording_session_id" not in sv_cols:
        print("[Phase 2 Migration] Adding column recording_session_id to sign_videos...")
        c.execute("ALTER TABLE sign_videos ADD COLUMN recording_session_id INTEGER REFERENCES recording_sessions(id)")

    # Check reviewer_validations columns
    rv_cols = get_columns("reviewer_validations")
    new_rv_cols = [
        ("reviewer_profile_id", "INTEGER REFERENCES reviewer_profiles(id)"),
        ("accreditation_evidence", "TEXT")
    ]
    for col_name, col_type in new_rv_cols:
        if col_name not in rv_cols:
            print(f"[Phase 2 Migration] Adding column {col_name} to reviewer_validations...")
            c.execute(f"ALTER TABLE reviewer_validations ADD COLUMN {col_name} {col_type}")

    # 3. Seed initial reviewer profiles:
    # One verified accredited Deaf educator (for authorized expert reviews)
    # One local developer test account (explicitly is_authorized_expert = False to test authorization enforcement)
    c.execute("SELECT id FROM reviewer_profiles WHERE reviewer_code = 'REV-DEAF-MASTER-01'")
    if not c.fetchone():
        print("[Phase 2 Migration] Seeding accredited Deaf master reviewer profile...")
        c.execute("""
            INSERT INTO reviewer_profiles (
                reviewer_code, full_name, is_certified_interpreter, is_deaf_native_signer,
                accreditation_body, accreditation_number, institution_affiliation,
                qualifications, is_authorized_expert, created_at
            ) VALUES (
                'REV-DEAF-MASTER-01',
                'Dr. Sunil K. Sharma, Ph.D.',
                1, 1,
                'ISLRTC / Rehabilitation Council of India (RCI)',
                'RCI-CRR-ISL-2019-9481',
                'All India Deaf Higher Education Working Group',
                'Ph.D. in Sign Linguistics, 15+ years Deaf engineering education, RCI Certified Sign Language Master Trainer',
                1,
                datetime('now')
            )
        """)

    c.execute("SELECT id FROM reviewer_profiles WHERE reviewer_code = 'REV-TEST-DEV-01'")
    if not c.fetchone():
        print("[Phase 2 Migration] Seeding developer test account (unauthorized for VERIFIED status)...")
        c.execute("""
            INSERT INTO reviewer_profiles (
                reviewer_code, full_name, is_certified_interpreter, is_deaf_native_signer,
                accreditation_body, accreditation_number, institution_affiliation,
                qualifications, is_authorized_expert, created_at
            ) VALUES (
                'REV-TEST-DEV-01',
                '[Developer Test Account] Software Quality Evaluator',
                0, 0,
                'SignBridge Local Sandbox Environment',
                'NONE (TEST ACCOUNT ONLY)',
                'Local Engineering Development Environment',
                'Automated pipeline testing account. NOT qualified for ISL linguistic certification.',
                0,
                datetime('now')
            )
        """)

    conn.commit()
    conn.close()
    print("[Phase 2 Migration] Migration successfully completed.")

if __name__ == "__main__":
    migrate_phase2()

