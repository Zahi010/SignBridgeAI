import React from 'react';
import {
  Play,
  Pause,
  RotateCcw,
  SkipBack,
  SkipForward,
  Repeat,
  Camera,
  Eye,
  Hand
} from 'lucide-react';

export type CameraPreset = 'default' | 'left45' | 'right45' | 'face' | 'hands';

interface AvatarControlsProps {
  isPlaying: boolean;
  onTogglePlay: () => void;
  speed: number;
  onSpeedChange: (speed: number) => void;
  currentTimeSeconds: number;
  totalDurationSeconds: number;
  onSeek: (seconds: number) => void;
  onStepFrame: (direction: 'forward' | 'backward') => void;
  isLooping: boolean;
  onToggleLoop: () => void;
  cameraPreset: CameraPreset;
  onSelectCameraPreset: (preset: CameraPreset) => void;
  onReset: () => void;
}

const SPEED_OPTIONS = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0];

export const AvatarControls: React.FC<AvatarControlsProps> = ({
  isPlaying,
  onTogglePlay,
  speed,
  onSpeedChange,
  currentTimeSeconds,
  totalDurationSeconds,
  onSeek,
  onStepFrame,
  isLooping,
  onToggleLoop,
  cameraPreset,
  onSelectCameraPreset,
  onReset
}) => {
  const formatTime = (secs: number) => {
    const s = Math.max(0, secs);
    return `${s.toFixed(2)}s`;
  };

  return (
    <div className="bg-slate-900 border-t border-slate-800 p-3 space-y-3 text-white select-none">
      {/* Top row: Scrub bar & time readout */}
      <div className="flex items-center gap-3">
        <span className="text-xs font-mono text-slate-400 min-w-[48px]">
          {formatTime(currentTimeSeconds)}
        </span>
        <div className="flex-1 relative flex items-center">
          <input
            type="range"
            min={0}
            max={Math.max(0.1, totalDurationSeconds)}
            step={0.033}
            value={currentTimeSeconds}
            onChange={(e) => onSeek(parseFloat(e.target.value))}
            className="w-full h-1.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
        <span className="text-xs font-mono text-slate-400 min-w-[48px] text-right">
          {formatTime(totalDurationSeconds)}
        </span>
      </div>

      {/* Middle row: Playback transport & speed */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-1.5">
          {/* Step backward */}
          <button
            onClick={() => onStepFrame('backward')}
            title="Step Back 1 Frame (33ms)"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            <SkipBack size={15} />
          </button>

          {/* Play / Pause */}
          <button
            onClick={onTogglePlay}
            title={isPlaying ? 'Pause' : 'Play'}
            className="p-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-md shadow-blue-900/40 transition"
          >
            {isPlaying ? <Pause size={17} /> : <Play size={17} className="ml-0.5" />}
          </button>

          {/* Step forward */}
          <button
            onClick={() => onStepFrame('forward')}
            title="Step Forward 1 Frame (33ms)"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            <SkipForward size={15} />
          </button>

          {/* Loop toggle */}
          <button
            onClick={onToggleLoop}
            title={isLooping ? 'Loop Enabled' : 'Loop Disabled'}
            className={`p-1.5 rounded-lg transition ${
              isLooping
                ? 'bg-blue-950 text-blue-300 border border-blue-700'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            <Repeat size={15} />
          </button>

          {/* Reset */}
          <button
            onClick={onReset}
            title="Reset Avatar to Neutral Rest Posture"
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            <RotateCcw size={15} />
          </button>
        </div>

        {/* Speed Selector */}
        <div className="flex items-center gap-1 bg-slate-800/80 p-1 rounded-lg border border-slate-700/60">
          <span className="text-[10px] uppercase font-semibold text-slate-400 px-1">Speed</span>
          {SPEED_OPTIONS.map((s) => (
            <button
              key={s}
              onClick={() => onSpeedChange(s)}
              className={`px-1.5 py-0.5 rounded text-xs font-mono transition ${
                speed === s
                  ? 'bg-blue-600 text-white font-semibold'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Bottom row: Camera presets */}
      <div className="flex flex-wrap items-center gap-1.5 pt-1 border-t border-slate-800/60 text-xs">
        <span className="text-[11px] font-medium text-slate-400 flex items-center gap-1 mr-1">
          <Camera size={13} className="text-slate-400" /> Camera:
        </span>
        <button
          onClick={() => onSelectCameraPreset('default')}
          className={`px-2 py-1 rounded-md text-xs font-medium transition ${
            cameraPreset === 'default'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-800'
          }`}
        >
          Front
        </button>
        <button
          onClick={() => onSelectCameraPreset('left45')}
          className={`px-2 py-1 rounded-md text-xs font-medium transition ${
            cameraPreset === 'left45'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-800'
          }`}
        >
          45° Left
        </button>
        <button
          onClick={() => onSelectCameraPreset('right45')}
          className={`px-2 py-1 rounded-md text-xs font-medium transition ${
            cameraPreset === 'right45'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-800'
          }`}
        >
          45° Right
        </button>
        <button
          onClick={() => onSelectCameraPreset('face')}
          className={`px-2 py-1 rounded-md text-xs font-medium flex items-center gap-1 transition ${
            cameraPreset === 'face'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-800'
          }`}
        >
          <Eye size={12} /> Face NMM
        </button>
        <button
          onClick={() => onSelectCameraPreset('hands')}
          className={`px-2 py-1 rounded-md text-xs font-medium flex items-center gap-1 transition ${
            cameraPreset === 'hands'
              ? 'bg-slate-700 text-white'
              : 'text-slate-400 hover:bg-slate-800'
          }`}
        >
          <Hand size={12} /> Hands
        </button>
      </div>
    </div>
  );
};

