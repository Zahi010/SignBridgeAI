import React, { useState } from 'react';
import {
  UserCheck,
  ShieldCheck,
  Award,
  Lock,
  Mail,
  User,
  Building,
  AlertTriangle,
  X,
  FileText
} from 'lucide-react';
import { api } from '../../api/client';
import { Phase5Reviewer, ReviewerRoleType } from '../../types';

interface ReviewerAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser: Phase5Reviewer | null;
  onUserChange: (user: Phase5Reviewer | null, token: string | null) => void;
}

export const ReviewerAuthModal: React.FC<ReviewerAuthModalProps> = ({
  isOpen,
  onClose,
  currentUser,
  onUserChange
}) => {
  const [tab, setTab] = useState<'login' | 'register' | 'credential'>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState<ReviewerRoleType>('reviewer');
  const [isDeafNative, setIsDeafNative] = useState(false);
  const [isCertifiedInterpreter, setIsCertifiedInterpreter] = useState(false);
  const [affiliation, setAffiliation] = useState('');
  const [yearsExp, setYearsExp] = useState(3);

  // Credential form
  const [credType, setCredType] = useState('rci_certificate');
  const [credIdentifier, setCredIdentifier] = useState('');
  const [issuingBody, setIssuingBody] = useState('Rehabilitation Council of India');
  const [credNotes, setCredNotes] = useState('');

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await api.loginReviewer({ username_or_email: username, password });
      localStorage.setItem('signbridge_reviewer_token', data.access_token);
      const profile = await api.getCurrentReviewer(data.access_token);
      onUserChange(profile, data.access_token);
      setSuccessMsg(`Welcome, ${profile.full_name}!`);
      setTimeout(() => onClose(), 1200);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    try {
      await api.registerReviewer({
        username,
        email,
        password,
        full_name: fullName,
        is_deaf_native_signer: isDeafNative,
        is_certified_interpreter: isCertifiedInterpreter,
        years_of_experience: yearsExp,
        institution_affiliation: affiliation,
        role
      });
      // Automatically log in
      const data = await api.loginReviewer({ username_or_email: username, password });
      localStorage.setItem('signbridge_reviewer_token', data.access_token);
      const profile = await api.getCurrentReviewer(data.access_token);
      onUserChange(profile, data.access_token);
      setSuccessMsg('Account registered! Status: UNVERIFIED pending credential verification.');
      setTab('credential');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitCredential = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg(null);
    try {
      const token = localStorage.getItem('signbridge_reviewer_token') || undefined;
      await api.submitCredential({
        credential_type: credType,
        credential_identifier: credIdentifier,
        issuing_body: issuingBody,
        notes: credNotes
      }, token);
      setSuccessMsg('Credential submitted! Status updated to VERIFICATION_PENDING.');
      if (token) {
        const updated = await api.getCurrentReviewer(token);
        onUserChange(updated, token);
      }
      setTimeout(() => onClose(), 1500);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to submit credential.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('signbridge_reviewer_token');
    onUserChange(null, null);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden border border-slate-200">
        {/* Header */}
        <div className="bg-slate-900 text-white p-5 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <ShieldCheck size={22} className="text-emerald-400" />
            <div>
              <h2 className="text-base font-bold">Reviewer Accreditation & Authentication</h2>
              <p className="text-xs text-slate-400">Zero-Fabrication Expert Review Governance</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition">
            <X size={20} />
          </button>
        </div>

        {/* Tab selection */}
        {currentUser ? (
          <div className="p-6 space-y-4">
            <div className="flex items-center gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200">
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold text-lg">
                {currentUser.full_name[0]}
              </div>
              <div>
                <h3 className="font-bold text-slate-900 text-sm">{currentUser.full_name}</h3>
                <p className="text-xs text-slate-500">@{currentUser.username} • {currentUser.role}</p>
                <div className="mt-1 flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wider uppercase ${
                    currentUser.verification_status === 'verified'
                      ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                      : currentUser.verification_status === 'verification_pending'
                      ? 'bg-amber-100 text-amber-800 border border-amber-300'
                      : 'bg-slate-100 text-slate-700 border border-slate-300'
                  }`}>
                    {currentUser.verification_status}
                  </span>
                  {currentUser.is_deaf_native_signer && (
                    <span className="text-[10px] bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded border border-blue-200">
                      Deaf Native Signer
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="space-y-2 text-xs text-slate-600 bg-amber-50 p-3.5 rounded-xl border border-amber-200">
              <div className="flex items-center gap-1.5 font-bold text-amber-900">
                <AlertTriangle size={14} />
                <span>Governance Rule: Verified Expert Requirement</span>
              </div>
              <p>
                Only reviewers with verified qualifications (RCI licensed interpreters, certified Deaf educators) can certify signs as <strong>VERIFIED_ISL_MOTION</strong>. Unverified accounts may submit draft feedback for review.
              </p>
            </div>

            <div className="flex items-center justify-between pt-2">
              <button
                onClick={() => setTab('credential')}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700 transition"
              >
                Submit Verifiable Credential
              </button>
              <button
                onClick={handleLogout}
                className="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold hover:bg-slate-300 transition"
              >
                Log Out
              </button>
            </div>
          </div>
        ) : (
          <div>
            <div className="flex border-b border-slate-200 bg-slate-50 text-xs font-semibold text-slate-600">
              <button
                onClick={() => setTab('login')}
                className={`flex-1 py-3 text-center transition ${tab === 'login' ? 'bg-white text-indigo-600 border-b-2 border-indigo-600 font-bold' : 'hover:bg-slate-100'}`}
              >
                Log In
              </button>
              <button
                onClick={() => setTab('register')}
                className={`flex-1 py-3 text-center transition ${tab === 'register' ? 'bg-white text-indigo-600 border-b-2 border-indigo-600 font-bold' : 'hover:bg-slate-100'}`}
              >
                Register Reviewer
              </button>
            </div>

            <div className="p-6">
              {errorMsg && (
                <div className="mb-4 p-3 bg-rose-50 border border-rose-200 rounded-lg text-rose-700 text-xs">
                  {errorMsg}
                </div>
              )}
              {successMsg && (
                <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-700 text-xs">
                  {successMsg}
                </div>
              )}

              {tab === 'login' && (
                <form onSubmit={handleLogin} className="space-y-3.5">
                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Username or Email</label>
                    <div className="relative">
                      <User size={15} className="absolute left-3 top-3 text-slate-400" />
                      <input
                        type="text"
                        required
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="e.g. admin or rev_sunita"
                        className="w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Password</label>
                    <div className="relative">
                      <Lock size={15} className="absolute left-3 top-3 text-slate-400" />
                      <input
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••"
                        className="w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-2.5 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition shadow disabled:opacity-50"
                  >
                    {loading ? 'Authenticating...' : 'Sign In as Reviewer'}
                  </button>

                  <div className="text-[11px] text-slate-500 text-center mt-2">
                    Default Administrator: <code className="bg-slate-100 px-1 py-0.5 rounded text-indigo-700">admin</code> / <code className="bg-slate-100 px-1 py-0.5 rounded text-indigo-700">admin_pass_2026_isl</code>
                  </div>
                </form>
              )}

              {tab === 'register' && (
                <form onSubmit={handleRegister} className="space-y-3">
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Username</label>
                      <input
                        type="text"
                        required
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="rev_username"
                        className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Email</label>
                      <input
                        type="email"
                        required
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="user@example.org"
                        className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Full Legal Name</label>
                      <input
                        type="text"
                        required
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="Dr. / Shri Full Name"
                        className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-bold text-slate-700 mb-1">Password</label>
                      <input
                        type="password"
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Min 6 characters"
                        className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-slate-700 mb-1">Reviewer Role</label>
                    <select
                      value={role}
                      onChange={(e) => setRole(e.target.value as ReviewerRoleType)}
                      className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                    >
                      <option value="reviewer">General Reviewer (Candidate)</option>
                      <option value="deaf_native_signer">Deaf Native Signer</option>
                      <option value="certified_interpreter">RCI Certified ISL Interpreter</option>
                      <option value="expert_reviewer">Academic ISL Linguist / Scholar</option>
                    </select>
                  </div>

                  <div className="flex gap-4 pt-1">
                    <label className="flex items-center gap-1.5 text-xs text-slate-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isDeafNative}
                        onChange={(e) => setIsDeafNative(e.target.checked)}
                        className="rounded text-indigo-600"
                      />
                      <span>Deaf Native Signer</span>
                    </label>
                    <label className="flex items-center gap-1.5 text-xs text-slate-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={isCertifiedInterpreter}
                        onChange={(e) => setIsCertifiedInterpreter(e.target.checked)}
                        className="rounded text-indigo-600"
                      />
                      <span>Certified Interpreter</span>
                    </label>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full mt-2 py-2.5 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition shadow disabled:opacity-50"
                  >
                    {loading ? 'Registering...' : 'Register as Candidate Reviewer'}
                  </button>
                </form>
              )}
            </div>
          </div>
        )}

        {/* Credential Tab */}
        {tab === 'credential' && (
          <div className="p-6 space-y-3.5 border-t border-slate-100">
            <div className="flex items-center gap-2 text-indigo-900 font-bold text-xs">
              <Award size={16} className="text-indigo-600" />
              <span>Submit Formal Qualifications for Review</span>
            </div>

            <form onSubmit={handleSubmitCredential} className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Credential Type</label>
                <select
                  value={credType}
                  onChange={(e) => setCredType(e.target.value)}
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                >
                  <option value="rci_certificate">Rehabilitation Council of India (RCI) Certificate</option>
                  <option value="deaf_association_member">Deaf Association Membership (AIFD / State)</option>
                  <option value="interpreter_license">National ISL Interpreter License</option>
                  <option value="academic_degree">Linguistics / Deaf Studies University Degree</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Credential Registration Number</label>
                <input
                  type="text"
                  required
                  value={credIdentifier}
                  onChange={(e) => setCredIdentifier(e.target.value)}
                  placeholder="e.g. RCI-CRR-A12345 or AIFD-DELHI-88"
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Issuing Authority / University</label>
                <input
                  type="text"
                  required
                  value={issuingBody}
                  onChange={(e) => setIssuingBody(e.target.value)}
                  placeholder="e.g. Rehabilitation Council of India"
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Supporting Notes</label>
                <textarea
                  rows={2}
                  value={credNotes}
                  onChange={(e) => setCredNotes(e.target.value)}
                  placeholder="Details of certification, years practicing, specialization in STEM terminology..."
                  className="w-full px-3 py-1.5 text-xs border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 py-2 bg-indigo-600 text-white rounded-lg text-xs font-bold hover:bg-indigo-700 transition"
                >
                  {loading ? 'Submitting...' : 'Submit for Admin Verification'}
                </button>
                <button
                  type="button"
                  onClick={() => setTab('login')}
                  className="px-4 py-2 bg-slate-100 text-slate-700 rounded-lg text-xs font-semibold hover:bg-slate-200 transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};
