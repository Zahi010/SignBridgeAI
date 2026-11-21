import React from 'react';
import { AlertCircle, HelpCircle, BookOpen, Layers, ArrowRight } from 'lucide-react';
import { PedagogicalExplanation } from '../../types';

interface PedagogicalExplanationCardProps {
  explanation: PedagogicalExplanation;
}

export const PedagogicalExplanationCard: React.FC<PedagogicalExplanationCardProps> = ({
  explanation,
}) => {
  return (
    <div className="bg-amber-50/70 border border-amber-200/90 rounded-xl p-4 shadow-sm space-y-3">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-amber-100 text-amber-800 rounded-lg">
            <AlertCircle size={16} />
          </div>
          <div>
            <h4 className="text-sm font-bold text-amber-950">
              Zero-Fabrication Pedagogical Guidance: {explanation.term}
            </h4>
            <span className="text-[10px] font-semibold uppercase tracking-wider text-amber-700">
              {explanation.category}
            </span>
          </div>
        </div>
      </div>

      <div className="text-xs text-amber-900 leading-relaxed bg-white/80 p-3 rounded-lg border border-amber-200/60">
        <strong>Linguistic Boundary: </strong>
        {explanation.why_unsupported}
      </div>

      {/* Fingerspelling representation */}
      {explanation.fingerspelling_sequence && explanation.fingerspelling_sequence.length > 0 && (
        <div className="space-y-1.5">
          <div className="text-[11px] font-semibold text-slate-700 flex items-center gap-1.5">
            <span>Recommended ISL Fingerspelling Sequence:</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {explanation.fingerspelling_sequence.map((letter, idx) => (
              <span
                key={idx}
                className="w-7 h-8 flex items-center justify-center font-mono font-bold text-xs bg-white text-indigo-700 border border-indigo-200 rounded shadow-xs"
              >
                {letter}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Pedagogical diagram & strategy */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
        <div className="p-2.5 bg-white/80 rounded-lg border border-slate-200/70">
          <strong className="text-slate-800 block mb-1">Recommended ISL Strategy:</strong>
          <p className="text-slate-600 text-[11px] leading-relaxed">
            {explanation.recommended_isl_strategy}
          </p>
        </div>

        {explanation.pedagogical_diagram_description && (
          <div className="p-2.5 bg-white/80 rounded-lg border border-slate-200/70">
            <strong className="text-slate-800 block mb-1">Visual Resource Diagram:</strong>
            <p className="text-slate-600 text-[11px] leading-relaxed">
              {explanation.pedagogical_diagram_description}
            </p>
          </div>
        )}
      </div>

      {explanation.technical_advice_for_educators && (
        <div className="text-[11px] text-slate-600 bg-amber-100/50 p-2.5 rounded-lg border border-amber-200/50 leading-relaxed">
          <strong className="text-amber-900">Advice for Deaf STEM Educators: </strong>
          {explanation.technical_advice_for_educators}
        </div>
      )}
    </div>
  );
};

