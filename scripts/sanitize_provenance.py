"""
Sanitizes the expert_reviews and dataset_provenances tables in SQLite
to ensure all reviewer and provenance accounts are transparently labeled as
Demonstration Seed Data / Local Test Accounts without misleading identities.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("backend/signbridge.db")

def sanitize():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("[Sanitize] Updating Expert Reviews to honest test/demo accounts...")
    cursor.execute("""
    UPDATE expert_reviews
    SET reviewer_name = '[Local Test Reviewer] Certified Deaf Educator',
        reviewer_role = 'Deaf STEM Specialist (Test Account)',
        affiliation = 'SignBridge Verification Testing Environment',
        review_notes = 'Pre-configured verification test record for local pipeline validation.'
    WHERE id = 1
    """)

    cursor.execute("""
    UPDATE expert_reviews
    SET reviewer_name = '[Local Test Reviewer] Academic Sign Linguist',
        reviewer_role = 'ISL Linguistic Researcher (Test Account)',
        affiliation = 'SignBridge Verification Testing Environment',
        review_notes = 'Candidate sign peer evaluation test profile.'
    WHERE id = 2
    """)

    print("[Sanitize] Updating Dataset Provenance names to clear reference models...")
    cursor.execute("""
    UPDATE dataset_provenances
    SET name = 'ISLRTC STEM Reference Framework (Government Open Reference Model)',
        methodology = 'Codification model based on ISLRTC 10,000-word STEM dictionary publications.'
    WHERE id = 1
    """)

    cursor.execute("""
    UPDATE dataset_provenances
    SET name = 'Deaf Technical Education Academic Consortium (Candidate Standard)',
        methodology = 'Curricular peer evaluation standard for polytechnic and engineering colleges.'
    WHERE id = 2
    """)

    conn.commit()
    conn.close()
    print("[Sanitize] Provenance and Reviewer records sanitized successfully!")

if __name__ == "__main__":
    sanitize()
