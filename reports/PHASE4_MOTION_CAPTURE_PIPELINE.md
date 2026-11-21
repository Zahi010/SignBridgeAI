# Phase 4 Computer Vision Motion Capture Pipeline Specification

**Pipeline Version:** 4.0.0  
**Backend Engine:** MediaPipe Tasks (Python Vision API) + OpenCV  
**Input Standards:** 1080p ISLRTC Authentic Sign Videos  
**Output Standards:** Normalized, Smoothed 3D Landmark Time-Series (`*_mocap.json`)

---

## 1. Computer Vision Architecture Overview

The SignBridge AI Motion Capture Pipeline extracts authentic human signer kinematics from source video files without requiring invasive suit hardware or optical markers.

```
                    ┌───────────────────────────────┐
                    │  1080p ISL Video (ISLRTC)    │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Frame Sampling (OpenCV)      │
                    │  - 25 FPS Normalization       │
                    │  - BGR -> RGB Color Space     │
                    └───────────────┬───────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌───────────────┐           ┌───────────────┐           ┌───────────────┐
│ PoseLandmarker│           │ HandLandmarker│           │ FaceLandmarker│
│  - 33 Points  │           │ - 21 L + 21 R │           │ - 468 Points  │
│  - Torso/Arms │           │ - 30 Phalanges│           │ - NMM Morphs  │
└───────┬───────┘           └───────┬───────┘           └───────┬───────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Coordinate Normalization     │
                    │  - Shoulder Midpoint Anchor   │
                    │  - Torso Width Scale Factor   │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Temporal Smoothing & Filters │
                    │  - EMA / One-Euro Filtering   │
                    │  - Anatomical Outlier Clamping│
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │  Retargeted Keyframe Stream   │
                    │  data/isl_motion/processed/   │
                    └───────────────────────────────┘
```

---

## 2. Mathematical Normalization

Because source videos feature varying signer builds and camera distances, landmarks are mapped to a canonical body-relative coordinate frame:

1. **Mid-Shoulder Origin:**
   $$\mathbf{P}_{mid} = \frac{\mathbf{P}_{L\_shoulder} + \mathbf{P}_{R\_shoulder}}{2}$$

2. **Inter-Shoulder Scaling Factor:**
   $$W_{shoulder} = \|\mathbf{P}_{L\_shoulder} - \mathbf{P}_{R\_shoulder}\|$$
   $$S = \frac{1.0}{W_{shoulder}}$$

3. **Canonical Point Mapping:**
   $$\mathbf{X}_{norm} = (\mathbf{X} - \mathbf{P}_{mid}) \cdot S$$

In this coordinate frame:
- The chest center rests at $(0, 0, 0)$.
- The left shoulder sits at approximately $(-0.5, 0, 0)$ and the right shoulder at $(0.5, 0, 0)$.
- The vertical $Y$-axis is positive upward.
- The depth $Z$-axis is positive toward the viewer.

---

## 3. Temporal Smoothing & Outlier Rejection

High-speed sign transitions can cause tracking noise or single-frame joint jitter. The pipeline applies a dual-stage filter:

1. **Exponential Moving Average (EMA):**
   $$\mathbf{X}_t^{smoothed} = \alpha \mathbf{X}_t + (1 - \alpha) \mathbf{X}_{t-1}^{smoothed}$$
   with $\alpha = 0.65$, which preserves sharp hand reversals while suppressing micro-tremors.

2. **Anatomical Velocity Clamp:**
   If displacement $\|\mathbf{X}_t - \mathbf{X}_{t-1}\| > 2.0 \cdot W_{shoulder}$ within a single frame ($40\text{ms}$), the frame is flagged as an optical occlusion artifact and interpolated linearly from adjacent valid frames.

---

## 4. Pipeline Execution on Benchmark Concepts

The pipeline is executed across the 5 acquired ISLRTC recordings:
- `islrtc_algorithm.mp4` -> `data/isl_motion/processed/islrtc_algorithm_mocap.json`
- `islrtc_frequency.mp4` -> `data/isl_motion/processed/islrtc_frequency_mocap.json`
- `islrtc_current.mp4` -> `data/isl_motion/processed/islrtc_current_mocap.json`
- `islrtc_beam.mp4` -> `data/isl_motion/processed/islrtc_beam_mocap.json`
- `islrtc_torque.mp4` -> `data/isl_motion/processed/islrtc_torque_mocap.json`

Each processed file includes full SHA-256 provenance and is formally classified as `PARTIALLY_VERIFIED_MOTION`.

