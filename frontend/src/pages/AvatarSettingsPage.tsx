import React, { useState } from 'react';
import {
  Sliders,
  User,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
  Eye,
  Zap,
  RotateCcw
} from 'lucide-react';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const AvatarSettingsPage: React.FC = () => {
  const [avatarStyle, setAvatarStyle] = useState<'academic' | 'neutral' | 'high_contrast'>('academic');
  const [defaultSpeed, setDefaultSpeed] = useState<number>(1.0);
  const [handClarityBoost, setHandClarityBoost] = useState<boolean>(true);
  const [nmmExpressiveness, setNmmExpressiveness] = useState<'standard' | 'amplified'>('standard');
  const [savedNotice, setSavedNotice] = useState(false);

  const handleSaveSettings = () => {
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 3000);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              3D Avatar Studio & Rig Settings
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
              Three.js · R3F Engine
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Configure signing workspace visualization, camera ergonomics, and accessibility preferences.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: Live Interactive Avatar Canvas */}
        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
            <span>Live Interactive WebGL Preview:</span>
            <span className="text-indigo-600 font-mono text-[11px]">Orbit / Zoom Enabled</span>
          </div>
          <AvatarViewer />
          <p className="text-[11px] text-slate-500 text-center">
            Click and drag to rotate the camera. Scroll to zoom in/out on signing hands.
          </p>
        </div>

        {/* Right Column: Settings Form */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <div className="flex items-center gap-2">
              <Sliders size={18} className="text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900">Avatar Configuration</h3>
            </div>
            {savedNotice && (
              <span className="text-xs text-emerald-600 font-bold flex items-center gap-1 animate-fade-in">
                <CheckCircle2 size={14} /> Settings Saved
              </span>
            )}
          </div>

          {/* Avatar Theme Style */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-800 uppercase tracking-wider block">
              Signer Avatar Style:
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { id: 'academic', label: 'Academic Blue', desc: 'Standard classroom' },
                { id: 'neutral', label: 'Neutral Gray', desc: 'Minimal distraction' },
                { id: 'high_contrast', label: 'High Contrast', desc: 'Max visual clarity' },
              ].map((style) => (
                <button
                  key={style.id}
                  onClick={() => setAvatarStyle(style.id as any)}
                  className={`p-3 rounded-xl border text-left transition-all ${
                    avatarStyle === style.id
                      ? 'border-indigo-600 bg-indigo-50/70 text-indigo-900 shadow-2xs'
                      : 'border-slate-200 hover:border-slate-300 text-slate-700'
                  }`}
                >
                  <span className="text-xs font-bold block">{style.label}</span>
                  <span className="text-[10px] text-slate-500">{style.desc}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Default Playback Speed */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-800 uppercase tracking-wider block">
              Default Signing Pace:
            </label>
            <div className="flex items-center gap-2">
              {[0.75, 1.0, 1.25].map((spd) => (
                <button
                  key={spd}
                  onClick={() => setDefaultSpeed(spd)}
                  className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${
                    defaultSpeed === spd
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {spd}x {spd === 1.0 && '(Natural)'}
                </button>
              ))}
            </div>
          </div>

          {/* Accessibility Enhancements */}
          <div className="space-y-3 pt-2 border-t border-slate-100">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Accessibility Enhancements
            </h4>

            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-200/80">
              <div className="space-y-0.5">
                <span className="text-xs font-bold text-slate-900 block">Hand Clarity & Silhouette Boost</span>
                <span className="text-[11px] text-slate-500">Subtle outline contrast for precise finger-configuration recognition</span>
              </div>
              <input
                type="checkbox"
                checked={handClarityBoost}
                onChange={(e) => setHandClarityBoost(e.target.checked)}
                className="w-4 h-4 text-indigo-600 rounded focus:ring-indigo-500 cursor-pointer"
              />
            </div>

            <div className="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-200/80">
              <div className="space-y-0.5">
                <span className="text-xs font-bold text-slate-900 block">Non-Manual Marker (NMM) Expression</span>
                <span className="text-[11px] text-slate-500">Eyebrow furrowing and head tilt cues for grammatical questions</span>
              </div>
              <select
                value={nmmExpressiveness}
                onChange={(e) => setNmmExpressiveness(e.target.value as any)}
                className="text-xs px-2.5 py-1.5 rounded-lg border border-slate-300 bg-white text-slate-700 font-medium"
              >
                <option value="standard">Standard NMM</option>
                <option value="amplified">Amplified NMM</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleSaveSettings}
            className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs rounded-xl shadow-md transition-colors cursor-pointer"
          >
            Save Avatar Preferences
          </button>
        </div>
      </div>

      {/* Integration Roadmap Transparency */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-3">
        <div className="flex items-center gap-2">
          <ShieldCheck size={18} className="text-blue-600" />
          <h3 className="text-sm font-bold text-slate-900">
            3D Animation Asset Pipeline & Policy Compliance
          </h3>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          SignBridge AI's 3D avatar pipeline uses standard MediaPipe-Holistic 54-keypoint skeletal rigs and ReadyPlayerMe-compatible GLTF/GLB models. 
          In accordance with our <strong>Zero Fabricated Signs Policy</strong>, procedural animation clips are only linked to vocabulary items once peer-reviewed motion-capture recordings from deaf native signers are authenticated. 
          When no verified animation is available, the neutral posture preview is presented with honest status disclosure.
        </p>
      </div>
    </div>
  );
};

