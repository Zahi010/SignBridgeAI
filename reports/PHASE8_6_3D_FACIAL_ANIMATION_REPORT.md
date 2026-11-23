# SIGNBRIDGE AI — PHASE 8.6
# FACIAL ANIMATION & NON-MANUAL MARKERS (NMM) REPORT

**Project:** `E:\SignBridgeAi`  
**Subsystem:** Facial Mesh Controls, Morph Targets, Grammatical ISL Markers  
**Audit Date:** 2026-11-23  
**Auditor:** ISL Linguistics Researcher & Facial Animation Systems Engineer  

---

## 1. FACIAL RIG ARCHITECTURE AUDIT

In `AvatarViewer.tsx`, the head and face assembly consists of:
- **Cranium:** `sphereGeometry args={[0.18, 24, 24]}`
- **Hair Cap:** `sphereGeometry args={[0.19, 20, 20]}`
- **Eyes (Left / Right):** `sphereGeometry args={[0.02, 12, 12]}`
- **Eyebrows (Left / Right):** `boxGeometry args={[0.05, 0.012, 0.02]}` (`leftEyebrowRef`, `rightEyebrowRef`)
- **Nose:** `coneGeometry args={[0.025, 0.05, 12]}`
- **Mouth:** `boxGeometry args={[0.05, 0.015, 0.015]}` (`mouthRef`)

### 1.1 Deformation Mechanism
There are **no GPU morph target vertex blendshapes** (e.g., glTF morph targets).
Instead, Non-Manual Markers (NMM) are applied procedurally in `useFrame`:
```typescript
const nmm = currentKeyframe.facial_blendshapes;
if (nmm) {
  // Eyebrow vertical displacement
  if (leftEyebrowRef.current && rightEyebrowRef.current) {
    const browOffsetY = (nmm.brow_raise_left - nmm.brow_furrow_left) * 0.025;
    leftEyebrowRef.current.position.y = 0.08 + browOffsetY;
    rightEyebrowRef.current.position.y = 0.08 + browOffsetY;
  }
  // Mouth opening and widening scale
  if (mouthRef.current) {
    const mouthScaleY = 1.0 + nmm.mouth_open * 2.5;
    const mouthScaleX = 1.0 + nmm.mouth_wide * 1.5;
    mouthRef.current.scale.set(mouthScaleX, mouthScaleY, 1.0);
  }
}
```

---

## 2. ISL GRAMMATICAL NON-MANUAL MARKERS EVALUATION

In Indian Sign Language, non-manual markers on the face are not decorative; they are obligatory grammatical morphemes indicating clause type, negation, topicalization, and conditional clauses.

| Grammatical Marker | Target Linguistic Trigger | Rig Implementation | Evaluated Behavior | Linguistic Fidelity Verdict |
|---|---|---|---|---|
| **WH-Question (Furrowed Brow)** | Questions with interrogative pronouns ("What", "Who", "Where") | `brow_furrow_left = 0.85` | Eyebrow boxes lower by $-0.021\,\text{m}$. | **PARTIALLY FUNCTIONAL** (Geometric proxy indicates furrow, but lacks glabella frowning creasing). |
| **Polar Question (Raised Brow + Head Tilt)** | Yes/No interrogative questions | `brow_raise_left = 0.80`, `head_pitch = 0.15` | Eyebrow boxes elevate $+0.020\,\text{m}$; head nods forward. | **PARTIALLY FUNCTIONAL** (Clear upward displacement, visible in front camera). |
| **Mouthing / Mouth Open** | Syllable articulation / technical gloss timing | `mouth_open = 0.65` | Mouth box expands vertically by $2.6\times$. | **PRIMITIVE PROXY** (Opens vertically, but cannot articulate labial or dental consonants). |
| **Head Shake (Negation)** | Negative declarative sentences | `head_yaw = \pm 0.25` | Head rotates around Y axis. | **FUNCTIONAL** (Smooth rotational oscillation). |

---

## 3. AUDIT CONCLUSION & LIMITATIONS DISCLOSURE

1. The facial controls are mechanically connected and successfully deform based on incoming keyframes.
2. They function adequately as **symbolic grammatical indicators** for an engineering research prototype.
3. However, they **do not constitute natural human facial signing** and must be honestly disclosed as geometric proxy markers rather than production-grade expressive facial performance.
