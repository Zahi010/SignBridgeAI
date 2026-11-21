"""
SignBridge AI - Semantic Understanding & Contextual Disambiguation Engine.
Distinguishes technical engineering concepts from colloquial or temporal words.
Identifies semantic relationships between detected engineering entities.
"""

import re
from typing import List, Dict, Any, Optional, Tuple, Set

# Domain context triggers
ELECTRICAL_CONTEXT_TERMS = {
    "flow", "flows", "flowing", "resistor", "resistance", "voltage", "circuit", "amperes",
    "ampere", "amps", "ac", "dc", "wire", "conductor", "charge", "battery", "terminal",
    "ground", "grounding", "transformer", "motor", "generator", "power", "switch", "breaker",
    "capacitance", "capacitor", "inductance", "inductor", "frequency", "hertz", "ohm", "ohms"
}

NON_TECHNICAL_CURRENT_TRIGGERS = {
    "research", "trend", "trends", "status", "events", "issues", "year", "state", "situation",
    "focuses", "focus", "studies", "literature", "paper", "market", "economy", "news",
    "now", "currently", "affairs", "scenario", "affair"
}

COMPUTER_SCIENCE_CONTEXT_TERMS = {
    "algorithm", "data", "database", "query", "sql", "operating", "system", "processor",
    "cpu", "memory", "ram", "storage", "cache", "thread", "process", "compiler", "code",
    "software", "hardware", "encryption", "cipher", "network", "packet", "routing",
    "deadlock", "stack", "recursion", "pointer", "virtual", "kernel", "cloud", "structure"
}

MECHANICAL_CONTEXT_TERMS = {
    "force", "motion", "torque", "friction", "energy", "power", "machine", "mechanism",
    "gear", "engine", "piston", "pressure", "velocity", "acceleration", "thermodynamics",
    "heat", "stress", "strain", "turbine", "viscosity", "momentum", "fluid", "mass"
}

CIVIL_CONTEXT_TERMS = {
    "structure", "foundation", "concrete", "beam", "column", "load", "shear", "soil",
    "surveying", "reinforcement", "rebar", "cement", "mortar", "retaining", "wall",
    "hydrology", "water", "drainage", "compaction", "tensile", "bracing", "settlement", "abutment"
}

# Semantic relationship rules between pairs of concepts
SEMANTIC_RELATION_RULES = [
    # ECE / EEE
    (("Voltage", "Current"), "drives_flow_of", "Voltage provides the electrical potential difference that drives the flow of Current."),
    (("Current", "Resistance"), "opposed_by", "Current flow through a conductor is opposed by the material's Resistance (Ohm's Law)."),
    (("Current", "Voltage"), "proportional_to", "Current is directly proportional to Voltage across a constant Resistance."),
    (("Transformer", "Voltage"), "steps_up_or_down", "The Transformer changes Voltage levels between primary and secondary circuits via induction."),
    (("Motor", "Electricity"), "converts_to_mechanical", "The Motor converts electrical energy into rotational mechanical motion."),
    (("Generator", "Motion"), "converts_to_electrical", "The Generator converts mechanical motion into electrical energy."),
    (("Circuit Breaker", "Current"), "interrupts_fault", "The Circuit Breaker trips to interrupt excessive fault Current."),

    # CS
    (("Operating System", "Memory"), "manages_allocation_of", "The Operating System manages virtual address spaces and physical Memory allocation."),
    (("Operating System", "Processor"), "schedules_execution_on", "The Operating System schedules concurrent execution threads across Processor cores."),
    (("Operating System", "Deadlock"), "detects_and_prevents", "The Operating System enforces resource allocation graphs to prevent Deadlock."),
    (("Algorithm", "Data Structure"), "operates_upon", "The Algorithm traverses and processes records stored within the Data Structure."),
    (("Processor", "Memory"), "fetches_instructions_from", "The Processor fetches instructions and data from Memory via the system bus."),
    (("Compiler", "Software"), "translates_source_of", "The Compiler translates high-level Software source code into executable machine binaries."),
    (("Computer Network", "Database"), "provides_access_to", "The Computer Network enables distributed client nodes to access the remote Database."),

    # MECH
    (("Force", "Motion"), "causes_change_in", "An unbalanced net Force produces Acceleration and changes the Motion of a mass."),
    (("Force", "Acceleration"), "directly_proportional_to", "Force equals mass times Acceleration (Newton's Second Law)."),
    (("Torque", "Motion"), "produces_rotational", "Torque produces angular acceleration and rotational Motion about a shaft axis."),
    (("Friction", "Motion"), "opposes_relative", "Friction opposes relative Motion between contacting solid surfaces."),
    (("Stress", "Strain"), "produces_deformation", "Internal Stress produces mechanical Strain deformation in structural members."),
    (("Turbine", "Fluid Mechanics"), "extracts_energy_from", "The Turbine runner extracts kinetic and pressure energy from fluid flow."),

    # CIVIL
    (("Load", "Beam"), "applied_to", "Dead and live Loads produce bending moments and shear stresses in the horizontal Beam."),
    (("Beam", "Column"), "transfers_load_to", "The Beam transfers floor loads into vertical Columns at structural joints."),
    (("Column", "Foundation"), "transfers_axial_load_to", "The Column transfers concentrated vertical compressive loads down to the Foundation."),
    (("Foundation", "Soil Mechanics"), "supported_by", "The Foundation bearing capacity depends on underlying soil shear strength and consolidation."),
    (("Concrete", "Reinforcement"), "composite_matrix_with", "Concrete provides compressive resistance while steel Reinforcement resists tensile forces.")
]

class DisambiguatedMatch:
    def __init__(
        self,
        concept_term: str,
        matched_text: str,
        is_valid_technical: bool,
        rationale: str,
        confidence: float
    ):
        self.concept_term = concept_term
        self.matched_text = matched_text
        self.is_valid_technical = is_valid_technical
        self.rationale = rationale
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept_term": self.concept_term,
            "matched_text": self.matched_text,
            "is_valid_technical": self.is_valid_technical,
            "rationale": self.rationale,
            "confidence": self.confidence
        }

class SemanticRelationship:
    def __init__(
        self,
        source_concept: str,
        target_concept: str,
        relation_type: str,
        description: str
    ):
        self.source_concept = source_concept
        self.target_concept = target_concept
        self.relation_type = relation_type
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_concept": self.source_concept,
            "target_concept": self.target_concept,
            "relation_type": self.relation_type,
            "description": self.description
        }

class SemanticAnalyzer:
    """
    Analyzes sentence context, disambiguates polysemous terms, and extracts
    semantic relationships between engineering entities.
    """

    def disambiguate_concept(
        self,
        concept_term: str,
        sentence_text: str,
        explicit_branch_code: Optional[str] = None
    ) -> DisambiguatedMatch:
        """
        Disambiguates a candidate concept based on sentence tokens and context triggers.
        """
        text_lower = sentence_text.lower()
        tokens = set(re.findall(r"\b\w+\b", text_lower))

        # 1. Disambiguate "Current"
        if concept_term.lower() == "current":
            # Check for non-technical indicators
            non_tech_overlap = tokens.intersection(NON_TECHNICAL_CURRENT_TRIGGERS)
            tech_overlap = tokens.intersection(ELECTRICAL_CONTEXT_TERMS)

            if non_tech_overlap and not tech_overlap and explicit_branch_code not in ("ece", "eee"):
                return DisambiguatedMatch(
                    concept_term=concept_term,
                    matched_text="current",
                    is_valid_technical=False,
                    rationale=f"Word 'current' is used as a temporal adjective modifying: {list(non_tech_overlap)[0]}. Not electrical charge flow.",
                    confidence=0.95
                )

            if tech_overlap or explicit_branch_code in ("ece", "eee"):
                return DisambiguatedMatch(
                    concept_term=concept_term,
                    matched_text="current",
                    is_valid_technical=True,
                    rationale=f"Identified as Electrical Current (charge flow) supported by electrical context terms: {list(tech_overlap)[:3]}.",
                    confidence=0.98
                )

            # Default to technical if in engineering sentence
            return DisambiguatedMatch(
                concept_term=concept_term,
                matched_text="current",
                is_valid_technical=True,
                rationale="Matched electrical current in engineering context.",
                confidence=0.75
            )

        # 2. Disambiguate "Power"
        if concept_term.lower() == "power":
            is_mech = any(t in tokens for t in ("engine", "torque", "shaft", "mechanical", "work", "turbine", "watts"))
            is_elec = any(t in tokens for t in ("system", "grid", "voltage", "current", "station", "plant", "transmission"))

            if is_mech or explicit_branch_code == "mech":
                return DisambiguatedMatch(
                    concept_term=concept_term,
                    matched_text="power",
                    is_valid_technical=True,
                    rationale="Identified as Mechanical Power (rate of work / energy transfer).",
                    confidence=0.92
                )
            if is_elec or explicit_branch_code in ("eee", "ece"):
                return DisambiguatedMatch(
                    concept_term=concept_term,
                    matched_text="power",
                    is_valid_technical=True,
                    rationale="Identified as Electrical Power (voltage-current product / grid load).",
                    confidence=0.95
                )

        # 3. Disambiguate "Stress"
        if concept_term.lower() == "stress":
            tech_overlap = tokens.intersection({"strain", "beam", "load", "concrete", "steel", "tensile", "shear", "force", "mpa", "pascals"})
            if tech_overlap or explicit_branch_code in ("mech", "civil"):
                return DisambiguatedMatch(
                    concept_term=concept_term,
                    matched_text="stress",
                    is_valid_technical=True,
                    rationale=f"Identified as Mechanical Stress (force per unit area) supported by: {list(tech_overlap)[:3]}.",
                    confidence=0.95
                )
            else:
                return DisambiguatedMatch(
                    concept_term=concept_term,
                    matched_text="stress",
                    is_valid_technical=True,
                    rationale="Interpreted as mechanical stress in engineering context.",
                    confidence=0.80
                )

        # Default for single-meaning technical concepts
        return DisambiguatedMatch(
            concept_term=concept_term,
            matched_text=concept_term,
            is_valid_technical=True,
            rationale=f"Unambiguous technical terminology matched in engineering knowledge base.",
            confidence=0.98
        )

    def extract_semantic_relations(
        self,
        detected_concept_terms: List[str]
    ) -> List[SemanticRelationship]:
        """
        Detects meaningful semantic relationships between pairs of extracted concepts.
        """
        relations: List[SemanticRelationship] = []
        concept_set = set(detected_concept_terms)

        for (c1, c2), rel_type, desc in SEMANTIC_RELATION_RULES:
            if c1 in concept_set and c2 in concept_set:
                relations.append(
                    SemanticRelationship(
                        source_concept=c1,
                        target_concept=c2,
                        relation_type=rel_type,
                        description=desc
                    )
                )

        return relations

    def infer_primary_domain(
        self,
        text: str,
        detected_concepts: List[str]
    ) -> Tuple[str, str]:
        """
        Infers the engineering branch and primary technical domain from text and concepts.
        Returns (branch_code, domain_name).
        """
        tokens = set(re.findall(r"\b\w+\b", text.lower()))

        scores = {
            "cs": len(tokens.intersection(COMPUTER_SCIENCE_CONTEXT_TERMS)),
            "ece": len(tokens.intersection(ELECTRICAL_CONTEXT_TERMS)),
            "mech": len(tokens.intersection(MECHANICAL_CONTEXT_TERMS)),
            "civil": len(tokens.intersection(CIVIL_CONTEXT_TERMS)),
            "eee": len(tokens.intersection(ELECTRICAL_CONTEXT_TERMS))
        }

        # Weight by detected concepts
        for c in detected_concepts:
            c_low = c.lower()
            if any(term in c_low for term in ("database", "algorithm", "operating", "software", "network")):
                scores["cs"] += 5
            elif any(term in c_low for term in ("circuit", "voltage", "diode", "transistor", "microprocessor")):
                scores["ece"] += 5
            elif any(term in c_low for term in ("force", "motion", "gear", "engine", "thermodynamics")):
                scores["mech"] += 5
            elif any(term in c_low for term in ("concrete", "beam", "foundation", "structure", "soil")):
                scores["civil"] += 5
            elif any(term in c_low for term in ("electricity", "transformer", "generator", "power system", "grid")):
                scores["eee"] += 5

        best_branch = max(scores, key=scores.get)
        domain_names = {
            "cs": "Systems Software & Algorithms",
            "ece": "Electronic Devices & Circuit Analysis",
            "mech": "Engineering Mechanics & Thermal Systems",
            "civil": "Structural Analysis & Geotechnical Engineering",
            "eee": "Electrical Power Systems & Machines"
        }

        return best_branch, domain_names.get(best_branch, "General Engineering")
