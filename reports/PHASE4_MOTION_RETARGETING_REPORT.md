# Phase 4 Motion Retargeting Engine Report

**Module:** `backend/app/services/motion_retargeting_service.py`  
**Target Rig:** SignBridge-Articulated-54 Skeletal Avatar  
**Status:** Operational  

---

## 1. Retargeting Objective

The motion retargeting engine solves the inverse and forward kinematics problem of mapping raw 3D landmark points into hierarchical Euler rotations for the 3D humanoid avatar.

---

## 2. Upper-Body Kinematics Solving

For each arm segment:
1. **Upper Arm Vector:** $\mathbf{v}_{upper} = \mathbf{P}_{elbow} - \mathbf{P}_{shoulder}$
2. **Elevation (Pitch):** $\theta_{pitch} = \text{atan2}(v_z, -v_y)$
3. **Abduction (Yaw):** $\theta_{yaw} = \text{atan2}(v_x, -v_y)$
4. **Forearm Vector:** $\mathbf{v}_{fore} = \mathbf{P}_{wrist} - \mathbf{P}_{elbow}$
5. **Elbow Flexion:**
   $$\theta_{flexion} = \arccos\left(\frac{\mathbf{v}_{upper} \cdot \mathbf{v}_{fore}}{\|\mathbf{v}_{upper}\| \|\mathbf{v}_{fore}\|}\right)$$

---

## 3. Finger Phalange Kinematics (15 Joints per Hand)

Finger articulation distinguishes ISL handshapes. For each finger:
- **Metacarpophalangeal (MCP):** Angle between Palm Vector ($\mathbf{P}_{wrist} \to \mathbf{P}_{MCP}$) and Proximal Vector ($\mathbf{P}_{MCP} \to \mathbf{P}_{PIP}$).
- **Proximal Interphalangeal (PIP):** Angle between Proximal Vector and Intermediate Vector ($\mathbf{P}_{PIP} \to \mathbf{P}_{DIP}$).
- **Distal Interphalangeal (DIP):** Angle between Intermediate Vector and Distal Vector ($\mathbf{P}_{DIP} \to \mathbf{P}_{TIP}$).

### Handshape Examples Retargeted:
- **Open 5-Handshape (as in `FREQUENCY`):** All MCP, PIP, DIP angles near $0.0\text{ rad}$ (extended).
- **Curved C-Handshape (as in `TORQUE`):** MCP $\approx 0.8\text{ rad}$, PIP $\approx 0.9\text{ rad}$, DIP $\approx 0.5\text{ rad}$.
- **Index 1-Handshape (as in pointing/referencing):** Index extended ($0.0\text{ rad}$); Middle, Ring, Pinky fully flexed ($>1.4\text{ rad}$).

---

## 4. Anatomical Joint Limits & Clamping Verification

To guarantee that retargeted motions never produce unnatural dislocations, every calculated rotation angle is passed through physiological clamping bounds:

| Joint | Rotation Channel | Min (rad) | Max (rad) | Min (deg) | Max (deg) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Shoulder** | Pitch (Flexion/Extension) | -1.57 | 2.35 | -90° | +135° |
| | Yaw (Abduction/Adduction) | -1.57 | 1.57 | -90° | +90° |
| | Roll (Internal/External) | -1.75 | 1.75 | -100° | +100° |
| **Elbow** | Flexion | 0.00 | 2.62 | 0° | +150° |
| **Wrist** | Pitch (Flexion/Extension) | -1.22 | 1.22 | -70° | +70° |
| | Yaw (Radial/Ulnar) | -0.70 | 0.70 | -40° | +40° |
| **Finger MCP** | Flexion | 0.00 | 1.60 | 0° | +92° |
| **Finger PIP** | Flexion | 0.00 | 1.80 | 0° | +103° |
| **Finger DIP** | Flexion | 0.00 | 1.30 | 0° | +75° |
| **Thumb CMC** | Abduction | 0.00 | 0.85 | 0° | +49° |
| **Thumb MCP** | Flexion | 0.00 | 1.10 | 0° | +63° |
| **Thumb IP** | Flexion | 0.00 | 1.40 | 0° | +80° |

All retargeted keyframes strictly conform to these limits.

