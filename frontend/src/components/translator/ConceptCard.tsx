import React, { useState } from 'react';
import { BookOpen, CheckCircle, AlertTriangle, ExternalLink, Video, ChevronDown, ChevronUp, Hand, Compass, Move } from 'lucide-react';
import { ExtractedConcept } from '../../types';
import { StatusBadge } from '../common/StatusBadge';

interface ConceptCardProps {
  concept: ExtractedConcept;
  onSelect?: () => void;
  isSelected?: boolean;
}

export const ConceptCard: React.FC<ConceptCardProps> = ({
  concept,
  onSelect,
  isSelected = false,
}) => {
  const [showPhonology, setShowPhonology] = useState(false);

  return (
    <div
      onClick={onSelect}
      className={`p-4 rounded-xl border transition-all cursor-pointer ${
        isSelected
          ? 'bg-indigo-50/70 border-indigo-400 shadow-sm'
          : 'bg-white border-slate-200/90 hover:border-slate-300 hover:shadow-sm'
      }`}
    >
      <div className="flex items-start justify-between gap-3 mb-2">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <h4 className="text-base font-bold text-slate-900">{concept.term}</h4>
            {concept.domain && (
              <span className="text-[10px] uppercase font-semibold tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-200/60 px-2 py-0.5 rounded">
                {concept.domain}
              </span>
            )}
            {concept.category && !concept.domain && (
              <span className="text-[10px] uppercase font-semibold tracking-wider bg-slate-100 text-slate-600 px-2 py-0.5 rounded">
                {concept.category}
              </span>
            )}
          </div>
          {concept.sign_gloss && (
            <div className="text-xs font-mono text-indigo-600 font-semibold mt-0.5">
              ISL Gloss: [{concept.sign_gloss}]
            </div>
          )}
        </div>
        <StatusBadge status={concept.validation_status} size="sm" />
      </div>

      <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed mb-3">
        {concept.definition}
      </p>

      {/* Disambiguation Rationale */}
      {concept.disambiguation_rationale && (
        <div className="p-2 bg-emerald-50/60 border border-emerald-200/60 rounded-lg text-[11px] text-emerald-800 mb-2 leading-relaxed flex items-start gap-1.5">
          <span className="font-semibold text-emerald-900 whitespace-nowrap">Context Analysis:</span>
          <span>{concept.disambiguation_rationale}</span>
        </div>
      )}

      {/* Linguistic notes */}
      {concept.linguistic_notes && (
        <div className="p-2 bg-slate-50 border border-slate-100 rounded-lg text-[11px] text-slate-600 mb-2 leading-relaxed">
          <strong className="text-slate-800">Linguistic Note: </strong>
          {concept.linguistic_notes}
        </div>
      )}

      {/* Toggle Phonological Parameters */}
      {(concept.handshape || concept.movement || concept.location) && (
        <div className="mb-2">
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              setShowPhonology(!showPhonology);
            }}
            className="text-[11px] text-indigo-600 hover:text-indigo-800 font-medium flex items-center gap-1 focus:outline-none"
          >
            <Hand size={12} />
            {showPhonology ? 'Hide ISL Phonological Parameters' : 'View ISL Phonological Parameters'}
            {showPhonology ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          </button>

          {showPhonology && (
            <div className="mt-2 p-2.5 bg-slate-50 rounded-lg border border-slate-200/70 text-[11px] space-y-1.5 animate-fadeIn">
              {concept.dominant_hand && (
                <div><span className="font-semibold text-slate-700">Dominant Hand:</span> {concept.dominant_hand}</div>
              )}
              {concept.handshape && (
                <div><span className="font-semibold text-slate-700">Handshape:</span> {concept.handshape}</div>
              )}
              {concept.movement && (
                <div><span className="font-semibold text-slate-700">Movement:</span> {concept.movement}</div>
              )}
              {concept.location && (
                <div><span className="font-semibold text-slate-700">Location:</span> {concept.location}</div>
              )}
              {concept.orientation && (
                <div><span className="font-semibold text-slate-700">Orientation:</span> {concept.orientation}</div>
              )}
              {concept.non_manual_markers && (
                <div><span className="font-semibold text-slate-700">Non-Manual Marker:</span> {concept.non_manual_markers}</div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Footer details */}
      <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500 flex-wrap gap-2">
        <div className="flex items-center gap-2">
          {concept.has_video && (
            <span className="flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-medium">
              <Video size={11} /> Verified Video
            </span>
          )}
          {concept.source_attribution && (
            <span className="text-slate-500 truncate max-w-[200px]" title={concept.source_attribution}>
              Source: {concept.source_attribution}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};
