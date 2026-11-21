"""
SignBridge AI - Enhanced Educational Explanation System
Provides multi-step pedagogical explanations for abstract, complex, or uncodified
engineering concepts. Employs ISL classifier predicates, spatial layouts, visual metaphors,
and structured decomposition designed specifically for deaf engineering students.
"""

from typing import Dict, Any, List, Optional

# Structured Educational Explanations for Core Complex / Uncodified Concepts
EDUCATIONAL_EXPLANATIONS: Dict[str, Dict[str, Any]] = {
    "deadlock": {
        "term": "Deadlock",
        "branch": "Computer Science & Engineering",
        "subject": "Operating Systems (CS301)",
        "canonical_status": "UNSUPPORTED",
        "linguistic_reality": "No atomic standardized sign exists in ISLRTC dictionary. Deaf educators recommend fingerspelling followed by spatial resource allocation graph demonstration.",
        "pedagogical_strategy": "Multi-resource circular dependency demonstration with two distinct processes waiting mutually on locks held by each other.",
        "analogical_metaphor": "Four cars simultaneously entering a 4-way intersection, each blocking the other from advancing.",
        "fingerspelling_sequence": ["D", "E", "A", "D", "L", "O", "C", "K"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell D-E-A-D-L-O-C-K in central signing space."
            },
            {
                "step": 2,
                "action": "SPATIAL_ESTABLISHMENT",
                "details": "Establish Process-1 at Left Locus (Locus A) and Process-2 at Right Locus (Locus B)."
            },
            {
                "step": 3,
                "action": "RESOURCE_LOCK_CLASSIFIER",
                "details": "Left hand signs [HOLD-RESOURCE-A]; right hand signs [HOLD-RESOURCE-B]."
            },
            {
                "step": 4,
                "action": "CIRCULAR_WAIT_CLASSIFIER",
                "details": "Hands cross over: Left hand reaches for Resource-B (blocked); Right hand reaches for Resource-A (blocked). Frozen posture with furrowed brow indicating zero progress."
            }
        ],
        "codified_related_concepts": ["PROCESS", "MEMORY", "RESOURCE", "WAIT", "BLOCK"],
        "student_explanation": (
            "A Deadlock occurs in an Operating System when two or more concurrent processes cannot proceed "
            "because each is holding a resource that the other process needs, forming a circular wait. "
            "Neither process can release its lock, resulting in an indefinite permanent stall."
        )
    },
    "compiler": {
        "term": "Compiler",
        "branch": "Computer Science & Engineering",
        "subject": "System Software & Compiler Design (CS401)",
        "canonical_status": "EXPLANATION_REQUIRED",
        "linguistic_reality": "Lacks an atomic ISLRTC sign. Deaf computer science scholars decompose into a 3-stage translation pipeline: Lexical/Syntax Analysis -> Intermediate Code -> Machine Code.",
        "pedagogical_strategy": "Spatial pipeline transformation: High-level readable program text enters from Left Locus, undergoes structural checking and optimization in Center, and emits binary 0/1 machine code at Right Locus.",
        "analogical_metaphor": "An expert book translator translating an entire English book into Hindi before anyone reads it, checking grammar and spelling throughout.",
        "fingerspelling_sequence": ["C", "O", "M", "P", "I", "L", "E", "R"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell C-O-M-P-I-L-E-R."
            },
            {
                "step": 2,
                "action": "INPUT_CODE_SIGN",
                "details": "Sign [PROGRAM-CODE] at Left Locus (text written by programmer)."
            },
            {
                "step": 3,
                "action": "TRANSFORMATION_CLASSIFIER",
                "details": "Both hands perform scanning and reorganizing movement in Center space (Lexical/Syntax parsing and optimization)."
            },
            {
                "step": 4,
                "action": "OUTPUT_BINARY_SIGN",
                "details": "Direct hands to Right Locus signing [BINARY-0-1] / [MACHINE-EXECUTE]."
            }
        ],
        "codified_related_concepts": ["ALGORITHM", "PROGRAM", "TRANSLATION", "COMPUTER"],
        "student_explanation": (
            "A Compiler is a specialized system program that translates an entire high-level programming language "
            "(like C++, Java, or Python) into binary machine instructions that the computer's CPU hardware can directly execute."
        )
    },
    "modulation": {
        "term": "Modulation",
        "branch": "Electronics & Communication",
        "subject": "Analog & Digital Communication (EC302)",
        "canonical_status": "EXPLANATION_REQUIRED",
        "linguistic_reality": "No single dictionary sign. Deaf STEM educators sign high-frequency carrier wave + information signal modulation using dual-hand sinusoidal classifiers.",
        "pedagogical_strategy": "Dual-hand spatial waveform interaction: Dominant hand demonstrates high-frequency carrier sinusoidal wave; non-dominant hand injects low-frequency information audio signal, visually demonstrating amplitude (AM) or frequency (FM) variation.",
        "analogical_metaphor": "Loading a heavy passenger (audio message) onto a high-speed supersonic jet (carrier wave) so the message can travel hundreds of kilometers without dying out.",
        "fingerspelling_sequence": ["M", "O", "D", "U", "L", "A", "T", "I", "O", "N"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell M-O-D-U-L-A-T-I-O-N."
            },
            {
                "step": 2,
                "action": "CARRIER_WAVE_CLASSIFIER",
                "details": "Dominant hand oscillates horizontally in tight rapid waves: [FAST-HIGH-FREQUENCY-CARRIER]."
            },
            {
                "step": 3,
                "action": "MESSAGE_SIGNAL_CLASSIFIER",
                "details": "Non-dominant hand demonstrates slow, low-frequency speech envelope: [AUDIO-MESSAGE-SIGNAL]."
            },
            {
                "step": 4,
                "action": "SUPERPOSITION_MODULATION",
                "details": "Hands combine: Carrier wave amplitude expands and contracts matching the message signal envelope (AM demonstration)."
            }
        ],
        "codified_related_concepts": ["FREQUENCY", "WAVE", "ANTENNA", "TRANSMIT"],
        "student_explanation": (
            "Modulation is the technique of modifying one or more properties (amplitude, frequency, or phase) of a "
            "high-frequency carrier electromagnetic wave with an information-bearing signal (like audio or data) so it can travel "
            "over long distances through antennas or fiber optic cables without significant attenuation."
        )
    },
    "electromagnetic induction": {
        "term": "Electromagnetic Induction",
        "branch": "Electrical & Electronics Engineering",
        "subject": "Electromagnetic Fields & Machines (EE301)",
        "canonical_status": "EXPLANATION_REQUIRED",
        "linguistic_reality": "Standard ISL has individual signs for 'Electricity' and 'Magnet', but no composite term for 'Induction'. Decomposed into magnetic flux variation generating voltage.",
        "pedagogical_strategy": "Dynamic physical demonstration: Non-dominant hand forms circular coiled conductor; dominant hand moves magnetic bar back and forth through coil, triggering current deflection.",
        "analogical_metaphor": "Pushing a piston through water generates a whirlpool; pushing magnetic lines of force through copper wire generates flowing electric current.",
        "fingerspelling_sequence": ["E", "M", "I"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell E-M-I (or E-L-E-C-T-R-O M-A-G-N-E-T)."
            },
            {
                "step": 2,
                "action": "COIL_CLASSIFIER",
                "details": "Non-dominant hand forms cylindrical helix [WIRE-COIL] in neutral chest space."
            },
            {
                "step": 3,
                "action": "MAGNETIC_FLUX_MOTION",
                "details": "Dominant fist represents [MAGNET]; thrusts repeatedly in and out of the coil aperture."
            },
            {
                "step": 4,
                "action": "INDUCED_CURRENT_CLASSIFIER",
                "details": "Both hands follow conductor leads showing spontaneous electron flow: [CURRENT-FLOW-INDUCED]."
            }
        ],
        "codified_related_concepts": ["VOLTAGE", "CURRENT", "TRANSFORMER", "GENERATOR"],
        "student_explanation": (
            "Electromagnetic Induction is the physical law (Faraday's Law) where a time-varying magnetic field passing "
            "through an electric circuit induces an electromotive force (voltage) across the circuit, driving electric current. "
            "This principle powers electrical generators and transformers worldwide."
        )
    },
    "shear stress": {
        "term": "Shear Stress",
        "branch": "Civil & Mechanical Engineering",
        "subject": "Mechanics of Solids & Structures (CE201 / ME202)",
        "canonical_status": "EXPLANATION_REQUIRED",
        "linguistic_reality": "No single dictionary sign. Taught using parallel sliding hand palms to contrast against normal tensile/compressive stress.",
        "pedagogical_strategy": "Opposing coplanar palms sliding past each other along a plane, causing angular skew distortion (gamma).",
        "analogical_metaphor": "Sliding a deck of cards across a table where each layer slips past the one beneath it, or shearing paper with scissors.",
        "fingerspelling_sequence": ["S", "H", "E", "A", "R", "S", "T", "R", "E", "S", "S"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell S-H-E-A-R S-T-R-E-S-S."
            },
            {
                "step": 2,
                "action": "PARALLEL_PLANE_ESTABLISHMENT",
                "details": "Both flat open-B hands placed parallel touching along palms."
            },
            {
                "step": 3,
                "action": "OPPOSING_TANGENTIAL_SLIP",
                "details": "Dominant hand pushes forward while non-dominant hand pulls backward in parallel shear slip."
            },
            {
                "step": 4,
                "action": "ANGULAR_DEFORMATION_INDICATION",
                "details": "Point to the skewed internal angle: [ANGULAR-STRAIN-DISTORTION]."
            }
        ],
        "codified_related_concepts": ["FORCE", "BEAM", "PRESSURE", "FRICTION"],
        "student_explanation": (
            "Shear Stress is a state of mechanical stress where an internal force acts coplanar or tangential to a material cross-section, "
            "causing adjacent layers of the material to slide parallel to one another rather than compressing or pulling apart."
        )
    },
    "finite element analysis": {
        "term": "Finite Element Analysis",
        "branch": "Mechanical & Civil Engineering",
        "subject": "Computational Mechanics & FEA (ME401 / CE403)",
        "canonical_status": "EXPLANATION_REQUIRED",
        "linguistic_reality": "Advanced numerical method with no isolated dictionary sign. Deaf engineering instructors use a 4-step discretization decomposition.",
        "pedagogical_strategy": "Structure decomposition: 1. Solid structure shape -> 2. Mesh grid partition into triangles/quads -> 3. Matrix stiffness calculation -> 4. Heatmap stress deformation.",
        "analogical_metaphor": "Representing a complex curved sculpture using thousands of small Lego bricks so each individual brick's strength can be computed numerically.",
        "fingerspelling_sequence": ["F", "E", "A"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell F-E-A."
            },
            {
                "step": 2,
                "action": "CONTINUOUS_SOLID_ESTABLISHMENT",
                "details": "Sign solid 3D mechanical component shape (e.g. beam or bracket)."
            },
            {
                "step": 3,
                "action": "MESH_DISCRETIZATION_CLASSIFIER",
                "details": "Both index fingers slice spatial grid lines across the volume: [DIVIDE-TINY-ELEMENTS-MESH]."
            },
            {
                "step": 4,
                "action": "NODAL_COMPUTATION_CLASSIFIER",
                "details": "Fingertips tap element nodes representing simultaneous matrix equations solving displacement and stress contours."
            }
        ],
        "codified_related_concepts": ["ALGORITHM", "FORCE", "CALCULATE", "COMPUTER"],
        "student_explanation": (
            "Finite Element Analysis (FEA) is a numerical computer simulation method used by engineers to predict how physical "
            "structures and parts behave under external forces, vibration, or heat by dividing a complex continuous body into thousands of small, simple 'finite elements'."
        )
    },
    "prestressed concrete": {
        "term": "Prestressed Concrete",
        "branch": "Civil Engineering",
        "subject": "Design of Concrete Structures (CE302)",
        "canonical_status": "UNSUPPORTED",
        "linguistic_reality": "No single dictionary sign. Taught via pre-tensioning tendons demonstration counteracting flexural tensile cracks.",
        "pedagogical_strategy": "High-strength steel cables stretched under high tension before concrete hardens; releasing tension places concrete in permanent pre-compression.",
        "analogical_metaphor": "Clamping a horizontal row of books together tightly with both hands so none can slip or fall through when lifted.",
        "fingerspelling_sequence": ["P", "R", "E", "S", "T", "R", "E", "S", "S"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell P-R-E-S-T-R-E-S-S C-O-N-C-R-E-T-E."
            },
            {
                "step": 2,
                "action": "STEEL_TENDON_TENSIONING",
                "details": "Hands pull high-strength steel tendon apart under high tensile force: [PULL-TENSION-HOLD]."
            },
            {
                "step": 3,
                "action": "CONCRETE_CASTING_CLASSIFIER",
                "details": "Sign [CONCRETE-POUR-SURROUND] engulfing the tensioned steel."
            },
            {
                "step": 4,
                "action": "RELEASE_PRECOMPRESSION",
                "details": "Both fists release tension against concrete ends, pressing inward into strong permanent compression: [COMPRESS-BEAM-STRONG]."
            }
        ],
        "codified_related_concepts": ["CONCRETE", "BEAM", "FORCE", "BUILD"],
        "student_explanation": (
            "Prestressed Concrete is structural concrete in which internal compressive stresses are intentionally introduced "
            "(using tensioned high-strength steel tendons) to counteract the tensile stresses that will occur when external loads are applied, preventing cracking."
        )
    },
    "synchronous motor": {
        "term": "Synchronous Motor",
        "branch": "Electrical & Electronics Engineering",
        "subject": "Electrical Machines (EE302)",
        "canonical_status": "UNSUPPORTED",
        "linguistic_reality": "Standard ISL has 'Motor', but synchronous lock requires classifier explanation of magnetic field locking rotor speed.",
        "pedagogical_strategy": "Stator rotating magnetic field locks with rotor poles; both rotate at exactly the same synchronous speed (Ns = 120f/P) with zero slip.",
        "analogical_metaphor": "Two interlocking gears spinning together in perfect lockstep where neither can slip ahead or lag behind.",
        "fingerspelling_sequence": ["S", "Y", "N", "C", "M", "O", "T", "O", "R"],
        "isl_representation_plan": [
            {
                "step": 1,
                "action": "TWO_HANDED_FINGERSPELLING",
                "details": "Spell S-Y-N-C-H-R-O-N-O-U-S M-O-T-O-R."
            },
            {
                "step": 2,
                "action": "STATOR_MAGNETIC_ROTATION",
                "details": "Non-dominant hand forms outer circular stator ring; index finger traces revolving magnetic field."
            },
            {
                "step": 3,
                "action": "ROTOR_MAGNETIC_LOCK",
                "details": "Dominant hand forms inner rotor; fingers interlock magnetically with stator field lines: [MAGNET-LOCK]."
            },
            {
                "step": 4,
                "action": "SYNCHRONOUS_REVOLUTION",
                "details": "Both hands spin together in locked angular velocity with zero slip: [EQUAL-SPEED-SPIN]."
            }
        ],
        "codified_related_concepts": ["MOTOR", "FREQUENCY", "MAGNETIC FIELD", "ELECTRICITY"],
        "student_explanation": (
            "A Synchronous Motor is an AC motor whose rotor rotates at exactly the same constant speed as the rotating "
            "magnetic field of the stator, meaning there is zero slip under normal operating conditions regardless of the mechanical load."
        )
    }
}

class EducationalExplanationService:
    """
    Manages and retrieves multi-step educational explanations for deaf engineering students.
    """

    @staticmethod
    def get_explanation(term: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves detailed structured pedagogical explanation for a concept.
        """
        clean_key = term.strip().lower()
        if clean_key in EDUCATIONAL_EXPLANATIONS:
            return EDUCATIONAL_EXPLANATIONS[clean_key]

        # Check partial key match
        for k, v in EDUCATIONAL_EXPLANATIONS.items():
            if k in clean_key or clean_key in k:
                return v

        return None

    @staticmethod
    def generate_generic_pedagogical_plan(
        term: str,
        category: Optional[str] = None,
        definition: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a standardized honest pedagogical plan for any unsupported/abstract concept.
        """
        clean_letters = [c.upper() for c in term if c.isalnum()][:10]
        return {
            "term": term,
            "branch": "General Engineering",
            "subject": category or "Technical Curriculum",
            "canonical_status": "EXPLANATION_REQUIRED",
            "linguistic_reality": f"The technical term '{term}' is not codified as a single lexicalized sign in standard ISL.",
            "pedagogical_strategy": f"Deconstruct '{term}' using fingerspelling followed by contextual classifier demonstration.",
            "analogical_metaphor": f"Relates to core principles described in definition: {definition or 'specialized engineering component'}.",
            "fingerspelling_sequence": clean_letters,
            "isl_representation_plan": [
                {
                    "step": 1,
                    "action": "TWO_HANDED_FINGERSPELLING",
                    "details": f"Fingerspell '{term.upper()}' using two-handed Indian Sign Language alphabet."
                },
                {
                    "step": 2,
                    "action": "CONTEXT_SPATIAL_INDEXING",
                    "details": "Establish physical domain in signing space (horizontal plane or vertical circuit diagram)."
                },
                {
                    "step": 3,
                    "action": "PEDAGOGICAL_CLASSIFIER",
                    "details": "Demonstrate the operational mechanism using representative handshape classifiers."
                }
            ],
            "codified_related_concepts": ["FUNCTION", "OPERATE", "STRUCTURE", "CALCULATE"],
            "student_explanation": definition or f"{term} is a specialized engineering concept taught using structured visual deconstruction."
        }

