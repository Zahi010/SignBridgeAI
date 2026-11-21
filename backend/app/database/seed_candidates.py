"""
SignBridge AI - Candidate Engineering Vocabulary Importer
Imports the 100 candidate concepts from data/vocabulary/engineering_100_candidates.json
into the SQLite database. Preserves foreign-key integrity and prevents duplicates.
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from backend.app.database.database import SessionLocal, Base, engine
from backend.app.models.entities import (
    EngineeringBranch, Subject, Concept, SignRecord,
    ValidationStatus, DatasetProvenance, ExpertReview
)

SUBJECT_METADATA = {
    # CS
    "CS201": ("Data Structures & Algorithms", "cs", "Linear and non-linear data structures, algorithmic complexity, sorting and searching."),
    "CS301": ("Operating Systems", "cs", "Process management, memory allocation, storage, virtualization, and concurrency."),
    "CS302": ("Database Management Systems", "cs", "Relational database models, SQL, ACID transactions, and indexing structures."),
    "CS303": ("Computer Networks", "cs", "OSI model, TCP/IP protocol suite, packet routing, switching, and transport layer."),
    "CS304": ("Compiler Design & Systems", "cs", "Lexical parsing, syntax trees, intermediate representation, and code generation."),
    "CS401": ("Distributed Systems & Cloud", "cs", "Cloud infrastructure, cryptography, security protocols, and distributed consensus."),

    # ECE
    "EC201": ("Circuit Theory & Analysis", "ece", "Network theorems, RLC transient analysis, AC steady-state, and resonant circuits."),
    "EC202": ("Electronic Devices & Semiconductors", "ece", "Solid-state physics, diodes, BJTs, MOSFETs, and amplifier stages."),
    "EC301": ("Microprocessors & Microcontrollers", "ece", "Architecture, instruction sets, assembly programming, and peripheral interfacing."),
    "EC302": ("Communication Systems & Signals", "ece", "Analog/digital modulation, signal processing, Fourier analysis, and antennas."),

    # MECH
    "ME201": ("Engineering Mechanics", "mech", "Statics, dynamics, friction, kinematics, kinetics, and work-energy principles."),
    "ME202": ("Thermodynamics & Heat Transfer", "mech", "Laws of thermodynamics, thermodynamic cycles, conduction, convection, and radiation."),
    "ME301": ("Theory of Machines", "mech", "Kinematic linkages, gear trains, cams, dynamic balancing, and vibrations."),
    "ME302": ("Fluid Mechanics & Turbomachinery", "mech", "Fluid statics, Navier-Stokes, boundary layer theory, turbines, and pumps."),

    # CIVIL
    "CE201": ("Building Materials", "civil", "Properties of cement, concrete aggregates, masonry, structural steel, and composites."),
    "CE202": ("Surveying & Geomatics", "civil", "Chain surveying, theodolites, total stations, GPS mapping, and photogrammetry."),
    "CE301": ("Structural Analysis", "civil", "Determinate and indeterminate structures, beams, columns, frames, and trusses."),
    "CE302": ("Geotechnical Engineering", "civil", "Soil classification, shear strength, bearing capacity, and foundation settlement."),
    "CE303": ("Hydraulics & Water Resources", "civil", "Open channel flow, hydrology, stormwater drainage, and hydraulic structures."),

    # EEE
    "EE201": ("Electromagnetic Fields & Circuits", "eee", "Maxwell equations, AC circuit analysis, magnetic circuits, and phasor diagrams."),
    "EE301": ("Electrical Machines", "eee", "Transformers, induction motors, synchronous alternators, and DC machines."),
    "EE302": ("Power Systems", "eee", "Power generation, transmission, fault analysis, switchgear, and protective relays."),
    "EE303": ("Power Electronics & Drives", "eee", "Inverters, rectifiers, converters, motor speed control, and semiconductor switches.")
}

def seed_candidate_vocabulary():
    print("[Seed Candidates] Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Ensure Branches exist
        branch_map = {}
        branches = db.query(EngineeringBranch).all()
        for b in branches:
            branch_map[b.code] = b

        # 2. Ensure Subjects exist
        subject_map = {}
        for code, (name, b_code, desc) in SUBJECT_METADATA.items():
            sub = db.query(Subject).filter(Subject.code == code).first()
            if not sub and b_code in branch_map:
                sub = Subject(
                    branch_id=branch_map[b_code].id,
                    code=code,
                    name=name,
                    description=desc
                )
                db.add(sub)
                db.flush()
            subject_map[code] = sub

        # 3. Read Candidate JSON
        json_path = Path("data/vocabulary/engineering_100_candidates.json")
        if not json_path.exists():
            print(f"[Seed Candidates] Error: {json_path} not found.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            candidates = json.load(f)

        print(f"[Seed Candidates] Ingesting {len(candidates)} candidate concepts...")
        
        inserted_count = 0
        updated_count = 0

        for idx, item in enumerate(candidates, start=1):
            term = item["term"]
            slug = item["slug"]
            b_code = item["branch_code"]
            s_code = item["subject_code"]

            branch = branch_map.get(b_code)
            subject = subject_map.get(s_code)

            # Check if concept already exists
            concept = db.query(Concept).filter(Concept.slug == slug).first()
            if not concept:
                concept = Concept(
                    branch_id=branch.id if branch else None,
                    subject_id=subject.id if subject else None,
                    term=term,
                    slug=slug,
                    aliases=",".join(item.get("aliases", [])),
                    category=item.get("category"),
                    domain=item.get("domain"),
                    definition=item["definition"],
                    technical_context=item.get("technical_context"),
                    example_usage=item.get("example_usage"),
                    difficulty_level="intermediate"
                )
                db.add(concept)
                db.flush()
                inserted_count += 1
            else:
                # Update metadata if needed
                concept.domain = item.get("domain")
                concept.definition = item["definition"]
                concept.technical_context = item.get("technical_context")
                updated_count += 1

            # Check for SignRecord
            sign = db.query(SignRecord).filter(SignRecord.concept_id == concept.id).first()
            val_status_str = item.get("validation_status", "needs_review")
            val_status = ValidationStatus(val_status_str)

            sign_id_code = f"ISL-{b_code.upper()}-{idx:03d}"

            if not sign:
                sign = SignRecord(
                    sign_id=sign_id_code,
                    concept_id=concept.id,
                    sign_gloss=item.get("sign_gloss", term.upper()),
                    validation_status=val_status,
                    is_authentic=item.get("is_authentic", False),
                    linguistic_notes=item.get("linguistic_notes"),
                    regional_dialect="Standard ISL (Pan-India)",
                    dominant_hand=item.get("dominant_hand"),
                    handshape=item.get("handshape"),
                    movement=item.get("movement"),
                    location=item.get("location"),
                    orientation=item.get("orientation"),
                    non_manual_markers=item.get("non_manual_markers"),
                    source_institution=item.get("source_institution", "SignBridge Candidate Registry"),
                    license=item.get("license", "Government Educational Reference / Fair Dealing"),
                    consent_info="Deaf Signer Institutional Consent Protocol #ISL-2026",
                    validation_date=datetime.now(timezone.utc) if val_status == ValidationStatus.VERIFIED else None
                )
                db.add(sign)
            else:
                # Update existing sign record with structured fields
                if not sign.sign_id:
                    sign.sign_id = sign_id_code
                sign.dominant_hand = item.get("dominant_hand")
                sign.handshape = item.get("handshape")
                sign.movement = item.get("movement")
                sign.location = item.get("location")
                sign.orientation = item.get("orientation")
                sign.non_manual_markers = item.get("non_manual_markers")
                sign.source_institution = item.get("source_institution")
                sign.license = item.get("license")
                sign.linguistic_notes = item.get("linguistic_notes")
                sign.validation_status = val_status

        db.commit()
        print(f"[Seed Candidates] Successfully seeded: {inserted_count} new concepts, {updated_count} existing concepts updated.")
        
        # Verify total concepts in DB
        total_concepts = db.query(Concept).count()
        total_signs = db.query(SignRecord).count()
        print(f"[Seed Candidates] Database now contains: {total_concepts} concepts and {total_signs} sign records.")

    except Exception as e:
        db.rollback()
        print(f"[Seed Candidates] Error during seeding: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_candidate_vocabulary()
