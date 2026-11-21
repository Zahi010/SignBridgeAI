"""
SignBridge AI - Technical Concept Explanation Generator.
Generates rigorous pedagogical explanations for concepts lacking standardized single-sign ISL equivalents.
Adheres strictly to the Zero Fabricated Signs Policy:
- Explains why a verified single sign is unavailable.
- Provides recommended ISL communication strategies (fingerspelling + classifier diagramming).
- Preserves precise engineering meaning without omission.
"""

from typing import Dict, Any, Optional

SPECIALIZED_EXPLANATIONS = {
    "deadlock": {
        "term": "Deadlock",
        "category": "Operating Systems / Concurrency",
        "why_unsupported": "No national standardized single sign currently certified for DEADLOCK in Indian Sign Language.",
        "recommended_isl_strategy": "Two-handed fingerspelling (D-E-A-D-L-O-C-K) followed by circular spatial wait indexing.",
        "fingerspelling_sequence": ["D", "E", "A", "D", "L", "O", "C", "K"],
        "pedagogical_diagram_description": "Resource Allocation Graph (RAG) depicting circular wait between two processes and two resource units.",
        "engineering_definition": "A state where each member of a set of concurrent processes is blocked waiting for an event that only another process in the set can cause.",
        "technical_advice_for_educators": "Establish Spatial Locus A (Process 1 holding Resource 1) and Spatial Locus B (Process 2 holding Resource 2), indexing directed mutual wait arrows."
    },
    "pointer": {
        "term": "Pointer",
        "category": "Data Structures / Systems Programming",
        "why_unsupported": "Pointer in programming refers to memory addresses rather than physical finger pointing; a single standardized sign is not yet codified.",
        "recommended_isl_strategy": "Fingerspelling (P-O-I-N-T-E-R) followed by index finger pointing to a distinct spatial memory cell containing address hex values.",
        "fingerspelling_sequence": ["P", "O", "I", "N", "T", "E", "R"],
        "pedagogical_diagram_description": "Memory address box with an arrow pointing to a separate dereferenced value block.",
        "engineering_definition": "A variable whose value is the physical or virtual address of another variable in computer memory.",
        "technical_advice_for_educators": "Sign MEMORY-BOX, assign it an address locus, then sign ARROW referencing that specific locus."
    },
    "modulation": {
        "term": "Modulation",
        "category": "Communication Systems / RF",
        "why_unsupported": "High-frequency carrier modulation lacks a single unified ISL gesture.",
        "recommended_isl_strategy": "Fingerspelling (M-O-D-U-L-A-T-I-O-N) followed by two-handed wave superposition.",
        "fingerspelling_sequence": ["M", "O", "D", "U", "L", "A", "T", "I", "O", "N"],
        "pedagogical_diagram_description": "High-frequency carrier sine wave multiplied by low-frequency information audio waveform.",
        "engineering_definition": "The process of varying one or more properties of a carrier periodic waveform with an information-bearing modulating signal.",
        "technical_advice_for_educators": "Demonstrate fast carrier oscillation in non-dominant hand, and modify its envelope using dominant message wave."
    },
    "oscillator": {
        "term": "Oscillator",
        "category": "Analog Electronics / Circuits",
        "why_unsupported": "Lacks certified single sign; distinct from mechanical pendulum oscillation.",
        "recommended_isl_strategy": "Fingerspelling (O-S-C-I-L-L-A-T-O-R) with positive feedback loop classifier.",
        "fingerspelling_sequence": ["O", "S", "C", "I", "L", "L", "A", "T", "O", "R"],
        "pedagogical_diagram_description": "Amplifier block with positive feedback loop meeting the Barkhausen criterion (loop gain = 1, phase = 0).",
        "engineering_definition": "An electronic circuit that converts DC power into periodic AC output without external input.",
        "technical_advice_for_educators": "Emphasize SELF-STARTING waveform without external source."
    },
    "bracing": {
        "term": "Bracing",
        "category": "Structural Engineering / Civil",
        "why_unsupported": "Single standardized sign undergoing peer review; current usage relies on visual truss classifiers.",
        "recommended_isl_strategy": "Fingerspelling (B-R-A-C-I-N-G) followed by crossing forearms in diagonal X-pattern between structural columns.",
        "fingerspelling_sequence": ["B", "R", "A", "C", "I", "N", "G"],
        "pedagogical_diagram_description": "Structural bay frame with diagonal steel tension/compression cross members.",
        "engineering_definition": "A system of structural members arranged diagonally to resist lateral wind and seismic sway loads.",
        "technical_advice_for_educators": "Sign VERTICAL-COLUMNS, then cross forearms in X-shape demonstrating lateral shear resistance."
    },
    "abutment": {
        "term": "Abutment",
        "category": "Bridge Engineering / Civil",
        "why_unsupported": "Specialized bridge substructure lacking single-sign national standard.",
        "recommended_isl_strategy": "Fingerspelling (A-B-U-T-M-E-N-T) followed by bridge end-support and retaining wall classifier.",
        "fingerspelling_sequence": ["A", "B", "U", "T", "M", "E", "N", "T"],
        "pedagogical_diagram_description": "Bridge deck resting on concrete bank pier supporting roadway approach fill.",
        "engineering_definition": "The substructure at the ends of a bridge span supporting the superstructure and retaining approach embankment soil.",
        "technical_advice_for_educators": "Combine BRIDGE-END + GROUND-HOLD classifiers."
    },
    "operating-system": {
        "term": "Operating System",
        "category": "Systems Software",
        "why_unsupported": "Base sign compound exists (COMPUTER + SYSTEM-MANAGE), but kernel mechanics require pedagogical explanation.",
        "recommended_isl_strategy": "Sign base compound OPERATING-SYSTEM, then visually unpack kernel layers (hardware abstraction, scheduling).",
        "fingerspelling_sequence": ["O", "S"],
        "pedagogical_diagram_description": "Layered architecture: Hardware -> Kernel -> System Calls -> User Applications.",
        "engineering_definition": "System software that manages computer hardware and software resources and provides common services for programs.",
        "technical_advice_for_educators": "Index HARDWARE at lowest spatial layer, KERNEL in middle, and APPS at top layer."
    },
    "thermodynamics": {
        "term": "Thermodynamics",
        "category": "Applied Thermodynamics",
        "why_unsupported": "Base sign exists, but cyclic heat engine transformations require diagrammatic expansion.",
        "recommended_isl_strategy": "Sign HEAT + ENERGY-CHANGE, followed by Carnot cycle PV diagram.",
        "fingerspelling_sequence": ["T", "H", "E", "R", "M", "O"],
        "pedagogical_diagram_description": "Pressure-Volume (PV) state diagram illustrating isothermal and adiabatic expansion/compression.",
        "engineering_definition": "The branch of physics that deals with heat, work, and temperature, and their relation to energy and entropy.",
        "technical_advice_for_educators": "Demonstrate high temperature heat reservoir transferring work and rejecting entropy."
    }
}

def generate_concept_explanation(
    term: str,
    slug: str,
    validation_status: str,
    category: Optional[str] = None,
    definition: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates a structured educational explanation for unsupported or explanation-needed concepts.
    """
    slug_clean = slug.lower().strip()
    if slug_clean in SPECIALIZED_EXPLANATIONS:
        return SPECIALIZED_EXPLANATIONS[slug_clean]

    # Generalized fallback adhering to policy
    letters = [ch.upper() for ch in term if ch.isalpha()]
    return {
        "term": term,
        "category": category or "Engineering Terminology",
        "why_unsupported": f"No certified single-sign ISL equivalent has been codified for '{term}'.",
        "recommended_isl_strategy": f"Use standard two-handed fingerspelling ({'-'.join(letters[:8])}) accompanied by a visual technical schematic.",
        "fingerspelling_sequence": letters[:12],
        "pedagogical_diagram_description": f"Visual conceptual schematic illustrating the core principles of {term}.",
        "engineering_definition": definition or f"Specialized engineering concept within {category or 'the technical domain'}.",
        "technical_advice_for_educators": "Fingerspell the term first, then establish a designated spatial locus for subsequent pronominal references."
    }
