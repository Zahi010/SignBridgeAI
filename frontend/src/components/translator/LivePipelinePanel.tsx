import React, { useState } from 'react';
import {
  Activity,
  Layers,
  CheckCircle2,
  AlertTriangle,
  Info,
  Clock,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Cpu,
  BookOpen,
  ShieldCheck,
  Film,
  Play,
  RotateCcw,
  ArrowRight,
  Database
} from 'lucide-react';
import { PipelineStage, ValidationStatus } from '../../types';
import { StatusBadge } from '../common/StatusBadge';

interface LivePipelinePanelProps {
  stages: PipelineStage[];
  totalDurationMs?: number;
  overallStatus: ValidationStatus;
  statusReason: string;
}

export const LivePipelinePanel: React.FC<LivePipelinePanelProps> = ({
  stages,
  totalDurationMs,
  overallStatus,
  statusReason,
}) => {
  const [expandedStageId, setExpandedStageId] = useState<string | null>(null);
  const [activeStepIndex, setActiveStepIndex] = useState<number | null>(null);

  const toggleExpand = (stageId: string) => {
    setExpandedStageId(expandedStageId === stageId ? null : stageId);
  };

  const stageIcons = {
    1: Activity,
    2: Database,
    3: Layers,
    4: ShieldCheck,
    5: Film,
  };

  const displayedStages = activeStepIndex !== null
    ? stages.filter((_, idx) => idx <= activeStepIndex)
    : stages;

  return (
    <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm overflow-hidden space-y-0">
      {/* Header Bar */}
      <div className="p-5 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center text-indigo-300">
              <Activity size={18} className="animate-pulse" />
            </div>
            <div>
              <h3 className="text-sm font-bold tracking-tight text-white flex items-center gap-2">
                <span>Live Translation Pipeline Execution Trace</span>
                <span className="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 text-[10px] font-mono">
                  Verified Backend Events
                </span>
              </h3>
              <p className="text-[11px] text-slate-400">
                Inspect stage-by-stage tokenization, ontology retrieval, linguistic grammar, and accreditation audit.
              </p>
            </div>
          </div>
        </div>

        {/* Right side stats & Stepper controls */}
        <div className="flex items-center gap-3">
          {totalDurationMs !== undefined && (
            <div className="text-right">
              <span className="text-[10px] uppercase font-bold text-slate-400 block tracking-wider">
                Total Backend Latency
              </span>
              <span className="font-mono text-sm font-extrabold text-indigo-300">
                {totalDurationMs.toFixed(1)} ms
              </span>
            </div>
          )}

          {/* Stepper modes for presentation */}
          <div className="flex items-center gap-1 bg-slate-800/80 p-1 rounded-xl border border-slate-700/70 text-xs">
            <button
              onClick={() => setActiveStepIndex(null)}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors ${
                activeStepIndex === null
                  ? 'bg-indigo-600 text-white font-semibold'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              All Stages
            </button>
            <button
              onClick={() => setActiveStepIndex(0)}
              className={`px-2.5 py-1 rounded-lg text-[11px] font-medium transition-colors ${
                activeStepIndex !== null
                  ? 'bg-indigo-600 text-white font-semibold'
                  : 'text-slate-300 hover:text-white'
              }`}
            >
              Step-by-Step
            </button>
            {activeStepIndex !== null && (
              <button
                onClick={() =>
                  setActiveStepIndex((prev) =>
                    prev !== null && prev < stages.length - 1 ? prev + 1 : 0
                  )
                }
                className="px-2 py-1 rounded-lg text-[11px] font-bold bg-indigo-500 hover:bg-indigo-400 text-white transition-colors flex items-center gap-1"
                title="Next Pipeline Stage"
              >
                <span>Stage {activeStepIndex + 1}/{stages.length}</span>
                <ArrowRight size={12} />
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Stage Breakdown List */}
      <div className="divide-y divide-slate-100 p-4 sm:p-5 space-y-3 bg-slate-50/40">
        {displayedStages.map((stage) => {
          const Icon = stageIcons[stage.stage_number as keyof typeof stageIcons] || Activity;
          const isExpanded = expandedStageId === stage.stage_id;

          const getStatusTheme = () => {
            switch (stage.status) {
              case 'completed':
                return {
                  border: 'border-emerald-200',
                  bg: 'bg-emerald-50/50',
                  badge: 'bg-emerald-100 text-emerald-800',
                  iconColor: 'text-emerald-600',
                };
              case 'warning':
                return {
                  border: 'border-amber-200',
                  bg: 'bg-amber-50/50',
                  badge: 'bg-amber-100 text-amber-800',
                  iconColor: 'text-amber-600',
                };
              case 'info':
              default:
                return {
                  border: 'border-blue-200',
                  bg: 'bg-blue-50/50',
                  badge: 'bg-blue-100 text-blue-800',
                  iconColor: 'text-blue-600',
                };
            }
          };

          const theme = getStatusTheme();

          return (
            <div
              key={stage.stage_id}
              className={`rounded-2xl border transition-all ${
                isExpanded ? 'bg-white shadow-sm border-indigo-200' : 'bg-white border-slate-200/80 hover:border-slate-300'
              }`}
            >
              {/* Stage Summary Header */}
              <div
                onClick={() => toggleExpand(stage.stage_id)}
                className="p-4 flex items-center justify-between gap-3 cursor-pointer select-none"
              >
                <div className="flex items-center gap-3 min-w-0">
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center font-bold text-xs shrink-0 ${theme.bg} ${theme.iconColor} border border-slate-200/60`}>
                    <Icon size={18} />
                  </div>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-xs font-mono font-bold text-slate-400">
                        STAGE {stage.stage_number}
                      </span>
                      <h4 className="text-xs sm:text-sm font-bold text-slate-900 truncate">
                        {stage.name}
                      </h4>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                        {stage.duration_ms} ms
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 truncate mt-0.5">
                      {stage.summary}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded-md ${theme.badge}`}>
                    {stage.status}
                  </span>
                  <button className="text-slate-400 hover:text-slate-600 p-1">
                    {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                  </button>
                </div>
              </div>

              {/* Stage Detailed Payload (Drawer) */}
              {isExpanded && (
                <div className="px-4 pb-4 pt-2 border-t border-slate-100 space-y-3 text-xs bg-slate-50/50 rounded-b-2xl">
                  <p className="text-slate-600 leading-relaxed text-[11px]">
                    {stage.description}
                  </p>

                  {/* Stage 1 Details: Tokens & Interrogatives */}
                  {stage.stage_id === 'stage_1_tokenization' && (
                    <div className="space-y-2">
                      <span className="font-semibold text-slate-700 block text-[11px]">
                        Segmented Lexical Tokens:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {stage.details.tokens?.map((tok: string, i: number) => {
                          const isWH = stage.details.detected_interrogatives?.includes(tok.toLowerCase());
                          const isNeg = stage.details.detected_negations?.includes(tok.toLowerCase());
                          return (
                            <span
                              key={i}
                              className={`px-2 py-1 rounded-lg font-mono text-[11px] font-medium border ${
                                isWH
                                  ? 'bg-purple-100 text-purple-900 border-purple-300 font-bold'
                                  : isNeg
                                  ? 'bg-rose-100 text-rose-900 border-rose-300 font-bold'
                                  : 'bg-white text-slate-700 border-slate-200'
                              }`}
                            >
                              {tok} {isWH && '(WH)'} {isNeg && '(NEG)'}
                            </span>
                          );
                        })}
                      </div>
                    </div>
                  )}

                  {/* Stage 2 Details: Matched vs Unmatched */}
                  {stage.stage_id === 'stage_2_concept_extraction' && (
                    <div className="space-y-3">
                      <div>
                        <span className="font-semibold text-slate-700 block text-[11px] mb-1.5">
                          Knowledge Base Concepts Extracted ({stage.details.matched_count || 0}):
                        </span>
                        {stage.details.matched_concepts?.length > 0 ? (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                            {stage.details.matched_concepts.map((mc: any, i: number) => (
                              <div key={i} className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-0.5">
                                <div className="flex items-center justify-between">
                                  <strong className="text-slate-900 font-bold">{mc.term}</strong>
                                  <span className="text-[10px] font-mono px-1.5 py-0.5 bg-indigo-50 text-indigo-700 rounded">
                                    {mc.branch}
                                  </span>
                                </div>
                                <span className="text-[10px] text-slate-500 block">
                                  Category: {mc.category} · Difficulty: {mc.difficulty}
                                </span>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="p-2 bg-amber-50 text-amber-800 rounded-lg text-[11px]">
                            No engineering concepts found in database. Zero synthetic terms will be generated.
                          </div>
                        )}
                      </div>

                      {stage.details.unmatched_tokens?.length > 0 && (
                        <div>
                          <span className="font-semibold text-slate-500 block text-[11px] mb-1">
                            Unmatched Function / Auxiliary Words:
                          </span>
                          <div className="flex flex-wrap gap-1 text-[11px] font-mono text-slate-500">
                            {stage.details.unmatched_tokens.map((u: string, idx: number) => (
                              <span key={idx} className="px-1.5 py-0.5 bg-slate-200/60 rounded">
                                {u}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Stage 3 Details: Grammar Restructuring */}
                  {stage.stage_id === 'stage_3_grammar_restructuring' && (
                    <div className="space-y-2">
                      <span className="font-semibold text-slate-700 block text-[11px]">
                        Linguistic Transformations Applied:
                      </span>
                      <div className="space-y-1">
                        {stage.details.rules_applied?.map((rule: string, idx: number) => (
                          <div key={idx} className="flex items-center gap-2 p-1.5 bg-white rounded-lg border border-slate-200 text-[11px]">
                            <Sparkles size={12} className="text-amber-500 shrink-0" />
                            <span className="font-semibold text-slate-800">{rule}</span>
                          </div>
                        ))}
                      </div>

                      <div className="pt-1">
                        <span className="font-semibold text-slate-700 block text-[11px] mb-1">
                          Generated ISL Gloss Sequence:
                        </span>
                        <div className="flex flex-wrap gap-1.5 font-mono text-[11px]">
                          {stage.details.isl_gloss_sequence?.map((g: string, i: number) => (
                            <span key={i} className="px-2 py-1 bg-slate-900 text-white rounded-lg font-bold">
                              {g}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Stage 4 Details: Zero-Fabrication Audit */}
                  {stage.stage_id === 'stage_4_policy_audit' && (
                    <div className="space-y-2.5">
                      <div className="p-3 bg-white rounded-xl border border-slate-200 space-y-1.5">
                        <div className="flex items-center justify-between">
                          <strong className="text-slate-900">Validation Status Determination:</strong>
                          <StatusBadge status={stage.details.validation_verdict as ValidationStatus} size="sm" />
                        </div>
                        <p className="text-[11px] text-slate-600 leading-relaxed">
                          {stage.details.assessment_notes}
                        </p>
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                        <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                          <strong className="text-slate-700 block">Dataset Provenance:</strong>
                          {stage.details.dataset_provenance?.map((prov: string, i: number) => (
                            <span key={i} className="text-slate-600 block text-[10px]">
                              • {prov}
                            </span>
                          ))}
                        </div>
                        <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                          <strong className="text-slate-700 block">Deaf Master Reviewers:</strong>
                          {stage.details.expert_reviewers?.map((rev: string, i: number) => (
                            <span key={i} className="text-slate-600 block text-[10px]">
                              • {rev}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Stage 5 Details: Media Stream Status */}
                  {stage.stage_id === 'stage_5_media_assembly' && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px]">
                      <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                        <strong className="text-slate-800 block">Human Sign Video Stream:</strong>
                        <span className="text-slate-600 block">
                          Status: {stage.details.video_available ? 'Accredited MP4 Mounted' : 'Unavailable (Awaiting Corpus)'}
                        </span>
                        {stage.details.video_path && (
                          <span className="font-mono text-[10px] text-indigo-600 block truncate">
                            Path: {stage.details.video_path}
                          </span>
                        )}
                      </div>
                      <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                        <strong className="text-slate-800 block">3D WebGL Avatar Engine:</strong>
                        <span className="text-slate-600 block">
                          Standard: {stage.details.avatar_rig}
                        </span>
                        <span className="text-slate-500 text-[10px] block">
                          Mode: Neutral Anatomical Preview (Zero-Fabrication Active)
                        </span>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

