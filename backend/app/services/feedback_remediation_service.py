"""
SignBridge AI - Feedback-Driven Remediation Service (Phase 7.6).
Transforms expert reviewer evaluations, phonological rubric criticisms, and millisecond
annotations into structured engineering remediation tasks.

Prevents premature sign modification: All changes require audit evidence, preserving original
reviewer comments and requiring formal adjudication where reviewers disagree.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from backend.app.models.validation_models import (
    SignEvaluation,
    EvaluationCriterionRating,
    ReviewerAnnotation,
    RubricCriterionRating,
    FeedbackRemediationTicket,
    RemediationCategory,
    RemediationStatus,
    ValidationTask
)

CRITERION_TO_CATEGORY_MAP: Dict[str, RemediationCategory] = {
    "handshape": RemediationCategory.HAND_ARTICULATION,
    "orientation": RemediationCategory.ORIENTATION_SOLVER,
    "movement": RemediationCategory.MOTION_RETARGETING,
    "coordination": RemediationCategory.MOTION_RETARGETING,
    "location": RemediationCategory.MOTION_RETARGETING,
    "facial_nmm": RemediationCategory.NMM_MAPPING,
    "contextual_meaning": RemediationCategory.LEXICON_INVESTIGATION,
    "lexical_correctness": RemediationCategory.LEXICON_INVESTIGATION,
    "grammatical_correctness": RemediationCategory.GRAMMAR_SEQUENCING,
    "naturalness": RemediationCategory.MOTION_RETARGETING,
    "regional_variation": RemediationCategory.LEXICON_INVESTIGATION,
    "ambiguity": RemediationCategory.LEXICON_INVESTIGATION,
}


class FeedbackRemediationService:
    def __init__(self, db: Session):
        self.db = db

    def generate_tickets_from_evaluation(self, evaluation_id: int) -> List[FeedbackRemediationTicket]:
        """
        Inspects an evaluation's rubric criteria and annotations to auto-generate
        actionable engineering remediation tickets for any identified defects.
        """
        evaluation = self.db.query(SignEvaluation).filter(SignEvaluation.id == evaluation_id).first()
        if not evaluation:
            raise ValueError(f"SignEvaluation {evaluation_id} not found.")

        task = self.db.query(ValidationTask).filter(ValidationTask.id == evaluation.task_id).first()
        created_tickets = []

        # Find annotations for this task and reviewer to match timestamps
        annotations = (
            self.db.query(ReviewerAnnotation)
            .filter(
                ReviewerAnnotation.task_id == evaluation.task_id,
                ReviewerAnnotation.reviewer_id == evaluation.reviewer_id
            )
            .all()
        )

        for cr in evaluation.criteria_ratings:
            if cr.rating in [RubricCriterionRating.MAJOR_ISSUE, RubricCriterionRating.INCORRECT] or cr.is_critical_error:
                category = CRITERION_TO_CATEGORY_MAP.get(cr.criterion_name.lower(), RemediationCategory.GENERAL_PHONOLOGY)
                severity = "critical" if cr.is_critical_error or cr.rating == RubricCriterionRating.INCORRECT else "major"

                # Check for matching annotation timestamp
                timestamp_ms = None
                matched_ann = [a for a in annotations if cr.criterion_name.lower() in a.category.lower()]
                if matched_ann:
                    timestamp_ms = matched_ann[0].timestamp_ms

                issue_desc = (
                    f"Phonological defect identified in '{cr.criterion_name}': {cr.rating.value.upper()}. "
                    f"Reviewer notes: {cr.notes or 'No specific criterion notes provided.'}"
                )

                proposed_fix = self._propose_remediation(category, cr.criterion_name)

                ticket = FeedbackRemediationTicket(
                    task_id=evaluation.task_id,
                    evaluation_id=evaluation.id,
                    criterion_name=cr.criterion_name,
                    category=category,
                    status=RemediationStatus.OPEN,
                    severity=severity,
                    issue_description=issue_desc,
                    reviewer_notes=cr.notes,
                    timestamp_ms=timestamp_ms,
                    proposed_remediation=proposed_fix,
                    created_at=datetime.now(timezone.utc)
                )
                self.db.add(ticket)
                created_tickets.append(ticket)

        self.db.commit()
        for t in created_tickets:
            self.db.refresh(t)
        return created_tickets

    def _propose_remediation(self, category: RemediationCategory, criterion_name: str) -> str:
        proposals = {
            RemediationCategory.HAND_ARTICULATION: "Inspect finger joint flexion/extension Euler limits in AvatarHandRig. Re-calibrate MediaPipe hand landmark smoothing.",
            RemediationCategory.ORIENTATION_SOLVER: "Re-solve palm normal vector against forearm orthogonal basis. Invert palm normal quaternion if 180-degree flip detected.",
            RemediationCategory.MOTION_RETARGETING: "Check stroke trajectory spline interpolation. Filter high-frequency jitter in elbow and wrist retargeting.",
            RemediationCategory.NMM_MAPPING: "Inspect face mesh blendshape weights for eyebrow raise/furrow and mouth shape. Verify NMM synchronization with manual stroke.",
            RemediationCategory.LEXICON_INVESTIGATION: "Cross-examine sign against official ISLRTC academic dictionary. Check if polysemic term requires conceptual sub-categorization.",
            RemediationCategory.GRAMMAR_SEQUENCING: "Audit Topic-Comment word order planner. Verify spatial indexing anchors and question/negator placement.",
            RemediationCategory.GENERAL_PHONOLOGY: "Conduct expert review adjudication and gather additional peer evaluations."
        }
        return proposals.get(category, "Conduct linguistic and technical review.")

    def list_tickets(
        self,
        task_id: Optional[int] = None,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[FeedbackRemediationTicket]:
        query = self.db.query(FeedbackRemediationTicket)
        if task_id:
            query = query.filter(FeedbackRemediationTicket.task_id == task_id)
        if category:
            query = query.filter(FeedbackRemediationTicket.category == category)
        if status:
            query = query.filter(FeedbackRemediationTicket.status == status)
        return query.order_by(FeedbackRemediationTicket.created_at.desc()).all()

    def update_ticket(
        self,
        ticket_id: int,
        new_status: RemediationStatus,
        resolution_notes: Optional[str] = None
    ) -> FeedbackRemediationTicket:
        ticket = self.db.query(FeedbackRemediationTicket).filter(FeedbackRemediationTicket.id == ticket_id).first()
        if not ticket:
            raise ValueError(f"Remediation ticket {ticket_id} not found.")

        ticket.status = new_status
        if resolution_notes:
            ticket.resolution_notes = resolution_notes
        if new_status in [RemediationStatus.RESOLVED, RemediationStatus.DISMISSED]:
            ticket.resolved_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
