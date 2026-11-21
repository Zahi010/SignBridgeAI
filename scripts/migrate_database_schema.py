"""
Database Schema Migration Helper for SignBridge AI.
Safely adds missing columns and creates new tables in SQLite without losing existing data.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("backend/signbridge.db")

def migrate():
    if not DB_PATH.exists():
        print(f"Database {DB_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("[Migration] Inspecting existing SQLite schema...")

    # 1. Check columns in 'concepts'
    cursor.execute("PRAGMA table_info(concepts)")
    concept_cols = [row[1] for row in cursor.fetchall()]
    
    if "domain" not in concept_cols:
        print("[Migration] Adding 'domain' to concepts table...")
        cursor.execute("ALTER TABLE concepts ADD COLUMN domain VARCHAR(100)")

    # 2. Check columns in 'sign_records'
    cursor.execute("PRAGMA table_info(sign_records)")
    sign_cols = [row[1] for row in cursor.fetchall()]

    new_sign_cols = [
        ("sign_id", "VARCHAR(50)"),
        ("dominant_hand", "VARCHAR(50)"),
        ("handshape", "VARCHAR(100)"),
        ("movement", "VARCHAR(150)"),
        ("location", "VARCHAR(150)"),
        ("orientation", "VARCHAR(150)"),
        ("non_manual_markers", "VARCHAR(150)"),
        ("source_institution", "VARCHAR(150)"),
        ("source_url_or_dataset_id", "VARCHAR(255)"),
        ("license", "VARCHAR(100)"),
        ("consent_info", "VARCHAR(255)"),
        ("validation_date", "DATETIME"),
        ("confidence_score", "FLOAT")
    ]

    for col_name, col_type in new_sign_cols:
        if col_name not in sign_cols:
            print(f"[Migration] Adding '{col_name}' to sign_records table...")
            cursor.execute(f"ALTER TABLE sign_records ADD COLUMN {col_name} {col_type}")

    # 3. Ensure 'reviewer_validations' table exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviewer_validations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sign_record_id INTEGER NOT NULL REFERENCES sign_records(id) ON DELETE CASCADE,
        reviewer_name VARCHAR(120) NOT NULL,
        reviewer_role VARCHAR(120) NOT NULL,
        affiliation VARCHAR(150),
        decision VARCHAR(50) DEFAULT 'requires_correction',
        assigned_status VARCHAR(50) DEFAULT 'needs_review',
        corrections TEXT,
        suggested_regional_variation VARCHAR(100),
        comments TEXT,
        accuracy_rating FLOAT,
        reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("[Migration] Schema migration completed successfully!")

if __name__ == "__main__":
    migrate()
