"""
SignBridge AI - Engineering Translation Planner
Constructs an explicit, transparent, multi-concept translation plan mapping
every element of the Structured Intermediate Representation (IR) to authentic lexical signs,
multi-step pedagogical explanations, or fingerspelling sequences.
Strictly enforces the Zero-Fabrication Policy.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.schemas.intermediate_representation import (
    IntermediateRepresentation, TranslationPlanIR, TranslationUnitIR,
    SemanticConceptIR, ConceptRelationshipIR
)
from backend.app.services.explanation_service import EducationalExplanationService
from backend.app.models.entities import ValidationStatus, SignVideo, SignRecord

class EngineeringTranslationPlanner:
    """
    Plans multimodal translation sequences based on linguistic, conceptual, and asset availability.
    """

    @staticmethod
    def construct_plan(ir: IntermediateRepresentation, db: Session) -> TranslationPlanIR:
        units: List[TranslationUnitIR] = []
        unit_counter = 1
        lexical_count = 0
        explanation_count = 0
        unsupported_count = 0

        # 1. Temporal Marker (Time-First Principle in ISL)
        if ir.temporal.has_temporal and ir.temporal.marker_token:
            units.append(TranslationUnitIR(
                unit_id=unit_counter,
                source_segment=ir.temporal.marker_token,
                strategy="LEXICAL_SIGN_DIRECT",
                assigned_gloss=f"{ir.temporal.marker_token.upper()} [TIME-MARKER]",
                rationale="In ISL syntax, temporal markers establish the time frame at the very beginning of the utterance before topic.",
                fingerspelling_sequence=[c.upper() for c in ir.temporal.marker_token if c.isalnum()]
            ))
            unit_counter += 1

        # 2. Technical Concepts (Topic-Comment Principle in ISL)
        for concept in ir.detected_concepts:
            term = concept.term
            gloss = concept.canonical_gloss

            # Query video availability
            video = None
            if concept.id:
                sr = db.query(SignRecord).filter(SignRecord.concept_id == concept.id).first()
                if sr:
                    video = db.query(SignVideo).filter(SignVideo.sign_record_id == sr.id).first()

            has_valid_video = (
                video is not None and
                concept.validation_status in (ValidationStatus.VERIFIED, ValidationStatus.PARTIAL)
            )

            if has_valid_video:
                lexical_count += 1
                units.append(TranslationUnitIR(
                    unit_id=unit_counter,
                    source_segment=term,
                    strategy="LEXICAL_SIGN_DIRECT",
                    assigned_gloss=gloss,
                    video_resource_ref=video.video_path if video else None,
                    rationale=f"Authentic ISL sign video available ({concept.validation_status.value.upper()}). Sourced from {video.source_attribution if video else 'ISLRTC'}.",
                    fingerspelling_sequence=[c.upper() for c in term if c.isalnum()]
                ))
            elif concept.validation_status in (ValidationStatus.EXPLANATION_REQUIRED, ValidationStatus.EXPLANATION_NEEDED):
                explanation_count += 1
                pedagogical_payload = EducationalExplanationService.get_explanation(term)
                if not pedagogical_payload:
                    pedagogical_payload = EducationalExplanationService.generate_generic_pedagogical_plan(
                        term, category=concept.category, definition=concept.definition
                    )
                units.append(TranslationUnitIR(
                    unit_id=unit_counter,
                    source_segment=term,
                    strategy="PEDAGOGICAL_EXPLANATION",
                    assigned_gloss=f"{gloss} [EXPLANATION-SEQUENCE]",
                    pedagogical_ref=pedagogical_payload,
                    fingerspelling_sequence=pedagogical_payload.get("fingerspelling_sequence", [c.upper() for c in term if c.isalnum()]),
                    rationale="Abstract or uncodified concept mapped to 4-step pedagogical classifier sequence and spatial demonstration."
                ))
            else: # UNSUPPORTED or NEEDS_REVIEW without video
                unsupported_count += 1
                fingerspell_letters = [c.upper() for c in term if c.isalnum()]
                units.append(TranslationUnitIR(
                    unit_id=unit_counter,
                    source_segment=term,
                    strategy="UNSUPPORTED_FINGERSPELLING",
                    assigned_gloss=f"{gloss} [FINGERSPELLING-ONLY]",
                    fingerspelling_sequence=fingerspell_letters,
                    rationale="No authentic sign video or codified standard available in ISL. Enforcing Zero-Fabrication Policy via two-handed fingerspelling."
                ))
            unit_counter += 1

        # 3. Interacting Concept Relationships (Spatial Loci & Directional Predicates)
        for rel in ir.concept_relationships:
            units.append(TranslationUnitIR(
                unit_id=unit_counter,
                source_segment=f"{rel.source_concept} {rel.relation_type} {rel.target_concept}",
                strategy="RELATIONAL_SPATIAL_INDEX",
                assigned_gloss=f"[{rel.source_concept.upper()} (LOCUS-A)] --> [{rel.relation_type.upper().replace('_', '-')}] --> [{rel.target_concept.upper()} (LOCUS-B)]",
                rationale=f"Relational predicate in ISL spatial signing space: {rel.description}",
                fingerspelling_sequence=None
            ))
            unit_counter += 1

        # 4. Sentence-Final Negation (with headshake)
        if ir.negation.is_negated:
            units.append(TranslationUnitIR(
                unit_id=unit_counter,
                source_segment=ir.negation.marker_token or "not",
                strategy="LEXICAL_SIGN_DIRECT",
                assigned_gloss="NOT [NMM: Headshake]",
                rationale="ISL places negation at the end of the verbal phrase, obligatorily co-occurring with negative headshake.",
                fingerspelling_sequence=["N", "O", "T"]
            ))
            unit_counter += 1

        # 5. Sentence-Final Interrogative / WH-Question (with furrowed brow)
        if ir.interrogative.is_interrogative:
            wh_word = ir.interrogative.wh_word or "WHAT"
            units.append(TranslationUnitIR(
                unit_id=unit_counter,
                source_segment=wh_word,
                strategy="LEXICAL_SIGN_DIRECT",
                assigned_gloss=f"{wh_word.upper()} [NMM: Furrowed Brow]",
                rationale="ISL positions interrogatives at sentence-final position, synchronized with furrowed eyebrows.",
                fingerspelling_sequence=[c.upper() for c in wh_word if c.isalnum()]
            ))
            unit_counter += 1

        summary = (
            f"Translation Plan: {len(units)} unit(s) total | "
            f"{lexical_count} lexical sign(s), {explanation_count} pedagogical explanation(s), "
            f"{unsupported_count} unsupported fingerspelling unit(s)."
        )

        return TranslationPlanIR(
            translation_units=units,
            total_units=len(units),
            lexical_count=lexical_count,
            explanation_count=explanation_count,
            unsupported_count=unsupported_count,
            overall_strategy_summary=summary
        )

