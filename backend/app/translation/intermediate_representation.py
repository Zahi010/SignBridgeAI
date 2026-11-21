"""
SignBridge AI - Translation Intermediate Representation (IR).
Defines the unified, structured linguistic and multimodal translation schema
shared between the human video renderer, 3D avatar animation sequencer, and client UI.
"""

from typing import List, Dict, Any, Optional

class TranslationIR:
    """
    Unified Intermediate Representation for an ISL translation request.
    """

    def __init__(
        self,
        source_text: str,
        detected_branch: Dict[str, Any],
        detected_subject: Optional[Dict[str, Any]],
        context_domain: str,
        token_analysis: List[Dict[str, Any]],
        detected_concepts: List[Dict[str, Any]],
        semantic_relations: List[Dict[str, Any]],
        isl_grammar_plan: Dict[str, Any],
        policy_verdict: Dict[str, Any],
        asset_resolution: Dict[str, Any]
    ):
        self.source_text = source_text
        self.detected_branch = detected_branch
        self.detected_subject = detected_subject
        self.context_domain = context_domain
        self.token_analysis = token_analysis
        self.detected_concepts = detected_concepts
        self.semantic_relations = semantic_relations
        self.isl_grammar_plan = isl_grammar_plan
        self.policy_verdict = policy_verdict
        self.asset_resolution = asset_resolution

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_text": self.source_text,
            "detected_branch": self.detected_branch,
            "detected_subject": self.detected_subject,
            "context_domain": self.context_domain,
            "token_analysis": self.token_analysis,
            "detected_concepts": self.detected_concepts,
            "semantic_relations": self.semantic_relations,
            "isl_grammar_plan": self.isl_grammar_plan,
            "policy_verdict": self.policy_verdict,
            "asset_resolution": self.asset_resolution
        }
