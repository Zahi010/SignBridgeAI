import React from 'react';
import { Route, Video, BookOpen, Hand, ShieldAlert, Sparkles, ArrowRight, Layers } from 'lucide-react';

interface TranslationUnit {
  unit_id: number;
  source_segment: string;
  strategy: 'LEXICAL_SIGN_DIRECT' | 'PEDAGOGICAL_EXPLANATION' | 'UNSUPPORTED_FINGERSPELLING' | 'RELATIONAL_SPATIAL_INDEX' | string;
  assigned_gloss: string;
  video_resource_ref?: string | null;
  pedagogical_ref?: Record<string, any> | null;
  fingerspelling_sequence?: string[] | null;
  rationale: string;
}

interface TranslationPlan {
  translation_units: TranslationUnit[];
  total_units: number;
  lexical_count: number;
  explanation_count: number;
  unsupported_count: number;
  overall_strategy_summary: string;
}

interface TranslationPlanCardProps {
  plan?: TranslationPlan;
}

export const TranslationPlanCard: React.FC<TranslationPlanCardProps> = ({ plan }) => {
  if (!plan || !plan.translation_units || plan.translation_units.length === 0) {
    return null;
  }

  const getStrategyBadge = (strategy: string) => {
    switch (strategy) {
      case 'LEXICAL_SIGN_DIRECT':
        return (
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
            <Video size={10} />
            <span>LEXICAL SIGN</span>
          </span>
        );
      case 'PEDAGOGICAL_EXPLANATION':
        return (
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">
            <BookOpen size={10} />
            <span>PEDAGOGICAL EXPLANATION</span>
          </span>
        );
      case 'UNSUPPORTED_FINGERSPELLING':
        return (
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-300">
            <Hand size={10} />
            <span>FINGERSPELLING ONLY</span>
          </span>
        );
      case 'RELATIONAL_SPATIAL_INDEX':
        return (
          <span className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 text-indigo-800 border border-indigo-300">
            <Layers size={10} />
            <span>SPATIAL LOCUS</span>
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-700">
            {strategy}
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-blue-50 text-blue-600 rounded-lg">
            <Route size={18} />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Engineering Translation Plan</h3>
            <p className="text-xs text-slate-500">
              Transparent multi-concept routing: Lexical videos, Pedagogical breakdowns & Fingerspelling
            </p>
          </div>
        </div>

        {/* Counter Pills */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-[11px] px-2 py-0.5 bg-emerald-50 text-emerald-700 rounded-md font-medium border border-emerald-200">
            {plan.lexical_count} Lexical
          </span>
          <span className="text-[11px] px-2 py-0.5 bg-amber-50 text-amber-700 rounded-md font-medium border border-amber-200">
            {plan.explanation_count} Pedagogical
          </span>
          <span className="text-[11px] px-2 py-0.5 bg-rose-50 text-rose-700 rounded-md font-medium border border-rose-200">
            {plan.unsupported_count} Fingerspelling
          </span>
        </div>
      </div>

      {/* Summary string */}
      <div className="text-xs text-slate-600 bg-slate-50 p-2.5 rounded-xl border border-slate-200 font-mono">
        {plan.overall_strategy_summary}
      </div>

      {/* Step by Step Units */}
      <div className="space-y-2.5">
        {plan.translation_units.map((unit) => (
          <div
            key={unit.unit_id}
            className="p-3.5 bg-white border border-slate-200 rounded-xl hover:border-indigo-300 transition-colors shadow-xs space-y-2"
          >
            <div className="flex items-center justify-between flex-wrap gap-2">
              <div className="flex items-center gap-2">
                <span className="w-5 h-5 rounded-full bg-slate-100 text-slate-700 font-mono text-[11px] font-bold flex items-center justify-center">
                  {unit.unit_id}
                </span>
                <span className="font-semibold text-slate-900 text-xs">
                  "{unit.source_segment}"
                </span>
                <ArrowRight size={12} className="text-slate-400" />
                <span className="font-mono text-xs font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100">
                  {unit.assigned_gloss}
                </span>
              </div>
              {getStrategyBadge(unit.strategy)}
            </div>

            <p className="text-[11px] text-slate-600 leading-relaxed pl-7">
              {unit.rationale}
            </p>

            {unit.fingerspelling_sequence && unit.fingerspelling_sequence.length > 0 && (
              <div className="pl-7 flex items-center gap-1 text-[10px] text-slate-500 font-mono">
                <span className="text-slate-400">ISL Fingerspelling:</span>
                <span className="bg-slate-100 px-1.5 py-0.5 rounded text-slate-700 font-bold tracking-wider">
                  {unit.fingerspelling_sequence.join(' - ')}
                </span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

