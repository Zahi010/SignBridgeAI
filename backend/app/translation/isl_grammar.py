"""
SignBridge AI - ISL Grammar & Linguistic Restructuring Engine (Experimental Heuristic)

DISCLAIMER: The syntactic transformations implemented here (Topic-Comment reordering,
Time-First placement, sentence-final WH/Negation movement, and spatial loci indexing)
represent rule-based working linguistic hypotheses derived from academic literature.
They are NOT certified or validated ISL grammar standards and have NOT been approved
by an authoritative Deaf linguistic consensus panel. They are provided as experimental
translation planning hypotheses for research and evaluation purposes.
"""

import re
from typing import List, Tuple, Dict, Any

WH_WORDS = {"what", "how", "why", "when", "where", "which", "who", "whom"}
NEGATION_WORDS = {"not", "never", "no", "cannot", "cant", "doesn't", "don't", "isn't", "aren't"}
TIME_WORDS = {"today", "now", "yesterday", "tomorrow", "before", "after", "always", "initially"}

DEFAULT_EXPERIMENTAL_DISCLAIMER = (
    "Experimental rule-based transformation hypothesis awaiting Deaf linguistic validation. "
    "Not a certified ISL grammar standard."
)

class ISLGrammarTransformer:
    
    @staticmethod
    def analyze_and_restructure(
        text: str,
        matched_concept_terms: List[str]
    ) -> Tuple[List[str], List[Dict[str, str]]]:
        """
        Analyzes the English technical text and generates:
        1. An ISL gloss sequence reflecting genuine ISL syntactic conventions.
        2. A list of linguistic explanations explaining why the restructuring occurs.
        """
        clean_text = text.strip()
        tokens = re.findall(r"\b[A-Za-z0-9_\-']+\b", clean_text)
        lower_tokens = [t.lower() for t in tokens]
        
        gloss_sequence: List[str] = []
        grammar_notes: List[Dict[str, str]] = []
        
        # 1. Detect Temporal Elements (Time-First principle)
        temporal_found = [t for t in lower_tokens if t in TIME_WORDS]
        if temporal_found:
            for t in temporal_found:
                gloss_sequence.append(t.upper())
            grammar_notes.append({
                "rule_type": "Temporal Primacy (Time-First)",
                "english_pattern": f"Temporal marker '{temporal_found[0]}'",
                "isl_structure": f"[{temporal_found[0].upper()}] (Initial position)",
                "explanation": "In ISL syntax, temporal markers establish the time frame at the very beginning of the utterance before the subject or topic."
            })
            
        # 2. Topic Establishment (Topic-Comment principle)
        # Technical engineering concepts are prioritized as the central Topic
        topics_added = []
        if matched_concept_terms:
            for concept in matched_concept_terms:
                concept_gloss = concept.upper().replace(" ", "-")
                if concept_gloss not in gloss_sequence:
                    gloss_sequence.append(concept_gloss)
                    topics_added.append(concept_gloss)
            
            grammar_notes.append({
                "rule_type": "Topic-Comment Structure",
                "english_pattern": clean_text,
                "isl_structure": f"[TOPIC: {' + '.join(topics_added)}] -> [COMMENT: ACTION/STATE]",
                "explanation": "Unlike English Subject-Verb-Object (SVO), ISL prioritizes establishing the central entity (Topic) first in the visual signing space before making a comment or asking a question about it."
            })
        else:
            # Fallback for general words
            for t in tokens[:3]:
                if t.lower() not in WH_WORDS and t.lower() not in NEGATION_WORDS:
                    gloss_sequence.append(t.upper())

        # 3. Action / Predicate / Comment
        # Look for operational verbs: work, explain, calculate, operate, connect, store, build, transmit
        action_verbs = {
            "work": "WORK-FUNCTION",
            "works": "WORK-FUNCTION",
            "working": "WORK-FUNCTION",
            "explain": "EXPLAIN-CLARIFY",
            "define": "EXPLAIN-MEANING",
            "function": "OPERATE",
            "operates": "OPERATE",
            "build": "BUILD-CONSTRUCT",
            "transmit": "TRANSMIT-SEND",
            "connect": "CONNECT-INTERFACE",
            "flow": "FLOW-MOVE",
            "store": "STORE-ACCUMULATE"
        }
        found_actions = []
        for t in lower_tokens:
            if t in action_verbs:
                verb_gloss = action_verbs[t]
                if verb_gloss not in gloss_sequence:
                    gloss_sequence.append(verb_gloss)
                    found_actions.append(verb_gloss)

        # 4. Negation (placed at end with headshake NMM)
        has_negation = any(t in NEGATION_WORDS for t in lower_tokens)
        if has_negation:
            gloss_sequence.append("NOT [NMM: Headshake]")
            grammar_notes.append({
                "rule_type": "Sentence-Final Negation",
                "english_pattern": "Negative clause present",
                "isl_structure": "[PREDICATE] + NOT (with headshake)",
                "explanation": "ISL positions negation markers at the end of the verbal phrase, obligatorily co-occurring with a negative headshake non-manual marker."
            })

        # 5. Interrogative / WH-Word Placement (Final position with furrowed brow)
        wh_found = [t for t in lower_tokens if t in WH_WORDS]
        if wh_found:
            wh_gloss = wh_found[0].upper() + " [NMM: Furrowed Brow]"
            gloss_sequence.append(wh_gloss)
            grammar_notes.append({
                "rule_type": "WH-Question Final Position",
                "english_pattern": f"Interrogative '{wh_found[0]}'",
                "isl_structure": f"[TOPIC] + [COMMENT] + [{wh_found[0].upper()}] (Final)",
                "explanation": "In natural ISL, WH-questions are placed at the end of the sentence rather than at the beginning, synchronized with lowered or furrowed eyebrows."
            })

        # Spatial Indexing Note if multiple concepts exist
        if len(matched_concept_terms) >= 2:
            grammar_notes.append({
                "rule_type": "Dual Spatial Indexing (Loci Assignment)",
                "english_pattern": f"Multiple interacting concepts: {', '.join(matched_concept_terms)}",
                "isl_structure": f"[{matched_concept_terms[0].upper()} (Spatial Locus A)] <--> [{matched_concept_terms[1].upper()} (Spatial Locus B)]",
                "explanation": "When comparing or linking two engineering entities, the signer establishes one at spatial locus A (e.g. left) and the second at locus B (right), using directional verbs to indicate interaction."
            })

        for note in grammar_notes:
            note["is_experimental_hypothesis"] = True
            note["validation_status"] = "UNVALIDATED_HYPOTHESIS"
            note["disclaimer"] = DEFAULT_EXPERIMENTAL_DISCLAIMER

        return gloss_sequence, grammar_notes

