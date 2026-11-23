import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  SkipBack,
  SkipForward,
  Camera,
  Layers,
  SplitSquareVertical,
  Sliders,
  CheckCircle2,
  AlertTriangle,
  Info,
  ShieldCheck,
  Eye,
  Hand,
  Maximize2
} from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid } from '@react-three/drei';
import * as THREE from 'three';

import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { AnimationStatusBadge } from '../components/avatar/AnimationStatusBadge';
import { CameraPreset } from '../components/avatar/AvatarControls';

interface ConceptOption {
  term: string;
  conceptId: number;
  gloss: string;
  videoUrl: string;
  mocapUrl: string;
  duration: number;
  fps: number;
  resolution: string;
  signer: string;
}

const BENCHMARK_CONCEPTS: ConceptOption[] = [
  {
    term: 'Algorithm',
    conceptId: 5,
    gloss: 'ALGORITHM',
    videoUrl: '/data/sign_videos/islrtc_algorithm.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_algorithm_mocap.json',
    duration: 6.0,
    fps: 25.0,
    resolution: '1920x1080 (Full HD)',
    signer: 'ISLRTC Master Signer (Certified ISL Instructor)'
  },
  {
    term: 'Frequency',
    conceptId: 40,
    gloss: 'FREQUENCY',
    videoUrl: '/data/sign_videos/islrtc_frequency.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_frequency_mocap.json',
    duration: 4.28,
    fps: 25.0,
    resolution: '1920x1080 (Full HD)',
    signer: 'ISLRTC Master Signer (Certified ISL Instructor)'
  },
  {
    term: 'Current',
    conceptId: 10,
    gloss: 'CURRENT',
    videoUrl: '/data/sign_videos/islrtc_current.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_current_mocap.json',
    duration: 5.0,
    fps: 25.0,
    resolution: '1920x1080 (Full HD)',
    signer: 'ISLRTC Master Signer (Certified ISL Instructor)'
  },
  {
    term: 'Beam',
    conceptId: 67,
    gloss: 'BEAM',
    videoUrl: '/data/sign_videos/islrtc_beam.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_beam_mocap.json',
    duration: 5.0,
    fps: 25.0,
    resolution: '1920x1080 (Full HD)',
    signer: 'ISLRTC Master Signer (Certified ISL Instructor)'
  },
  {
    term: 'Torque',
    conceptId: 50,
    gloss: 'TORQUE',
    videoUrl: '/data/sign_videos/islrtc_torque.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_torque_mocap.json',
    duration: 7.2,
    fps: 25.0,
    resolution: '3840x2160 (4K UHD, 60fps)',
    signer: 'ISLRTC Master Signer (Certified ISL Instructor)'
  }
];

export const AvatarAuditComparisonPage: React.FC = () => {
  const [selectedConcept, setSelectedConcept] = useState<ConceptOption>(BENCHMARK_CONCEPTS[0]);
  const [isSynchronized, setIsSynchronized] = useState<boolean>(true);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [speed, setSpeed] = useState<number>(1.0);
  const [currentTime, setCurrentTime] = useState<number>(0.0);
  const [mocapData, setMocapData] = useState<any>(null);
  const [fidelityMetrics, setFidelityMetrics] = useState<any>(null);

  const videoRef = useRef<HTMLVideoElement>(null);

  // Load mocap JSON & fidelity metrics when selected concept changes
  useEffect(() => {
    let isMounted = true;
    setCurrentTime(0.0);
    setIsPlaying(false);

    // Fetch keyframes from processed endpoint or static file
    fetch(selectedConcept.mocapUrl)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (isMounted && data) {
          setMocapData(data);
        }
      })
      .catch(() => {});

    // Fetch fidelity metrics from backend
    fetch(`/api/v1/avatar/fidelity/${selectedConcept.term}`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (isMounted && data) {
          setFidelityMetrics(data);
        }
      })
      .catch(() => {});

    return () => {
      isMounted = false;
    };
  }, [selectedConcept]);

  // Video and master time synchronization
  useEffect(() => {
    if (!videoRef.current || !isSynchronized) return;

    if (isPlaying) {
      videoRef.current.playbackRate = speed;
      videoRef.current.play().catch(() => {});
    } else {
      videoRef.current.pause();
    }
  }, [isPlaying, speed, isSynchronized]);

  // Sync video time when user seeks
  const handleSeek = (newTime: number) => {
    const clamped = Math.max(0, Math.min(selectedConcept.duration, newTime));
    setCurrentTime(clamped);
    if (videoRef.current && isSynchronized) {
      videoRef.current.currentTime = clamped;
    }
  };

  // Video time update listener
  const handleVideoTimeUpdate = () => {
    if (!isSynchronized || !videoRef.current) return;
    const vTime = videoRef.current.currentTime;
    // Loop if reached end of mocap duration
    if (vTime >= selectedConcept.duration) {
      if (isPlaying) {
        videoRef.current.currentTime = 0;
        setCurrentTime(0);
      }
    } else {
      setCurrentTime(vTime);
    }
  };

  const handleStepFrame = (dir: 'forward' | 'backward') => {
    setIsPlaying(false);
    const dt = 0.033;
    const next = dir === 'forward' ? currentTime + dt : currentTime - dt;
    handleSeek(next);
  };

  const handleRestart = () => {
    handleSeek(0.0);
  };

  const handleTogglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-xs">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-200">
              Phase 4.5 Audit Subsystem
            </span>
            <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
              Side-by-Side Dual Engine
            </span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
            Original Signer vs 3D Avatar Motion Audit
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Synchronized frame-by-frame comparison between authentic ISLRTC signing recordings and the 54-joint avatar.
          </p>
        </div>

        {/* Concept Selector Dropdown */}
        <div className="flex items-center gap-3">
          <label className="text-xs font-semibold text-slate-600">Select Concept:</label>
          <select
            value={selectedConcept.term}
            onChange={(e) => {
              const found = BENCHMARK_CONCEPTS.find((c) => c.term === e.target.value);
              if (found) setSelectedConcept(found);
            }}
            className="px-3 py-2 bg-slate-50 border border-slate-300 rounded-xl text-sm font-semibold text-slate-800 shadow-2xs focus:ring-2 focus:ring-blue-500 outline-none"
          >
            {BENCHMARK_CONCEPTS.map((c) => (
              <option key={c.term} value={c.term}>
                {c.term} ({c.gloss}) — {c.duration}s
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Synchronized Master Control Bar */}
      <div className="bg-slate-900 text-white p-4 rounded-2xl shadow-lg border border-slate-800 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          {/* Transport buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={handleRestart}
              title="Restart from Beginning (0.00s)"
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
            >
              <RotateCcw size={16} />
            </button>
            <button
              onClick={() => handleStepFrame('backward')}
              title="Step Back 1 Frame (33ms)"
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
            >
              <SkipBack size={16} />
            </button>
            <button
              onClick={handleTogglePlay}
              title={isPlaying ? 'Pause' : 'Play Synchronized'}
              className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold flex items-center gap-1.5 shadow-md shadow-blue-900/40 transition"
            >
              {isPlaying ? <Pause size={17} /> : <Play size={17} />}
              <span className="text-xs">{isPlaying ? 'Pause' : 'Play Both'}</span>
            </button>
            <button
              onClick={() => handleStepFrame('forward')}
              title="Step Forward 1 Frame (33ms)"
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
            >
              <SkipForward size={16} />
            </button>
          </div>

          {/* Sync Mode Toggle */}
          <div className="flex items-center gap-2 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700">
            <SplitSquareVertical size={16} className="text-indigo-400" />
            <span className="text-xs font-semibold text-slate-300">Sync Mode:</span>
            <button
              onClick={() => setIsSynchronized(!isSynchronized)}
              className={`px-2 py-0.5 rounded text-xs font-semibold transition ${
                isSynchronized
                  ? 'bg-indigo-600 text-white shadow-2xs'
                  : 'bg-slate-700 text-slate-400 hover:text-white'
              }`}
            >
              {isSynchronized ? 'Synchronized (Locked)' : 'Independent'}
            </button>
          </div>

          {/* Speed Buttons */}
          <div className="flex items-center gap-1 bg-slate-800/80 p-1 rounded-xl border border-slate-700">
            <span className="text-[10px] uppercase font-bold text-slate-400 px-1.5">Speed</span>
            {[0.25, 0.5, 1.0, 1.5, 2.0].map((s) => (
              <button
                key={s}
                onClick={() => setSpeed(s)}
                className={`px-2 py-1 rounded-lg text-xs font-mono font-semibold transition ${
                  speed === s ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>

          {/* Timestamp Readout */}
          <div className="bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800 text-right">
            <span className="text-[11px] font-mono text-slate-400">Timestamp: </span>
            <span className="text-sm font-mono font-bold text-blue-400">
              {currentTime.toFixed(3)}s
            </span>
            <span className="text-[11px] font-mono text-slate-500">
              {' '}/ {selectedConcept.duration.toFixed(2)}s
            </span>
          </div>
        </div>

        {/* Master Scrubber Slider */}
        <div className="flex items-center gap-3 pt-1">
          <input
            type="range"
            min={0}
            max={selectedConcept.duration}
            step={0.033}
            value={currentTime}
            onChange={(e) => handleSeek(parseFloat(e.target.value))}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
      </div>

      {/* Side-by-Side Dual Viewports */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* LEFT VIEWPORT: Authentic ISLRTC Video */}
        <div className="bg-slate-950 rounded-2xl overflow-hidden border border-slate-800 shadow-xl flex flex-col">
          <div className="px-4 py-3 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">
                1. Authentic ISLRTC Reference Video
              </span>
            </div>
            <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
              {selectedConcept.resolution}
            </span>
          </div>

          {/* Video Player */}
          <div className="relative aspect-video bg-black flex items-center justify-center overflow-hidden">
            <video
              ref={videoRef}
              src={selectedConcept.videoUrl}
              onTimeUpdate={handleVideoTimeUpdate}
              className="w-full h-full object-contain"
              playsInline
              muted
            />

            {/* In-video HUD Overlay */}
            <div className="absolute top-3 left-3 bg-black/70 backdrop-blur-md px-2.5 py-1 rounded-md text-[11px] font-mono text-emerald-300 border border-emerald-900/40">
              Source: <span className="text-white font-bold">{selectedConcept.term}</span> ({selectedConcept.gloss})
            </div>
            <div className="absolute bottom-3 left-3 bg-black/70 backdrop-blur-md px-2.5 py-1 rounded-md text-[10px] font-mono text-slate-300 border border-slate-800">
              Signer: {selectedConcept.signer}
            </div>
          </div>

          {/* Video Metadata Footer */}
          <div className="p-3 bg-slate-900/90 border-t border-slate-800 text-xs text-slate-400 flex items-center justify-between">
            <span>License: Government Open Data License (GODL-India)</span>
            <span className="font-mono text-[11px] text-slate-300">
              Frame: {Math.floor(currentTime * selectedConcept.fps)} / {Math.floor(selectedConcept.duration * selectedConcept.fps)}
            </span>
          </div>
        </div>

        {/* RIGHT VIEWPORT: 3D Articulated Avatar */}
        <div className="flex flex-col">
          <AvatarViewer
            conceptTerm={selectedConcept.term}
            avatarData={{
              available: true,
              model_type: 'SignBridge-Articulated-54',
              animation_name: `islrtc_${selectedConcept.term.toLowerCase()}_mocap`,
              rig_standard: 'SignBridge-Articulated-54',
              validation_status: 'partial',
              motion_status: 'PARTIALLY_VERIFIED_MOTION',
              notice: 'Authentic ISLRTC mocap retargeted to 54-joint rig.'
            }}
            controlledIsPlaying={isPlaying}
            controlledSpeed={speed}
            controlledCurrentTime={currentTime}
            onTimeUpdate={(t) => setCurrentTime(t)}
            onTogglePlay={handleTogglePlay}
            onSeek={handleSeek}
            showControls={false}
          />
        </div>
      </div>

      {/* Discrepancy & Quantitative Fidelity Metrics Section */}
      {fidelityMetrics && (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center gap-2">
              <ShieldCheck className="text-blue-600" size={20} />
              <h2 className="text-base font-bold text-slate-900">
                Linguistic Discrepancy & Motion Fidelity Metrics ({selectedConcept.term})
              </h2>
            </div>
            <span className="text-xs font-mono bg-blue-50 text-blue-700 px-2.5 py-1 rounded-lg border border-blue-200">
              Total Keyframes: {fidelityMetrics.total_keyframes}
            </span>
          </div>

          {/* Metric cards grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200/80">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">Mean Error (NMLE)</span>
              <p className="text-xl font-bold font-mono text-slate-900 mt-1">
                {fidelityMetrics.normalized_mean_landmark_error}
              </p>
              <span className="text-[10px] text-slate-400">normalized body units</span>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200/80">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">95th %ile Error</span>
              <p className="text-xl font-bold font-mono text-slate-900 mt-1">
                {fidelityMetrics.p95_landmark_error}
              </p>
              <span className="text-[10px] text-slate-400">outlier bound</span>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200/80">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">Smoothness Score</span>
              <p className="text-xl font-bold font-mono text-emerald-600 mt-1">
                {fidelityMetrics.trajectory_smoothness_score} / 1.0
              </p>
              <span className="text-[10px] text-slate-400">One-Euro filter</span>
            </div>

            <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200/80">
              <span className="text-[11px] font-semibold text-slate-500 uppercase">Dominant Handshape</span>
              <p className="text-xs font-bold text-indigo-700 mt-2 truncate" title={fidelityMetrics.handshape_fidelity?.detected_dominant_handshape}>
                {fidelityMetrics.handshape_fidelity?.detected_dominant_handshape}
              </p>
              <span className="text-[10px] text-slate-400">15-joint articulation</span>
            </div>
          </div>

          {/* Detailed Regional Analysis */}
          <div className="bg-slate-50/60 p-4 rounded-xl border border-slate-200 text-xs text-slate-700 space-y-2">
            <h4 className="font-bold text-slate-900 flex items-center gap-1.5">
              <Info size={14} className="text-blue-600" />
              Regional Error Breakdown & Audit Observations:
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 pt-1 font-mono text-[11px]">
              <div>Head: <span className="font-bold text-slate-900">{fidelityMetrics.per_body_part_error?.head}</span></div>
              <div>Shoulders: <span className="font-bold text-slate-900">{fidelityMetrics.per_body_part_error?.shoulders}</span></div>
              <div>Elbows: <span className="font-bold text-slate-900">{fidelityMetrics.per_body_part_error?.elbows}</span></div>
              <div>Wrists: <span className="font-bold text-slate-900">{fidelityMetrics.per_body_part_error?.wrists}</span></div>
              <div>Fingers: <span className="font-bold text-slate-900">{fidelityMetrics.per_body_part_error?.fingers}</span></div>
            </div>
            <p className="text-[11px] text-slate-500 italic pt-2 border-t border-slate-200/60">
              {fidelityMetrics.limitations_disclaimer}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
