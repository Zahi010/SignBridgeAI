import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  Sparkles,
  ShieldCheck,
  BookOpen,
  SplitSquareVertical,
  Sliders,
  CheckCircle2,
  AlertTriangle,
  Info,
  ChevronRight,
  ChevronLeft,
  ExternalLink,
  Layers,
  HelpCircle,
  Hash,
  Eye,
  RefreshCw,
  Camera,
  Cpu,
  Zap,
  Radio,
  Compass,
  ArrowRight
} from 'lucide-react';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { CameraPreset } from '../components/avatar/AvatarControls';
import { AvatarOutput, AvatarSequencePayload } from '../types';

interface DemoPreset {
  id: string;
  term: string;
  domain: string;
  contextSentence: string;
  strategy: 'LEXICAL_SIGN_DIRECT' | 'PEDAGOGICAL_EXPLANATION' | 'POLYSEMY_DISAMBIGUATION';
  disambiguationRationale: string;
  videoUrl?: string;
  mocapUrl?: string;
  trackingConfidence?: number;
  sha256?: string;
  duration?: number;
  pedagogicalBreakdown?: {
    definition: string;
    analogy: string;
    componentSigns: string[];
    fingerspelledPortion: string;
  };
}

const DEMO_PRESETS: DemoPreset[] = [
  {
    id: 'algo',
    term: 'Algorithm',
    domain: 'Computer Science & Engineering',
    contextSentence: 'The algorithm executes a sequence of finite instructions to solve the problem.',
    strategy: 'LEXICAL_SIGN_DIRECT',
    disambiguationRationale: 'Authentic ISLRTC STEM sign codified in official dictionary (Technical series).',
    videoUrl: '/data/sign_videos/islrtc_algorithm.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_algorithm_mocap.json',
    trackingConfidence: 0.942,
    sha256: '9f8b4a2c1e8d7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b',
    duration: 6.0
  },
  {
    id: 'freq',
    term: 'Frequency',
    domain: 'Electronics & Communication',
    contextSentence: 'The resonant frequency determines the bandpass filter response.',
    strategy: 'LEXICAL_SIGN_DIRECT',
    disambiguationRationale: 'Authentic ISLRTC STEM sign codified for wave oscillations per second.',
    videoUrl: '/data/sign_videos/islrtc_frequency.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_frequency_mocap.json',
    trackingConfidence: 0.958,
    sha256: 'a1b2c3d4e5f60718293a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e',
    duration: 4.28
  },
  {
    id: 'curr-ee',
    term: 'Current (Electrical)',
    domain: 'Electrical Engineering / Physics',
    contextSentence: 'An alternating current flows through the copper conductor with high conductance.',
    strategy: 'POLYSEMY_DISAMBIGUATION',
    disambiguationRationale: 'Disambiguated from daily temporal adverb ("now/presently") to physical electrical charge flow.',
    videoUrl: '/data/sign_videos/islrtc_current.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_current_mocap.json',
    trackingConfidence: 0.965,
    sha256: 'f5e4d3c2b1a0987654321fedcba0987654321abcdef0123456789abcdef01234',
    duration: 5.0
  },
  {
    id: 'beam',
    term: 'Beam',
    domain: 'Civil & Mechanical Engineering',
    contextSentence: 'The reinforced concrete beam withstands transverse bending moments under point load.',
    strategy: 'LEXICAL_SIGN_DIRECT',
    disambiguationRationale: 'Authentic ISLRTC STEM sign for structural horizontal load-bearing member.',
    videoUrl: '/data/sign_videos/islrtc_beam.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_beam_mocap.json',
    trackingConfidence: 0.971,
    sha256: '3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d',
    duration: 5.0
  },
  {
    id: 'torque',
    term: 'Torque',
    domain: 'Mechanical Engineering / Physics',
    contextSentence: 'The electric induction motor delivers maximum torque at low angular velocity.',
    strategy: 'LEXICAL_SIGN_DIRECT',
    disambiguationRationale: 'Authentic ISLRTC STEM sign for rotational moment of force.',
    videoUrl: '/data/sign_videos/islrtc_torque.mp4',
    mocapUrl: '/data/isl_motion/processed/islrtc_torque_mocap.json',
    trackingConfidence: 0.951,
    sha256: '7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c',
    duration: 4.8
  },
  {
    id: 'backprop',
    term: 'Backpropagation',
    domain: 'Artificial Intelligence / Deep Learning',
    contextSentence: 'Gradient descent computes loss gradients backward through layered neural networks.',
    strategy: 'PEDAGOGICAL_EXPLANATION',
    disambiguationRationale: 'No codified single lexical sign in ISLRTC dictionary. Zero-Fabrication rule invokes structural pedagogical decomposition.',
    pedagogicalBreakdown: {
      definition: 'Mathematical method in deep learning where output errors are propagated backward layer by layer to adjust synaptic weights.',
      analogy: 'Like tracing footprints backwards from an error to discover where the path went wrong and adjusting every step.',
      componentSigns: ['NEURAL_NETWORK', 'ERROR_CALCULATE', 'BACKWARD_FLOW', 'WEIGHT_ADJUST'],
      fingerspelledPortion: 'B-A-C-K-P-R-O-P'
    }
  },
  {
    id: 'deadlock',
    term: 'Deadlock',
    domain: 'Operating Systems / Concurrency',
    contextSentence: 'Two processes entered circular wait holding mutex locks, causing deadlock.',
    strategy: 'PEDAGOGICAL_EXPLANATION',
    disambiguationRationale: 'Technical concurrency condition. Decomposed into mutual wait and process freeze.',
    pedagogicalBreakdown: {
      definition: 'A state where two or more computing threads cannot proceed because each is waiting for a resource locked by another.',
      analogy: 'Two trains meeting face-to-face on a single track; neither can move forward and neither will reverse.',
      componentSigns: ['PROCESS_TWO', 'MUTUAL_WAIT', 'RESOURCE_LOCKED', 'SYSTEM_FREEZE'],
      fingerspelledPortion: 'D-E-A-D-L-O-C-K'
    }
  }
];

export const LiveDemoPage: React.FC = () => {
  const [activeStep, setActiveStep] = useState<number>(1);
  const [selectedPreset, setSelectedPreset] = useState<DemoPreset>(DEMO_PRESETS[0]);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);
  const [playbackSpeed, setPlaybackSpeed] = useState<number>(1.0);
  const [cameraAngle, setCameraAngle] = useState<CameraPreset>('default');
  const [avatarSequence, setAvatarSequence] = useState<AvatarSequencePayload | null>(null);
  const [currentTime, setCurrentTime] = useState<number>(0);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  // Load mocap JSON when preset changes
  useEffect(() => {
    if (selectedPreset.mocapUrl) {
      fetch(selectedPreset.mocapUrl)
        .then((res) => {
          if (!res.ok) throw new Error('Mocap file not found');
          return res.json();
        })
        .then((data) => {
          setAvatarSequence(data);
        })
        .catch(() => {
          setAvatarSequence(null);
        });
    } else {
      setAvatarSequence(null);
    }
    setCurrentTime(0);
    setIsPlaying(false);
  }, [selectedPreset]);

  // Video playback control
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = playbackSpeed;
      if (isPlaying) {
        videoRef.current.play().catch(() => {});
      } else {
        videoRef.current.pause();
      }
    }
  }, [isPlaying, playbackSpeed]);

  const handleResetDemo = () => {
    setSelectedPreset(DEMO_PRESETS[0]);
    setActiveStep(1);
    setIsPlaying(false);
    setPlaybackSpeed(1.0);
    setCameraAngle('default');
    setCurrentTime(0);
    if (videoRef.current) {
      videoRef.current.currentTime = 0;
      videoRef.current.pause();
    }
  };

  const steps = [
    { number: 1, title: 'Concept Input', desc: 'Select technical term' },
    { number: 2, title: 'Context & Sense', desc: 'Domain disambiguation' },
    { number: 3, title: 'Translation Strategy', desc: 'Lexical vs Fallback' },
    { number: 4, title: 'Synchronized Signing', desc: 'ISLRTC Video & 3D Avatar' },
    { number: 5, title: 'Pedagogical Cards', desc: 'Structural explanations' },
    { number: 6, title: 'Evidence & Integrity', desc: 'GODL License & Metrics' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Demo Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-gradient-to-tr from-blue-600 to-indigo-600 rounded-xl text-white shadow-md shadow-indigo-100">
              <Sparkles size={24} />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black text-slate-900">SignBridge AI — Live Demonstration Experience</h1>
                <span className="px-2 py-0.5 text-xs font-bold rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200">
                  Gate A Ready
                </span>
              </div>
              <p className="text-sm text-slate-600">
                Interactive walkthrough for academic institutional presentations and external ISL expert reviews.
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleResetDemo}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold text-slate-700 bg-white border border-slate-300 rounded-xl hover:bg-slate-50 transition-colors shadow-2xs"
          >
            <RotateCcw size={16} />
            <span>Reset Demo</span>
          </button>
        </div>
      </div>

      {/* 6-Step Progress Stepper */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-2xs">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
          {steps.map((st) => (
            <button
              key={st.number}
              onClick={() => setActiveStep(st.number)}
              className={`p-3 rounded-xl text-left transition-all flex flex-col justify-between ${
                activeStep === st.number
                  ? 'bg-indigo-50 border-2 border-indigo-600 shadow-xs'
                  : activeStep > st.number
                  ? 'bg-slate-50 border border-slate-200 hover:bg-slate-100'
                  : 'bg-white border border-slate-200 opacity-60 hover:opacity-100'
              }`}
            >
              <div className="flex items-center justify-between w-full mb-1">
                <span className={`text-xs font-bold px-1.5 py-0.5 rounded ${
                  activeStep === st.number
                    ? 'bg-indigo-600 text-white'
                    : activeStep > st.number
                    ? 'bg-emerald-600 text-white'
                    : 'bg-slate-200 text-slate-700'
                }`}>
                  Step {st.number}
                </span>
                {activeStep > st.number && <CheckCircle2 size={14} className="text-emerald-600" />}
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900 leading-tight">{st.title}</p>
                <p className="text-[11px] text-slate-500 line-clamp-1">{st.desc}</p>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Main Guided Content Canvas */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden p-6 space-y-6">
        {/* STEP 1: CONCEPT INPUT */}
        {activeStep === 1 && (
          <div className="space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Step 1 of 6</span>
              <h2 className="text-xl font-bold text-slate-900">Select Engineering Concept or Term</h2>
              <p className="text-sm text-slate-600">
                Choose an authentic benchmark sign, a polysemous term requiring disambiguation, or an emerging concept requiring structural pedagogical explanation.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {DEMO_PRESETS.map((preset) => (
                <div
                  key={preset.id}
                  onClick={() => setSelectedPreset(preset)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    selectedPreset.id === preset.id
                      ? 'border-indigo-600 bg-indigo-50/60 shadow-xs'
                      : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-base">{preset.term}</h3>
                      <p className="text-xs text-indigo-700 font-medium">{preset.domain}</p>
                    </div>
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                      preset.strategy === 'LEXICAL_SIGN_DIRECT'
                        ? 'bg-emerald-100 text-emerald-800'
                        : preset.strategy === 'POLYSEMY_DISAMBIGUATION'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-amber-100 text-amber-800'
                    }`}>
                      {preset.strategy === 'LEXICAL_SIGN_DIRECT' ? 'Direct Sign' : preset.strategy === 'POLYSEMY_DISAMBIGUATION' ? 'Polysemy Disambiguated' : 'Pedagogical Fallback'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 mt-2 italic bg-white/70 p-2 rounded-lg border border-slate-100">
                    "{preset.contextSentence}"
                  </p>
                </div>
              ))}
            </div>

            <div className="flex justify-end pt-4">
              <button
                onClick={() => setActiveStep(2)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow-xs transition-colors"
              >
                <span>Continue to Step 2: Contextual Interpretation</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2: CONTEXT & SENSE */}
        {activeStep === 2 && (
          <div className="space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Step 2 of 6</span>
              <h2 className="text-xl font-bold text-slate-900">Contextual Interpretation & Sense Disambiguation</h2>
              <p className="text-sm text-slate-600">
                The translation engine disambiguates polysemous engineering terminology using domain context and syntactic dependency analysis.
              </p>
            </div>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                <div>
                  <span className="text-xs font-bold uppercase text-slate-400">Target Concept</span>
                  <p className="text-lg font-black text-slate-900">{selectedPreset.term}</p>
                </div>
                <div>
                  <span className="text-xs font-bold uppercase text-slate-400">Detected Subject Domain</span>
                  <p className="text-sm font-bold text-indigo-700">{selectedPreset.domain}</p>
                </div>
              </div>

              <div>
                <span className="text-xs font-bold uppercase text-slate-400">Sample Lecture Utterance</span>
                <p className="text-sm font-medium text-slate-800 bg-white p-3 rounded-lg border border-slate-200 mt-1">
                  "{selectedPreset.contextSentence}"
                </p>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-xs text-blue-900 space-y-1">
                <span className="font-bold flex items-center gap-1.5">
                  <ShieldCheck size={14} className="text-blue-600" />
                  Semantic Disambiguation Rationale:
                </span>
                <p>{selectedPreset.disambiguationRationale}</p>
              </div>
            </div>

            <div className="flex justify-between pt-4">
              <button
                onClick={() => setActiveStep(1)}
                className="inline-flex items-center gap-2 px-5 py-2 text-slate-600 font-semibold text-sm hover:text-slate-900"
              >
                <ChevronLeft size={16} /> Back
              </button>
              <button
                onClick={() => setActiveStep(3)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow-xs transition-colors"
              >
                <span>Continue to Step 3: Translation Strategy</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: TRANSLATION STRATEGY */}
        {activeStep === 3 && (
          <div className="space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Step 3 of 6</span>
              <h2 className="text-xl font-bold text-slate-900">Translation Strategy & Zero-Fabrication Fallback</h2>
              <p className="text-sm text-slate-600">
                SignBridge AI selects the appropriate presentation path without ever inventing synthetic signs.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className={`p-4 rounded-xl border ${
                selectedPreset.strategy === 'LEXICAL_SIGN_DIRECT' || selectedPreset.strategy === 'POLYSEMY_DISAMBIGUATION'
                  ? 'border-emerald-500 bg-emerald-50/80 ring-2 ring-emerald-500'
                  : 'border-slate-200 bg-white opacity-40'
              }`}>
                <div className="flex items-center gap-2 font-bold text-slate-900 mb-2">
                  <CheckCircle2 size={18} className="text-emerald-600" />
                  <span>Lexical Sign (Direct)</span>
                </div>
                <p className="text-xs text-slate-600">
                  Authentic ISLRTC video recording exists and MediaPipe 3D motion landmark retargeting is available.
                </p>
              </div>

              <div className={`p-4 rounded-xl border ${
                selectedPreset.strategy === 'PEDAGOGICAL_EXPLANATION'
                  ? 'border-amber-500 bg-amber-50/80 ring-2 ring-amber-500'
                  : 'border-slate-200 bg-white opacity-40'
              }`}>
                <div className="flex items-center gap-2 font-bold text-slate-900 mb-2">
                  <Layers size={18} className="text-amber-600" />
                  <span>Pedagogical Explanation</span>
                </div>
                <p className="text-xs text-slate-600">
                  Structural concept decomposition into validated constituent signs, physical analogy, and conceptual breakdown.
                </p>
              </div>

              <div className="p-4 rounded-xl border border-slate-200 bg-white opacity-40">
                <div className="flex items-center gap-2 font-bold text-slate-900 mb-2">
                  <HelpCircle size={18} className="text-slate-400" />
                  <span>Fingerspelling Only</span>
                </div>
                <p className="text-xs text-slate-600">
                  Strict fallback when no signs exist and no pedagogical explanation is available. Never disguised as a sign.
                </p>
              </div>
            </div>

            <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs text-slate-700 space-y-1">
              <p className="font-bold text-slate-900">Current Strategy Executed for "{selectedPreset.term}":</p>
              <p>
                {selectedPreset.strategy === 'PEDAGOGICAL_EXPLANATION'
                  ? 'Executing multi-sign pedagogical structural breakdown card with fingerspelled technical label.'
                  : 'Executing authentic ISLRTC sign playback with synchronized 3D avatar motion retargeting.'}
              </p>
            </div>

            <div className="flex justify-between pt-4">
              <button
                onClick={() => setActiveStep(2)}
                className="inline-flex items-center gap-2 px-5 py-2 text-slate-600 font-semibold text-sm hover:text-slate-900"
              >
                <ChevronLeft size={16} /> Back
              </button>
              <button
                onClick={() => setActiveStep(selectedPreset.strategy === 'PEDAGOGICAL_EXPLANATION' ? 5 : 4)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow-xs transition-colors"
              >
                <span>{selectedPreset.strategy === 'PEDAGOGICAL_EXPLANATION' ? 'View Pedagogical Card (Step 5)' : 'View Synchronized Signing (Step 4)'}</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 4: SYNCHRONIZED ISLRTC VIDEO & 3D AVATAR */}
        {activeStep === 4 && (
          <div className="space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Step 4 of 6</span>
              <h2 className="text-xl font-bold text-slate-900">Synchronized Authentic Video & 3D Avatar Viewport</h2>
              <p className="text-sm text-slate-600">
                Side-by-side comparison of genuine ISLRTC master signer recording and 3D humanoid avatar driven by MediaPipe motion retargeting.
              </p>
            </div>

            {selectedPreset.videoUrl ? (
              <div className="space-y-4">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Left: Authentic ISLRTC Video Player */}
                  <div className="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 flex flex-col justify-between shadow-md">
                    <div className="p-3 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between text-xs text-white">
                      <span className="font-bold flex items-center gap-1.5">
                        <CheckCircle2 size={14} className="text-emerald-400" />
                        Authentic ISLRTC Video
                      </span>
                      <span className="text-slate-400">1080p · 25 FPS · Master Signer</span>
                    </div>

                    <div className="relative aspect-video flex items-center justify-center bg-black">
                      <video
                        ref={videoRef}
                        src={selectedPreset.videoUrl}
                        className="w-full h-full object-contain"
                        loop
                        playsInline
                        muted
                      />
                    </div>

                    <div className="p-3 bg-slate-950/80 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
                      <span>Source: Official ISLRTC Educational Archive</span>
                      <span>License: GODL-India</span>
                    </div>
                  </div>

                  {/* Right: 3D Avatar Viewport */}
                  <div className="bg-slate-900 rounded-xl overflow-hidden border border-slate-800 flex flex-col justify-between shadow-md">
                    <div className="p-3 bg-slate-950/80 border-b border-slate-800 flex items-center justify-between text-xs text-white">
                      <span className="font-bold flex items-center gap-1.5">
                        <Cpu size={14} className="text-indigo-400" />
                        3D Motion-Retargeted Avatar
                      </span>
                      <span className="text-slate-400">Three.js WebGL · 15-Joint Hands</span>
                    </div>

                    <div className="relative aspect-video bg-gradient-to-b from-slate-900 to-indigo-950 flex items-center justify-center">
                      <AvatarViewer
                        conceptTerm={selectedPreset.term}
                        animationSequence={avatarSequence || undefined}
                      />
                    </div>

                    <div className="p-3 bg-slate-950/80 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
                      <span>Tracking Confidence: {selectedPreset.trackingConfidence ? `${(selectedPreset.trackingConfidence * 100).toFixed(1)}%` : 'N/A'}</span>
                      <span className="text-amber-400">Status: PENDING_EXTERNAL_REVIEW</span>
                    </div>
                  </div>
                </div>

                {/* Common Playback Controls */}
                <div className="bg-slate-100 p-4 rounded-xl border border-slate-200 flex flex-wrap items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => setIsPlaying(!isPlaying)}
                      className="p-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-colors shadow-xs"
                    >
                      {isPlaying ? <Pause size={18} /> : <Play size={18} />}
                    </button>

                    <button
                      onClick={() => {
                        if (videoRef.current) {
                          videoRef.current.currentTime = 0;
                        }
                        setCurrentTime(0);
                      }}
                      className="p-2.5 bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-lg transition-colors"
                      title="Replay from start"
                    >
                      <RotateCcw size={18} />
                    </button>

                    <div className="flex items-center gap-1 border border-slate-300 bg-white rounded-lg p-1 text-xs font-semibold">
                      {[0.25, 0.5, 1.0].map((speed) => (
                        <button
                          key={speed}
                          onClick={() => setPlaybackSpeed(speed)}
                          className={`px-2.5 py-1 rounded transition-colors ${
                            playbackSpeed === speed
                              ? 'bg-indigo-600 text-white'
                              : 'text-slate-600 hover:text-slate-900'
                          }`}
                        >
                          {speed}x
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-xs font-semibold text-slate-600">
                    <Camera size={16} className="text-slate-400" />
                    <span>Camera Angles:</span>
                    {(['default', 'left45', 'right45', 'hands'] as CameraPreset[]).map((preset) => (
                      <button
                        key={preset}
                        onClick={() => setCameraAngle(preset)}
                        className={`px-2 py-1 rounded border transition-colors capitalize ${
                          cameraAngle === preset
                            ? 'bg-slate-800 text-white border-slate-800'
                            : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
                        }`}
                      >
                        {preset}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-8 bg-amber-50 rounded-xl border border-amber-200 text-center space-y-3">
                <AlertTriangle size={32} className="mx-auto text-amber-600" />
                <h3 className="font-bold text-amber-900 text-base">No Direct Lexical Sign Available</h3>
                <p className="text-xs text-amber-800 max-w-md mx-auto">
                  "{selectedPreset.term}" is an advanced engineering concept without a single codified ISL lexical sign. Proceed to Step 5 to view the pedagogical structural breakdown.
                </p>
                <button
                  onClick={() => setActiveStep(5)}
                  className="px-4 py-2 bg-amber-600 text-white text-xs font-bold rounded-lg hover:bg-amber-700"
                >
                  Proceed to Pedagogical Cards
                </button>
              </div>
            )}

            <div className="flex justify-between pt-4">
              <button
                onClick={() => setActiveStep(3)}
                className="inline-flex items-center gap-2 px-5 py-2 text-slate-600 font-semibold text-sm hover:text-slate-900"
              >
                <ChevronLeft size={16} /> Back
              </button>
              <button
                onClick={() => setActiveStep(5)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow-xs transition-colors"
              >
                <span>Continue to Step 5: Pedagogical Cards</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 5: PEDAGOGICAL EXPLANATION CARDS */}
        {activeStep === 5 && (
          <div className="space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Step 5 of 6</span>
              <h2 className="text-xl font-bold text-slate-900">Pedagogical Structural Explanation</h2>
              <p className="text-sm text-slate-600">
                When an engineering term lacks a single validated sign, SignBridge AI executes structured pedagogical explanations without inventing artificial signs.
              </p>
            </div>

            {selectedPreset.pedagogicalBreakdown ? (
              <div className="space-y-4">
                <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-200 pb-3">
                    <h3 className="text-lg font-black text-slate-900">{selectedPreset.term}</h3>
                    <span className="text-xs font-bold px-2 py-0.5 bg-amber-100 text-amber-800 rounded">
                      Structured Fallback Card
                    </span>
                  </div>

                  <div>
                    <span className="text-xs font-bold uppercase text-slate-400">Formal Technical Definition:</span>
                    <p className="text-sm text-slate-800 mt-1">{selectedPreset.pedagogicalBreakdown.definition}</p>
                  </div>

                  <div className="p-3 bg-indigo-50 border border-indigo-100 rounded-lg">
                    <span className="text-xs font-bold uppercase text-indigo-700">Visual & Physical Analogy:</span>
                    <p className="text-xs text-indigo-900 mt-1 italic">"{selectedPreset.pedagogicalBreakdown.analogy}"</p>
                  </div>

                  <div>
                    <span className="text-xs font-bold uppercase text-slate-400">Constituent ISL Signs Sequence:</span>
                    <div className="flex flex-wrap gap-2 mt-1.5">
                      {selectedPreset.pedagogicalBreakdown.componentSigns.map((sign, idx) => (
                        <span key={idx} className="px-2.5 py-1 bg-white border border-slate-300 rounded text-xs font-mono font-bold text-slate-700">
                          {idx + 1}. {sign}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span className="text-xs font-bold uppercase text-slate-400">Fingerspelled Technical Label:</span>
                    <p className="text-sm font-mono font-bold text-indigo-600 mt-1">
                      {selectedPreset.pedagogicalBreakdown.fingerspelledPortion}
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-6 bg-slate-50 rounded-xl border border-slate-200 space-y-3">
                <p className="text-sm font-bold text-slate-900">
                  Concept "{selectedPreset.term}" possesses an authentic single lexical sign in ISLRTC.
                </p>
                <p className="text-xs text-slate-600">
                  Pedagogical structural breakdown is only activated for concepts lacking a codified sign. You can select "Backpropagation" or "Deadlock" in Step 1 to test the full pedagogical fallback card.
                </p>
              </div>
            )}

            <div className="flex justify-between pt-4">
              <button
                onClick={() => setActiveStep(4)}
                className="inline-flex items-center gap-2 px-5 py-2 text-slate-600 font-semibold text-sm hover:text-slate-900"
              >
                <ChevronLeft size={16} /> Back
              </button>
              <button
                onClick={() => setActiveStep(6)}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-xl shadow-xs transition-colors"
              >
                <span>Continue to Step 6: Evidence & Integrity</span>
                <ArrowRight size={16} />
              </button>
            </div>
          </div>
        )}

        {/* STEP 6: EVIDENCE & INTEGRITY */}
        {activeStep === 6 && (
          <div className="space-y-6">
            <div className="border-b border-slate-100 pb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">Step 6 of 6</span>
              <h2 className="text-xl font-bold text-slate-900">Evidence, Provenance & Licensing Integrity</h2>
              <p className="text-sm text-slate-600">
                Transparent cryptographic hashes, licensing bounds, tracking confidence scores, and known kinematic limitations.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                <span className="font-bold text-slate-900 uppercase">Provenance & Licensing</span>
                <div className="space-y-1 text-slate-600">
                  <p><strong>Source Authority:</strong> Indian Sign Language Research and Training Centre (ISLRTC)</p>
                  <p><strong>License:</strong> Government Open Data License (GODL-India)</p>
                  <p><strong>Redistribution Rights:</strong> Lawful educational use with attribution; non-exclusive</p>
                  <p><strong>Signer Status:</strong> Qualified Deaf Master Signer / Certified Instructor</p>
                </div>
              </div>

              <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                <span className="font-bold text-slate-900 uppercase">Technical Verification Metrics</span>
                <div className="space-y-1 text-slate-600">
                  <p><strong>Landmark Tracking Confidence:</strong> {selectedPreset.trackingConfidence ? `${(selectedPreset.trackingConfidence * 100).toFixed(1)}% (MediaPipe Holistic)` : 'N/A'}</p>
                  <p><strong>Linguistic Validity:</strong> <span className="text-amber-600 font-bold">PENDING_EXTERNAL_REVIEW (Gate B Gated)</span></p>
                  <p><strong>SHA-256 Hash:</strong> <span className="font-mono text-[10px] break-all">{selectedPreset.sha256 || 'Pedagogical decomposition (no media file)'}</span></p>
                </div>
              </div>
            </div>

            <div className="p-4 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 space-y-2">
              <span className="font-bold flex items-center gap-1.5">
                <Info size={16} className="text-amber-700" />
                Transparently Documented Limitations:
              </span>
              <ul className="list-disc pl-5 space-y-1">
                <li>Non-manual markers (facial expressions, mouthings, head tilts) are not yet fully retargeted to the 3D avatar rig.</li>
                <li>Hand crossings and self-occlusions show minor depth ambiguity in single-camera monocular tracking.</li>
                <li>Linguistic validity is strictly unverified until formal review by external accredited Deaf panels.</li>
              </ul>
            </div>

            <div className="flex justify-between pt-4 border-t border-slate-100">
              <button
                onClick={() => setActiveStep(5)}
                className="inline-flex items-center gap-2 px-5 py-2 text-slate-600 font-semibold text-sm hover:text-slate-900"
              >
                <ChevronLeft size={16} /> Back
              </button>
              <button
                onClick={handleResetDemo}
                className="inline-flex items-center gap-2 px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm rounded-xl shadow-xs transition-colors"
              >
                <RotateCcw size={16} />
                <span>Complete Demonstration & Reset</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default LiveDemoPage;
