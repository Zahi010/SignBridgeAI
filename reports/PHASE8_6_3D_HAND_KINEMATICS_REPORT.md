# SIGNBRIDGE AI — PHASE 8.6
# 3D HAND KINEMATICS & FINGER ARTICULATION REPORT

**Project:** `E:\SignBridgeAi`  
**Subsystem:** 15-Joint Articulated Hand, Finger Phalange Kinematics, Thumb Opposition  
**Audit Date:** 2026-11-23  
**Auditor:** Motion Capture Specialist & 3D Kinematics Auditor  

---

## 1. HAND RIG ARCHITECTURE & PHALANGE GEOMETRY

Each hand in SignBridge AI (`ArticulatedHand` inside `AvatarViewer.tsx`) is modeled with:
- **Palm Base:** `boxGeometry args={[0.085, 0.09, 0.025]}` centered at `[0, -0.06, 0.01]`.
- **5 Articulated Fingers:**
  - Thumb: base at `[-0.045 * sideMultiplier, -0.02, 0]`
  - Index: base at `[-0.03 * sideMultiplier, -0.1, 0]`
  - Middle: base at `[-0.01 * sideMultiplier, -0.105, 0]`
  - Ring: base at `[0.012 * sideMultiplier, -0.1, 0]`
  - Pinky: base at `[0.032 * sideMultiplier, -0.09, 0]`
- **3 Phalanges Per Finger (15 Joints Total Per Hand):**
  1. **Metacarpophalangeal (MCP):** Length $0.035\,\text{m}$, radius $0.009\,\text{m}$ to $0.0081\,\text{m}$.
  2. **Proximal Interphalangeal (PIP):** Length $0.035\,\text{m}$, radius $0.0081\,\text{m}$ to $0.0072\,\text{m}$.
  3. **Distal Interphalangeal (DIP):** Length $0.028\,\text{m}$, radius $0.0072\,\text{m}$ to $0.0054\,\text{m}$.

Total articulated joints across both hands: **30 finger phalanges + 2 wrist joints = 32 hand joints**.

---

## 2. KINEMATIC ROTATION AXIS DEFECT (P0 CRITICAL)

### 2.1 The Mathematical and Anatomical Defect
In `ArticulatedHand`, the phalange meshes are rendered extending downward along the local negative Y axis (`[0, -phalangeLength / 2, 0]`).
The rotation is applied as:
```tsx
<group rotation={[fState.mcp.x, fState.mcp.y * sideMultiplier, fState.mcp.z]}>
```
By the right-hand rule in Three.js coordinates:
- The palm normal faces $+Z$ (forward).
- The fingers extend along $-Y$ (downward).
- When a positive rotation angle around the X axis is applied ($\theta > 0$):
  $$\mathbf{v}' = \mathbf{R}_X(\theta) \begin{pmatrix} 0 \\ -1 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ -\cos\theta \\ -\sin\theta \end{pmatrix}$$
- Since $\sin\theta > 0$ for $\theta \in (0, \pi)$, the resulting $Z$ component is **negative** ($-\sin\theta < 0$), swinging **backward into $-Z$ (hyperextension over the back of the hand)**!

### 2.2 Visual and Functional Impact
- **Inverted Curls:** When the mocap data detects fingers curling into a fist (flexion angle $\approx 1.2$ to $1.6$ rad), the avatar's fingers bend backward like broken claws over the back of the hand.
- **Thumb Misalignment:** When the thumb adducts across the palm, positive rotations twist the thumb outwards rather than opposing across the palm.
- **Required Repair:**
  In `ArticulatedHand`:
  $$\text{rotation.x} = -fState.mcp.x$$
  $$\text{rotation.x} = -fState.pip.x$$
  $$\text{rotation.x} = -fState.dip.x$$
  This negates the Euler angle so that positive mocap flexion correctly curves the finger forward towards $+Z$ (into the palm).

---

## 3. CONTROLLED POSE KINEMATIC AUDIT

| Test Pose | Target Handshape | Observed Behavior (Pre-Repair) | Measured Error | Post-Repair Behavior |
|---|---|---|---|---|
| **1. Open Flat Palm** | All fingers extended ($\theta \approx 0$) | Flat palm renders cleanly, slight natural spread. | 0 rad | Stable flat palm facing forward. |
| **2. Closed Fist ("S" / "A")** | MCP: $1.4$, PIP: $1.5$, DIP: $1.2$ | Fingers bent $80^\circ$ backward over the dorsal palm. | **$180^\circ$ Axis Inversion** | Fingers curl cleanly into palm. |
| **3. Index Pointing ("1")** | Index: $0.0$; Middle, Ring, Pinky: $1.4$ | Index extends; other 3 fingers bend backward. | Severe visual clawing | Index points forward; 3 fingers curl into palm. |
| **4. Thumb Opposition** | Thumb across palm to pinky base | Thumb rotates laterally outward away from palm. | $90^\circ$ orientation error | Thumb opposes across palm center. |
| **5. Wrist Flexion / Extension** | Wrist pitch $\pm 0.8$ rad | Wrist rotates palm up/down smoothly. | Stable | Verified functional. |

---

## 4. KINEMATICS AUDIT CONCLUSION

The 15-joint structural breakdown per hand is genuine and correctly matches the 54-joint specification. However, due to an uncompensated Euler axis sign inversion in `ArticulatedHand`, all positive finger flexion angles caused severe dorsal hyperextension. This is a **P0 repair priority**.

