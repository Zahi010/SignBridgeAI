# SignBridge AI — Indian Sign Language Knowledge Base Architecture

**Document Version:** 2.0.0  
**Effective Date:** November 19, 2026  
**Standards:** Zero Fabricated Signs Policy, Relational Provenance Tracking, Pan-Indian ISL Linguistic Parameters

---

## 1. Overview & Architectural Principles

The SignBridge AI Knowledge Base serves as the authoritative lexical and phonological foundation for technical engineering translation into Indian Sign Language (ISL). 

### Foundational Principles:
1. **Linguistic Authenticity:** Signs are codified based on established ISLRTC dictionary records and accredited deaf education glossaries.
2. **Transparent Validation Lifecycle:** Every sign holds an explicit validation status (`VERIFIED`, `PARTIAL`, `NEEDS_REVIEW`, `EXPLANATION_REQUIRED`, `UNSUPPORTED`).
3. **Phonological Parameter Completeness:** In accordance with sign linguistics (Stokoe / HamNoSys taxonomy), each sign records handshape, location, movement, orientation, dominant hand, and non-manual markers.
4. **Relational Traceability:** Each sign maps to an accredited Engineering Branch, Subject Code, Source Dataset, and Review Audit Trail.

---

## 2. Knowledge Base Schema & Entity Relationships

```
EngineeringBranch (1) ──< Subject (N) ──< Concept (N) ──< SignRecord (N)
                                                               │
                       ┌───────────────────────────────────────┼────────────────────────────────────────┐
                       │                                       │                                        │
             DatasetProvenance (1)                   SignVideo (N)                               ReviewerValidation (N)
                                                                                                        │
                                                                                              [Audit Trail of Decisions]
```

### 2.1 Phonological & Linguistic Parameter Attributes
Every `SignRecord` supports:
- `sign_id`: Unique hierarchical identifier (e.g. `ISL-CS-001`, `ISL-ECE-015`).
- `sign_gloss`: Standardized ISL gloss notation in all-caps (e.g., `DATABASE`, `VOLTAGE`).
- `dominant_hand`: Single-hand (`Right`, `Left`), `Two-Handed`, or `Symmetric`.
- `handshape`: Descriptive notation of active finger geometry (e.g., `Bent-C hands`, `Flat B-Handshape`).
- `movement`: Trajectory, dynamic repetition, and oscillation patterns.
- `location`: Anatomical signing space (e.g., `Neutral space in front of torso`, `Chin level`).
- `orientation`: Palm and finger direction relative to the signer's torso.
- `non_manual_markers`: Facial expressions, head tilts, and mouth morphemes.

---

## 3. Initial 100 Candidate Engineering Concepts

The knowledge base seeds an initial structured vocabulary of **100 candidate engineering concepts** spanning 5 core branches and 23 curricular subjects:

| Engineering Branch | Code | Curricular Subjects | Concept Count | Verified Status | Needs Review | Partial | Explanation Needed | Unsupported |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Computer Science & Engineering** | `cs` | CS201, CS301, CS302, CS303, CS304, CS401 | 20 | 8 | 5 | 3 | 2 | 2 |
| **Electronics & Communication** | `ece` | EC201, EC202, EC301, EC302 | 20 | 8 | 8 | 2 | 0 | 2 |
| **Mechanical Engineering** | `mech` | ME201, ME202, ME301, ME302 | 20 | 9 | 6 | 3 | 1 | 1 |
| **Civil Engineering** | `civil` | CE201, CE202, CE301, CE302, CE303 | 20 | 7 | 8 | 2 | 0 | 3 |
| **Electrical & Electronics** | `eee` | EE201, EE301, EE302, EE303 | 20 | 8 | 8 | 3 | 0 | 1 |
| **Total Registry** | — | **23 Subjects** | **100** | **40** | **35** | **13** | **3** | **9** |

---

## 4. Curricular Subject Mapping

### Computer Science & Engineering:
- `CS201` Data Structures & Algorithms: Algorithm, Programming, Data Structure, Pointer, Recursion, Stack.
- `CS301` Operating Systems: Operating System, Processor, Memory, Deadlock, Hardware, Cache, Thread, Virtual Memory.
- `CS302` Database Management Systems: Database.
- `CS303` Computer Networks: Computer Network.
- `CS304` Compiler Design & Systems: Compiler.
- `CS401` Distributed Systems & Cloud: Encryption, Cloud Computing.

### Electronics & Communication Engineering:
- `EC201` Circuit Theory & Analysis: Voltage, Current, Resistance, Capacitance, Inductance, Circuit.
- `EC202` Electronic Devices & Semiconductors: Diode, Transistor, Amplifier, Semiconductor, Oscillator, Rectifier.
- `EC301` Microprocessors & Microcontrollers: Microprocessor, Logic Gate, Sensor.
- `EC302` Communication Systems & Signals: Signal, Frequency, Modulation, Antenna, Bandwidth.

### Mechanical Engineering:
- `ME201` Engineering Mechanics: Force, Motion, Torque, Friction, Power, Velocity, Acceleration, Stress, Strain, Momentum.
- `ME202` Thermodynamics & Heat Transfer: Energy, Thermodynamics, Heat Transfer.
- `ME301` Theory of Machines: Machine, Gear, Engine.
- `ME302` Fluid Mechanics & Turbomachinery: Pressure, Turbine, Viscosity, Fluid Mechanics.

### Civil Engineering:
- `CE201` Building Materials: Concrete, Reinforcement, Cement, Mortar, Tensile Strength.
- `CE202` Surveying & Geomatics: Surveying.
- `CE301` Structural Analysis: Structure, Beam, Column, Load, Shear, Bracing, Abutment.
- `CE302` Geotechnical Engineering: Foundation, Soil Mechanics, Compaction, Settlement, Retaining Wall.
- `CE303` Hydraulics & Water Resources: Hydrology, Drainage.

### Electrical & Electronics Engineering:
- `EE201` Electromagnetic Fields & Circuits: Alternating Current, Direct Current, Induction, Magnetic Flux, Electrical Impedance, Phasor.
- `EE301` Electrical Machines: Transformer, Motor, Generator, Armature.
- `EE302` Power Systems: Electricity, Power System, Distribution, Transmission, Circuit Breaker, Relay, Substation, Power Grid, Electrical Grounding.
- `EE303` Power Electronics & Drives: Inverter.

---

## 5. Lexical Access & Search API

- `GET /api/v1/vocabulary`: Full search and filtering by term, branch, and validation status.
- `GET /api/v1/vocabulary/{concept_id}`: Granular concept detail with phonological metadata.
- `GET /api/v1/signs/{concept_id}`: Dedicated sign retrieval for video and avatar engines.

---

*Document certified by Lead AI Engineer & Technical Architect on November 19, 2026.*
