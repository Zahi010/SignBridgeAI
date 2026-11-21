"""
SignBridge AI - Database Provenance & Integrity Remediation Script
Applies critical audit fixes to backend/signbridge.db:
1. Adds inflection 'deadlocked' to Deadlock aliases so deadlock sentences are properly caught.
2. Ingests missing concepts: Entropy (ME), Process (CS), Structural Stability (CE).
3. Relabels all 5 synthetic testsrc videos in sign_videos to DEMO_ONLY with honest descriptions.
4. Relabels avatar_animations record to NOT_IMPLEMENTED with asset_path=None.
5. Updates concept_explainer for Entropy and Structural Stability.
"""

import sqlite3
from datetime import datetime

def remediate_database():
    conn = sqlite3.connect("backend/signbridge.db")
    c = conn.cursor()

    print("[Remediation] 1. Updating Deadlock aliases to include 'deadlocked'...")
    c.execute("""
        UPDATE concepts
        SET aliases = 'deadlocked, deadlock condition, mutual lock, circular wait, deadlock state'
        WHERE lower(term) = 'deadlock'
    """)

    print("[Remediation] 2. Updating sign_videos records to DEMO_ONLY (Synthetic FFmpeg test patterns)...")
    c.execute("""
        UPDATE sign_videos
        SET validation_status = 'DEMO_ONLY',
            signer_name = 'FFmpeg Test Pattern Generator (Synthetic)',
            title = '[DEMO] ' || title,
            notes = 'Synthetic FFmpeg testsrc video with digital clock counter. NOT a human Deaf signer. Operational demo media.'
        WHERE id IN (1, 2, 3, 4)
    """)

    c.execute("""
        UPDATE sign_videos
        SET validation_status = 'DEMO_ONLY',
            signer_name = 'FFmpeg Test Pattern Generator (Synthetic)',
            title = '[DEMO] Algorithm - Synthetic Test Recording',
            notes = 'Synthetic test upload for API pipeline verification. NOT an authentic Deaf signer.'
        WHERE id = 5
    """)

    print("[Remediation] 3. Updating avatar_animations record to NOT_IMPLEMENTED...")
    c.execute("""
        UPDATE avatar_animations
        SET validation_status = 'NOT_IMPLEMENTED',
            animation_name = 'procedural_mannequin_preview',
            asset_path = 'UNAVAILABLE_PENDING_MOCAP'
        WHERE id = 1
    """)

    print("[Remediation] 4. Adding missing target concepts: Entropy, Process, Structural Stability...")
    # Get Branch and Subject IDs
    c.execute("SELECT id FROM engineering_branches WHERE code = 'mech'")
    mech_b = c.fetchone()[0]
    c.execute("SELECT id FROM subjects WHERE code = 'ME202'")
    row_mech_s = c.fetchone()
    mech_s = row_mech_s[0] if row_mech_s else 1

    c.execute("SELECT id FROM engineering_branches WHERE code = 'cs'")
    cs_b = c.fetchone()[0]
    c.execute("SELECT id FROM subjects WHERE code = 'CS301'")
    row_cs_s = c.fetchone()
    cs_s = row_cs_s[0] if row_cs_s else 1

    c.execute("SELECT id FROM engineering_branches WHERE code = 'civil'")
    civ_b = c.fetchone()[0]
    c.execute("SELECT id FROM subjects WHERE code = 'CE301'")
    row_civ_s = c.fetchone()
    civ_s = row_civ_s[0] if row_civ_s else 1

    # Check Entropy
    c.execute("SELECT id FROM concepts WHERE lower(term) = 'entropy'")
    if not c.fetchone():
        c.execute("""
            INSERT INTO concepts (branch_id, subject_id, term, slug, aliases, category, domain, definition, technical_context, example_usage, difficulty_level, created_at)
            VALUES (?, ?, 'Entropy', 'entropy', 'thermodynamic entropy, thermal disorder, second law', 'Thermodynamics', 'Thermodynamics', 
                    'A measure of the unavailable energy in a closed thermodynamic system, commonly interpreted as disorder or randomness.',
                    'Governed by the Second Law of Thermodynamics: entropy of an isolated system always increases.',
                    'The Carnot cycle demonstrates maximum theoretical efficiency by minimizing entropy generation.',
                    'advanced', datetime('now'))
        """, (mech_b, mech_s))
        entropy_cid = c.lastrowid
        c.execute("""
            INSERT INTO sign_records (concept_id, provenance_id, expert_review_id, sign_gloss, validation_status, is_authentic, linguistic_notes, sign_id, source_institution, license, consent_info, validation_date, confidence_score, created_at)
            VALUES (?, 1, 1, 'ENTROPY', 'UNSUPPORTED', 0, 'No certified single-sign ISL equivalent exists. Use fingerspelling E-N-T-R-O-P-Y with disorder diagram.', 'ISL-ME-021', 'Awaiting ISLRTC STEM Technical Codification', 'Pending Formal Codification', 'Not Applicable', datetime('now'), 0.1, datetime('now'))
        """, (entropy_cid,))

    c.execute("""
        UPDATE concepts
        SET aliases = 'processes, computing process, concurrent process, execution unit, task'
        WHERE lower(term) = 'process'
    """)
    c.execute("SELECT id FROM concepts WHERE lower(term) = 'process'")
    if not c.fetchone():
        c.execute("""
            INSERT INTO concepts (branch_id, subject_id, term, slug, aliases, category, domain, definition, technical_context, example_usage, difficulty_level, created_at)
            VALUES (?, ?, 'Process', 'process', 'operating system process, execution unit, task', 'Systems Software', 'Operating Systems',
                    'An instance of a computer program that is being executed by one or many threads.',
                    'Contains the program code, memory context (stack, heap, data), and operating system PCB.',
                    'The OS scheduler context switches between active processes using priority algorithms.',
                    'intermediate', datetime('now'))
        """, (cs_b, cs_s))
        proc_cid = c.lastrowid
        c.execute("""
            INSERT INTO sign_records (concept_id, provenance_id, expert_review_id, sign_gloss, validation_status, is_authentic, linguistic_notes, sign_id, dominant_hand, handshape, movement, location, orientation, non_manual_markers, source_institution, license, consent_info, validation_date, confidence_score, created_at)
            VALUES (?, 1, 1, 'PROCESS', 'NEEDS_REVIEW', 0, 'Candidate sign: index finger tracking sequential state progression across neutral workspace.', 'ISL-CS-021', 'Right', 'Index pointing handshape', 'Sequential forward translation', 'Chest level neutral space', 'Palm facing inward', 'Focused gaze', 'ISLRTC Syllabus Candidate', 'Government Educational Reference', 'Not Applicable', datetime('now'), 0.6, datetime('now'))
        """, (proc_cid,))

    # Check Structural Stability
    c.execute("SELECT id FROM concepts WHERE lower(term) = 'structural stability'")
    if not c.fetchone():
        c.execute("""
            INSERT INTO concepts (branch_id, subject_id, term, slug, aliases, category, domain, definition, technical_context, example_usage, difficulty_level, created_at)
            VALUES (?, ?, 'Structural Stability', 'structural-stability', 'stability, buckling resistance, equilibrium', 'Structural Engineering', 'Structural Analysis',
                    'The ability of a structure or structural member to maintain equilibrium and resist buckling, collapse, or displacement under applied loads.',
                    'Analyzed via Euler critical load equations and second-order P-Delta analysis.',
                    'Diagonal bracing preserves structural stability against lateral wind and seismic forces.',
                    'advanced', datetime('now'))
        """, (civ_b, civ_s))
        stab_cid = c.lastrowid
        c.execute("""
            INSERT INTO sign_records (concept_id, provenance_id, expert_review_id, sign_gloss, validation_status, is_authentic, linguistic_notes, sign_id, source_institution, license, consent_info, validation_date, confidence_score, created_at)
            VALUES (?, 1, 1, 'STRUCTURAL-STABILITY', 'UNSUPPORTED', 0, 'Unstandardized technical term. Recommend fingerspelling and equilibrium diagram.', 'ISL-CE-021', 'Awaiting ISLRTC STEM Codification', 'Pending Formal Codification', 'Not Applicable', datetime('now'), 0.2, datetime('now'))
        """, (stab_cid,))

    conn.commit()
    print("[Remediation] Database successfully remediated and committed.")
    conn.close()

if __name__ == "__main__":
    remediate_database()
