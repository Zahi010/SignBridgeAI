"""
SignBridge AI - Validation Lifecycle, Disagreement Detection & Adjudication Service (Phase 5).
"""

import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from backend.app.models.entities import SignRecord, Concept, ValidationStatus
from backend.app.models.validation_models import (
    Reviewer,
    ReviewerRole,
    ReviewerVerificationStatus,
    ValidationTask,
    ValidationTaskStatus,
    SignEvaluation,
    EvaluationCriterionRating,
    ReviewerAnnotation,
    EvaluationDisagreement,
    ValidationDecision,
    AdjudicationDecisionEnum,
    RubricCriterionRating,
    ValidationAuditLog
)

logger = logging.getLogger("signbridge.validation_service")

# 12 Core Linguistic Rubric Criteria
RUBRIC_CRITERIA_LIST = [
    "handshape",
    "orientation",
    "location",
    "movement",
    "coordination",
    "facial_nmm",
    "grammatical_correctness",
    "contextual_meaning",
    "naturalness",
    "comprehensibility",
    "regional_variation",
    "ambiguity"
]


class ValidationWorkflowService:
    def __init__(self, db: Session):
        self.db = db

    def log_action(self, actor_id: Optional[int], actor_username: str, action: str, target_type: str, target_id: str, details: Dict[str, Any]):
        """Append an immutable entry to ValidationAuditLog."""
        entry = ValidationAuditLog(
            actor_id=actor_id,
            actor_username=actor_username,
            action=action,
            target_type=target_type,
            target_id=str(target_id),
            details_json=json.dumps(details),
            timestamp=datetime.now(timezone.utc)
        )
        self.db.add(entry)

    def submit_evaluation(
        self,
        task_id: int,
        reviewer: Reviewer,
        is_draft: bool,
        overall_recommendation: str,
        general_feedback: Optional[str],
        suggested_dialect: Optional[str],
        criteria_ratings: List[Dict[str, Any]],
        annotations: List[Dict[str, Any]]
    ) -> SignEvaluation:
        """
        Submits or updates a structured evaluation for a validation task.
        Checks for critical linguistic errors and triggers disagreement detection.
        """
        task = self.db.query(ValidationTask).filter(ValidationTask.id == task_id).first()
        if not task:
            raise ValueError(f"ValidationTask {task_id} not found.")

        # Check existing evaluation from this reviewer
        evaluation = (
            self.db.query(SignEvaluation)
            .filter(SignEvaluation.task_id == task_id, SignEvaluation.reviewer_id == reviewer.id)
            .first()
        )

        if not evaluation:
            evaluation = SignEvaluation(
                task_id=task_id,
                reviewer_id=reviewer.id,
                sign_record_id=task.sign_record_id,
                is_draft=is_draft,
                overall_recommendation=overall_recommendation,
                general_feedback=general_feedback,
                suggested_dialect=suggested_dialect,
                submitted_at=datetime.now(timezone.utc)
            )
            self.db.add(evaluation)
            self.db.flush()
        else:
            evaluation.is_draft = is_draft
            evaluation.overall_recommendation = overall_recommendation
            evaluation.general_feedback = general_feedback
            evaluation.suggested_dialect = suggested_dialect
            evaluation.submitted_at = datetime.now(timezone.utc)
            # Clear old criteria ratings to overwrite with updated submission
            self.db.query(EvaluationCriterionRating).filter(EvaluationCriterionRating.evaluation_id == evaluation.id).delete()

        # Add criteria ratings
        has_critical_error = False
        for c in criteria_ratings:
            c_name = c.get("criterion_name")
            rating_str = c.get("rating", "pass").lower()
            try:
                rating_enum = RubricCriterionRating(rating_str)
            except ValueError:
                rating_enum = RubricCriterionRating.PASS

            is_crit = c.get("is_critical_error", False) or rating_enum in [RubricCriterionRating.INCORRECT, RubricCriterionRating.MAJOR_ISSUE]
            if is_crit and rating_enum in [RubricCriterionRating.INCORRECT, RubricCriterionRating.MAJOR_ISSUE]:
                has_critical_error = True

            cr = EvaluationCriterionRating(
                evaluation_id=evaluation.id,
                criterion_name=c_name,
                rating=rating_enum,
                notes=c.get("notes"),
                is_critical_error=is_crit
            )
            self.db.add(cr)

        # Critical error rule: if a major/incorrect error exists, recommendation cannot be 'accept'
        if has_critical_error and overall_recommendation.lower() == "accept":
            # Force recommendation to needs_revision or reject
            evaluation.overall_recommendation = "needs_revision"

        # Add annotations
        for a in annotations:
            ann = ReviewerAnnotation(
                task_id=task_id,
                reviewer_id=reviewer.id,
                timestamp_ms=a.get("timestamp_ms", 0),
                duration_ms=a.get("duration_ms", 0),
                target_type=a.get("target_type", "avatar"),
                category=a.get("category", "general"),
                comment=a.get("comment", ""),
                created_at=datetime.now(timezone.utc)
            )
            self.db.add(ann)

        # Update task stats and lifecycle status
        if not is_draft:
            completed_evals = (
                self.db.query(SignEvaluation)
                .filter(SignEvaluation.task_id == task_id, SignEvaluation.is_draft.is_(False))
                .all()
            )
            task.completed_reviews_count = len(completed_evals)

            if len(completed_evals) == 1:
                task.status = ValidationTaskStatus.UNDER_REVIEW
            elif len(completed_evals) >= 2:
                task.status = ValidationTaskStatus.REVIEWED
                # Run disagreement detection
                self.detect_disagreements(task)

        self.log_action(
            actor_id=reviewer.id,
            actor_username=reviewer.username,
            action="EVALUATION_DRAFT_SAVED" if is_draft else "EVALUATION_SUBMITTED",
            target_type="task",
            target_id=str(task_id),
            details={"overall_recommendation": evaluation.overall_recommendation, "is_draft": is_draft}
        )

        self.db.commit()
        self.db.refresh(evaluation)
        return evaluation

    def detect_disagreements(self, task: ValidationTask) -> List[EvaluationDisagreement]:
        """
        Scans all submitted evaluations for a task to identify rating or recommendation conflicts.
        If disagreements are found, marks task as DISAGREEMENT_DETECTED.
        """
        evals = (
            self.db.query(SignEvaluation)
            .filter(SignEvaluation.task_id == task.id, SignEvaluation.is_draft.is_(False))
            .all()
        )
        if len(evals) < 2:
            return []

        # 1. Recommendation conflict
        recommendations = {e.reviewer.username: e.overall_recommendation for e in evals}
        unique_recs = set(recommendations.values())
        disagreements = []

        if len(unique_recs) > 1:
            # Check if one says accept and another says reject or needs_revision
            d = EvaluationDisagreement(
                task_id=task.id,
                criterion_name="overall_recommendation",
                disagreement_type="recommendation_conflict",
                reviewer_ratings_json=json.dumps(recommendations),
                status="open",
                detected_at=datetime.now(timezone.utc)
            )
            self.db.add(d)
            disagreements.append(d)

        # 2. Criterion-level conflicts
        # Gather ratings per criterion
        criterion_map: Dict[str, Dict[str, str]] = {}
        for e in evals:
            for cr in e.criteria_ratings:
                c_name = cr.criterion_name
                if c_name not in criterion_map:
                    criterion_map[c_name] = {}
                criterion_map[c_name][e.reviewer.username] = cr.rating.value

        for c_name, raters in criterion_map.items():
            ratings = set(raters.values())
            # Conflict if one says 'pass' and another says 'major_issue' or 'incorrect'
            has_pass = "pass" in ratings
            has_major = any(r in ratings for r in ["major_issue", "incorrect"])
            if has_pass and has_major:
                d = EvaluationDisagreement(
                    task_id=task.id,
                    criterion_name=c_name,
                    disagreement_type="rating_conflict",
                    reviewer_ratings_json=json.dumps(raters),
                    status="open",
                    detected_at=datetime.now(timezone.utc)
                )
                self.db.add(d)
                disagreements.append(d)

        if disagreements:
            task.status = ValidationTaskStatus.DISAGREEMENT_DETECTED
            self.log_action(
                actor_id=None,
                actor_username="system_detector",
                action="DISAGREEMENT_DETECTED",
                target_type="task",
                target_id=str(task.id),
                details={"disagreements_count": len(disagreements)}
            )

        return disagreements

    def adjudicate_task(
        self,
        task_id: int,
        adjudicator: Reviewer,
        decision_enum: AdjudicationDecisionEnum,
        resulting_motion_status: str,
        rationale: str,
        evidence_summary: Optional[str]
    ) -> ValidationDecision:
        """
        Adjudicates a task under disagreement or pending decision.
        Enforces Zero-Fabrication gate: only VERIFIED admin or expert can make binding decision.
        """
        task = self.db.query(ValidationTask).filter(ValidationTask.id == task_id).first()
        if not task:
            raise ValueError(f"Task {task_id} not found.")

        # Zero-Fabrication check: must be a verified reviewer
        if adjudicator.verification_status != ReviewerVerificationStatus.VERIFIED:
            raise PermissionError(
                f"Adjudicator '{adjudicator.username}' is not verified. "
                "Only administrative verified reviewers can issue binding adjudication decisions."
            )

        # Create decision
        decision = ValidationDecision(
            task_id=task_id,
            adjudicator_id=adjudicator.id,
            decision=decision_enum,
            resulting_motion_status=resulting_motion_status,
            rationale=rationale,
            evidence_summary=evidence_summary,
            decided_at=datetime.now(timezone.utc)
        )
        self.db.add(decision)

        # Update task status
        if decision_enum == AdjudicationDecisionEnum.ACCEPTED:
            task.status = ValidationTaskStatus.ACCEPTED
        elif decision_enum == AdjudicationDecisionEnum.REJECTED:
            task.status = ValidationTaskStatus.REJECTED
        elif decision_enum == AdjudicationDecisionEnum.INCONCLUSIVE:
            task.status = ValidationTaskStatus.INCONCLUSIVE
        else:
            task.status = ValidationTaskStatus.PENDING_REVIEW

        # Close open disagreements
        open_disagreements = (
            self.db.query(EvaluationDisagreement)
            .filter(EvaluationDisagreement.task_id == task_id, EvaluationDisagreement.status == "open")
            .all()
        )
        for d in open_disagreements:
            d.status = "adjudicated"

        # Update underlying SignRecord if decision is binding
        sign = self.db.query(SignRecord).filter(SignRecord.id == task.sign_record_id).first()
        if sign:
            if decision_enum == AdjudicationDecisionEnum.ACCEPTED and resulting_motion_status == "VERIFIED_ISL_MOTION":
                sign.validation_status = ValidationStatus.VERIFIED
                sign.is_authentic = True
                sign.validation_date = datetime.now(timezone.utc)
            elif decision_enum == AdjudicationDecisionEnum.REJECTED:
                sign.validation_status = ValidationStatus.UNSUPPORTED
                sign.is_authentic = False

        self.log_action(
            actor_id=adjudicator.id,
            actor_username=adjudicator.username,
            action="TASK_ADJUDICATED",
            target_type="task",
            target_id=str(task_id),
            details={
                "decision": decision_enum.value,
                "resulting_motion_status": resulting_motion_status,
                "rationale": rationale
            }
        )

        self.db.commit()
        self.db.refresh(decision)
        return decision

