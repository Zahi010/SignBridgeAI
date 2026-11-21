import React from 'react';
import { ArrowRight, BookOpen, Layers, Lightbulb, Sparkles } from 'lucide-react';
import { GrammarNote } from '../../types';

interface ISLGrammarViewProps {
  glossSequence: string[];
  grammarNotes: GrammarNote[];
}

export const ISLGrammarView: React.FC<ISLGrammarViewProps> = ({
  glossSequence,
  grammarNotes,
}) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
      {/* Title */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-indigo-50 text-indigo-600 rounded-lg">
            <Layers size={18} />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900">Experimental ISL Syntactic Restructuring</h3>
            <p className="text-xs text-slate-500">Rule-based linguistic hypotheses awaiting Deaf consensus</p>
          </div>
        </div>
        <span className="text-xs px-2.5 py-1 bg-amber-50 text-amber-700 font-semibold rounded-full border border-amber-200">
          Experimental Grammar Hypothesis
        </span>
      </div>

      {/* Scientific & Linguistic Disclaimer Banner */}
      <div className="p-3 bg-amber-50/80 border border-amber-200/90 rounded-xl text-xs text-amber-900 flex items-start gap-2.5">
        <Lightbulb size={16} className="text-amber-600 shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <span className="font-semibold text-amber-950">Linguistic Research Disclaimer:</span> Topic-Comment, Time-First, and sentence-final WH/Negation transformations represent rule-based working hypotheses awaiting formal Deaf community peer validation. They are not certified national ISL standards.
        </p>
      </div>

      {/* Gloss sequence display */}
      <div className="p-4 bg-slate-900 rounded-xl text-white">
        <div className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold mb-2 flex items-center justify-between">
          <span>ISL Gloss Syntax Output:</span>
          <span className="font-mono text-[10px] text-indigo-300">Non-Manual Markers Included</span>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {glossSequence.length > 0 ? (
            glossSequence.map((gloss, idx) => (
              <React.Fragment key={idx}>
                <span
                  className={`px-3 py-1.5 rounded-lg font-mono text-xs font-bold tracking-wide shadow-sm ${
                    gloss.includes('TOPIC')
                      ? 'bg-blue-600 text-white border border-blue-400'
                      : gloss.includes('WHAT') || gloss.includes('EXPLAIN') || gloss.includes('NMM')
                      ? 'bg-purple-600 text-white border border-purple-400'
                      : gloss.includes('NOT')
                      ? 'bg-rose-600 text-white border border-rose-400'
                      : 'bg-slate-800 text-slate-200 border border-slate-700'
                  }`}
                >
                  {gloss}
                </span>
                {idx < glossSequence.length - 1 && (
                  <ArrowRight size={14} className="text-slate-600" />
                )}
              </React.Fragment>
            ))
          ) : (
            <span className="text-xs text-slate-400 italic">No gloss sequence generated.</span>
          )}
        </div>
      </div>

      {/* Grammar annotations breakdown */}
      {grammarNotes.length > 0 && (
        <div className="space-y-2.5 pt-1">
          <h4 className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
            <Lightbulb size={14} className="text-amber-500" />
            Linguistic Rules Applied:
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {grammarNotes.map((note, index) => (
              <div
                key={index}
                className="p-3 bg-slate-50 border border-slate-200/80 rounded-xl text-xs space-y-1.5"
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-slate-900">{note.rule_type}</span>
                  <span className="text-[10px] font-mono bg-white px-2 py-0.5 rounded border border-slate-200 text-slate-600">
                    Rule #{index + 1}
                  </span>
                </div>
                <div className="font-mono text-[11px] text-indigo-600 bg-white p-1.5 rounded border border-slate-200/60">
                  {note.isl_structure}
                </div>
                <p className="text-[11px] text-slate-600 leading-relaxed">
                  {note.explanation}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

