import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.database.database import SessionLocal
from backend.app.models.entities import (
    EngineeringBranch, Subject, Concept, DatasetProvenance,
    ExpertReview, SignRecord, SignVariant, SignVideo, AvatarAnimation,
    GrammarAnnotation, TranslationHistory
)

db = SessionLocal()

print("=" * 60)
print("1. DATABASE AUDIT: ENGINEERING BRANCHES")
print("=" * 60)
branches = db.query(EngineeringBranch).all()
print(f"Total Branches: {len(branches)}")
for b in branches:
    print(f"  [{b.code}] {b.name}: {len(b.subjects)} subjects, {len(b.concepts)} concepts")

print("\n" + "=" * 60)
print("2. DATABASE AUDIT: SUBJECTS")
print("=" * 60)
subjects = db.query(Subject).all()
print(f"Total Subjects: {len(subjects)}")
for s in subjects:
    print(f"  [{s.code}] {s.name} (Branch: {s.branch.name if s.branch else 'None'}) - {len(s.concepts)} concepts")

print("\n" + "=" * 60)
print("3. DATABASE AUDIT: TECHNICAL CONCEPTS & STATUSES")
print("=" * 60)
concepts = db.query(Concept).all()
print(f"Total Concepts: {len(concepts)}")

status_counts = {}
for c in concepts:
    sign = c.signs[0] if c.signs else None
    status = sign.validation_status.value if sign else "NONE"
    status_counts[status] = status_counts.get(status, 0) + 1
    has_vid = (len(sign.videos) > 0 and sign.validation_status.value == "verified") if sign else False
    vid_path = sign.videos[0].video_path if (sign and sign.videos) else "None"
    print(f"  [{c.branch.code if c.branch else '?'}] {c.term:20} | Status: {status:18} | Video: {str(has_vid):5} | Path: {vid_path}")

print("\nStatus Distribution:")
for st, cnt in status_counts.items():
    print(f"  - {st}: {cnt}")

print("\n" + "=" * 60)
print("4. DATABASE AUDIT: DATASET PROVENANCE")
print("=" * 60)
provenances = db.query(DatasetProvenance).all()
print(f"Total Provenances: {len(provenances)}")
for p in provenances:
    print(f"  - Name: {p.name}")
    print(f"    Org: {p.organization}")
    print(f"    License: {p.license}")
    print(f"    URL: {p.source_url}")
    print(f"    Peer Reviewed: {p.peer_reviewed}")

print("\n" + "=" * 60)
print("5. DATABASE AUDIT: EXPERT REVIEWERS")
print("=" * 60)
reviewers = db.query(ExpertReview).all()
print(f"Total Reviewers: {len(reviewers)}")
for r in reviewers:
    print(f"  - Name: {r.reviewer_name}")
    print(f"    Role: {r.reviewer_role}")
    print(f"    Affiliation: {r.affiliation}")
    print(f"    Status: {r.status.value}")
    print(f"    Accuracy Rating: {r.sign_accuracy_rating}")

print("\n" + "=" * 60)
print("6. DATABASE AUDIT: SIGN VIDEOS")
print("=" * 60)
videos = db.query(SignVideo).all()
print(f"Total Videos in DB: {len(videos)}")
for v in videos:
    print(f"  - Title: {v.title}")
    print(f"    Path: {v.video_path}")
    print(f"    Duration: {v.duration_seconds}s")
    print(f"    Signer: {v.signer_name}")
    print(f"    Status: {v.validation_status.value}")
    print(f"    Attribution: {v.source_attribution}")

print("\n" + "=" * 60)
print("7. DATABASE AUDIT: AVATAR ANIMATIONS")
print("=" * 60)
animations = db.query(AvatarAnimation).all()
print(f"Total Avatar Animations in DB: {len(animations)}")
for a in animations:
    print(f"  - Name: {a.animation_name}")
    print(f"    Asset: {a.asset_path}")
    print(f"    Neutral Preview: {a.is_neutral_preview}")
    print(f"    Rig: {a.rig_standard}")

print("\n" + "=" * 60)
print("8. DATABASE AUDIT: TRANSLATION HISTORY")
print("=" * 60)
history = db.query(TranslationHistory).all()
print(f"Total History Records: {len(history)}")

db.close()

