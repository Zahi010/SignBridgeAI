import React from 'react';
import { AvatarAnimationTrack, MotionVerificationStatus } from '../../types';
import { AnimationStatusBadge } from './AnimationStatusBadge';

interface AnimationTimelineProps {
  tracks: AvatarAnimationTrack[];
  currentTimeSeconds: number;
  totalDurationSeconds: number;
  onSeek: (seconds: number) => void;
  activeTrackIndex?: number;
}

export const AnimationTimeline: React.FC<AnimationTimelineProps> = ({
  tracks,
  currentTimeSeconds,
  totalDurationSeconds,
  onSeek,
  activeTrackIndex
}) => {
  if (!tracks || tracks.length === 0) {
    return (
      <div className="bg-slate-900/90 border-t border-slate-800 p-3 text-center text-xs text-slate-500">
        No active animation timeline. Avatar is maintaining neutral resting posture.
      </div>
    );
  }

  const effectiveDuration = Math.max(0.1, totalDurationSeconds);
  const playheadPercent = Math.min(100, Math.max(0, (currentTimeSeconds / effectiveDuration) * 100));

  const handleTimelineClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const ratio = Math.max(0, Math.min(1, clickX / rect.width));
    onSeek(ratio * effectiveDuration);
  };

  return (
    <div className="bg-slate-900 border-t border-slate-800 p-3 space-y-2 text-white">
      <div className="flex items-center justify-between text-xs font-semibold text-slate-300">
        <span className="flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
          Animation Sequence Timeline
        </span>
        <span className="text-[11px] font-mono text-slate-400">
          {tracks.length} {tracks.length === 1 ? 'Track' : 'Tracks'} • {effectiveDuration.toFixed(2)}s Total
        </span>
      </div>

      {/* Interactive visual track bar */}
      <div
        onClick={handleTimelineClick}
        className="relative h-14 bg-slate-950 rounded-xl overflow-hidden border border-slate-800 cursor-pointer select-none group"
      >
        {/* Track blocks */}
        <div className="absolute inset-0 flex h-full">
          {tracks.map((track, idx) => {
            const widthPct = Math.max(3, (track.duration_seconds / effectiveDuration) * 100);
            const isCurrent =
              currentTimeSeconds >= track.start_time_seconds &&
              currentTimeSeconds <= track.start_time_seconds + track.duration_seconds;

            let bgColor = 'bg-slate-800/60 border-slate-700/80';
            if (track.verification_status === 'VERIFIED_ISL_MOTION') {
              bgColor = isCurrent ? 'bg-emerald-900/60 border-emerald-500' : 'bg-emerald-950/40 border-emerald-800/40';
            } else if (
              track.verification_status === 'PARTIALLY_VERIFIED_MOTION' ||
              track.verification_status === ('partial' as MotionVerificationStatus)
            ) {
              bgColor = isCurrent ? 'bg-amber-900/60 border-amber-500' : 'bg-amber-950/40 border-amber-800/40';
            } else if (track.verification_status === 'REQUIRES_LINGUISTIC_REVIEW') {
              bgColor = isCurrent ? 'bg-blue-900/60 border-blue-500' : 'bg-blue-950/40 border-blue-800/40';
            } else if (track.verification_status === 'DEMO_ONLY') {
              bgColor = isCurrent ? 'bg-purple-900/60 border-purple-500' : 'bg-purple-950/40 border-purple-800/40';
            }

            return (
              <div
                key={track.track_id || idx}
                style={{ width: `${widthPct}%` }}
                className={`h-full border-r relative flex flex-col justify-between p-1.5 transition-colors ${bgColor}`}
              >
                <div className="flex items-center justify-between gap-1 overflow-hidden">
                  <span className="text-[11px] font-bold font-mono truncate text-white">
                    {track.gloss_token}
                  </span>
                  <span className="text-[9px] font-mono text-slate-400">
                    {track.duration_seconds.toFixed(1)}s
                  </span>
                </div>
                <div className="flex items-center justify-between text-[9px] text-slate-400 truncate">
                  <span>{track.track_type.replace('_', ' ')}</span>
                  {track.keyframes && track.keyframes.length > 0 && (
                    <span className="text-[8px] bg-slate-800 px-1 rounded">
                      {track.keyframes.length} kf
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Playhead needle */}
        <div
          style={{ left: `${playheadPercent}%` }}
          className="absolute top-0 bottom-0 w-0.5 bg-red-500 shadow-md pointer-events-none z-10 flex flex-col items-center"
        >
          <div className="w-2.5 h-2.5 bg-red-500 rotate-45 -mt-1 rounded-xs" />
        </div>
      </div>

      {/* Active Track Metadata Card */}
      {tracks.length > 0 && (
        <div className="bg-slate-950/60 rounded-lg p-2 border border-slate-800/80 text-xs flex flex-wrap items-center justify-between gap-2">
          {(() => {
            const currentTrack =
              tracks.find(
                (t) =>
                  currentTimeSeconds >= t.start_time_seconds &&
                  currentTimeSeconds <= t.start_time_seconds + t.duration_seconds
              ) || tracks[0];

            return (
              <>
                <div className="flex items-center gap-2">
                  <span className="text-slate-400">Active Token:</span>
                  <span className="font-bold text-white font-mono">{currentTrack.gloss_token}</span>
                  {currentTrack.concept_term && (
                    <span className="text-slate-400">({currentTrack.concept_term})</span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <AnimationStatusBadge status={currentTrack.verification_status} />
                  {currentTrack.is_mocap && (
                    <span className="text-[10px] bg-blue-950 text-blue-300 border border-blue-800 px-1.5 py-0.5 rounded font-mono">
                      Mocap 54-Rig
                    </span>
                  )}
                </div>
              </>
            );
          })()}
        </div>
      )}
    </div>
  );
};

