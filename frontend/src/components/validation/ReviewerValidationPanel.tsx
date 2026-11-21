import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  RotateCcw,
  UserCheck,
  Building,
  Hand,
  Clock,
  Star,
  MessageSquare,
  Award,
  AlertOctagon
} from 'lucide-react';
import { api } from '../../api/client';
import { PendingValidationItem, SignRecordDetail, ReviewerValidationDecision, ReviewerProfile } from '../../types';
import { StatusBadge } from '../common/StatusBadge';

export const ReviewerValidationPanel: React.FC = () => {
  const [pendingItems, setPendingItems] = useState<PendingValidationItem[]>([]);
  const [reviewerProfiles, setReviewerProfiles] = useState<ReviewerProfile[]>([]);
  const [selectedProfileId, setSelectedProfileId] = useState<number | null>(null);
  const [selectedSignId, setSelectedSignId] = useState<number | null>(null);
  const [selectedSign, setSelectedSign] = useState<SignRecordDetail | null>(null);
  const [auditTrail, setAuditTrail] = useState<ReviewerValidationDecision[]>([]);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Form states
  const [reviewerName, setReviewerName] = useState('Shri Rajesh Sharma');
  const [reviewerRole, setReviewerRole] = useState('Master Deaf Signer & RCI Certified Specialist');
  const [affiliation, setAffiliation] = useState('ISLRTC Technical Working Group & Delhi Association of the Deaf');
  const [decision, setDecision] = useState('approved');
  const [assignedStatus, setAssignedStatus] = useState('verified');
  const [comments, setComments] = useState('');
  const [corrections, setCorrections] = useState('');
  const [suggestedDialect, setSuggestedDialect] = useState('Standard Pan-India');
  const [rating, setRating] = useState<number>(4.8);

  const selectedProfile = reviewerProfiles.find((p) => p.id === selectedProfileId);

  const fetchPending = async () => {
    setLoading(true);
    try {
      const items = await api.getPendingValidations();
      setPendingItems(items);
      if (items.length > 0 && !selectedSignId) {
        setSelectedSignId(items[0].sign_record_id);
      }
    } catch (err) {
      console.error('Failed to load pending validation items', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchProfiles = async () => {
    try {
      const profiles = await api.getReviewerProfiles();
      setReviewerProfiles(profiles);
      if (profiles.length > 0) {
        const defaultProfile = profiles.find((p) => p.is_authorized_expert) || profiles[0];
        setSelectedProfileId(defaultProfile.id);
        setReviewerName(defaultProfile.full_name);
        setReviewerRole(defaultProfile.qualifications || 'ISL Specialist');
        setAffiliation(defaultProfile.institution_affiliation || 'ISLRTC Technical Working Group');
      }
    } catch (err) {
      console.error('Failed to load reviewer profiles', err);
    }
  };

  useEffect(() => {
    fetchPending();
    fetchProfiles();
  }, []);

  const handleProfileChange = (profileId: number) => {
    setSelectedProfileId(profileId);
    const profile = reviewerProfiles.find((p) => p.id === profileId);
    if (profile) {
      setReviewerName(profile.full_name);
      setReviewerRole(profile.qualifications || 'ISL Specialist');
      setAffiliation(profile.institution_affiliation || 'Independent Reviewer');
      if (!profile.is_authorized_expert && assignedStatus === 'verified') {
        setAssignedStatus('needs_review');
        setDecision('requires_correction');
      }
    }
  };

  useEffect(() => {
    if (!selectedSignId) return;

    api.getSignForValidation(selectedSignId)
      .then(setSelectedSign)
      .catch(console.error);

    api.getValidationAuditTrail(selectedSignId)
      .then(setAuditTrail)
      .catch(console.error);
  }, [selectedSignId]);

  const handleSubmitDecision = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSignId) return;

    setSubmitting(true);
    setFeedbackMsg(null);
    setErrorMessage(null);

    try {
      const res = await api.submitValidationDecision({
        sign_record_id: selectedSignId,
        reviewer_profile_id: selectedProfile?.id,
        reviewer_code: selectedProfile?.reviewer_code,
        reviewer_name: reviewerName,
        reviewer_role: reviewerRole,
        affiliation,
        decision,
        assigned_status: assignedStatus,
        corrections: corrections || undefined,
        suggested_regional_variation: suggestedDialect,
        comments: comments || undefined,
        accuracy_rating: rating,
      });

      setFeedbackMsg(res.message);
      fetchPending();

      // Refresh current sign & audit trail
      const updatedSign = await api.getSignForValidation(selectedSignId);
      setSelectedSign(updatedSign);
      const updatedTrail = await api.getValidationAuditTrail(selectedSignId);
      setAuditTrail(updatedTrail);
    } catch (err: any) {
      console.error('Failed to submit decision', err);
      const detail = err.response?.data?.detail || err.message || 'Failed to submit validation decision.';
      setErrorMessage(detail);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 flex-wrap gap-3">
        <div className="flex items-center gap-2">
          <div className="p-2 bg-indigo-50 text-indigo-700 rounded-xl">
            <ShieldCheck size={20} />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">
              Expert ISL Peer Review & Validation Console
            </h2>
            <p className="text-xs text-slate-500">
              Audit queue for certified deaf educators and academic sign linguists
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={fetchPending}
          className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold px-3 py-1.5 rounded-lg bg-indigo-50 border border-indigo-100 flex items-center gap-1.5 cursor-pointer"
        >
          <RotateCcw size={13} />
          Refresh Queue ({pendingItems.length} Pending)
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Queue List */}
        <div className="space-y-2 lg:col-span-1">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Validation Queue ({pendingItems.length})
          </h3>
          <div className="max-h-[500px] overflow-y-auto space-y-2 pr-1">
            {pendingItems.map((item) => (
              <div
                key={item.sign_record_id}
                onClick={() => setSelectedSignId(item.sign_record_id)}
                className={`p-3 rounded-xl border text-xs cursor-pointer transition-all ${
                  selectedSignId === item.sign_record_id
                    ? 'bg-indigo-50/80 border-indigo-400 shadow-xs'
                    : 'bg-white border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-bold text-slate-900">{item.concept_term}</span>
                  <StatusBadge status={item.current_status} size="sm" />
                </div>
                <div className="text-[11px] text-slate-500 font-mono">
                  Sign ID: {item.sign_id || `ID-${item.sign_record_id}`}
                </div>
                <div className="text-[10px] text-slate-400 mt-1 flex items-center gap-2">
                  <span>{item.branch_name}</span>
                  <span>·</span>
                  <span>{item.review_count} review(s)</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Center: Sign Inspection */}
        <div className="space-y-4 lg:col-span-1">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Sign Inspection & Phonology
          </h3>

          {selectedSign ? (
            <div className="bg-slate-50/70 rounded-xl border border-slate-200 p-4 space-y-3 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-sm font-bold text-slate-900">
                  {selectedSign.sign_gloss}
                </span>
                <StatusBadge status={selectedSign.validation_status} size="sm" />
              </div>

              <div className="space-y-1.5 text-[11px] text-slate-600">
                <div><strong className="text-slate-800">Dialect:</strong> {selectedSign.regional_dialect}</div>
                <div><strong className="text-slate-800">Dominant Hand:</strong> {selectedSign.dominant_hand || 'Unrecorded'}</div>
                <div><strong className="text-slate-800">Handshape:</strong> {selectedSign.handshape || 'Unrecorded'}</div>
                <div><strong className="text-slate-800">Movement:</strong> {selectedSign.movement || 'Unrecorded'}</div>
                <div><strong className="text-slate-800">Location:</strong> {selectedSign.location || 'Unrecorded'}</div>
                <div><strong className="text-slate-800">Orientation:</strong> {selectedSign.orientation || 'Unrecorded'}</div>
                <div><strong className="text-slate-800">Non-Manual Marker:</strong> {selectedSign.non_manual_markers || 'None'}</div>
              </div>

              {selectedSign.linguistic_notes && (
                <div className="p-2.5 bg-white rounded-lg border border-slate-200/80 text-[11px] text-slate-600 leading-relaxed">
                  <strong className="text-slate-800 block mb-0.5">Linguistic Notes:</strong>
                  {selectedSign.linguistic_notes}
                </div>
              )}

              {/* Audit trail */}
              <div className="pt-2 border-t border-slate-200 space-y-2">
                <span className="text-[11px] font-bold text-slate-700 block">
                  Past Review Ledger ({auditTrail.length})
                </span>
                {auditTrail.length > 0 ? (
                  <div className="space-y-1.5 max-h-36 overflow-y-auto">
                    {auditTrail.map((at: any) => (
                      <div key={at.id} className="p-2 bg-white rounded border border-slate-200 text-[10px] space-y-0.5">
                        <div className="flex justify-between font-semibold">
                          <span className="text-slate-800">{at.reviewer_name}</span>
                          <span className="text-indigo-600 uppercase">{at.decision}</span>
                        </div>
                        {at.accreditation_evidence && (
                          <div className="text-[9px] text-emerald-700 font-medium">
                            Accreditation: {at.accreditation_evidence}
                          </div>
                        )}
                        {at.comments && <p className="text-slate-500">{at.comments}</p>}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-[10px] text-slate-400">Awaiting first formal peer evaluation.</p>
                )}
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-xs text-slate-400 border border-slate-200 rounded-xl">
              Select a candidate sign to inspect.
            </div>
          )}
        </div>

        {/* Right: Decision Submission Form */}
        <div className="space-y-4 lg:col-span-1">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Submit Peer Evaluation
          </h3>

          <form onSubmit={handleSubmitDecision} className="bg-slate-50/70 rounded-xl border border-slate-200 p-4 space-y-3 text-xs">
            {feedbackMsg && (
              <div className="p-2.5 bg-emerald-50 border border-emerald-200 rounded-lg text-[11px] text-emerald-800 font-medium">
                {feedbackMsg}
              </div>
            )}

            {errorMessage && (
              <div className="p-2.5 bg-rose-50 border border-rose-200 rounded-lg text-[11px] text-rose-800 font-medium flex items-start gap-1.5">
                <AlertOctagon size={15} className="shrink-0 mt-0.5 text-rose-600" />
                <span className="leading-snug">{errorMessage}</span>
              </div>
            )}

            {/* Profile Selection */}
            <div>
              <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                Active Reviewer Profile:
              </label>
              <select
                value={selectedProfileId || ''}
                onChange={(e) => handleProfileChange(Number(e.target.value))}
                className="w-full text-xs p-2 rounded-lg border border-slate-300 bg-white"
              >
                {reviewerProfiles.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.full_name} ({p.reviewer_code}) {p.is_authorized_expert ? '★ [Accredited Expert]' : '[Test Account]'}
                  </option>
                ))}
              </select>
            </div>

            {/* Accreditation Status Badge */}
            {selectedProfile && (
              <div
                className={`p-2 rounded-lg border text-[10px] flex items-start gap-1.5 ${
                  selectedProfile.is_authorized_expert
                    ? 'bg-emerald-50/80 border-emerald-200 text-emerald-900'
                    : 'bg-amber-50/80 border-amber-200 text-amber-900'
                }`}
              >
                {selectedProfile.is_authorized_expert ? (
                  <Award size={14} className="shrink-0 mt-0.5 text-emerald-600" />
                ) : (
                  <AlertTriangle size={14} className="shrink-0 mt-0.5 text-amber-600" />
                )}
                <div>
                  <div className="font-bold">
                    {selectedProfile.is_authorized_expert
                      ? 'Accredited ISL Expert Reviewer'
                      : 'Unaccredited / Developer Test Profile'}
                  </div>
                  <div className="text-[9px] opacity-90">
                    {selectedProfile.is_authorized_expert
                      ? `${selectedProfile.accreditation_body || 'RCI'} · Ref: ${selectedProfile.accreditation_number || 'N/A'}`
                      : 'Restricted account: Cannot certify VERIFIED. Submit reviews or revisions only.'}
                  </div>
                </div>
              </div>
            )}

            <div>
              <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                Reviewer Name & Designation:
              </label>
              <input
                type="text"
                value={reviewerName}
                onChange={(e) => setReviewerName(e.target.value)}
                className="w-full text-xs p-2 rounded-lg border border-slate-300 bg-white"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-[11px] font-semibold text-slate-700 mb-1">Decision:</label>
                <select
                  value={decision}
                  onChange={(e) => {
                    const dec = e.target.value;
                    setDecision(dec);
                    if (dec === 'approved') setAssignedStatus('verified');
                    else if (dec === 'rejected') setAssignedStatus('unsupported');
                    else if (dec === 'requires_correction') setAssignedStatus('needs_review');
                  }}
                  className="w-full text-xs p-2 rounded-lg border border-slate-300 bg-white"
                >
                  <option value="approved">Approved</option>
                  <option value="requires_correction">Requires Correction</option>
                  <option value="rejected">Rejected (Unsupported)</option>
                  <option value="status_modified">Modify Status</option>
                </select>
              </div>

              <div>
                <label className="block text-[11px] font-semibold text-slate-700 mb-1">Assigned Status:</label>
                <select
                  value={assignedStatus}
                  onChange={(e) => setAssignedStatus(e.target.value)}
                  className="w-full text-xs p-2 rounded-lg border border-slate-300 bg-white"
                >
                  <option value="verified">Verified</option>
                  <option value="needs_review">Needs Review</option>
                  <option value="partial">Partial</option>
                  <option value="explanation_needed">Explanation Needed</option>
                  <option value="unsupported">Unsupported</option>
                </select>
              </div>
            </div>

            {/* Governance Warning if attempting to verify with unauthorized account */}
            {assignedStatus === 'verified' && !selectedProfile?.is_authorized_expert && (
              <div className="p-2 bg-rose-50 border border-rose-200 rounded-lg text-[10px] text-rose-800 flex items-start gap-1.5">
                <AlertTriangle size={13} className="shrink-0 text-rose-600 mt-0.5" />
                <span>
                  <strong>Governance Policy:</strong> Profile {selectedProfile?.reviewer_code} lacks RCI/Deaf Master accreditation. Certifying as <em>Verified</em> will be blocked by backend governance (HTTP 403).
                </span>
              </div>
            )}

            <div>
              <label className="block text-[11px] font-semibold text-slate-700 mb-1">
                Accuracy Rating (1.0 to 5.0):
              </label>
              <div className="flex items-center gap-2">
                <input
                  type="range"
                  min="1.0"
                  max="5.0"
                  step="0.1"
                  value={rating}
                  onChange={(e) => setRating(parseFloat(e.target.value))}
                  className="w-full accent-indigo-600"
                />
                <span className="font-mono font-bold text-xs text-indigo-700">{rating.toFixed(1)}/5</span>
              </div>
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-700 mb-1">Comments & Rationale:</label>
              <textarea
                rows={2}
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                placeholder="Linguistic justification and feedback..."
                className="w-full text-xs p-2 rounded-lg border border-slate-300 bg-white resize-none"
              />
            </div>

            <div>
              <label className="block text-[11px] font-semibold text-slate-700 mb-1">Phonological Corrections (if any):</label>
              <input
                type="text"
                value={corrections}
                onChange={(e) => setCorrections(e.target.value)}
                placeholder="e.g. Adjust palm orientation inwards"
                className="w-full text-xs p-2 rounded-lg border border-slate-300 bg-white"
              />
            </div>

            <button
              type="submit"
              disabled={submitting || !selectedSignId}
              className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg transition-colors cursor-pointer disabled:opacity-50 text-xs shadow-xs"
            >
              {submitting ? 'Submitting to Blockchain/Ledger...' : 'Submit Evaluation Decision'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

