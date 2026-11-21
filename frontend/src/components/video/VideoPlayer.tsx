import React, { useRef, useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Volume2, VolumeX, ShieldCheck, Film, VideoOff, Maximize2, AlertTriangle } from 'lucide-react';
import { VideoOutput } from '../../types';
import { StatusBadge } from '../common/StatusBadge';

interface VideoPlayerProps {
  video: VideoOutput;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({ video }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isMuted, setIsMuted] = useState(true);

  useEffect(() => {
    setIsPlaying(false);
    setCurrentTime(0);
    if (videoRef.current) {
      videoRef.current.playbackRate = playbackSpeed;
      videoRef.current.currentTime = 0;
    }
  }, [video.video_url]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play().then(() => setIsPlaying(true)).catch(() => { });
    }
  };

  const handleReplay = () => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = 0;
    videoRef.current.play().then(() => setIsPlaying(true)).catch(() => { });
  };

  const handleSpeedChange = (speed: number) => {
    setPlaybackSpeed(speed);
    if (videoRef.current) {
      videoRef.current.playbackRate = speed;
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
      setDuration(videoRef.current.duration || 0);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
  };

  if (!video.available || !video.video_url) {
    return (
      <div className="bg-slate-900/95 text-slate-100 rounded-2xl p-6 h-80 flex flex-col items-center justify-center text-center border border-slate-800 shadow-md">
        <div className="w-14 h-14 bg-slate-800/80 rounded-full flex items-center justify-center text-slate-400 mb-3 border border-slate-700">
          <VideoOff size={26} />
        </div>
        <h4 className="text-base font-semibold text-slate-200 mb-1">No Verified Sign Video</h4>
        <p className="text-xs text-slate-400 max-w-sm leading-relaxed mb-4">
          {video.notes || "In accordance with our Zero Fabricated Signs Policy, SignBridge does not generate synthetic or fake videos when verified human recordings are not yet accredited."}
        </p>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-slate-800 text-slate-300 rounded-full text-[11px] border border-slate-700">
          <ShieldCheck size={13} className="text-blue-400" />
          <span>Awaiting Deaf Peer Validation Corpus</span>
        </div>
      </div>
    );
  }

  const speeds = [0.5, 0.75, 1.0, 1.25];

  const isDemoVideo =
    video.validation_status === 'demo_only' ||
    (video.title && video.title.includes('[DEMO]')) ||
    (video.notes && video.notes.toLowerCase().includes('synthetic'));

  return (
    <div className="bg-slate-900 rounded-2xl overflow-hidden shadow-lg border border-slate-800 text-white flex flex-col">
      {/* Demo media banner */}
      {isDemoVideo && (
        <div className="bg-amber-950/80 border-b border-amber-600/50 px-3 py-1.5 flex items-center gap-2 text-amber-200 text-xs">
          <AlertTriangle size={14} className="shrink-0 text-amber-400" />
          <span className="text-[11px] leading-tight">
            <strong>Benchmark Demo Media:</strong> FFmpeg synthetic test pattern. Authentic Deaf signer recordings scheduled for studio production.
          </span>
        </div>
      )}

      {/* Header bar */}
      <div className="px-4 py-3 bg-slate-800/70 border-b border-slate-700/60 flex items-center justify-between">
        <div className="flex items-center gap-2 min-w-0">
          <Film size={16} className="text-indigo-400 shrink-0" />
          <span className="text-xs font-semibold truncate text-slate-200">
            {video.title || "Authentic ISL Sign Reference Video"}
          </span>
        </div>
        <StatusBadge status={video.validation_status} size="sm" />
      </div>

      {/* Video element */}
      <div className="relative bg-black flex items-center justify-center aspect-video max-h-72">
        <video
          ref={videoRef}
          src={video.video_url}
          className="w-full h-full object-contain cursor-pointer"
          onClick={togglePlay}
          onTimeUpdate={handleTimeUpdate}
          onEnded={handleEnded}
          muted={isMuted}
          playsInline
        />

        {!isPlaying && (
          <button
            onClick={togglePlay}
            className="absolute inset-0 m-auto w-14 h-14 bg-indigo-600/90 hover:bg-indigo-600 text-white rounded-full flex items-center justify-center shadow-lg transition-transform hover:scale-110 focus:outline-none"
            aria-label="Play video"
          >
            <Play size={24} className="ml-1" />
          </button>
        )}
      </div>

      {/* Controls Bar */}
      <div className="p-3 bg-slate-800/90 border-t border-slate-700 space-y-2.5">
        {/* Progress track */}
        <div className="flex items-center gap-2 text-[11px] text-slate-400 font-mono">
          <span>{currentTime.toFixed(1)}s</span>
          <div className="flex-1 bg-slate-700 h-1.5 rounded-full overflow-hidden">
            <div
              className="bg-indigo-500 h-full rounded-full transition-all"
              style={{ width: `${duration > 0 ? (currentTime / duration) * 100 : 0}%` }}
            />
          </div>
          <span>{duration > 0 ? duration.toFixed(1) : video.duration_seconds.toFixed(1)}s</span>
        </div>

        <div className="flex items-center justify-between flex-wrap gap-2">
          {/* Play/Pause & Replay */}
          <div className="flex items-center gap-1.5">
            <button
              onClick={togglePlay}
              className="p-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white transition-colors"
              title={isPlaying ? "Pause" : "Play"}
            >
              {isPlaying ? <Pause size={16} /> : <Play size={16} />}
            </button>
            <button
              onClick={handleReplay}
              className="p-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white transition-colors"
              title="Replay from start"
            >
              <RotateCcw size={16} />
            </button>
            <button
              onClick={() => setIsMuted(!isMuted)}
              className="p-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-white transition-colors"
              title={isMuted ? "Unmute" : "Mute"}
            >
              {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
            </button>
          </div>

          {/* Speed Selector */}
          <div className="flex items-center gap-1 text-xs">
            <span className="text-slate-400 mr-1 text-[11px]">Speed:</span>
            {speeds.map((s) => (
              <button
                key={s}
                onClick={() => handleSpeedChange(s)}
                className={`px-2 py-0.5 rounded text-[11px] font-medium transition-colors ${playbackSpeed === s
                    ? 'bg-indigo-600 text-white font-semibold'
                    : 'bg-slate-700/60 text-slate-300 hover:bg-slate-700'
                  }`}
              >
                {s}x
              </button>
            ))}
          </div>
        </div>

        {/* Source Attribution & License Info */}
        <div className="pt-2 border-t border-slate-700/50 flex flex-col sm:flex-row sm:items-center justify-between text-[11px] text-slate-400 gap-1">
          <div>
            <span className="text-slate-500 font-medium">Attribution: </span>
            <span className="text-slate-300 font-medium">
              {video.source_attribution || "ISLRTC Technical STEM Reference Pilot"}
            </span>
          </div>
          <div className="flex items-center gap-2">
            {video.signer_name && (
              <span className="text-slate-400">
                Signer: <strong className="text-slate-300">{video.signer_name}</strong>
              </span>
            )}
            <span className="px-1.5 py-0.5 bg-slate-700 text-slate-300 rounded font-mono text-[10px]">
              {video.license || "CC-BY-NC"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

