import React, { useRef, useState, useMemo, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';
import * as THREE from 'three';
import { User, ShieldAlert, Sparkles, Sliders, Film } from 'lucide-react';

import {
  AvatarOutput,
  AvatarSequencePayload,
  AvatarAnimationTrack,
  AvatarKeyframe,
  MotionVerificationStatus
} from '../../types';
import { AvatarControls, CameraPreset } from './AvatarControls';
import { AnimationTimeline } from './AnimationTimeline';
import { AnimationStatusBadge } from './AnimationStatusBadge';

export interface AvatarViewerProps {
  avatarData?: AvatarOutput;
  animationSequence?: AvatarSequencePayload;
  conceptTerm?: string;
  // Controlled inputs for dual-viewport synchronization
  controlledIsPlaying?: boolean;
  controlledSpeed?: number;
  controlledCurrentTime?: number;
  controlledCameraPreset?: CameraPreset;
  onTimeUpdate?: (time: number) => void;
  onTogglePlay?: () => void;
  onSeek?: (time: number) => void;
  onSelectCameraPreset?: (preset: CameraPreset) => void;
  showControls?: boolean;
}

// 15-Joint Articulated Hand Component
interface ArticulatedHandProps {
  isLeft: boolean;
  handPose?: any;
  skinMaterial: THREE.Material;
}

const ArticulatedHand: React.FC<ArticulatedHandProps> = ({ isLeft, handPose, skinMaterial }) => {
  const sideMultiplier = isLeft ? -1 : 1;

  // Finger segment dimensions
  const phalangeLength = 0.035;
  const phalangeRadius = 0.009;

  const renderFinger = (fingerKey: 'thumb' | 'index' | 'middle' | 'ring' | 'pinky', offsetX: number, offsetY: number) => {
    const fState = handPose?.[fingerKey] || {
      mcp: { x: 0.2, y: 0, z: 0 },
      pip: { x: 0.3, y: 0, z: 0 },
      dip: { x: 0.2, y: 0, z: 0 }
    };

    return (
      <group position={[offsetX * sideMultiplier, offsetY, 0]}>
        {/* Proximal Phalange (MCP) - Negate X rotation so flexion curls forward into palm (+Z) */}
        <group rotation={[-fState.mcp.x, fState.mcp.y * sideMultiplier, fState.mcp.z]}>
          <mesh position={[0, -phalangeLength / 2, 0]} material={skinMaterial} castShadow>
            <cylinderGeometry args={[phalangeRadius, phalangeRadius * 0.9, phalangeLength, 8]} />
          </mesh>

          {/* Intermediate Phalange (PIP) */}
          <group position={[0, -phalangeLength, 0]} rotation={[-fState.pip.x, fState.pip.y, fState.pip.z]}>
            <mesh position={[0, -phalangeLength / 2, 0]} material={skinMaterial} castShadow>
              <cylinderGeometry args={[phalangeRadius * 0.9, phalangeRadius * 0.8, phalangeLength, 8]} />
            </mesh>

            {/* Distal Phalange (DIP) */}
            <group position={[0, -phalangeLength, 0]} rotation={[-fState.dip.x, fState.dip.y, fState.dip.z]}>
              <mesh position={[0, -phalangeLength * 0.4, 0]} material={skinMaterial} castShadow>
                <cylinderGeometry args={[phalangeRadius * 0.8, phalangeRadius * 0.6, phalangeLength * 0.8, 8]} />
              </mesh>
            </group>
          </group>
        </group>
      </group>
    );
  };

  return (
    <group rotation={[handPose?.wrist?.x || 0, handPose?.wrist?.y || 0, handPose?.wrist?.z || 0]}>
      {/* Palm Base */}
      <mesh position={[0, -0.06, 0.01]} material={skinMaterial} castShadow>
        <boxGeometry args={[0.085, 0.09, 0.025]} />
      </mesh>

      {/* 5 Articulated Fingers */}
      {renderFinger('thumb', -0.045, -0.02)}
      {renderFinger('index', -0.03, -0.1)}
      {renderFinger('middle', -0.01, -0.105)}
      {renderFinger('ring', 0.012, -0.1)}
      {renderFinger('pinky', 0.032, -0.09)}
    </group>
  );
};

// Articulated 3D Upper-Body Humanoid Signer Model (54 Rig Points)
const ArticulatedHumanoidSigner = ({
  currentKeyframe,
  isPlaying,
  speed
}: {
  currentKeyframe?: AvatarKeyframe;
  isPlaying: boolean;
  speed: number;
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const chestRef = useRef<THREE.Group>(null);
  const headRef = useRef<THREE.Group>(null);
  const leftArmRef = useRef<THREE.Group>(null);
  const leftForearmRef = useRef<THREE.Group>(null);
  const rightArmRef = useRef<THREE.Group>(null);
  const rightForearmRef = useRef<THREE.Group>(null);

  // Facial Non-Manual Marker refs
  const leftEyebrowRef = useRef<THREE.Mesh>(null);
  const rightEyebrowRef = useRef<THREE.Mesh>(null);
  const mouthRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    const t = state.clock.getElapsedTime() * speed;

    if (currentKeyframe) {
      // Retargeted keyframe driven motion
      if (chestRef.current && currentKeyframe.chest_rotation) {
        chestRef.current.rotation.x = currentKeyframe.chest_rotation.x;
        chestRef.current.rotation.y = currentKeyframe.chest_rotation.y;
        chestRef.current.rotation.z = currentKeyframe.chest_rotation.z;
        // Breathing motion superimposed
        chestRef.current.position.y = 0.95 + Math.sin(t * 1.5) * 0.01;
      }

      if (headRef.current && currentKeyframe.head_rotation) {
        headRef.current.rotation.x = currentKeyframe.head_rotation.x;
        headRef.current.rotation.y = currentKeyframe.head_rotation.y;
        headRef.current.rotation.z = currentKeyframe.head_rotation.z;
      }

      // Dominant Right Arm (positioned at -0.44 X, viewer's left)
      // Negate X so positive mocap pitch/flexion swings arm forward (+Z) towards camera
      if (rightArmRef.current && currentKeyframe.right_arm_rotation) {
        rightArmRef.current.rotation.x = -currentKeyframe.right_arm_rotation.x;
        rightArmRef.current.rotation.y = currentKeyframe.right_arm_rotation.y;
        rightArmRef.current.rotation.z = currentKeyframe.right_arm_rotation.z;
      }

      if (rightForearmRef.current && currentKeyframe.right_forearm_rotation) {
        rightForearmRef.current.rotation.x = -currentKeyframe.right_forearm_rotation.x;
        rightForearmRef.current.rotation.y = currentKeyframe.right_forearm_rotation.y;
        rightForearmRef.current.rotation.z = currentKeyframe.right_forearm_rotation.z;
      }

      // Left Arm (positioned at +0.44 X, viewer's right)
      if (leftArmRef.current && currentKeyframe.left_arm_rotation) {
        leftArmRef.current.rotation.x = -currentKeyframe.left_arm_rotation.x;
        leftArmRef.current.rotation.y = currentKeyframe.left_arm_rotation.y;
        leftArmRef.current.rotation.z = currentKeyframe.left_arm_rotation.z;
      }

      if (leftForearmRef.current && currentKeyframe.left_forearm_rotation) {
        leftForearmRef.current.rotation.x = -currentKeyframe.left_forearm_rotation.x;
        leftForearmRef.current.rotation.y = currentKeyframe.left_forearm_rotation.y;
        leftForearmRef.current.rotation.z = currentKeyframe.left_forearm_rotation.z;
      }

      // Facial Blendshapes
      const nmm = currentKeyframe.facial_blendshapes;
      if (nmm) {
        if (leftEyebrowRef.current && rightEyebrowRef.current) {
          const browOffsetY = (nmm.brow_raise_left - nmm.brow_furrow_left) * 0.025;
          leftEyebrowRef.current.position.y = 0.08 + browOffsetY;
          rightEyebrowRef.current.position.y = 0.08 + browOffsetY;
        }

        if (mouthRef.current) {
          const mouthScaleY = 1.0 + nmm.mouth_open * 2.5;
          const mouthScaleX = 1.0 + nmm.mouth_wide * 1.5;
          mouthRef.current.scale.set(mouthScaleX, mouthScaleY, 1.0);
        }
      }
    } else {
      // Attentive neutral resting posture (Zero-Fabrication Safeguard)
      if (chestRef.current) {
        chestRef.current.position.y = 0.95 + Math.sin(t * 1.5) * 0.015;
        chestRef.current.rotation.set(0, 0, 0);
      }

      if (headRef.current) {
        headRef.current.rotation.y = Math.sin(t * 0.8) * 0.04;
        headRef.current.rotation.x = Math.sin(t * 1.2) * 0.02;
        headRef.current.rotation.z = 0;
      }

      if (rightArmRef.current && leftArmRef.current) {
        // Right arm is at -0.44 X, abducted with -0.22 Z
        rightArmRef.current.rotation.set(-0.35, 0, -0.22);
        // Left arm is at +0.44 X, abducted with +0.22 Z
        leftArmRef.current.rotation.set(-0.35, 0, 0.22);
      }

      if (rightForearmRef.current && leftForearmRef.current) {
        rightForearmRef.current.rotation.set(-0.15, 0, 0);
        leftForearmRef.current.rotation.set(-0.15, 0, 0);
      }
    }
  });

  // Memoized GPU Materials
  const { skinMaterial, shirtMaterial, hairMaterial, darkMaterial, mouthMaterial } = useMemo(() => {
    return {
      skinMaterial: new THREE.MeshStandardMaterial({
        color: '#d4a373',
        roughness: 0.5,
        metalness: 0.05
      }),
      shirtMaterial: new THREE.MeshStandardMaterial({
        color: '#2563eb', // Royal Academic Blue
        roughness: 0.65
      }),
      hairMaterial: new THREE.MeshStandardMaterial({
        color: '#1e293b',
        roughness: 0.85
      }),
      darkMaterial: new THREE.MeshStandardMaterial({
        color: '#0f172a',
        roughness: 0.9
      }),
      mouthMaterial: new THREE.MeshStandardMaterial({
        color: '#991b1b',
        roughness: 0.4
      })
    };
  }, []);

  return (
    <group ref={groupRef} position={[0, -0.65, 0]}>
      {/* Torso / Upper Body */}
      <group ref={chestRef} position={[0, 0.95, 0]}>
        {/* Chest & Shirt */}
        <mesh position={[0, 0.2, 0]} material={shirtMaterial} castShadow>
          <boxGeometry args={[0.68, 0.62, 0.34]} />
        </mesh>

        {/* Collar / V-neck */}
        <mesh position={[0, 0.44, 0.12]} material={darkMaterial}>
          <boxGeometry args={[0.26, 0.12, 0.14]} />
        </mesh>

        {/* Neck */}
        <mesh position={[0, 0.56, 0]} material={skinMaterial} castShadow>
          <cylinderGeometry args={[0.09, 0.1, 0.16, 16]} />
        </mesh>

        {/* Head Group */}
        <group ref={headRef} position={[0, 0.8, 0]}>
          {/* Cranium */}
          <mesh material={skinMaterial} castShadow>
            <sphereGeometry args={[0.18, 24, 24]} />
          </mesh>

          {/* Stylized Hair */}
          <mesh position={[0, 0.06, -0.02]} material={hairMaterial}>
            <sphereGeometry args={[0.19, 20, 20]} />
          </mesh>

          {/* Eyes */}
          <mesh position={[-0.06, 0.03, 0.16]} material={darkMaterial}>
            <sphereGeometry args={[0.02, 12, 12]} />
          </mesh>
          <mesh position={[0.06, 0.03, 0.16]} material={darkMaterial}>
            <sphereGeometry args={[0.02, 12, 12]} />
          </mesh>

          {/* Eyebrows (Dynamic for Non-Manual Markers) */}
          <mesh ref={leftEyebrowRef} position={[-0.06, 0.08, 0.16]} material={darkMaterial}>
            <boxGeometry args={[0.05, 0.012, 0.02]} />
          </mesh>
          <mesh ref={rightEyebrowRef} position={[0.06, 0.08, 0.16]} material={darkMaterial}>
            <boxGeometry args={[0.05, 0.012, 0.02]} />
          </mesh>

          {/* Nose */}
          <mesh position={[0, -0.01, 0.18]} material={skinMaterial}>
            <coneGeometry args={[0.025, 0.05, 12]} />
          </mesh>

          {/* Mouth (Dynamic opening for mouthing morphemes) */}
          <mesh ref={mouthRef} position={[0, -0.07, 0.165]} material={mouthMaterial}>
            <boxGeometry args={[0.05, 0.015, 0.015]} />
          </mesh>
        </group>

        {/* Right Arm Group (Anatomical Right = Viewer's Left at -0.44 X) */}
        <group ref={rightArmRef} position={[-0.44, 0.4, 0]}>
          <mesh material={shirtMaterial} castShadow>
            <sphereGeometry args={[0.1, 16, 16]} />
          </mesh>
          <mesh position={[0, -0.2, 0]} material={shirtMaterial} castShadow>
            <cylinderGeometry args={[0.075, 0.07, 0.32, 16]} />
          </mesh>

          {/* Right Forearm */}
          <group ref={rightForearmRef} position={[0, -0.36, 0]}>
            <mesh position={[0, -0.16, 0]} material={skinMaterial} castShadow>
              <cylinderGeometry args={[0.065, 0.055, 0.3, 16]} />
            </mesh>

            {/* Right 15-Joint Hand */}
            <group position={[0, -0.32, 0]}>
              <ArticulatedHand
                isLeft={false}
                handPose={currentKeyframe?.right_hand}
                skinMaterial={skinMaterial}
              />
            </group>
          </group>
        </group>

        {/* Left Arm Group (Anatomical Left = Viewer's Right at +0.44 X) */}
        <group ref={leftArmRef} position={[0.44, 0.4, 0]}>
          <mesh material={shirtMaterial} castShadow>
            <sphereGeometry args={[0.1, 16, 16]} />
          </mesh>
          <mesh position={[0, -0.2, 0]} material={shirtMaterial} castShadow>
            <cylinderGeometry args={[0.075, 0.07, 0.32, 16]} />
          </mesh>

          {/* Left Forearm */}
          <group ref={leftForearmRef} position={[0, -0.36, 0]}>
            <mesh position={[0, -0.16, 0]} material={skinMaterial} castShadow>
              <cylinderGeometry args={[0.065, 0.055, 0.3, 16]} />
            </mesh>

            {/* Left 15-Joint Hand */}
            <group position={[0, -0.32, 0]}>
              <ArticulatedHand
                isLeft={true}
                handPose={currentKeyframe?.left_hand}
                skinMaterial={skinMaterial}
              />
            </group>
          </group>
        </group>
      </group>

      {/* Waist Pedestal */}
      <mesh position={[0, 0.48, 0]} material={darkMaterial}>
        <boxGeometry args={[0.62, 0.24, 0.3]} />
      </mesh>
      <mesh position={[0, 0.15, 0]} material={darkMaterial}>
        <cylinderGeometry args={[0.22, 0.35, 0.42, 24]} />
      </mesh>
    </group>
  );
};

export const AvatarViewer: React.FC<AvatarViewerProps> = ({
  avatarData,
  animationSequence,
  conceptTerm,
  controlledIsPlaying,
  controlledSpeed,
  controlledCurrentTime,
  controlledCameraPreset,
  onTimeUpdate,
  onTogglePlay,
  onSeek,
  onSelectCameraPreset,
  showControls = true
}) => {
  const [internalIsPlaying, setInternalIsPlaying] = useState<boolean>(true);
  const [internalSpeed, setInternalSpeed] = useState<number>(1.0);
  const [internalCurrentTime, setInternalCurrentTime] = useState<number>(0.0);
  const [isLooping, setIsLooping] = useState<boolean>(true);
  const [cameraPreset, setCameraPreset] = useState<CameraPreset>(controlledCameraPreset || 'default');
  const [activeMocapData, setActiveMocapData] = useState<any>(null);

  const isControlledTime = controlledCurrentTime !== undefined;
  const isPlaying = controlledIsPlaying !== undefined ? controlledIsPlaying : internalIsPlaying;
  const speed = controlledSpeed !== undefined ? controlledSpeed : internalSpeed;
  const currentTime = controlledCurrentTime !== undefined ? controlledCurrentTime : internalCurrentTime;

  const controlsRef = useRef<any>(null);

  // Sync camera preset when controlled prop changes
  useEffect(() => {
    if (controlledCameraPreset && controlledCameraPreset !== cameraPreset) {
      handleSelectCameraPreset(controlledCameraPreset);
    }
  }, [controlledCameraPreset]);

  // Fetch mocap keyframes if concept is provided and has mocap
  useEffect(() => {
    let isMounted = true;
    const fetchMocap = async () => {
      const targetTerm = conceptTerm || (avatarData?.animation_name ? avatarData.animation_name.replace('islrtc_', '').replace('_mocap', '') : null);
      if (!targetTerm) return;

      try {
        const listRes = await fetch('/api/v1/avatar/animations');
        if (listRes.ok) {
          const listData = await listRes.json();
          const matched = listData.animations?.find(
            (a: any) =>
              a.concept_term?.toLowerCase() === targetTerm.toLowerCase() ||
              a.animation_name?.toLowerCase().includes(targetTerm.toLowerCase())
          );
          if (matched && isMounted) {
            const detailRes = await fetch(`/api/v1/avatar/animations/${matched.id}`);
            if (detailRes.ok) {
              const detailData = await detailRes.json();
              if (detailData.keyframes && detailData.keyframes.length > 0 && isMounted) {
                setActiveMocapData(detailData);
              }
            }
          }
        }
      } catch (e) {
        // Fallback to neutral rest
      }
    };

    fetchMocap();
    return () => {
      isMounted = false;
    };
  }, [conceptTerm, avatarData]);

  // Determine active tracks & total duration
  const tracks: AvatarAnimationTrack[] = useMemo(() => {
    if (animationSequence?.tracks && animationSequence.tracks.length > 0) {
      return animationSequence.tracks;
    }
    if (activeMocapData && activeMocapData.keyframes) {
      return [
        {
          track_id: 'track_mocap_active',
          track_type: 'LEXICAL_SIGN',
          gloss_token: activeMocapData.sign_gloss || 'SIGN',
          concept_term: activeMocapData.concept_term,
          start_time_seconds: 0,
          duration_seconds: activeMocapData.duration_seconds || 5.0,
          verification_status: 'PARTIALLY_VERIFIED_MOTION',
          is_mocap: true,
          keyframes: activeMocapData.keyframes
        }
      ];
    }
    return [];
  }, [animationSequence, activeMocapData]);

  const totalDuration = useMemo(() => {
    if (tracks.length === 0) return 0;
    const lastTrack = tracks[tracks.length - 1];
    return lastTrack.start_time_seconds + lastTrack.duration_seconds;
  }, [tracks]);

  // Frame tick animation loop
  useEffect(() => {
    if (isControlledTime) return;
    if (!isPlaying || totalDuration <= 0) return;

    const interval = setInterval(() => {
      setInternalCurrentTime((prev) => {
        const next = prev + 0.033 * speed;
        if (next >= totalDuration) {
          return isLooping ? 0.0 : totalDuration;
        }
        return next;
      });
    }, 33);

    return () => clearInterval(interval);
  }, [isControlledTime, isPlaying, speed, totalDuration, isLooping]);

  // Calculate current interpolated keyframe
  const currentKeyframe = useMemo(() => {
    if (tracks.length === 0) return undefined;

    // Find active track
    const track = tracks.find(
      (t) => currentTime >= t.start_time_seconds && currentTime <= t.start_time_seconds + t.duration_seconds
    ) || tracks[0];

    if (!track.keyframes || track.keyframes.length === 0) return undefined;

    const trackTimeMs = (currentTime - track.start_time_seconds) * 1000;
    // Find closest keyframe
    let closest = track.keyframes[0];
    let minDiff = Infinity;

    for (const kf of track.keyframes) {
      const diff = Math.abs(kf.timestamp_ms - trackTimeMs);
      if (diff < minDiff) {
        minDiff = diff;
        closest = kf;
      }
    }
    return closest;
  }, [tracks, currentTime]);

  // Camera preset handler
  const handleSelectCameraPreset = (preset: CameraPreset) => {
    setCameraPreset(preset);
    if (!controlsRef.current) return;

    if (preset === 'left45') {
      controlsRef.current.target.set(0, 0.5, 0);
      controlsRef.current.object.position.set(-1.8, 0.7, 1.8);
    } else if (preset === 'right45') {
      controlsRef.current.target.set(0, 0.5, 0);
      controlsRef.current.object.position.set(1.8, 0.7, 1.8);
    } else if (preset === 'face') {
      controlsRef.current.target.set(0, 0.85, 0);
      controlsRef.current.object.position.set(0, 0.95, 1.15);
    } else if (preset === 'hands') {
      controlsRef.current.target.set(0, 0.45, 0.1);
      controlsRef.current.object.position.set(0, 0.55, 1.4);
    } else {
      // Default front
      controlsRef.current.target.set(0, 0.5, 0);
      controlsRef.current.object.position.set(0, 0.7, 2.5);
    }
    controlsRef.current.update();
  };

  const handleSeek = (newTime: number) => {
    if (onSeek) {
      onSeek(newTime);
    } else {
      setInternalCurrentTime(newTime);
    }
  };

  const handleStepFrame = (dir: 'forward' | 'backward') => {
    if (onTogglePlay && isPlaying) {
      onTogglePlay();
    } else {
      setInternalIsPlaying(false);
    }
    const dt = 0.033;
    const next = dir === 'forward' ? currentTime + dt : currentTime - dt;
    handleSeek(Math.max(0, Math.min(totalDuration, next)));
  };

  const handleReset = () => {
    handleSeek(0.0);
    if (isPlaying) {
      if (onTogglePlay) onTogglePlay();
      else setInternalIsPlaying(false);
    }
    handleSelectCameraPreset('default');
  };

  const currentStatus =
    animationSequence?.overall_motion_status ||
    (tracks.length > 0 ? tracks[0].verification_status : 'NOT_IMPLEMENTED');

  return (
    <div className="bg-slate-900 rounded-2xl overflow-hidden shadow-xl border border-slate-800 text-white flex flex-col">
      {/* Header Bar */}
      <div className="px-4 py-3 bg-slate-800/90 border-b border-slate-700/60 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <User size={16} className="text-blue-400" />
          <span className="text-xs font-semibold text-slate-200">
            3D ISL Avatar (SignBridge-Articulated-54 Rig)
          </span>
          <span className="text-[10px] bg-blue-950 text-blue-300 border border-blue-800/60 px-2 py-0.5 rounded font-mono">
            54 Joints • 15 Finger Phalanges
          </span>
        </div>
        <AnimationStatusBadge status={currentStatus} />
      </div>

      {/* 3D Canvas Viewport */}
      <div className="relative bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 h-84 w-full cursor-grab active:cursor-grabbing">
        <Canvas camera={{ position: [0, 0.7, 2.5], fov: 45 }} shadows>
          <ambientLight intensity={0.75} />
          <directionalLight
            position={[3, 5, 4]}
            intensity={1.3}
            castShadow
            shadow-mapSize={[1024, 1024]}
          />
          <directionalLight position={[-3, 2, -2]} intensity={0.5} color="#93c5fd" />
          <pointLight position={[0, 2, 2]} intensity={0.6} />

          <ArticulatedHumanoidSigner
            currentKeyframe={currentKeyframe}
            isPlaying={isPlaying}
            speed={speed}
          />

          <Grid
            renderOrder={-1}
            position={[0, -0.66, 0]}
            infiniteGrid
            cellSize={0.4}
            sectionSize={1.2}
            sectionColor="#3b82f6"
            cellColor="#1e293b"
            fadeDistance={20}
          />

          <OrbitControls
            ref={controlsRef}
            target={[0, 0.5, 0]}
            maxPolarAngle={Math.PI / 2 + 0.1}
            minDistance={0.8}
            maxDistance={4.5}
            enablePan={true}
          />
        </Canvas>

        {/* Live HUD overlay */}
        <div className="absolute top-3 left-3 pointer-events-none flex flex-col gap-1">
          <div className="bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-md border border-slate-700/50 text-[10px] font-mono text-slate-300">
            Preset: <span className="text-blue-400 capitalize">{cameraPreset}</span>
          </div>
          {tracks.length > 0 && (
            <div className="bg-slate-900/80 backdrop-blur-md px-2.5 py-1 rounded-md border border-slate-700/50 text-[10px] font-mono text-emerald-400">
              Mocap Keyframes Active ({tracks[0].keyframes.length} pts)
            </div>
          )}
        </div>
      </div>

      {/* Transport Controls */}
      {showControls && (
        <AvatarControls
          isPlaying={isPlaying}
          onTogglePlay={() => {
            if (onTogglePlay) onTogglePlay();
            else setInternalIsPlaying(!internalIsPlaying);
          }}
          speed={speed}
          onSpeedChange={(newSpeed) => setInternalSpeed(newSpeed)}
          currentTimeSeconds={currentTime}
          totalDurationSeconds={totalDuration}
          onSeek={handleSeek}
          onStepFrame={handleStepFrame}
          isLooping={isLooping}
          onToggleLoop={() => setIsLooping(!isLooping)}
          cameraPreset={cameraPreset}
          onSelectCameraPreset={(p) => {
            handleSelectCameraPreset(p);
            if (onSelectCameraPreset) onSelectCameraPreset(p);
          }}
          onReset={handleReset}
        />
      )}

      {/* Animation Sequence Timeline */}
      {showControls && tracks.length > 0 && (
        <AnimationTimeline
          tracks={tracks}
          currentTimeSeconds={currentTime}
          totalDurationSeconds={totalDuration}
          onSeek={handleSeek}
        />
      )}
    </div>
  );
};
