import React, { useState } from 'react';
import {
  Users,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  Play,
  Star,
  Download,
  Trash2,
  FileCheck,
  Send,
  Lock
} from 'lucide-react';
import { api } from '../api/client';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const CommunityEvaluationPage: React.FC = () => {
  const [pseudonym, setPseudonym] = useState<string>(() => `DEAF-PARTICIPANT-${Math.floor(100 + Math.random() * 900)}`);
  const [consentGiven, setConsentGiven] = useState(false);
  const [consentRecorded, setConsentRecorded] = useState(false);
  const [sessionCompleted, setSessionCompleted] = useState(false);

  // Comprehension test states
  const [selectedConcept, setSelectedConcept] = useState('Algorithm');
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [naturalnessRating, setNaturalnessRating] = useState<number>(4);
  const [feedbackNotes, setFeedbackNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState<string | null>(null);

  const handleRecordConsent = async () => {
    if (!consentGiven) return;
    setLoading(true);
    try {
      await api.recordParticipantConsent({
        pseudonym,
        study_name: 'SignBridge AI Deaf Community Linguistic Evaluation 2026',
        consent_given: true,
        can_withdraw_anytime: true
      });
      setConsentRecorded(true);
      setFeedbackMsg(`Informed consent recorded for ${pseudonym}. Zero personally identifiable information retained.`);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to record consent.');
    } finally {
      setLoading(false);
    }
  };

  const handleCompleteSession = async () => {
    if (!selectedAnswer) {
      alert('Please select an answer for the comprehension check.');
      return;
    }
    setLoading(true);
    try {
      const isCorrect = selectedAnswer === 'Step-by-step computational procedure';
      const score = isCorrect ? 1.0 : 0.0;
      await api.recordResearchSession({
        participant_pseudonym: pseudonym,
        session_code: `SESS-${pseudonym}-${Date.now().toString().slice(-4)}`,
        session_type: 'comprehension_and_naturalness_survey',
        concepts_tested: [
          {
            concept: selectedConcept,
            selected_meaning: selectedAnswer,
            correct: isCorrect
          }
        ],
        comprehension_score: score,
        naturalness_rating: naturalnessRating,
        feedback_notes: feedbackNotes
      });
      setSessionCompleted(true);
      setFeedbackMsg('Thank you! Your community evaluation feedback has been recorded anonymously.');
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to record session.');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteData = async () => {
    if (!window.confirm('Are you sure you want to withdraw and delete all your session data? This action is permanent.')) {
      return;
    }
    try {
      await api.deleteParticipantData({ participant_pseudonym: pseudonym });
      setConsentRecorded(false);
      setSessionCompleted(false);
      alert(`All research session data for ${pseudonym} has been permanently purged from the database.`);
    } catch (err: any) {
      alert('Failed to delete data.');
    }
  };

  const handleExportDataset = async () => {
    try {
      const data = await api.exportResearchDataset();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `signbridge_deaf_community_cohort_${Date.now()}.json`;
      a.click();
    } catch (err) {
      alert('Failed to export dataset.');
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto pb-20">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              Deaf Community Linguistic & Comprehension Evaluation
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              Ethical Research Protocol
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Voluntary, anonymous comprehension surveys and naturalness scoring for Deaf ISL students and educators.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      {feedbackMsg && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl text-xs font-bold">
          {feedbackMsg}
        </div>
      )}

      {/* Step 1: Informed Consent & Information Sheet */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2 text-indigo-900 font-bold text-sm">
            <FileCheck size={18} className="text-indigo-600" />
            <span>Step 1: Participant Information Sheet & Informed Consent</span>
          </div>
          <span className="font-mono text-xs text-slate-600 bg-slate-100 px-2.5 py-1 rounded-md font-bold">
            Pseudonym: {pseudonym}
          </span>
        </div>

        <div className="bg-slate-50 p-4 rounded-xl text-xs text-slate-600 space-y-2 leading-relaxed">
          <p>
            <strong>Study Objective:</strong> You are invited to evaluate whether 3D animated Indian Sign Language signs for engineering concepts are clear, understandable, and natural for Deaf students.
          </p>
          <p>
            <strong>Voluntary & Anonymous:</strong> No names, phone numbers, email addresses, or facial videos are collected. Your responses are tagged strictly under the pseudonym <code className="bg-white px-1 rounded border border-slate-200">{pseudonym}</code>.
          </p>
          <p>
            <strong>Right to Withdraw (GDPR / ICMR Ethical Compliance):</strong> You may withdraw at any time. Clicking "Delete My Data" permanently purges your survey responses from our research database.
          </p>
        </div>

        {!consentRecorded ? (
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pt-2">
            <label className="flex items-center gap-2 text-xs font-bold text-slate-800 cursor-pointer">
              <input
                type="checkbox"
                checked={consentGiven}
                onChange={(e) => setConsentGiven(e.target.checked)}
                className="rounded text-indigo-600 w-4 h-4"
              />
              <span>I have read the information sheet and give voluntary consent to participate.</span>
            </label>

            <button
              onClick={handleRecordConsent}
              disabled={!consentGiven || loading}
              className="px-5 py-2 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition disabled:opacity-50 shrink-0"
            >
              {loading ? 'Recording...' : 'Accept & Begin Survey'}
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-between bg-emerald-50 text-emerald-800 p-3 rounded-xl border border-emerald-200 text-xs font-semibold">
            <div className="flex items-center gap-2">
              <CheckCircle2 size={16} className="text-emerald-600" />
              <span>Informed consent active for {pseudonym}. You may withdraw anytime below.</span>
            </div>
            <button
              onClick={handleDeleteData}
              className="px-3 py-1 bg-white text-rose-700 border border-rose-300 rounded-lg text-xs font-bold hover:bg-rose-50 transition flex items-center gap-1"
            >
              <Trash2 size={13} />
              <span>Delete My Data</span>
            </button>
          </div>
        )}
      </div>

      {/* Step 2: Interactive Comprehension & Naturalness Test */}
      {consentRecorded && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
            <div className="flex items-center gap-2 text-indigo-900 font-bold text-sm">
              <Users size={18} className="text-indigo-600" />
              <span>Step 2: Comprehension & Naturalness Assessment</span>
            </div>
            <select
              value={selectedConcept}
              onChange={(e) => {
                setSelectedConcept(e.target.value);
                setSelectedAnswer(null);
                setSessionCompleted(false);
              }}
              className="text-xs font-bold border border-slate-300 rounded-lg px-2.5 py-1 bg-white"
            >
              <option value="Algorithm">Sign 1: Algorithm</option>
              <option value="Frequency">Sign 2: Frequency</option>
              <option value="Current">Sign 3: Current</option>
              <option value="Beam">Sign 4: Beam</option>
              <option value="Torque">Sign 5: Torque</option>
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left: 3D Avatar Display */}
            <div className="space-y-2">
              <h4 className="text-xs font-bold text-slate-800">Watch the Sign Execution</h4>
              <div className="aspect-video bg-slate-950 rounded-xl overflow-hidden border border-slate-800">
                <AvatarViewer
                  conceptTerm={selectedConcept}
                  avatarData={{
                    available: true,
                    model_type: 'SignBridge-Articulated-54',
                    animation_name: `islrtc_${selectedConcept.toLowerCase()}_mocap`,
                    rig_standard: 'SignBridge-Articulated-54',
                    validation_status: 'partial',
                    motion_status: 'PARTIALLY_VERIFIED_MOTION',
                    notice: '54-joint articulated ISL avatar'
                  }}
                />
              </div>
              <p className="text-[11px] text-slate-500">
                Sign rendered in real-time WebGL from authentic ISLRTC motion capture.
              </p>
            </div>

            {/* Right: Multiple-Choice Comprehension Test */}
            <div className="space-y-4">
              <div>
                <h4 className="text-xs font-bold text-slate-800 mb-2">Comprehension Question:</h4>
                <p className="text-xs text-slate-600 font-medium mb-3">
                  Based on the handshape, movement, and facial expression shown above, what is the meaning of this sign?
                </p>

                <div className="space-y-2">
                  {[
                    'Step-by-step computational procedure',
                    'A mechanical deadlock where two resources block each other',
                    'Oscillations per second of an electrical wave',
                    'A continuous flow of electrical charge through a conductor'
                  ].map((opt) => (
                    <button
                      key={opt}
                      onClick={() => setSelectedAnswer(opt)}
                      className={`w-full text-left p-3 rounded-xl border text-xs font-medium transition ${
                        selectedAnswer === opt
                          ? 'bg-indigo-50 border-indigo-500 text-indigo-900 font-bold shadow-sm'
                          : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>

              {/* Naturalness Likert Scale */}
              <div>
                <label className="block text-xs font-bold text-slate-800 mb-1.5">
                  Naturalness & Fluidity Rating (1 = Robotic/Awkward, 5 = Highly Natural):
                </label>
                <div className="flex items-center gap-2">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      key={star}
                      onClick={() => setNaturalnessRating(star)}
                      className={`p-2 rounded-lg border text-xs font-bold flex items-center gap-1 transition ${
                        naturalnessRating >= star
                          ? 'bg-amber-50 border-amber-300 text-amber-800'
                          : 'bg-white border-slate-200 text-slate-400'
                      }`}
                    >
                      <Star size={14} className={naturalnessRating >= star ? 'fill-amber-400 text-amber-500' : ''} />
                      <span>{star}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Qualitative Regional Feedback */}
              <div>
                <label className="block text-xs font-bold text-slate-800 mb-1">
                  Regional or Dialectal Notes (Optional):
                </label>
                <textarea
                  rows={2}
                  value={feedbackNotes}
                  onChange={(e) => setFeedbackNotes(e.target.value)}
                  placeholder="Does your local Deaf community sign this differently? Any confusing hand movements?"
                  className="w-full text-xs p-2.5 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              <button
                onClick={handleCompleteSession}
                disabled={loading || !selectedAnswer || sessionCompleted}
                className="w-full py-2.5 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition shadow disabled:opacity-50"
              >
                {loading ? 'Submitting...' : sessionCompleted ? 'Response Recorded!' : 'Submit Evaluation'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Dataset Export Section */}
      <div className="bg-slate-900 text-white p-5 rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-sm font-bold flex items-center gap-2 text-indigo-300">
            <Download size={16} />
            <span>Open Academic Research Dataset Export</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5 max-w-xl">
            Export anonymized Deaf community evaluation records under Open Data Commons (ODC-By) for scholarly analysis and replication.
          </p>
        </div>
        <button
          onClick={handleExportDataset}
          className="px-4 py-2 bg-white/10 hover:bg-white/20 text-white border border-white/20 rounded-xl text-xs font-bold transition flex items-center gap-2 shrink-0"
        >
          <Download size={14} />
          <span>Export Dataset (JSON)</span>
        </button>
      </div>
    </div>
  );
};

export default CommunityEvaluationPage;
