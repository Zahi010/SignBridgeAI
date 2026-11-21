import React from 'react';
import { ArrowRight, Network, Sparkles } from 'lucide-react';
import { SemanticRelationship } from '../../types';

interface SemanticRelationsCardProps {
  relations: SemanticRelationship[];
}

export const SemanticRelationsCard: React.FC<SemanticRelationsCardProps> = ({ relations }) => {
  if (!relations || relations.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-3">
      <div className="flex items-center gap-2">
        <div className="p-1.5 bg-indigo-50 text-indigo-700 rounded-lg">
          <Network size={16} />
        </div>
        <div>
          <h3 className="text-sm font-bold text-slate-900">
            Detected Semantic Relationships
          </h3>
          <p className="text-[11px] text-slate-500">
            Contextual engineering interactions mapped between detected entities
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-2.5">
        {relations.map((rel, idx) => (
          <div
            key={idx}
            className="p-3 bg-slate-50/70 border border-slate-200/80 rounded-xl space-y-1.5 hover:border-indigo-300 transition-colors"
          >
            <div className="flex items-center gap-2 flex-wrap text-xs">
              <span className="font-bold text-slate-900 bg-white px-2.5 py-1 rounded-md border border-slate-200 shadow-2xs">
                {rel.source_concept}
              </span>
              <span className="flex items-center gap-1 font-mono text-[11px] font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                <ArrowRight size={12} />
                {rel.relation_type}
              </span>
              <span className="font-bold text-slate-900 bg-white px-2.5 py-1 rounded-md border border-slate-200 shadow-2xs">
                {rel.target_concept}
              </span>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              {rel.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

