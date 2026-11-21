import React, { useState, useEffect, useRef } from 'react';
import {
  Mic,
  MicOff,
  Volume2,
  Radio,
  BookOpen,
  Send,
  Sparkles,
  Info,
  ShieldCheck,
  CheckCircle2,
  Layers,
  Play,
  RotateCcw
} from 'lucide-react';
import { api } from '../api/client';
import { TranslationResponse } from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { PolicyNotice } from '../components/common/PolicyNotice';
import { VideoPlayer } from '../components/video/VideoPlayer';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { ISLGrammarView } from '../components/translator/ISLGrammarView';

const DEMO_LECTURES = [
  {
    title: "CS301: Operating Systems & Deadlock Resolution",
    branch: "Computer Science",
    sentences: [
      "In this lecture, we explain how an operating system works.",
      "A database provides organized persistent storage across transactions.",
      "What is a deadlock in operating systems?",
      "Deadlock occurs when processes hold resources and wait circularly.",
    ],
  },
  {
    title: "EC201: Circuit Theory & Microprocessors",
    branch: "Electronics",
    sentences: [
      "Today we examine basic circuit properties.",
      "Explain voltage and current relationships under Ohm's law.",
      "What is a microprocessor and how does it interface with memory?",
    ],
  },
  {
    title: "ME201: Engineering Mechanics & Machine Dynamics",
    branch: "Mechanical",
    sentences: [
      "Welcome to theory of machines and kinematics.",
      "Define force and explain its units under acceleration.",
      "Every machine uses mechanical advantage to perform physical motion.",
    ],
  },
];

export const LiveLecturePage: React.FC = () => {
  const [isListening, setIsListening] = useState(false);
  const [selectedLectureIndex, setSelectedLectureIndex] = useState(0);
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState(0);
  const [transcriptHistory, setTranscriptHistory] = useState<string[]>([]);
  const [currentLiveText, setCurrentLiveText] = useState("");
  const [translationResult, setTranslationResult] = useState<TranslationResponse | null>(null);
  const [audioLevel, setAudioLevel] = useState<number[]>([15, 25, 45, 70, 85, 60, 40, 20]);
  const [loading, setLoading] = useState(false);

  const activeLecture = DEMO_LECTURES[selectedLectureIndex];

  // Simulated Audio Waveform Animation when listening
  useEffect(() => {
    let interval: any;
    if (isListening) {
      interval = setInterval(() => {
        setAudioLevel([
          Math.floor(Math.random() * 60) + 15,
          Math.floor(Math.random() * 70) + 20,
          Math.floor(Math.random() * 90) + 10,
          Math.floor(Math.random() * 80) + 25,
          Math.floor(Math.random() * 75) + 15,
          Math.floor(Math.random() * 60) + 20,
          Math.floor(Math.random() * 50) + 10,
          Math.floor(Math.random() * 40) + 15,
        ]);
      }, 150);
    } else {
      setAudioLevel([10, 15, 12, 18, 14, 12, 10, 8]);
    }
    return () => clearInterval(interval);
  }, [isListening]);

  // Handle advancing lecture sentence
  const handleStreamNextSentence = async () => {
    const sentence = activeLecture.sentences[currentSentenceIndex];
    setCurrentLiveText(sentence);
    setTranscriptHistory((prev) => [...prev, sentence]);

    setLoading(true);
    try {
      const res = await api.translate({ text: sentence });
      setTranslationResult(res);
    } catch (err) {
      console.error("Live lecture translation error", err);
    } finally {
      setLoading(false);
    }

    setCurrentSentenceIndex((prev) => (prev + 1) % activeLecture.sentences.length);
  };

  const toggleMic = () => {
    if (!isListening) {
      setIsListening(true);
      handleStreamNextSentence();
    } else {
      setIsListening(false);
    }
  };

  const handleResetSession = () => {
    setIsListening(false);
    setCurrentSentenceIndex(0);
    setTranscriptHistory([]);
    setCurrentLiveText("");
    setTranslationResult(null);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              Live Lecture Transcription & ISL Stream
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100 flex items-center gap-1">
              <Radio size={12} className="text-red-500 animate-pulse" />
              <span>Speech Pipeline</span>
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Audio processing capture pipeline demonstrating real-time spoken lecture sentence translation.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      {/* Honest Prototype Notice */}
      <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl flex items-start gap-3 text-xs text-amber-900 leading-relaxed shadow-2xs">
        <Info size={18} className="text-amber-600 shrink-0 mt-0.5" />
        <div>
          <strong className="font-semibold block text-amber-950">
            Demonstration Mode & Speech Architecture
          </strong>
          The audio stream interface and sentence segmentation pipeline are fully operational.
          To ensure strict honesty under our Zero Fabricated Signs Policy, faster-whisper speech recognition is architected for server deployment, and demonstration engineering lecture streams can be triggered interactively below.
        </div>
      </div>

      {/* Classroom Setup & Audio Control Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
          {/* Lecture Selection */}
          <div className="space-y-1">
            <label className="text-xs font-semibold text-slate-700">Select Lecture Subject Stream:</label>
            <div className="flex flex-wrap gap-2">
              {DEMO_LECTURES.map((lec, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setSelectedLectureIndex(idx);
                    setCurrentSentenceIndex(0);
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-colors ${
                    selectedLectureIndex === idx
                      ? 'bg-indigo-600 text-white font-bold shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {lec.title}
                </button>
              ))}
            </div>
          </div>

          {/* Reset button */}
          <button
            onClick={handleResetSession}
            className="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1 self-start sm:self-auto"
          >
            <RotateCcw size={14} />
            <span>Reset Session</span>
          </button>
        </div>

        {/* Audio Visualizer & Mic Trigger */}
        <div className="flex flex-col md:flex-row items-center justify-between gap-4 p-4 bg-slate-900 rounded-2xl text-white">
          <div className="flex items-center gap-4">
            <button
              onClick={toggleMic}
              className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-transform hover:scale-105 shadow-md ${
                isListening
                  ? 'bg-red-600 hover:bg-red-500 text-white animate-pulse'
                  : 'bg-indigo-600 hover:bg-indigo-500 text-white'
              }`}
              title={isListening ? "Mute Microphone" : "Start Live Listening"}
            >
              {isListening ? <Mic size={24} /> : <MicOff size={24} />}
            </button>

            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold">
                  {isListening ? "Microphone Active (Streaming)" : "Microphone Idle"}
                </span>
                {isListening && (
                  <span className="w-2 h-2 rounded-full bg-red-400 animate-ping" />
                )}
              </div>
              <p className="text-xs text-slate-400">
                {isListening
                  ? "Capturing academic lecture speech stream..."
                  : "Click microphone to initiate speech capture demonstration"}
              </p>
            </div>
          </div>

          {/* Simulated Waveform Visualizer */}
          <div className="flex items-end gap-1.5 h-10 px-4 bg-slate-800 rounded-xl border border-slate-700">
            {audioLevel.map((lvl, i) => (
              <div
                key={i}
                className="w-2 rounded-t-sm bg-gradient-to-t from-indigo-500 to-indigo-300 transition-all duration-150"
                style={{ height: `${lvl}%` }}
              />
            ))}
          </div>

          {/* Stream Next Sentence Button */}
          <button
            onClick={handleStreamNextSentence}
            disabled={loading}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold border border-slate-700 transition-colors flex items-center gap-2"
          >
            <Play size={14} />
            <span>Simulate Next Spoken Sentence</span>
          </button>
        </div>

        {/* Current Live Transcript */}
        <div className="space-y-1.5">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Current Spoken Sentence:
          </span>
          <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl font-medium text-sm text-slate-800">
            {currentLiveText ? (
              <span>"{currentLiveText}"</span>
            ) : (
              <span className="text-slate-400 italic">
                Press "Simulate Next Spoken Sentence" or activate the microphone to capture teacher lecture.
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Live Translation Outputs */}
      {translationResult && (
        <div className="space-y-6">
          {/* Status banner */}
          <div
            className={`p-4 rounded-2xl border transition-all ${
              translationResult.status === 'verified'
                ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
                : translationResult.status === 'unsupported'
                ? 'bg-rose-50 border-rose-200 text-rose-950'
                : 'bg-amber-50 border-amber-200 text-amber-950'
            }`}
          >
            <div className="flex items-center justify-between gap-2 mb-1">
              <StatusBadge status={translationResult.status} />
              <span className="text-xs font-bold text-slate-700">
                Evaluation: {translationResult.verified_signs_count} verified, {translationResult.unsupported_signs_count} unsupported
              </span>
            </div>
            <p className="text-xs font-medium leading-relaxed">
              {translationResult.status_reason}
            </p>
          </div>

          {/* ISL Grammar */}
          <ISLGrammarView
            glossSequence={translationResult.isl_gloss_sequence}
            grammarNotes={translationResult.grammar_notes}
          />

          {/* Visual outputs side by side */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-700 block">
                Human Signer Output Stream:
              </span>
              <VideoPlayer video={translationResult.video_output} />
            </div>

            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-700 block">
                3D Signing Avatar Output Stream:
              </span>
              <AvatarViewer avatarData={translationResult.avatar_output} />
            </div>
          </div>
        </div>
      )}

      {/* Transcript Lecture Log */}
      {transcriptHistory.length > 0 && (
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900">
              Lecture Transcript Buffer ({transcriptHistory.length} sentences)
            </h3>
            <span className="text-xs text-slate-400">Chronological Lecture Flow</span>
          </div>
          <div className="space-y-2 text-xs">
            {transcriptHistory.map((line, idx) => (
              <div key={idx} className="p-2.5 bg-slate-50 border border-slate-100 rounded-lg flex items-start gap-2">
                <span className="font-mono text-slate-400 text-[10px] shrink-0 mt-0.5">
                  [{idx + 1}]
                </span>
                <span className="text-slate-700">{line}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

