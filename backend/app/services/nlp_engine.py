"""
SignBridge AI - Engineering NLP & Semantic Understanding Engine
High-performance, deterministic natural language processing engine designed specifically
for engineering educational text across Computer Science, Electronics, Mechanical,
Civil, and Electrical branches.

Key Features:
- Linguistic tokenization, POS tagging, and rule-based lemmatization
- Technical terminology recognition across 5 major engineering branches
- Contextual polysemy disambiguation (Current, Class, Stress, Resistance, Beam, Java, Bus, Port, State, Network)
- Subject-Predicate-Object semantic triple extraction for interacting technical entities
"""

import re
from typing import List, Dict, Any, Optional, Tuple, Set

# Universal POS constants
POS_NOUN = "NOUN"
POS_PROPN = "PROPN"
POS_VERB = "VERB"
POS_ADJ = "ADJ"
POS_ADV = "ADV"
POS_PRON = "PRON"
POS_DET = "DET"
POS_ADP = "ADP"
POS_CCONJ = "CCONJ"
POS_SCONJ = "SCONJ"
POS_AUX = "AUX"
POS_PUNCT = "PUNCT"
POS_NUM = "NUM"

# Common function words
DETERMINERS = {"the", "a", "an", "this", "that", "these", "those", "every", "each", "all", "some"}
PREPOSITIONS = {"in", "on", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "over", "under"}
COORDINATING_CONJUNCTIONS = {"and", "but", "or", "nor", "so", "yet", "for"}
SUBORDINATING_CONJUNCTIONS = {"if", "because", "since", "unless", "while", "whereas", "although", "though"}
AUXILIARY_VERBS = {"is", "am", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "can", "could", "will", "would", "shall", "should", "may", "might", "must"}
PRONOUNS = {"it", "its", "they", "them", "their", "theirs", "he", "him", "his", "she", "her", "hers", "we", "us", "our", "ours", "i", "me", "my", "mine", "you", "your", "yours", "which", "who", "whom", "what"}

# Technical Engineering Lexicon by Branch
BRANCH_VOCABULARY = {
    "cs": {
        "processor", "processors", "cpu", "memory", "ram", "storage", "cache", "operating system",
        "algorithm", "algorithms", "database", "databases", "sql", "compiler", "compilers",
        "deadlock", "deadlocks", "data structure", "data structures", "stack", "stacks",
        "queue", "queues", "thread", "threads", "process", "processes", "instruction", "instructions",
        "pointer", "pointers", "virtual memory", "kernel", "cloud", "tree", "graph", "bus", "network",
        "encryption", "cipher", "bytecode", "binary", "source code", "machine code"
    },
    "ece": {
        "voltage", "voltages", "current", "currents", "frequency", "frequencies", "modulation",
        "diode", "diodes", "microcontroller", "microcontrollers", "transistor", "transistors",
        "amplifier", "amplifiers", "oscillator", "oscillators", "signal", "signals", "carrier wave",
        "antenna", "antennas", "demodulation", "filter", "filters", "resistor", "resistors",
        "capacitor", "capacitors", "inductor", "inductors", "semiconductor", "integrated circuit"
    },
    "mech": {
        "force", "forces", "velocity", "velocities", "torque", "torques", "friction",
        "thermodynamic entropy", "entropy", "finite element analysis", "fea", "stress", "stresses",
        "strain", "strains", "pressure", "pressures", "momentum", "gear", "gears", "turbine",
        "turbines", "piston", "pistons", "kinematics", "dynamics", "viscosity", "acceleration"
    },
    "civil": {
        "beam", "beams", "column", "columns", "foundation", "foundations", "concrete",
        "reinforced concrete", "prestressed concrete", "shear stress", "shear", "soil mechanics",
        "soil", "surveying", "load", "loads", "truss", "trusses", "slab", "slabs", "retaining wall",
        "abutment", "mortar", "cement", "settlement", "bearing capacity", "bracing"
    },
    "eee": {
        "transformer", "transformers", "generator", "generators", "alternating current", "ac",
        "direct current", "dc", "electromagnetic induction", "synchronous motor", "motor", "motors",
        "induction motor", "magnetic field", "circuit breaker", "power grid", "transmission line",
        "three phase", "rotor", "stator", "armature", "impedance", "reactance"
    }
}

# Domain Disambiguation Rules for Polysemous Engineering Words
DISAMBIGUATION_SPECS = {
    "current": {
        "tech_branch": "ece/eee",
        "tech_meaning": "Electrical Current (rate of flow of electric charge in amperes)",
        "tech_triggers": {
            "flow", "flows", "flowing", "resistor", "resistance", "voltage", "circuit", "amperes",
            "ampere", "amps", "ac", "dc", "wire", "conductor", "charge", "battery", "terminal",
            "ground", "transformer", "motor", "generator", "switch", "breaker", "ohm", "ohms",
            "electric", "electrical", "electricity", "induction", "magnetic"
        },
        "non_tech_triggers": {
            "research", "trend", "trends", "status", "events", "issues", "year", "state", "situation",
            "focuses", "focus", "studies", "literature", "paper", "market", "economy", "news",
            "now", "currently", "affairs", "scenario", "affair", "today", "era", "generation"
        },
        "non_tech_rationale": "Word 'current' is used as a temporal adjective/adverb (contemporary / existing status), not electric charge flow."
    },
    "class": {
        "tech_branch": "cs",
        "tech_meaning": "Software Class (object-oriented blueprint / user-defined data type)",
        "tech_triggers": {
            "object", "objects", "instance", "instances", "instantiate", "method", "methods",
            "attribute", "attributes", "inheritance", "polymorphism", "encapsulation", "oop",
            "java", "c++", "python", "constructor", "destructor", "variable", "interface", "subclass",
            "superclass", "property", "code", "programming", "software"
        },
        "non_tech_triggers": {
            "lecture", "room", "student", "students", "teacher", "attendance", "period", "bell",
            "classroom", "semester", "session", "course", "attend", "exam", "grade", "school"
        },
        "non_tech_rationale": "Word 'class' refers to an academic lecture or room of students, not an object-oriented programming construct."
    },
    "stress": {
        "tech_branch": "mech/civil",
        "tech_meaning": "Mechanical Stress (internal restoring force per unit cross-sectional area, measured in Pascals/MPa)",
        "tech_triggers": {
            "strain", "beam", "load", "concrete", "steel", "tensile", "shear", "force", "mpa", "pascals",
            "area", "deformation", "yield", "elastic", "plastic", "bending", "torsion", "compression",
            "cross-section", "megapascals", "finite", "element", "structural", "material"
        },
        "non_tech_triggers": {
            "mental", "emotional", "anxiety", "depression", "workload", "psychological", "exam", "personal",
            "lifestyle", "feeling", "feel", "worry", "worried", "calm", "relax", "tired", "health"
        },
        "non_tech_rationale": "Word 'stress' indicates psychological tension or emotional pressure, not mechanical force per unit area."
    },
    "resistance": {
        "tech_branch": "ece/eee",
        "tech_meaning": "Electrical Resistance (opposition to the passage of electric current, measured in Ohms)",
        "tech_triggers": {
            "ohm", "ohms", "current", "voltage", "resistor", "circuit", "conductor", "wire", "impedance",
            "flow", "amperes", "conductivity", "dissipation", "heat", "potential", "drop"
        },
        "non_tech_triggers": {
            "political", "social", "movement", "immune", "antibiotic", "bacterial", "protest", "policy",
            "change", "friction", "oppose", "rebel", "rebellion", "treatment", "disease"
        },
        "non_tech_rationale": "Word 'resistance' refers to social/biological opposition (e.g. antibiotic or political resistance), not electrical ohms."
    },
    "beam": {
        "tech_branch": "civil/mech",
        "tech_meaning": "Structural Beam (horizontal structural member supporting transverse loads)",
        "tech_triggers": {
            "column", "columns", "load", "loads", "concrete", "steel", "support", "supports", "bending",
            "moment", "shear", "span", "cantilever", "deflection", "truss", "foundation", "slab",
            "timber", "flange", "web", "structural", "reinforced"
        },
        "non_tech_triggers": {
            "light", "laser", "sun", "sunlight", "ray", "rays", "flashlight", "photon", "photons",
            "smile", "beaming", "optic", "optical", "projector", "broadcast"
        },
        "non_tech_rationale": "Word 'beam' denotes an optical ray of light or radiation, not a physical load-bearing structural member."
    },
    "java": {
        "tech_branch": "cs",
        "tech_meaning": "Java (high-level, class-based, object-oriented programming language and platform)",
        "tech_triggers": {
            "code", "program", "programming", "language", "class", "jvm", "compiler", "syntax",
            "object", "method", "variable", "software", "developer", "bytecode", "package", "spring"
        },
        "non_tech_triggers": {
            "coffee", "drink", "cup", "roast", "island", "indonesia", "trip", "travel", "beans"
        },
        "non_tech_rationale": "Word 'java' refers to coffee beverage or the Indonesian island, not the Java programming language."
    },
    "bus": {
        "tech_branch": "cs/eee",
        "tech_meaning": "System Bus / Busbar (communication pathway transmitting data between components, or power conductor bar)",
        "tech_triggers": {
            "processor", "cpu", "memory", "data", "address", "control", "pcie", "pci", "i2c", "spi",
            "bits", "bandwidth", "speed", "transfer", "substation", "busbar", "power", "electrical", "grid"
        },
        "non_tech_triggers": {
            "transit", "passenger", "driver", "ticket", "station", "stop", "route", "travel", "school",
            "vehicle", "commute", "ride", "passengers"
        },
        "non_tech_rationale": "Word 'bus' designates a public transit road vehicle, not a computer bus or electrical busbar."
    },
    "port": {
        "tech_branch": "cs/ece",
        "tech_meaning": "Hardware / Networking Port (interface endpoint for data input/output or socket communication)",
        "tech_triggers": {
            "usb", "ethernet", "hardware", "serial", "parallel", "i/o", "pin", "pins", "socket",
            "tcp", "udp", "connection", "device", "input", "output", "packet", "communication", "network"
        },
        "non_tech_triggers": {
            "ship", "ships", "harbor", "harbour", "cargo", "vessel", "dock", "docks", "sea", "ocean",
            "wine", "maritime", "coast", "import", "export"
        },
        "non_tech_rationale": "Word 'port' refers to a maritime harbor for ships or port wine, not a hardware/networking I/O interface."
    },
    "state": {
        "tech_branch": "cs/mech",
        "tech_meaning": "System / Thermodynamic State (complete set of operating parameters or automata condition)",
        "tech_triggers": {
            "machine", "automata", "transition", "variable", "memory", "thread", "process", "registers",
            "thermodynamic", "temperature", "pressure", "enthalpy", "entropy", "phase", "equilibrium"
        },
        "non_tech_triggers": {
            "country", "nation", "government", "delhi", "maharashtra", "california", "governor", "election",
            "politics", "province", "border", "republic"
        },
        "non_tech_rationale": "Word 'state' refers to a political geographic entity or government jurisdiction, not a machine or thermodynamic state."
    },
    "network": {
        "tech_branch": "cs/ece",
        "tech_meaning": "Computer / Electrical Network (interconnected nodes transmitting data packets or electrical power)",
        "tech_triggers": {
            "packet", "packets", "router", "routers", "switch", "protocol", "ip", "tcp", "lan", "wan",
            "bandwidth", "topology", "node", "nodes", "graph", "circuits", "grid", "transmission"
        },
        "non_tech_triggers": {
            "social", "friends", "networking", "colleagues", "linkedin", "party", "mingle", "meetup", "family"
        },
        "non_tech_rationale": "Word 'network' indicates human interpersonal social networking, not a technical data or power network."
    }
}

class EngineeringNLPEngine:
    """
    Modular Natural Language Processing Engine for Engineering Education.
    Performs tokenization, lemmatization, POS tagging, polysemy disambiguation,
    and semantic triple extraction.
    """

    @staticmethod
    def tokenize(text: str) -> List[Dict[str, Any]]:
        """
        Tokenizes raw text into structured tokens with basic grammatical classification.
        """
        # Match words, numbers, hyphenated engineering terms, contractions
        raw_tokens = re.findall(r"\b[A-Za-z0-9_\-]+(?:\'[A-Za-z]+)?\b|[.,!?;:]", text.strip())
        tokens: List[Dict[str, Any]] = []

        for idx, token_str in enumerate(raw_tokens):
            lower = token_str.lower()
            pos = POS_NOUN
            lemma = lower

            # Punctuation check
            if re.match(r"^[.,!?;:]$", token_str):
                pos = POS_PUNCT
                lemma = token_str
            elif re.match(r"^\d+(?:\.\d+)?$", token_str):
                pos = POS_NUM
                lemma = token_str
            elif lower in DETERMINERS:
                pos = POS_DET
                lemma = lower
            elif lower in PREPOSITIONS:
                pos = POS_ADP
                lemma = lower
            elif lower in COORDINATING_CONJUNCTIONS:
                pos = POS_CCONJ
                lemma = lower
            elif lower in SUBORDINATING_CONJUNCTIONS:
                pos = POS_SCONJ
                lemma = lower
            elif lower in AUXILIARY_VERBS:
                pos = POS_AUX
                lemma = EngineeringNLPEngine._lemmatize_verb(lower)
            elif lower in PRONOUNS:
                pos = POS_PRON
                lemma = lower
            elif EngineeringNLPEngine._is_common_verb(lower):
                pos = POS_VERB
                lemma = EngineeringNLPEngine._lemmatize_verb(lower)
            elif EngineeringNLPEngine._is_common_adjective(lower):
                pos = POS_ADJ
                lemma = lower
            else:
                # Default noun / proper noun; lemmatize plural
                lemma = EngineeringNLPEngine._lemmatize_noun(lower)
                if token_str.isupper() and len(token_str) > 1:
                    pos = POS_PROPN

            tokens.append({
                "index": idx,
                "text": token_str,
                "lemma": lemma,
                "pos": pos,
                "is_stop": lower in (DETERMINERS | PREPOSITIONS | AUXILIARY_VERBS | PRONOUNS)
            })

        return tokens

    @staticmethod
    def _lemmatize_noun(word: str) -> str:
        """Strips regular and irregular English plural inflections."""
        irregular_plurals = {
            "matrices": "matrix", "vertices": "vertex", "indices": "index",
            "analyses": "analysis", "hypotheses": "hypothesis", "bases": "base",
            "criteria": "criterion", "phenomena": "phenomenon", "data": "data"
        }
        if word in irregular_plurals:
            return irregular_plurals[word]
        if word.endswith("ies") and len(word) > 4:
            return word[:-3] + "y"
        if word.endswith("es") and len(word) > 3:
            if word.endswith(("sses", "shes", "ches", "xes", "zes")):
                return word[:-2]
            return word[:-1]
        if word.endswith("s") and not word.endswith("ss") and len(word) > 2:
            return word[:-1]
        return word

    @staticmethod
    def _lemmatize_verb(word: str) -> str:
        """Reduces verb inflections to root lemma form."""
        irregular_verbs = {
            "is": "be", "am": "be", "are": "be", "was": "be", "were": "be",
            "has": "have", "had": "have", "does": "do", "did": "do",
            "stored": "store", "driven": "drive", "drove": "drive", "drives": "drive",
            "flows": "flow", "flowed": "flow", "induces": "induce", "induced": "induce",
            "executes": "execute", "executed": "execute", "executing": "execute",
            "transfers": "transfer", "transferred": "transfer", "transferring": "transfer",
            "calculates": "calculate", "calculated": "calculate", "calculating": "calculate",
            "manages": "manage", "managed": "manage", "managing": "manage",
            "translates": "translate", "translated": "translate", "translating": "translate",
            "converts": "convert", "converted": "convert", "converting": "convert",
            "modulates": "modulate", "modulated": "modulate", "modulating": "modulate",
            "operates": "operate", "operated": "operate", "operating": "operate"
        }
        if word in irregular_verbs:
            return irregular_verbs[word]
        if word.endswith("ing") and len(word) > 4:
            base = word[:-3]
            if len(base) > 2 and base[-1] == base[-2]:
                return base[:-1] # transferring -> transfer
            if base + "e" in irregular_verbs or base.endswith(("at", "iz", "us")):
                return base + "e"
            return base
        if word.endswith("ed") and len(word) > 3:
            base = word[:-2]
            if len(base) > 2 and base[-1] == base[-2]:
                return base[:-1]
            if base + "e" in irregular_verbs:
                return base + "e"
            return base
        if word.endswith("s") and not word.endswith("ss") and len(word) > 2:
            if word.endswith("es"):
                return word[:-2]
            return word[:-1]
        return word

    @staticmethod
    def _is_common_verb(word: str) -> bool:
        verbs = {
            "execute", "executes", "executed", "executing", "store", "stores", "stored", "storing",
            "flow", "flows", "flowed", "flowing", "induce", "induces", "induced", "inducing",
            "drive", "drives", "drove", "driven", "driving", "transfer", "transfers", "transferred",
            "calculate", "calculates", "calculated", "manage", "manages", "managed",
            "convert", "converts", "converted", "translate", "translates", "translated",
            "modulate", "modulates", "modulated", "operate", "operates", "operated",
            "oppose", "opposes", "opposed", "generate", "generates", "generated",
            "connect", "connects", "connected", "transmit", "transmits", "transmitted",
            "apply", "applies", "applied", "support", "supports", "supported",
            "produce", "produces", "produced", "cause", "causes", "caused"
        }
        return word in verbs

    @staticmethod
    def _is_common_adjective(word: str) -> bool:
        adjs = {
            "electrical", "mechanical", "magnetic", "structural", "optical", "thermal",
            "high", "low", "constant", "variable", "direct", "alternating", "digital",
            "analog", "linear", "rotational", "horizontal", "vertical", "elastic", "plastic"
        }
        return word in adjs

    @staticmethod
    def disambiguate_term(
        term: str,
        sentence_text: str,
        explicit_branch_code: Optional[str] = None
    ) -> Tuple[bool, str, float]:
        """
        Disambiguates polysemous words against domain context.
        Returns: (is_valid_technical, rationale, confidence)
        """
        lower_term = term.lower()
        if lower_term not in DISAMBIGUATION_SPECS:
            return True, f"Standard technical term '{term}' registered.", 1.0

        spec = DISAMBIGUATION_SPECS[lower_term]
        tokens = set(re.findall(r"\b\w+\b", sentence_text.lower()))

        tech_overlap = tokens.intersection(spec["tech_triggers"])
        non_tech_overlap = tokens.intersection(spec["non_tech_triggers"])

        # Explicit branch override
        if explicit_branch_code:
            branch_branches = spec["tech_branch"].split("/")
            if explicit_branch_code.lower() in branch_branches:
                return True, f"Explicit branch '{explicit_branch_code.upper()}' validates technical sense of '{term}'.", 0.99

        # Strong non-technical indicators present without technical triggers
        if non_tech_overlap and not tech_overlap:
            matched_trigger = list(non_tech_overlap)[0]
            rationale = f"{spec['non_tech_rationale']} (Context indicator: '{matched_trigger}')."
            return False, rationale, 0.95

        # Strong technical indicators present
        if tech_overlap:
            matched_sample = list(tech_overlap)[:3]
            rationale = f"Validated as {spec['tech_meaning']} supported by context: {matched_sample}."
            return True, rationale, 0.98

        # Fallback in engineering system
        return True, f"Identified as {spec['tech_meaning']} in engineering context.", 0.75

    @staticmethod
    def extract_semantic_triples(
        sentence_text: str,
        detected_concepts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Extracts Subject-Predicate-Object triples linking interacting engineering concepts.
        Supports both syntactic pattern matching and engineering relational knowledge.
        """
        triples: List[Dict[str, Any]] = []
        if not detected_concepts:
            return triples

        normalized_text = f" {sentence_text.lower()} "

        # 1. Direct syntactic patterns linking two concepts
        # Pattern: [Concept1] ... [Verb/Relation] ... [Concept2]
        relation_patterns = [
            (r"\bexecutes\b", "executes", "executes instructions / operations on"),
            (r"\bstored\s+in\b", "stored_in", "is stored within memory location"),
            (r"\bdrives\s+(?:the\s+)?flow\s+of\b", "drives_flow_of", "drives the flow of electrical charge"),
            (r"\bdrives\b", "drives", "drives the operation of"),
            (r"\bopposed\s+by\b", "opposed_by", "flow is resisted or opposed by"),
            (r"\bproportional\s+to\b", "proportional_to", "is directly or inversely proportional to"),
            (r"\bsteps\s+up\b", "steps_up", "steps up voltage level to higher potential"),
            (r"\bsteps\s+down\b", "steps_down", "steps down voltage level to lower potential"),
            (r"\btransfers\s+load\s+to\b", "transfers_load_to", "transfers compressive/shear load to"),
            (r"\btransfers\b", "transfers", "transfers load, energy, or data to"),
            (r"\bconverts\s+to\b", "converts_to", "converts input energy into output energy form"),
            (r"\btranslates\b", "translates", "translates high-level source to machine target"),
            (r"\bmanages\b", "manages", "allocates and manages hardware resources for"),
            (r"\binduces\b", "induces", "induces electromotive force or current in"),
            (r"\bcauses\b", "causes", "causes mechanical deformation or change in state"),
            (r"\bproduces\b", "produces", "produces stress, torque, or magnetic flux"),
            (r"\bmodulates\b", "modulates", "modulates carrier wave parameters with message signal"),
            (r"\bflows\s+through\b", "flows_through", "flows through conductive material or circuit"),
            (r"\bconnects\s+to\b", "connects_to", "interfaces and connects with")
        ]

        # Concept pairs in sentence order
        concepts_in_order = []
        for c in detected_concepts:
            pattern = r"\b" + re.escape(c.lower()) + r"(?:s|es)?\b"
            m = re.search(pattern, normalized_text)
            if m:
                concepts_in_order.append((m.start(), c))
        concepts_in_order.sort(key=lambda x: x[0])

        # Check adjacent or interacting pairs in sentence
        for i in range(len(concepts_in_order) - 1):
            c1 = concepts_in_order[i][1]
            c2 = concepts_in_order[i + 1][1]
            start_pos = concepts_in_order[i][0]
            end_pos = concepts_in_order[i + 1][0]
            between_text = normalized_text[start_pos:end_pos + len(c2) + 2]

            matched_pattern = False
            for pat, rel_type, rel_desc in relation_patterns:
                if re.search(pat, between_text):
                    triples.append({
                        "source_concept": c1,
                        "target_concept": c2,
                        "relation_type": rel_type,
                        "description": f"{c1} {rel_desc} {c2}.",
                        "triple_string": f"[{c1}] -> [{rel_type}] -> [{c2}]",
                        "confidence": 0.95
                    })
                    matched_pattern = True
                    break

        # 2. Also check for multi-hop secondary clauses: e.g. "instructions stored in memory"
        # If text has "stored in" and a third concept exists
        if "stored in" in normalized_text or "stored within" in normalized_text:
            for c_src in detected_concepts:
                for c_dest in detected_concepts:
                    if c_src != c_dest:
                        pattern = rf"\b{re.escape(c_src.lower())}(?:s|es)?\b.*?\bstored\s+in\b.*?\b{re.escape(c_dest.lower())}(?:s|es)?\b"
                        if re.search(pattern, normalized_text):
                            existing = any(t["source_concept"] == c_src and t["target_concept"] == c_dest for t in triples)
                            if not existing:
                                triples.append({
                                    "source_concept": c_src,
                                    "target_concept": c_dest,
                                    "relation_type": "stored_in",
                                    "description": f"{c_src} is stored within {c_dest}.",
                                    "triple_string": f"[{c_src}] -> [stored_in] -> [{c_dest}]",
                                    "confidence": 0.94
                                })

        # 3. Known domain relational defaults if syntactic matching did not find connection
        # E.g. Processor and Memory, Voltage and Current, Beam and Column
        if not triples and len(detected_concepts) >= 2:
            from backend.app.translation.semantic_analyzer import SEMANTIC_RELATION_RULES
            concept_set = set(detected_concepts)
            for (c1, c2), rel_type, desc in SEMANTIC_RELATION_RULES:
                if c1 in concept_set and c2 in concept_set:
                    triples.append({
                        "source_concept": c1,
                        "target_concept": c2,
                        "relation_type": rel_type,
                        "description": desc,
                        "triple_string": f"[{c1}] -> [{rel_type}] -> [{c2}]",
                        "confidence": 0.90
                    })

        return triples
