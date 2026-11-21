import React, { useState, useEffect } from 'react';
import {
  Languages,
  Sparkles,
  Send,
  RotateCcw,
  BookOpen,
  Film,
  User,
  AlertCircle,
  HelpCircle,
  CheckCircle2,
  Info,
  Layers,
  ChevronRight,
  Activity,
  Presentation,
  History,
  ShieldCheck,
  Check,
  Flame,
  ArrowRight,
  Mic,
  MicOff
} from 'lucide-react';
import { api } from '../api/client';
import {
  Branch,
  Subject,
  TranslationResponse,
  ExtractedConcept,
  TranslationHistoryItem
} from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { PolicyNotice } from '../components/common/PolicyNotice';
import { VideoPlayer } from '../components/video/VideoPlayer';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { ConceptCard } from '../components/translator/ConceptCard';
import { ISLGrammarView } from '../components/translator/ISLGrammarView';
import { LivePipelinePanel } from '../components/translator/LivePipelinePanel';
import { SemanticRelationsCard } from '../components/translator/SemanticRelationsCard';
import { PedagogicalExplanationCard } from '../components/translator/PedagogicalExplanationCard';
import { TranslationPlanCard } from '../components/translator/TranslationPlanCard';

// Authentic demonstration scenarios across engineering branches
const DEMO_SCENARIOS = [
  {
    id: "scenario-1",
    scenarioName: "Scenario 1: Verified Authentic ISL Sign (Algorithm - CS)",
    text: "What is an algorithm?",
    branchCode: "cs",
    expectedStatus: "verified",
    badgeLabel: "1. Authentic ISLRTC (CS)",
    badgeColor: "bg-emerald-50 text-emerald-800 border-emerald-300",
    description: "Genuine ISLRTC human signing video, certified by RCI accredited Deaf master reviewer."
  },
  {
    id: "scenario-2",
    scenarioName: "Scenario 2: Dual Signals Concept (Frequency & Current)",
    text: "How does frequency relate to current?",
    branchCode: "ece",
    expectedStatus: "verified",
    badgeLabel: "2. Dual Verified (ECE/EEE)",
    badgeColor: "bg-blue-50 text-blue-800 border-blue-300",
    description: "Multi-concept sentence retrieving genuine ISLRTC recordings for Frequency & Current."
  },
  {
    id: "scenario-3",
    scenarioName: "Scenario 3: Civil & Mechanical Systems (Beam & Torque)",
    text: "A structural beam supports torque.",
    branchCode: "civil",
    expectedStatus: "verified",
    badgeLabel: "3. Dual Verified (Civil/Mech)",
    badgeColor: "bg-indigo-50 text-indigo-800 border-indigo-300",
    description: "Genuine ISLRTC 1080p human signing clips for Beam and Torque."
  },
  {
    id: "scenario-4",
    scenarioName: "Scenario 4: Partially Supported Sentence (OS & Memory)",
    text: "Explain how an operating system works with memory.",
    branchCode: "cs",
    expectedStatus: "partial",
    badgeLabel: "4. Partial (OS & Memory)",
    badgeColor: "bg-amber-50 text-amber-800 border-amber-300",
    description: "Memory sign is verified; Operating System triggers pedagogical explanation."
  },
  {
    id: "scenario-5",
    scenarioName: "Scenario 5: Unsupported Concept (Deadlock - Concurrency)",
    text: "What is a deadlock in operating systems?",
    branchCode: "cs",
    expectedStatus: "unsupported",
    badgeLabel: "5. Unsupported (Deadlock)",
    badgeColor: "bg-rose-50 text-rose-800 border-rose-300",
    description: "Zero-Fabrication Policy: transparent refusal to synthesize uncodified university sign."
  }
];

export const TranslatorPage: React.FC = () => {
  const [inputText, setInputText] = useState("What is a database?");
  const [branches, setBranches] = useState<Branch[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedBranchId, setSelectedBranchId] = useState<number | undefined>(undefined);
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | undefined>(undefined);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<TranslationResponse | null>(null);
  const [activeOutputTab, setActiveOutputTab] = useState<'both' | 'video' | 'avatar'>('both');
  const [selectedConcept, setSelectedConcept] = useState<ExtractedConcept | null>(null);
  const [showIR, setShowIR] = useState(false);

  // Live Demonstration Mode state
  const [isDemoModeActive, setIsDemoModeActive] = useState(true);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string>("scenario-1");
  const [historyItems, setHistoryItems] = useState<TranslationHistoryItem[]>([]);

  // Speech-to-ISL state
  const [isRecording, setIsRecording] = useState(false);
  const [speechFeedback, setSpeechFeedback] = useState<string | null>(null);

  const handleToggleSpeech = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      if (isRecording) {
        setIsRecording(false);
        setSpeechFeedback(null);
        return;
      }
      try {
        const recognition = new SpeechRecognition();
        recognition.lang = 'en-IN';
        recognition.continuous = false;
        recognition.interimResults = true;

        setIsRecording(true);
        setSpeechFeedback('Listening... speak an engineering concept or lecture question.');

        recognition.onresult = (event: any) => {
          const transcript = Array.from(event.results)
            .map((res: any) => res[0].transcript)
            .join('');
          setInputText(transcript);
        };

        recognition.onerror = (event: any) => {
          console.warn('Speech recognition error:', event.error);
          setIsRecording(false);
          setSpeechFeedback('Microphone notice. Falling back to preloaded engineering presets.');
        };

        recognition.onend = () => {
          setIsRecording(false);
          setSpeechFeedback('Speech captured! You can review or edit the text, then click Translate.');
        };

        recognition.start();
      } catch (e) {
        setIsRecording(false);
        setSpeechFeedback('Voice input unavailable. Falling back to text mode.');
      }
    } else {
      // Browser Web Speech API not active in environment; cycle realistic classroom speech lecture prompt
      const speechPresets = [
        "The processor executes instructions stored in memory.",
        "Voltage drives current through the circuit.",
        "A structural beam transfers horizontal load to columns.",
        "What is an algorithm?",
        "How does a compiler translate high-level code into machine instructions?"
      ];
      const randomPrompt = speechPresets[Math.floor(Math.random() * speechPresets.length)];
      setInputText(randomPrompt);
      setSpeechFeedback(`Speech recognized (simulated lecture voice input): "${randomPrompt}"`);
    }
  };

  // Load branches & initial history on mount
  useEffect(() => {
    api.getBranches()
      .then((data) => {
        setBranches(data);
        if (data.length > 0) {
          const csBranch = data.find((b) => b.code === 'cs') || data[0];
          setSelectedBranchId(csBranch.id);
        }
      })
      .catch((err) => {
        console.error("Failed to load branches", err);
      });

    refreshHistory();
  }, []);

  const refreshHistory = () => {
    api.getHistory(6)
      .then((data) => setHistoryItems(data))
      .catch((err) => console.error("Failed to fetch history", err));
  };

  // Load subjects when branch changes
  useEffect(() => {
    if (selectedBranchId) {
      api.getSubjects(selectedBranchId)
        .then((data) => {
          setSubjects(data);
          setSelectedSubjectId(undefined);
        })
        .catch((err) => {
          console.error("Failed to load subjects", err);
        });
    } else {
      setSubjects([]);
      setSelectedSubjectId(undefined);
    }
  }, [selectedBranchId]);

  // Initial auto-translation on mount once branches load
  useEffect(() => {
    if (branches.length > 0 && !result && !loading) {
      handleTranslate();
    }
  }, [branches]);

  const handleTranslate = async (overrideText?: string, overrideBranchCode?: string) => {
    const textToSubmit = overrideText !== undefined ? overrideText : inputText;
    if (!textToSubmit.trim()) return;

    let targetBranchId = selectedBranchId;
    if (overrideBranchCode && branches.length > 0) {
      const b = branches.find((item) => item.code === overrideBranchCode);
      if (b) {
        targetBranchId = b.id;
        setSelectedBranchId(b.id);
      }
    }

    setLoading(true);
    setError(null);

    try {
      const data = await api.translate({
        text: textToSubmit,
        branch_id: targetBranchId,
        subject_id: selectedSubjectId,
      });
      setResult(data);
      if (data.extracted_concepts.length > 0) {
        setSelectedConcept(data.extracted_concepts[0]);
      } else {
        setSelectedConcept(null);
      }
      // Re-fetch translation history to demonstrate real persistence
      refreshHistory();
    } catch (err: any) {
      console.error("Translation error", err);
      setError(err?.response?.data?.detail || "Failed to process translation. Please check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  const handleTriggerScenario = (scenario: typeof DEMO_SCENARIOS[0]) => {
    setSelectedScenarioId(scenario.id);
    setInputText(scenario.text);
    handleTranslate(scenario.text, scenario.branchCode);
  };

  const handleResetDemonstration = () => {
    setInputText("");
    setResult(null);
    setSelectedConcept(null);
    setError(null);
    setSelectedScenarioId("");
    refreshHistory();
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      {/* Page Title & Demo Toggle */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              Text-to-ISL Translation Engine
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
              Primary Feature
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Real-time concept extraction, ISL syntax restructuring, and zero-fabrication verification pipeline.
          </p>
        </div>

        {/* Live Demo Mode Status Pill */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsDemoModeActive(!isDemoModeActive)}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all border ${
              isDemoModeActive
                ? 'bg-gradient-to-r from-indigo-900 to-slate-900 text-white border-indigo-700 shadow-sm'
                : 'bg-white text-slate-700 border-slate-300 hover:bg-slate-50'
            }`}
          >
            <Presentation size={15} className={isDemoModeActive ? 'text-indigo-400' : 'text-slate-500'} />
            <span>Live Presentation Mode: {isDemoModeActive ? 'ON' : 'OFF'}</span>
          </button>
        </div>
      </div>

      {/* DEDICATED LIVE PROTOTYPE DEMONSTRATION PANEL */}
      {isDemoModeActive && (
        <div className="bg-gradient-to-br from-indigo-950 via-slate-900 to-indigo-900 text-white rounded-3xl p-5 sm:p-6 shadow-xl border border-indigo-800/80 space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-indigo-800/60">
            <div className="flex items-center gap-2.5">
              <div className="p-2 bg-indigo-500/20 text-indigo-300 rounded-xl border border-indigo-400/30">
                <Sparkles size={20} />
              </div>
              <div>
                <h2 className="text-base font-extrabold text-white flex items-center gap-2">
                  <span>Dedicated Live Prototype Demonstration Mode</span>
                  <span className="text-[10px] uppercase font-mono px-2 py-0.5 bg-indigo-500/30 text-indigo-200 border border-indigo-400/30 rounded-full">
                    Audience Ready
                  </span>
                </h2>
                <p className="text-xs text-indigo-200/80">
                  Select a preloaded demonstration scenario to inspect the internal pipeline and verification decision tree.
                </p>
              </div>
            </div>

            {/* Reset Demonstration Button */}
            <button
              onClick={handleResetDemonstration}
              className="px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-white border border-white/20 text-xs font-semibold flex items-center gap-1.5 transition-colors self-start sm:self-auto cursor-pointer"
            >
              <RotateCcw size={14} />
              <span>Reset Demonstration</span>
            </button>
          </div>

          {/* Preloaded Demonstration Scenarios */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {DEMO_SCENARIOS.map((scen) => {
              const isSelected = selectedScenarioId === scen.id;
              return (
                <div
                  key={scen.id}
                  onClick={() => handleTriggerScenario(scen)}
                  className={`p-3.5 rounded-2xl border transition-all cursor-pointer flex flex-col justify-between ${
                    isSelected
                      ? 'bg-indigo-600/40 border-indigo-400 shadow-md ring-2 ring-indigo-400/50'
                      : 'bg-white/5 border-white/10 hover:bg-white/10 hover:border-white/20'
                  }`}
                >
                  <div className="space-y-1.5">
                    <div className="flex items-center justify-between">
                      <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded border ${scen.badgeColor}`}>
                        {scen.badgeLabel}
                      </span>
                      {isSelected && (
                        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                      )}
                    </div>
                    <div className="text-xs font-bold text-white pt-1">
                      "{scen.text}"
                    </div>
                    <p className="text-[11px] text-indigo-200/70 leading-relaxed">
                      {scen.description}
                    </p>
                  </div>

                  <div className="pt-2 mt-2 border-t border-white/10 flex items-center justify-between text-[10px] text-indigo-300">
                    <span>Expected: {scen.expectedStatus.toUpperCase()}</span>
                    <span className="font-semibold flex items-center gap-0.5 text-white">
                      <span>Click to Execute</span>
                      <ArrowRight size={10} />
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Main Translation Form Card */}
      <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
        {/* Branch and Subject Selectors */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Engineering Branch:
            </label>
            <select
              value={selectedBranchId || ''}
              onChange={(e) => setSelectedBranchId(Number(e.target.value) || undefined)}
              className="w-full text-xs rounded-xl border border-slate-300 px-3 py-2 bg-slate-50/50 text-slate-800 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
            >
              <option value="">All Engineering Branches</option>
              {branches.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name} ({b.code.toUpperCase()})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Engineering Subject:
            </label>
            <select
              value={selectedSubjectId || ''}
              onChange={(e) => setSelectedSubjectId(Number(e.target.value) || undefined)}
              disabled={subjects.length === 0}
              className="w-full text-xs rounded-xl border border-slate-300 px-3 py-2 bg-slate-50/50 text-slate-800 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white disabled:opacity-50"
            >
              <option value="">All Subjects</option>
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name} ({s.code})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Input Text Area */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs">
            <label className="font-semibold text-slate-700">English Technical Text:</label>
            <span className="text-slate-400 font-mono text-[11px]">
              {inputText.length}/2000 chars
            </span>
          </div>
          <div className="relative">
            <textarea
              rows={2}
              value={inputText}
              onChange={(e) => {
                setInputText(e.target.value);
                setSelectedScenarioId("");
              }}
              placeholder="Enter an engineering explanation or question (e.g. 'What is a database?', 'What is a deadlock in operating systems?')..."
              className="w-full text-sm rounded-xl border border-slate-300 p-3 text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none"
            />
          </div>

          {/* Quick Authentic ISL Engineering Prompts */}
          <div className="flex items-center gap-1.5 flex-wrap pt-1 text-[11px]">
            <span className="text-slate-400 font-medium">Quick Curricular Tests:</span>
            <button
              type="button"
              onClick={() => {
                const q = "What is an algorithm?";
                setInputText(q);
                handleTranslate(q, "cs");
              }}
              className="px-2 py-0.5 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200/60 hover:bg-emerald-100 font-medium transition-colors cursor-pointer"
            >
              CS: Algorithm ★
            </button>
            <button
              type="button"
              onClick={() => {
                const q = "How does frequency relate to current?";
                setInputText(q);
                handleTranslate(q, "ece");
              }}
              className="px-2 py-0.5 rounded-lg bg-blue-50 text-blue-800 border border-blue-200/60 hover:bg-blue-100 font-medium transition-colors cursor-pointer"
            >
              ECE/EEE: Frequency & Current ★
            </button>
            <button
              type="button"
              onClick={() => {
                const q = "What is a structural beam?";
                setInputText(q);
                handleTranslate(q, "civil");
              }}
              className="px-2 py-0.5 rounded-lg bg-indigo-50 text-indigo-800 border border-indigo-200/60 hover:bg-indigo-100 font-medium transition-colors cursor-pointer"
            >
              Civil: Beam ★
            </button>
            <button
              type="button"
              onClick={() => {
                const q = "Explain torque in mechanical systems.";
                setInputText(q);
                handleTranslate(q, "mech");
              }}
              className="px-2 py-0.5 rounded-lg bg-amber-50 text-amber-800 border border-amber-200/60 hover:bg-amber-100 font-medium transition-colors cursor-pointer"
            >
              Mech: Torque ★
            </button>
            <button
              type="button"
              onClick={() => {
                const q = "What is a deadlock in operating systems?";
                setInputText(q);
                handleTranslate(q, "cs");
              }}
              className="px-2 py-0.5 rounded-lg bg-rose-50 text-rose-800 border border-rose-200/60 hover:bg-rose-100 font-medium transition-colors cursor-pointer"
            >
              Safeguard: Deadlock [Unsupported]
            </button>
          </div>
        </div>

        {/* Speech feedback banner */}
        {speechFeedback && (
          <div className="p-2.5 bg-indigo-50 border border-indigo-200 rounded-xl text-xs text-indigo-900 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Mic size={14} className="text-indigo-600 animate-pulse" />
              <span>{speechFeedback}</span>
            </div>
            <button
              type="button"
              onClick={() => setSpeechFeedback(null)}
              className="text-[11px] text-indigo-500 hover:text-indigo-800 cursor-pointer"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => {
                setInputText("");
                setSelectedScenarioId("");
                setSpeechFeedback(null);
              }}
              className="text-xs text-slate-500 hover:text-slate-700 px-2 py-1 flex items-center gap-1 cursor-pointer"
            >
              <RotateCcw size={13} />
              <span>Clear Input</span>
            </button>

            <button
              type="button"
              onClick={handleToggleSpeech}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all border cursor-pointer ${
                isRecording
                  ? 'bg-rose-600 text-white border-rose-700 animate-pulse'
                  : 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100'
              }`}
            >
              {isRecording ? <MicOff size={14} /> : <Mic size={14} />}
              <span>{isRecording ? 'Stop Recording' : 'Speech Input (Mic)'}</span>
            </button>
          </div>

          <button
            type="button"
            disabled={loading || !inputText.trim()}
            onClick={() => handleTranslate()}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-700 text-white font-bold text-xs shadow-md shadow-indigo-200 hover:shadow-lg hover:shadow-indigo-300 disabled:opacity-50 transition-all cursor-pointer"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Executing Pipeline on Backend...</span>
              </>
            ) : (
              <>
                <Languages size={15} />
                <span>Translate to ISL</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-xs flex items-center gap-2">
          <AlertCircle size={16} className="shrink-0 text-rose-600" />
          <span>{error}</span>
        </div>
      )}

      {/* Results Section */}
      {result && (
        <div className="space-y-6">
          {/* Status Assessment Banner */}
          <div
            className={`p-4 rounded-2xl border transition-all ${
              result.status === 'verified'
                ? 'bg-emerald-50/80 border-emerald-200 text-emerald-950'
                : result.status === 'unsupported'
                ? 'bg-rose-50/80 border-rose-200 text-rose-950'
                : result.status === 'explanation_needed'
                ? 'bg-purple-50/80 border-purple-200 text-purple-950'
                : result.status === 'needs_review'
                ? 'bg-sky-50/80 border-sky-200 text-sky-950'
                : 'bg-amber-50/80 border-amber-200 text-amber-950'
            }`}
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-black/5">
              <div className="flex items-center gap-2">
                <StatusBadge status={result.status} size="lg" />
                <span className="text-xs font-bold text-slate-700">
                  {result.branch_name ? `${result.branch_name}` : 'General Engineering'}
                </span>
              </div>
              <div className="flex items-center gap-3 text-xs">
                <span>Verified Signs: <strong>{result.verified_signs_count}</strong></span>
                <span>Unsupported: <strong>{result.unsupported_signs_count}</strong></span>
                {result.total_pipeline_duration_ms && (
                  <span className="font-mono text-slate-500">
                    Backend Latency: <strong>{result.total_pipeline_duration_ms} ms</strong>
                  </span>
                )}
              </div>
            </div>

            <div className="pt-2 text-xs leading-relaxed font-medium">
              <strong>Evaluation Assessment: </strong>
              {result.status_reason}
            </div>
          </div>

          {/* 1. LIVE PIPELINE STAGES VISUALIZER PANEL */}
          {result.pipeline_stages && result.pipeline_stages.length > 0 && (
            <LivePipelinePanel
              stages={result.pipeline_stages}
              totalDurationMs={result.total_pipeline_duration_ms}
              overallStatus={result.status}
              statusReason={result.status_reason}
            />
          )}

          {/* 2. ISL Syntactic Restructuring & Gloss */}
          <ISLGrammarView
            glossSequence={result.isl_gloss_sequence}
            grammarNotes={result.grammar_notes}
          />

          {/* 2b. Engineering Translation Plan */}
          {result.translation_plan && (
            <TranslationPlanCard plan={result.translation_plan as any} />
          )}

          {/* 3. Media Streams (Human Video + 3D Avatar) */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Film size={18} className="text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900">
                  Multimodal ISL Output Stream
                </h3>
              </div>

              {/* View tabs */}
              <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold text-slate-600">
                <button
                  onClick={() => setActiveOutputTab('both')}
                  className={`px-3 py-1 rounded-lg transition-colors ${
                    activeOutputTab === 'both' ? 'bg-white text-indigo-700 shadow-2xs' : 'hover:text-slate-900'
                  }`}
                >
                  Side-by-Side
                </button>
                <button
                  onClick={() => setActiveOutputTab('video')}
                  className={`px-3 py-1 rounded-lg transition-colors ${
                    activeOutputTab === 'video' ? 'bg-white text-indigo-700 shadow-2xs' : 'hover:text-slate-900'
                  }`}
                >
                  Video Only
                </button>
                <button
                  onClick={() => setActiveOutputTab('avatar')}
                  className={`px-3 py-1 rounded-lg transition-colors ${
                    activeOutputTab === 'avatar' ? 'bg-white text-indigo-700 shadow-2xs' : 'hover:text-slate-900'
                  }`}
                >
                  3D Avatar Only
                </button>
              </div>
            </div>

            <div
              className={`grid gap-4 ${
                activeOutputTab === 'both'
                  ? 'grid-cols-1 lg:grid-cols-2'
                  : 'grid-cols-1'
              }`}
            >
              {(activeOutputTab === 'both' || activeOutputTab === 'video') && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                    <span>1. Human Signing Video Player</span>
                    <span className="text-[11px] text-slate-400">Authentic Footage</span>
                  </div>
                  <VideoPlayer video={result.video_output} />
                </div>
              )}

              {(activeOutputTab === 'both' || activeOutputTab === 'avatar') && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                    <span>2. 3D Signing Avatar Viewer</span>
                    <span className="text-[11px] text-slate-400">Interactive WebGL</span>
                  </div>
                  <AvatarViewer 
                    avatarData={result.avatar_output} 
                    conceptTerm={result.extracted_concepts?.[0]?.term}
                  />
                </div>
              )}
            </div>
          </div>

          {/* 4. Extracted Concepts Breakdown */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BookOpen size={18} className="text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900">
                  Extracted Technical Concepts ({result.extracted_concepts.length})
                </h3>
              </div>
              <span className="text-xs text-slate-500">
                Linguistic provenance, license, and reviewer accreditation
              </span>
            </div>

            {result.extracted_concepts.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {result.extracted_concepts.map((concept) => (
                  <ConceptCard
                    key={concept.id}
                    concept={concept}
                    isSelected={selectedConcept?.id === concept.id}
                    onSelect={() => setSelectedConcept(concept)}
                  />
                ))}
              </div>
            ) : (
              <div className="p-8 bg-white border border-slate-200 rounded-2xl text-center text-slate-500 text-xs">
                No registered engineering concepts detected in this phrase.
              </div>
            )}
          </div>

          {/* 4b. Semantic Relationships */}
          {result.semantic_relations && result.semantic_relations.length > 0 && (
            <SemanticRelationsCard relations={result.semantic_relations} />
          )}

          {/* 4c. Pedagogical Guidance for Unsupported Concepts */}
          {result.pedagogical_explanations && result.pedagogical_explanations.length > 0 && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <AlertCircle size={18} className="text-amber-600" />
                <h3 className="text-sm font-bold text-slate-900">
                  Pedagogical Visual Guidance & Explanations ({result.pedagogical_explanations.length})
                </h3>
              </div>
              <div className="space-y-3">
                {result.pedagogical_explanations.map((exp, idx) => (
                  <PedagogicalExplanationCard key={idx} explanation={exp} />
                ))}
              </div>
            </div>
          )}

          {/* 4d. Intermediate Representation (IR) Toggle */}
          {result.intermediate_representation && (
            <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Layers size={16} className="text-indigo-600" />
                  <span className="text-xs font-bold text-slate-800">
                    Translation Intermediate Representation (Shared IR Schema)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setShowIR(!showIR)}
                  className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold px-2.5 py-1 rounded-lg bg-indigo-50 border border-indigo-100 cursor-pointer"
                >
                  {showIR ? 'Hide IR Payload' : 'Inspect Unified IR (JSON)'}
                </button>
              </div>

              {showIR && (
                <div className="mt-3 p-3 bg-slate-900 text-slate-100 rounded-xl overflow-x-auto text-[11px] font-mono leading-relaxed max-h-96">
                  <pre>{JSON.stringify(result.intermediate_representation, null, 2)}</pre>
                </div>
              )}
            </div>
          )}

          {/* 5. Live Translation Session History (Real-Time Audit Trail) */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <History size={18} className="text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-900">
                  Live Translation Session History ({historyItems.length} records logged)
                </h3>
              </div>
              <span className="text-xs text-slate-400 font-mono">
                Auto-refreshed from backend SQLite
              </span>
            </div>

            <div className="divide-y divide-slate-100">
              {historyItems.map((item) => (
                <div key={item.id} className="py-2.5 flex items-center justify-between gap-3 text-xs">
                  <div className="min-w-0">
                    <span className="font-bold text-slate-800 truncate block">
                      "{item.source_text}"
                    </span>
                    <div className="flex items-center gap-2 text-[10px] text-slate-400">
                      <span>{item.branch_name || 'General Engineering'}</span>
                      <span>·</span>
                      <span>{new Date(item.created_at).toLocaleTimeString()}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <StatusBadge status={item.status} size="sm" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
