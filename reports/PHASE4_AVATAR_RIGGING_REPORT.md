# Phase 4 Avatar Rigging & Character Architecture Specification

**Standard:** SignBridge-Articulated-54 Skeletal Hierarchy  
**Coordinate System:** Three.js Standard Right-Handed (X: Right, Y: Up, Z: Out towards camera)  
**Applicability:** Indian Sign Language (ISL) Engineering Translation Platform  
**Compliance:** Zero-Fabrication Rigging Policy

---

## 1. Skeletal Joint Hierarchy (54 Points)

Indian Sign Language requires precise phonological articulation. The four primary manual parameters (Handshape, Location, Movement, Orientation) demand independent control over shoulder, arm, forearm, wrist, and 15 finger phalanges per hand.

```
Root (Hips / Base)
 └── Spine
      └── Spine1 (Lower Chest)
           └── Chest (Spine2 / Upper Torso)
                ├── Neck
                │    └── Head
                │         ├── LeftEyeTarget / RightEyeTarget
                │         └── Non-Manual Facial Morph Targets (Blendshapes)
                ├── LeftClavicle (LeftShoulder)
                │    └── LeftUpperArm (LeftArm)
                │         └── LeftForearm (LeftForeArm)
                │              └── LeftWrist (LeftHand)
                │                   ├── LeftThumbCMC ── LeftThumbMCP ── LeftThumbIP
                │                   ├── LeftIndexMCP ── LeftIndexPIP ── LeftIndexDIP
                │                   ├── LeftMiddleMCP ── LeftMiddlePIP ── LeftMiddleDIP
                │                   ├── LeftRingMCP ── LeftRingPIP ── LeftRingDIP
                │                   └── LeftPinkyMCP ── LeftPinkyPIP ── LeftPinkyDIP
                └── RightClavicle (RightShoulder)
                     └── RightUpperArm (RightArm)
                          └── RightForearm (RightForeArm)
                               └── RightWrist (RightHand)
                                    ├── RightThumbCMC ── RightThumbMCP ── RightThumbIP
                                    ├── RightIndexMCP ── RightIndexPIP ── RightIndexDIP
                                    ├── RightMiddleMCP ── RightMiddlePIP ── RightMiddleDIP
                                    ├── RightRingMCP ── RightRingPIP ── RightRingDIP
                                    └── RightPinkyMCP ── RightPinkyPIP ── RightPinkyDIP
```

---

## 2. Hand & Finger Articulation (30 Joints)

In ISL, minimal finger variations distinguish distinct phonemes (e.g. 1-handshape vs B-handshape vs V-handshape). Each finger comprises three anatomical degrees of freedom:

| Finger | Joint Segment | Anatomical Name | Primary Motion | Flexion Range (rad) | Abduction Range (rad) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Thumb** | Proximal | Carpometacarpal (CMC) | Palmar abduction & opposition | 0.0 to 0.8 rad | -0.4 to 0.6 rad |
| | Intermediate | Metacarpophalangeal (MCP) | Flexion / Extension | 0.0 to 1.1 rad | -0.1 to 0.1 rad |
| | Distal | Interphalangeal (IP) | Terminal flexion | 0.0 to 1.4 rad | Fixed (Hinge) |
| **Index** | Proximal | Metacarpophalangeal (MCP) | Knuckle flexion / spread | 0.0 to 1.6 rad | -0.3 to 0.3 rad |
| | Intermediate | Proximal Interphalangeal (PIP) | Mid-joint flexion | 0.0 to 1.8 rad | Fixed (Hinge) |
| | Distal | Distal Interphalangeal (DIP) | Fingertip flexion | 0.0 to 1.3 rad | Fixed (Hinge) |
| **Middle** | Proximal | Metacarpophalangeal (MCP) | Knuckle flexion / spread | 0.0 to 1.6 rad | -0.2 to 0.2 rad |
| | Intermediate | Proximal Interphalangeal (PIP) | Mid-joint flexion | 0.0 to 1.8 rad | Fixed (Hinge) |
| | Distal | Distal Interphalangeal (DIP) | Fingertip flexion | 0.0 to 1.3 rad | Fixed (Hinge) |
| **Ring** | Proximal | Metacarpophalangeal (MCP) | Knuckle flexion / spread | 0.0 to 1.6 rad | -0.2 to 0.2 rad |
| | Intermediate | Proximal Interphalangeal (PIP) | Mid-joint flexion | 0.0 to 1.8 rad | Fixed (Hinge) |
| | Distal | Distal Interphalangeal (DIP) | Fingertip flexion | 0.0 to 1.3 rad | Fixed (Hinge) |
| **Pinky** | Proximal | Metacarpophalangeal (MCP) | Knuckle flexion / spread | 0.0 to 1.6 rad | -0.3 to 0.4 rad |
| | Intermediate | Proximal Interphalangeal (PIP) | Mid-joint flexion | 0.0 to 1.8 rad | Fixed (Hinge) |
| | Distal | Distal Interphalangeal (DIP) | Fingertip flexion | 0.0 to 1.3 rad | Fixed (Hinge) |

---

## 3. Anatomical Joint Limits & Clamping Matrix

To prevent physically impossible or jarring avatar poses ("broken arms" or hyper-extended elbows), all retargeted bone rotations must pass through strict physiological limit clamps:

```json
{
  "chest": {
    "pitch": [-0.35, 0.35],
    "yaw": [-0.52, 0.52],
    "roll": [-0.26, 0.26]
  },
  "neck": {
    "pitch": [-0.52, 0.60],
    "yaw": [-0.78, 0.78],
    "roll": [-0.44, 0.44]
  },
  "shoulder": {
    "pitch": [-1.57, 2.35],
    "yaw": [-1.57, 1.57],
    "roll": [-1.75, 1.75]
  },
  "elbow": {
    "flexion": [0.0, 2.62],
    "hyperextension": [0.0, 0.05],
    "pronation_supination": [-1.57, 1.57]
  },
  "wrist": {
    "flexion_extension": [-1.22, 1.22],
    "radial_ulnar_deviation": [-0.52, 0.70]
  }
}
```

---

## 4. Facial Non-Manual Markers (NMM) & Morph Targets

In Indian Sign Language, non-manual signals are grammatical morphemes, not emotional decorations. The rig supports 8 discrete morph targets:

1. `brow_furrow_left` / `brow_furrow_right`: Lowering and drawing together of brows.
   - Grammatical Function: WH-interrogatives (WHAT, WHERE, WHY, HOW, WHEN) and negative declarations.
2. `brow_raise_left` / `brow_raise_right`: Raising of eyebrows with slight head forward thrust.
   - Grammatical Function: Polar (Yes/No) questions, conditional clauses ("IF ... THEN"), topic markers.
3. `mouth_open`: Mandible depression.
   - Grammatical Function: Mouthing of technical acronyms or open vowel morphemes.
4. `mouth_wide`: Lateral retraction of lips.
   - Grammatical Function: Intensity / precision morpheme (e.g. "exact limit", "narrow beam").
5. `eye_blink_left` / `eye_blink_right`: Natural corneal hydration and intentional emphatic eye closures at prosodic boundaries.
6. `head_pitch` / `head_yaw` / `head_roll`: Head nodding (affirmation), head shaking (negation), and head tilt toward spatial reference loci.

---

## 5. Rest Pose Specification (Attentive Neutral Posture)

When no verified motion is executing, the avatar returns to the **Attentive Neutral Posture**:
- **Arms:** Upper arms hang relaxed at ~20° lateral angle, forearms resting at ~30° flexion, hands held in the lower signing quadrant (lap/lower abdomen level).
- **Fingers:** Naturally relaxed in slight loose flexion (10-15°), thumbs resting against the index side without tension.
- **Head:** Upright, facing the user directly with gentle periodic micro-movements (simulating attentive human posture).
- **Zero-Fabrication Safeguard:** Hand movements are never synthesized or randomly oscillated. Only subtle diaphragm breathing is applied to the torso mesh.

