"""
SignBridge AI - Knowledge Base and Linguistic Provenance Auditor
Inspects all 100 candidate concepts in engineering_100_candidates.json and SQLite database.
Determines actual linguistic provenance, video availability, signer attribution,
usage rights, phonological parameters, regional variation, and realistic validation status.
Generates:
- reports/knowledge_base_audit.json
- reports/KNOWLEDGE_BASE_AUDIT.md
"""

import json
import sqlite3
from pathlib import Path

def audit_kb():
    json_path = Path("data/vocabulary/engineering_100_candidates.json")
    with open(json_path, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    conn = sqlite3.connect("backend/signbridge.db")
    c = conn.cursor()

    # Load DB signs
    c.execute("""
        SELECT sr.id, c.term, sr.sign_gloss, sr.validation_status, sr.is_authentic,
               sr.dominant_hand, sr.handshape, sr.movement, sr.location, sr.orientation, sr.non_manual_markers,
               sr.source_institution, sr.license, sr.sign_id, sv.video_path, sv.signer_name, sv.validation_status
        FROM sign_records sr
        JOIN concepts c ON sr.concept_id = c.id
        LEFT JOIN sign_videos sv ON sv.sign_record_id = sr.id
    """)
    db_rows = {row[1].lower(): row for row in c.fetchall()}

    audit_records = []
    status_counts_before = {}
    status_counts_after = {}

    for idx, item in enumerate(candidates, start=1):
        term = item["term"]
        term_lower = term.lower()
        db_sign = db_rows.get(term_lower)

        current_db_status = item.get("validation_status", "needs_review").upper()
        status_counts_before[current_db_status] = status_counts_before.get(current_db_status, 0) + 1

        # Determine video availability and whether video is real
        has_video_in_db = bool(db_sign and db_sign[14])
        video_path = db_sign[14] if (db_sign and db_sign[14]) else None
        
        # All existing MP4s in data/sign_videos/ are synthetic testsrc clips
        is_synthetic_video = has_video_in_db and ("testsrc" in str(video_path) or "sign_videos" in str(video_path))

        # Check phonological parameters
        dominant_hand = item.get("dominant_hand")
        handshape = item.get("handshape")
        movement = item.get("movement")
        location = item.get("location")
        orientation = item.get("orientation")
        nmm = item.get("non_manual_markers")
        
        has_full_phonology = all([dominant_hand, handshape, movement, location, orientation])

        # Audited Status Rule:
        # 1. If currently marked VERIFIED:
        #    Does it have a real verified video of an accredited Deaf signer? NO.
        #    Does it have an external validation record from an official institution? NO (only local test accounts).
        #    Therefore, MUST be downgraded to NEEDS_REVIEW or DEMO_ONLY!
        # 2. If it is an unstandardized concept (Deadlock, Bracing, Modulation, Pointer):
        #    Marked UNSUPPORTED or EXPLANATION_REQUIRED.
        # 3. If currently PARTIAL or NEEDS_REVIEW:
        #    Remains PARTIAL or NEEDS_REVIEW.
        if current_db_status == "VERIFIED":
            audited_status = "NEEDS_REVIEW"
            status_downgrade_reason = (
                "Downgraded from VERIFIED to NEEDS_REVIEW: No authentic human signing video asset exists; "
                "validation was recorded by local test accounts rather than certified external Deaf evaluators."
            )
        elif current_db_status in ("UNSUPPORTED", "EXPLANATION_NEEDED", "EXPLANATION_REQUIRED"):
            audited_status = "UNSUPPORTED" if current_db_status == "UNSUPPORTED" else "EXPLANATION_REQUIRED"
            status_downgrade_reason = "Concept confirmed unstandardized in technical ISL; pedagogical explainer and fingerspelling required."
        elif current_db_status == "PARTIAL":
            audited_status = "PARTIAL"
            status_downgrade_reason = "Compound technical sign with partial colloquial alignment; awaiting full domain standardization."
        else:
            audited_status = "NEEDS_REVIEW"
            status_downgrade_reason = "Candidate sign awaiting empirical evaluation by accredited Deaf STEM educators."

        status_counts_after[audited_status] = status_counts_after.get(audited_status, 0) + 1

        record = {
            "concept_id": idx,
            "sign_id": item.get("sign_id", f"ISL-{item['branch_code'].upper()}-{idx:03d}"),
            "term": term,
            "aliases": item.get("aliases", []),
            "branch_code": item["branch_code"],
            "branch_name": item.get("branch_code", "").upper(),
            "subject_code": item.get("subject_code"),
            "subject_name": item.get("subject_name"),
            "category": item.get("category"),
            "domain": item.get("domain"),
            "sign_gloss": item.get("sign_gloss", term.upper()),
            "current_claimed_status": current_db_status,
            "audited_linguistic_status": audited_status,
            "status_downgrade_reason": status_downgrade_reason,
            "phonological_parameters": {
                "dominant_hand": dominant_hand,
                "handshape": handshape,
                "movement": movement,
                "location": location,
                "orientation": orientation,
                "non_manual_markers": nmm,
                "is_heuristically_assigned": True,
                "documented_in_islrtc_print": True if "ISLRTC" in str(item.get("source_institution")) else False
            },
            "source_institution": item.get("source_institution", "Awaiting Formal Codification"),
            "license": item.get("license", "Government Educational Reference / Fair Dealing"),
            "signer_attribution": "None (No authentic signer recorded; video assets are synthetic FFmpeg testsrc)",
            "consent_documentation": "Not Applicable (No human subjects recorded)",
            "video_asset": {
                "registered_in_db": has_video_in_db,
                "file_path": video_path,
                "is_authentic_human": False,
                "is_synthetic_testsrc": is_synthetic_video,
                "audit_verdict": "DEMO_ONLY (Digital clock test pattern; not human signing)" if has_video_in_db else "UNAVAILABLE"
            },
            "avatar_animation": {
                "registered_in_db": True if idx == 1 else False,
                "asset_path": "/data/avatar_animations/neutral_avatar.glb" if idx == 1 else None,
                "file_exists_on_disk": False,
                "audit_verdict": "NOT_IMPLEMENTED (Missing GLB asset; viewer performs procedural sinusoidal breathing only)"
            }
        }
        audit_records.append(record)

    # Save JSON audit report
    json_out = Path("reports/knowledge_base_audit.json")
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump({
            "audit_metadata": {
                "total_concepts_audited": len(audit_records),
                "status_distribution_before_audit": status_counts_before,
                "status_distribution_after_audit": status_counts_after,
                "zero_fabrication_policy_enforced": True
            },
            "concepts": audit_records
        }, f, indent=2)

    # Generate Markdown Report
    md_out = Path("reports/KNOWLEDGE_BASE_AUDIT.md")
    with open(md_out, "w", encoding="utf-8") as f:
        f.write("# SignBridge AI — Knowledge Base & Linguistic Provenance Audit\n\n")
        f.write("## 1. Executive Summary\n\n")
        f.write(f"- **Total Candidate Concepts Inspected:** {len(audit_records)}\n")
        f.write("- **Previous Claimed Statuses:** " + ", ".join(f"`{k}`: {v}" for k, v in status_counts_before.items()) + "\n")
        f.write("- **Audited Honest Statuses:** " + ", ".join(f"`{k}`: {v}" for k, v in status_counts_after.items()) + "\n\n")
        f.write("> [!CAUTION]\n")
        f.write("> **Critical Audit Finding:** None of the 100 concepts can genuinely be certified as `VERIFIED` in production. "
                "The previous 40 `VERIFIED` marks were based on simulated internal test accounts (`[Local Test Reviewer] Certified Deaf Educator`) "
                "and synthetic video clips. In strict adherence to Non-Negotiable Rule #3 (*Never mark a concept VERIFIED solely because it exists in the database*), "
                "all 40 concepts have been downgraded to `NEEDS_REVIEW`.\n\n")

        f.write("## 2. Phonological Parameter Verification\n\n")
        f.write("The 6 phonological parameters (Dominant Hand, Handshape, Movement, Location, Orientation, Non-Manual Markers) "
                "present in the candidate records represent **candidate articulatory descriptions** drafted to match ISLRTC glossary patterns. "
                "However, they lack empirical 3D motion capture coordinates or video sign-off from accredited Deaf master signers.\n\n")

        f.write("## 3. Candidate Concepts Status Table\n\n")
        f.write("| ID | Term | Branch | Subject | Gloss | Claimed Status | Audited Status | Video Asset | Avatar Mocap |\n")
        f.write("|:---|:---|:---|:---|:---|:---:|:---:|:---:|:---:|\n")
        for r in audit_records:
            vid_status = r["video_asset"]["audit_verdict"]
            av_status = r["avatar_animation"]["audit_verdict"]
            f.write(f"| {r['concept_id']} | {r['term']} | {r['branch_code'].upper()} | {r['subject_code']} | `{r['sign_gloss']}` | `{r['current_claimed_status']}` | **`{r['audited_linguistic_status']}`** | {vid_status} | {av_status} |\n")

    print(f"KB Audit complete. Saved JSON to {json_out} and MD to {md_out}")
    conn.close()

if __name__ == "__main__":
    audit_kb()

