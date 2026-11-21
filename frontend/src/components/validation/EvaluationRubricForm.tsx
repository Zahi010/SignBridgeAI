import React, { useState } from 'react';
import {
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  HelpCircle,
  Plus,
  Trash2,
  Clock,
  Send,
  Save,
  MessageSquare,
  AlertOctagon
} from 'lucide-react';
import { RubricRatingType, Phase5CriterionRating, Phase5Annotation } from '../../types';

interface EvaluationRubricFormProps {
  taskId: number;
  currentTimestampMs: number;
  onSubmit: (data: {
    isDraft: boolean;
    overallRecommendation: string;
    generalFeedback: string;
    suggestedDialect: string;
    criteriaRatings: Phase5CriterionRating[];
    annotations: Phase5Annotation[];
  }) => Promise<void>;
  submitting: boolean;
}

const CRITERIA_DEFINITIONS: Array<{ id: string; label: string; desc: string }> = [
  { id: 'lexical_correctness', label: '1. Lexical Sign Correctness', desc: 'Is the core sign vocabulary accurate for this concept in Indian Sign Language?' },
  { id: 'handshape', label: '2. Handshape', desc: 'Are finger configurations, knuckle flexion, and thumb opposition phonologically accurate?' },
  { id: 'orientation', label: '3. Palm & Finger Orientation', desc: 'Is the palm facing the correct anatomical direction relative to the signer?' },
  { id: 'location', label: '4. Signing Location', desc: 'Is the sign executed in the proper signing space (neutral chest, head, chin, temple)?' },
  { id: 'movement', label: '5. Movement Trajectory', desc: 'Is the stroke path, speed, repetition, and direction of motion authentic?' },
  { id: 'coordination', label: '6. Dominant / Non-Dominant Coordination', desc: 'In two-handed signs, do the dominant and base hands coordinate correctly?' },
  { id: 'facial_nmm', label: '7. Non-Manual Facial Markers', desc: 'Are eyebrow raises/furrows, mouth morphemes, and head nods appropriately matched?' },
  { id: 'grammatical_correctness', label: '8. Grammatical Correctness', desc: 'Does the sign follow ISL grammatical structure (Topic-Comment, spatial agreement)?' },
  { id: 'contextual_meaning', label: '9. Contextual Engineering Meaning', desc: 'Does this sign appropriately convey the technical academic meaning (avoiding polysemic confusion)?' },
  { id: 'naturalness', label: '10. Naturalness & Fluidity', desc: 'Does the motion look human and fluid rather than robotic or abrupt?' },
  { id: 'regional_variation', label: '11. Regional / Community Variation', desc: 'Is this sign compliant with standard ISLRTC or recognized regional variants (Delhi/Mumbai/Chennai)?' },
  { id: 'ambiguity', label: '12. Ambiguity & Alternative Interpretations', desc: 'Could this sign be mistaken for a different everyday concept?' }
];

export const EvaluationRubricForm: React.FC<EvaluationRubricFormProps> = ({
  taskId,
  currentTimestampMs,
  onSubmit,
  submitting
}) => {
  const [ratings, setRatings] = useState<Record<string, { rating: RubricRatingType; notes: string; isCritical: boolean }>>(
    () => {
      const initial: Record<string, { rating: RubricRatingType; notes: string; isCritical: boolean }> = {};
      CRITERIA_DEFINITIONS.forEach((c) => {
        initial[c.id] = { rating: 'pass', notes: '', isCritical: false };
      });
      return initial;
    }
  );

  const [overallRecommendation, setOverallRecommendation] = useState<string>('accept');
  const [generalFeedback, setGeneralFeedback] = useState<string>('');
  const [suggestedDialect, setSuggestedDialect] = useState<string>('Standard Pan-India (ISLRTC)');

  // Annotations list
  const [annotations, setAnnotations] = useState<Phase5Annotation[]>([]);
  const [annCategory, setAnnCategory] = useState<string>('handshape_error');
  const [annComment, setAnnComment] = useState<string>('');

  // Check if any criterion is flagged as major or incorrect
  const hasCriticalErrors = Object.values(ratings).some(
    (r) => r.rating === 'major_issue' || r.rating === 'incorrect' || r.isCritical
  );

  const handleRatingChange = (criterionId: string, rating: RubricRatingType) => {
    setRatings((prev) => {
      const current = prev[criterionId] || { rating: 'pass', notes: '', isCritical: false };
      const isCritical = rating === 'major_issue' || rating === 'incorrect';
      return {
        ...prev,
        [criterionId]: { ...current, rating, isCritical }
      };
    });

    // If critical error introduced and recommendation was accept, flip to needs_revision
    if ((rating === 'major_issue' || rating === 'incorrect') && overallRecommendation === 'accept') {
      setOverallRecommendation('needs_revision');
    }
  };

  const handleNotesChange = (criterionId: string, notes: string) => {
    setRatings((prev) => {
      const current = prev[criterionId] || { rating: 'pass', notes: '', isCritical: false };
      return {
        ...prev,
        [criterionId]: { ...current, notes }
      };
    });
  };

  const handleAddAnnotation = () => {
    if (!annComment.trim()) return;
    const newAnn: Phase5Annotation = {
      task_id: taskId,
      timestamp_ms: currentTimestampMs,
      duration_ms: 300,
      target_type: 'comparison',
      category: annCategory,
      comment: annComment
    };
    setAnnotations((prev) => [...prev, newAnn]);
    setAnnComment('');
  };

  const handleRemoveAnnotation = (index: number) => {
    setAnnotations((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = (isDraft: boolean) => {
    const formattedRatings: Phase5CriterionRating[] = CRITERIA_DEFINITIONS.map((c) => {
      const r = ratings[c.id];
      return {
        criterion_name: c.id,
        rating: r.rating,
        notes: r.notes,
        is_critical_error: r.isCritical
      };
    });

    onSubmit({
      isDraft,
      overallRecommendation,
      generalFeedback,
      suggestedDialect,
      criteriaRatings: formattedRatings,
      annotations
    });
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4">
        <div>
          <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
            <ShieldCheck size={20} className="text-indigo-600" />
            <span>Structured 12-Criterion Linguistic Evaluation</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Linguistic and phonological assessment rubric. Critical errors disallow final acceptance.
          </p>
        </div>

        {hasCriticalErrors && (
          <div className="flex items-center gap-1.5 px-3 py-1 bg-rose-50 text-rose-700 border border-rose-200 rounded-lg text-xs font-bold">
            <AlertOctagon size={14} className="shrink-0" />
            <span>Critical Phonological Flaws Flagged</span>
          </div>
        )}
      </div>

      {/* 12-Criterion Form Grid */}
      <div className="space-y-4">
        {CRITERIA_DEFINITIONS.map((crit) => {
          const currentRating = ratings[crit.id]?.rating || 'pass';
          const currentNotes = ratings[crit.id]?.notes || '';

          return (
            <div key={crit.id} className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition space-y-2">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h4 className="text-xs font-bold text-slate-900">{crit.label}</h4>
                  <p className="text-[11px] text-slate-500">{crit.desc}</p>
                </div>

                {/* Rating Badges */}
                <div className="flex flex-wrap items-center gap-1">
                  {(['pass', 'minor_issue', 'major_issue', 'incorrect', 'unable_to_assess'] as RubricRatingType[]).map((rType) => {
                    const isSelected = currentRating === rType;
                    const colorClass =
                      rType === 'pass'
                        ? isSelected ? 'bg-emerald-600 text-white shadow' : 'bg-white text-emerald-700 border-slate-200 hover:bg-emerald-50'
                        : rType === 'minor_issue'
                        ? isSelected ? 'bg-amber-500 text-white shadow' : 'bg-white text-amber-700 border-slate-200 hover:bg-amber-50'
                        : rType === 'major_issue'
                        ? isSelected ? 'bg-rose-600 text-white shadow' : 'bg-white text-rose-700 border-slate-200 hover:bg-rose-50'
                        : rType === 'incorrect'
                        ? isSelected ? 'bg-red-700 text-white shadow' : 'bg-white text-red-800 border-slate-200 hover:bg-red-50'
                        : isSelected ? 'bg-slate-600 text-white shadow' : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-100';

                    return (
                      <button
                        key={rType}
                        type="button"
                        onClick={() => handleRatingChange(crit.id, rType)}
                        className={`px-2 py-1 text-[10px] font-bold rounded-md border transition uppercase tracking-wider ${colorClass}`}
                      >
                        {rType.replace('_', ' ')}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Criterion Notes */}
              <input
                type="text"
                value={currentNotes}
                onChange={(e) => handleNotesChange(crit.id, e.target.value)}
                placeholder="Specific phonological notes, anatomical observations, or dialect details..."
                className="w-full px-3 py-1.5 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>
          );
        })}
      </div>

      {/* Video / Avatar Timestamp Annotations */}
      <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
            <Clock size={16} className="text-indigo-600" />
            <span>Timestamped Video & Avatar Annotations</span>
          </div>
          <span className="text-[11px] text-slate-500 font-mono">
            Active Scrubber: {(currentTimestampMs / 1000).toFixed(2)}s ({currentTimestampMs}ms)
          </span>
        </div>

        <div className="flex flex-col sm:flex-row gap-2">
          <select
            value={annCategory}
            onChange={(e) => setAnnCategory(e.target.value)}
            className="text-xs border border-slate-300 rounded-lg px-2.5 py-1.5 bg-white font-medium focus:outline-none"
          >
            <option value="handshape_error">Handshape Error</option>
            <option value="movement_jerk">Movement / Jitter Issue</option>
            <option value="orientation_flaw">Orientation Flaw</option>
            <option value="expression_missing">Facial Expression Missing</option>
            <option value="timing_lag">Timing / Foreshortening Lag</option>
            <option value="general">General Linguistic Observation</option>
          </select>
          <input
            type="text"
            value={annComment}
            onChange={(e) => setAnnComment(e.target.value)}
            placeholder="Describe flaw at this exact millisecond..."
            className="flex-1 text-xs border border-slate-300 rounded-lg px-3 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
          <button
            type="button"
            onClick={handleAddAnnotation}
            className="px-3 py-1.5 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition flex items-center gap-1.5 shrink-0"
          >
            <Plus size={14} />
            <span>Add Tag</span>
          </button>
        </div>

        {annotations.length > 0 && (
          <div className="space-y-1.5 pt-2">
            {annotations.map((ann, idx) => (
              <div key={idx} className="flex items-center justify-between p-2 bg-white rounded-lg border border-slate-200 text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-mono bg-slate-100 px-1.5 py-0.5 rounded text-[10px] text-slate-600 font-bold">
                    {(ann.timestamp_ms / 1000).toFixed(2)}s
                  </span>
                  <span className="font-semibold text-slate-800">{ann.category}:</span>
                  <span className="text-slate-600">{ann.comment}</span>
                </div>
                <button
                  type="button"
                  onClick={() => handleRemoveAnnotation(idx)}
                  className="text-slate-400 hover:text-rose-600 transition p-1"
                >
                  <Trash2 size={13} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Overall Assessment & Dialect */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-bold text-slate-800 mb-1">Overall Recommendation</label>
          <select
            value={overallRecommendation}
            onChange={(e) => setOverallRecommendation(e.target.value)}
            disabled={hasCriticalErrors}
            className={`w-full text-xs font-bold p-2.5 rounded-lg border focus:outline-none ${
              hasCriticalErrors
                ? 'bg-rose-50 text-rose-800 border-rose-300 cursor-not-allowed'
                : 'bg-white text-slate-800 border-slate-300'
            }`}
          >
            <option value="accept">Accept as Authentically Representative</option>
            <option value="needs_revision">Needs Phonological / Retargeting Revision</option>
            <option value="reject">Reject (Linguistically Invalid or Inaccurate)</option>
            <option value="inconclusive">Inconclusive (Requires Additional Reviewers)</option>
          </select>
          {hasCriticalErrors && (
            <p className="text-[11px] text-rose-600 mt-1 font-medium">
              * Acceptance locked: major/incorrect phonological errors require revision or rejection.
            </p>
          )}
        </div>

        <div>
          <label className="block text-xs font-bold text-slate-800 mb-1">Suggested Regional Dialect / Variant</label>
          <input
            type="text"
            value={suggestedDialect}
            onChange={(e) => setSuggestedDialect(e.target.value)}
            placeholder="e.g. Standard Pan-India, Northern (Delhi), Western (Mumbai)..."
            className="w-full text-xs p-2.5 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* General Feedback Comments */}
      <div>
        <label className="block text-xs font-bold text-slate-800 mb-1">Comprehensive Reviewer Comments</label>
        <textarea
          rows={3}
          value={generalFeedback}
          onChange={(e) => setGeneralFeedback(e.target.value)}
          placeholder="Linguistic commentary on comprehensibility, educational suitability for Deaf STEM students, and phonological corrections..."
          className="w-full text-xs p-3 border border-slate-300 rounded-xl focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white"
        />
      </div>

      {/* Submission Actions */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
        <button
          type="button"
          disabled={submitting}
          onClick={() => handleSubmit(true)}
          className="px-4 py-2 bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-lg text-xs font-bold transition flex items-center gap-1.5 disabled:opacity-50"
        >
          <Save size={15} />
          <span>Save Review Draft</span>
        </button>

        <button
          type="button"
          disabled={submitting}
          onClick={() => handleSubmit(false)}
          className="px-6 py-2.5 bg-indigo-600 text-white hover:bg-indigo-700 rounded-lg text-xs font-bold transition flex items-center gap-2 shadow-md hover:shadow disabled:opacity-50"
        >
          <Send size={15} />
          <span>{submitting ? 'Submitting Evaluation...' : 'Submit Final Evaluation'}</span>
        </button>
      </div>
    </div>
  );
};
