import React, { useState, useEffect, useRef } from 'react';
import {
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Play,
  Pause,
  RotateCcw,
  SkipBack,
  SkipForward,
  UserCheck,
  Award,
  Video,
  Eye,
  AlertOctagon,
  HelpCircle,
  FileText
} from 'lucide-react';
import { api } from '../api/client';
import { Phase5Task, Phase5Reviewer, Phase5CriterionRating, Phase5Annotation } from '../types';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { EvaluationRubricForm } from '../components/validation/EvaluationRubricForm';
import { ReviewerAuthModal } from '../components/validation/ReviewerAuthModal';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const ExpertReviewPortalPage: React.FC = () => {
  const [tasks, setTasks] = useState<Phase5Task[]>([]);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
  const [taskDetail, setTaskDetail] = useState<any | null>(null);
  const [currentUser, setCurrentUser] = useState<Phase5Reviewer | null>(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);

  // Playback sync states
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTimeMs, setCurrentTimeMs] = useState(0);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [durationMs, setDurationMs] = useState(3000);
  const [submitting, setSubmitting] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState<string | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const animationFrameRef = useRef<number | null>(null);

  // Load current user from token on mount
  useEffect(() => {
    const token = localStorage.getItem('signbridge_reviewer_token');
    if (token) {
      api.getCurrentReviewer(token)
        .then((user: any) => setCurrentUser(user))
        .catch(() => localStorage.removeItem('signbridge_reviewer_token'));
    }
  }, []);

  // Load tasks on mount
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const data = await api.listValidationTasks();
      setTasks(data);
      if (data.length > 0 && !selectedTaskId) {
        setSelectedTaskId(data[0].id);
      }
    } catch (err) {
      console.error('Failed to load validation tasks', err);
    }
  };

  // Load selected task details
  useEffect(() => {
    if (selectedTaskId) {
      api.getValidationTaskDetail(selectedTaskId)
        .then((detail: any) => {
          setTaskDetail(detail);
          setCurrentTimeMs(0);
          setIsPlaying(false);
        })
        .catch((err: any) => console.error('Failed to load task details', err));
    }
  }, [selectedTaskId]);

  // Synchronized playback loop
  useEffect(() => {
    if (isPlaying) {
      const startTime = performance.now() - currentTimeMs / playbackSpeed;
      const step = () => {
        const elapsed = (performance.now() - startTime) * playbackSpeed;
        if (elapsed >= durationMs) {
          setCurrentTimeMs(0);
          setIsPlaying(false);
          if (videoRef.current) videoRef.current.currentTime = 0;
        } else {
          setCurrentTimeMs(Math.floor(elapsed));
          if (videoRef.current && Math.abs(videoRef.current.currentTime - elapsed / 1000) > 0.1) {
            videoRef.current.currentTime = elapsed / 1000;
          }
          animationFrameRef.current = requestAnimationFrame(step);
        }
      };
      animationFrameRef.current = requestAnimationFrame(step);
    } else {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    }
    return () => {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
    };
  }, [isPlaying, playbackSpeed, durationMs]);

  const togglePlay = () => {
    const nextPlay = !isPlaying;
    setIsPlaying(nextPlay);
    if (videoRef.current) {
      if (nextPlay) videoRef.current.play().catch(() => {});
      else videoRef.current.pause();
    }
  };

  const stepFrame = (deltaMs: number) => {
    setIsPlaying(false);
    if (videoRef.current) videoRef.current.pause();
    const nextTime = Math.max(0, Math.min(durationMs, currentTimeMs + deltaMs));
    setCurrentTimeMs(nextTime);
    if (videoRef.current) videoRef.current.currentTime = nextTime / 1000;
  };

  const handleSeek = (ms: number) => {
    setCurrentTimeMs(ms);
    if (videoRef.current) videoRef.current.currentTime = ms / 1000;
  };

  const handleEvaluationSubmit = async (formData: {
    isDraft: boolean;
    overallRecommendation: string;
    generalFeedback: string;
    suggestedDialect: string;
    criteriaRatings: Phase5CriterionRating[];
    annotations: Phase5Annotation[];
  }) => {
    if (!selectedTaskId) return;
    setSubmitting(true);
    setFeedbackMsg(null);
    try {
      const token = localStorage.getItem('signbridge_reviewer_token') || undefined;
      await api.submitTaskEvaluation(selectedTaskId, {
        task_id: selectedTaskId,
        ...formData
      }, token);
      setFeedbackMsg(formData.isDraft ? 'Draft evaluation saved successfully.' : 'Evaluation submitted! Status updated.');
      fetchTasks();
      if (selectedTaskId) {
        const updated = await api.getValidationTaskDetail(selectedTaskId);
        setTaskDetail(updated);
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to submit evaluation.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-20">
      {/* Top Header & Reviewer Status Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              ISL Expert Review & Validation Portal
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
              Phase 5 Linguistic Gate
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Synchronized human-vs-avatar evaluation, 12-criterion phonological rubric, and disagreement adjudication.
          </p>
        </div>

        {/* Reviewer identity badge */}
        <div className="flex items-center gap-3">
          {currentUser ? (
            <div className="flex items-center gap-2.5 p-2 px-3 bg-slate-50 rounded-xl border border-slate-200">
              <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold text-xs">
                {currentUser.full_name[0]}
              </div>
              <div>
                <p className="text-xs font-bold text-slate-900 leading-none">{currentUser.full_name}</p>
                <div className="flex items-center gap-1.5 mt-1">
                  <span className={`text-[10px] font-bold uppercase px-1.5 py-0.2 rounded ${
                    currentUser.verification_status === 'verified'
                      ? 'bg-emerald-100 text-emerald-800'
                      : 'bg-amber-100 text-amber-800'
                  }`}>
                    {currentUser.verification_status}
                  </span>
                  <button
                    onClick={() => setIsAuthModalOpen(true)}
                    className="text-[10px] text-indigo-600 hover:underline font-semibold"
                  >
                    Manage Credentials
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold hover:bg-indigo-700 transition shadow flex items-center gap-1.5"
            >
              <UserCheck size={15} />
              <span>Sign In / Register Reviewer</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left: Task Queue */}
        <div className="lg:col-span-1 space-y-3">
          <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
            <h3 className="text-xs font-extrabold uppercase text-slate-700 tracking-wider mb-2 flex items-center justify-between">
              <span>Candidate Signs Queue</span>
              <span className="text-indigo-600 font-mono">({tasks.length})</span>
            </h3>

            <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
              {tasks.map((t) => {
                const isSelected = selectedTaskId === t.id;
                return (
                  <button
                    key={t.id}
                    onClick={() => setSelectedTaskId(t.id)}
                    className={`w-full text-left p-3 rounded-xl border transition flex flex-col gap-1 ${
                      isSelected
                        ? 'bg-indigo-50 border-indigo-300 shadow-sm'
                        : 'bg-slate-50/60 border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-slate-900">{t.concept_term}</span>
                      <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded ${
                        t.status === 'disagreement_detected'
                          ? 'bg-rose-100 text-rose-800 border border-rose-200'
                          : t.status === 'under_review'
                          ? 'bg-amber-100 text-amber-800'
                          : t.status === 'reviewed'
                          ? 'bg-blue-100 text-blue-800'
                          : 'bg-slate-200 text-slate-700'
                      }`}>
                        {t.status.replace('_', ' ')}
                      </span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-500">{t.sign_gloss}</span>
                    <div className="flex items-center gap-2 mt-1 text-[10px] text-slate-500">
                      <span>Reviews: {t.completed_reviews_count}</span>
                      {t.disagreements_count > 0 && (
                        <span className="text-rose-600 font-bold flex items-center gap-0.5">
                          <AlertTriangle size={11} /> {t.disagreements_count} Conflicts
                        </span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          <PolicyNotice compact />
        </div>

        {/* Right: Dual Viewport & Rubric */}
        <div className="lg:col-span-3 space-y-6">
          {taskDetail ? (
            <>
              {/* Sign Concept Details Card */}
              <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-lg font-bold text-slate-900">{taskDetail.concept.term}</h2>
                    <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 text-xs font-mono">
                      {taskDetail.sign_record.sign_gloss}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 mt-1 max-w-2xl">{taskDetail.concept.definition}</p>
                </div>

                <div className="shrink-0 flex items-center gap-2">
                  <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-1 rounded-lg border border-amber-200">
                    Technical: Partially Verified
                  </span>
                  <span className="text-xs font-bold text-slate-700 bg-slate-100 px-2.5 py-1 rounded-lg border border-slate-200">
                    Linguistic: {taskDetail.status.toUpperCase()}
                  </span>
                </div>
              </div>

              {/* Disagreement Warning Banner */}
              {taskDetail.disagreements && taskDetail.disagreements.length > 0 && (
                <div className="bg-rose-50 border border-rose-200 p-4 rounded-2xl flex items-start gap-3 text-rose-900 text-xs">
                  <AlertOctagon size={18} className="text-rose-600 shrink-0 mt-0.5" />
                  <div className="space-y-1">
                    <p className="font-bold">Inter-Reviewer Linguistic Disagreement Detected!</p>
                    <p>
                      Multiple expert reviewers have submitted conflicting evaluations for this sign. An administrative adjudication or additional review is required before this sign can proceed.
                    </p>
                  </div>
                </div>
              )}

              {/* Synchronized Dual Viewport (Human vs Avatar) */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900 p-4 rounded-2xl shadow-lg border border-slate-800">
                {/* Left: Authentic Human ISLRTC Video */}
                <div className="flex flex-col space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-300 font-bold px-1">
                    <span className="flex items-center gap-1.5 text-emerald-400">
                      <Video size={14} /> Authentic ISLRTC Reference Video
                    </span>
                    <span className="text-[10px] text-slate-400">1080p Frontal Studio</span>
                  </div>
                  <div className="relative aspect-video bg-black rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center">
                    {taskDetail.video.available && taskDetail.video.video_path ? (
                      <video
                        ref={videoRef}
                        src={taskDetail.video.video_path}
                        className="w-full h-full object-contain"
                        onLoadedMetadata={(e) => {
                          const d = e.currentTarget.duration * 1000;
                          if (d > 0) setDurationMs(Math.round(d));
                        }}
                      />
                    ) : (
                      <div className="text-center p-4 text-slate-500 text-xs">
                        Reference video stream loaded via normalized ISLRTC cache.
                      </div>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-400 px-1 truncate">
                    Source: {taskDetail.video.source_attribution || 'ISLRTC Official Benchmark'}
                  </div>
                </div>

                {/* Right: 3D Articulated Avatar */}
                <div className="flex flex-col space-y-2">
                  <div className="flex items-center justify-between text-xs text-slate-300 font-bold px-1">
                    <span className="flex items-center gap-1.5 text-indigo-400">
                      <Eye size={14} /> 3D Articulated Avatar (54-Joint Rig)
                    </span>
                    <span className="text-[10px] text-slate-400">WebGL 60 FPS</span>
                  </div>
                  <div className="aspect-video bg-slate-950 rounded-xl overflow-hidden border border-slate-800">
                    <AvatarViewer
                      conceptTerm={taskDetail.concept.term}
                      avatarData={{
                        available: true,
                        model_type: 'SignBridge-Articulated-54',
                        animation_name: `islrtc_${taskDetail.concept.term.toLowerCase()}_mocap`,
                        rig_standard: 'SignBridge-Articulated-54',
                        validation_status: 'partial',
                        motion_status: 'PARTIALLY_VERIFIED_MOTION',
                        notice: 'Authentic mocap retargeted to 54-joint rig.'
                      }}
                    />
                  </div>
                  <div className="text-[11px] text-slate-400 px-1">
                    Rig: SignBridge-Articulated-54 (15 finger phalanges per hand)
                  </div>
                </div>
              </div>

              {/* Master Synchronized Transport Bar */}
              <div className="bg-slate-800 text-white p-3.5 rounded-xl flex flex-wrap items-center justify-between gap-3 shadow">
                <div className="flex items-center gap-2">
                  <button
                    onClick={togglePlay}
                    className="p-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 transition"
                  >
                    {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                  </button>
                  <button
                    onClick={() => {
                      setCurrentTimeMs(0);
                      setIsPlaying(false);
                      if (videoRef.current) videoRef.current.currentTime = 0;
                    }}
                    className="p-2 rounded-lg bg-slate-700 hover:bg-slate-600 transition"
                  >
                    <RotateCcw size={16} />
                  </button>
                  <button
                    onClick={() => stepFrame(-33)}
                    className="px-2 py-1 text-xs font-mono rounded bg-slate-700 hover:bg-slate-600"
                  >
                    -33ms
                  </button>
                  <button
                    onClick={() => stepFrame(33)}
                    className="px-2 py-1 text-xs font-mono rounded bg-slate-700 hover:bg-slate-600"
                  >
                    +33ms
                  </button>
                </div>

                {/* Scrubber slider */}
                <div className="flex-1 min-w-[200px] flex items-center gap-3">
                  <input
                    type="range"
                    min={0}
                    max={durationMs}
                    value={currentTimeMs}
                    onChange={(e) => handleSeek(Number(e.target.value))}
                    className="w-full h-1.5 bg-slate-600 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                  />
                  <span className="text-xs font-mono text-slate-300 shrink-0">
                    {(currentTimeMs / 1000).toFixed(2)}s / {(durationMs / 1000).toFixed(2)}s
                  </span>
                </div>

                {/* Speed controls */}
                <div className="flex items-center gap-1 text-xs">
                  {[0.25, 0.5, 1.0, 1.5].map((spd) => (
                    <button
                      key={spd}
                      onClick={() => setPlaybackSpeed(spd)}
                      className={`px-2 py-0.5 rounded font-mono ${
                        playbackSpeed === spd ? 'bg-indigo-600 font-bold' : 'bg-slate-700 hover:bg-slate-600'
                      }`}
                    >
                      {spd}x
                    </button>
                  ))}
                </div>
              </div>

              {/* Feedback Alert */}
              {feedbackMsg && (
                <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold">
                  {feedbackMsg}
                </div>
              )}

              {/* 12-Criterion Rubric Form */}
              <EvaluationRubricForm
                taskId={taskDetail.task_id}
                currentTimestampMs={currentTimeMs}
                onSubmit={handleEvaluationSubmit}
                submitting={submitting}
              />
            </>
          ) : (
            <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 text-slate-500 text-xs">
              Select a candidate sign from the queue to start expert review.
            </div>
          )}
        </div>
      </div>

      {/* Reviewer Auth & Credential Modal */}
      <ReviewerAuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        currentUser={currentUser}
        onUserChange={(user: any, token: any) => setCurrentUser(user)}
      />
    </div>
  );
};

export default ExpertReviewPortalPage;
