import React from 'react';
import { ReviewerValidationPanel } from '../components/validation/ReviewerValidationPanel';
import { PolicyNotice } from '../components/common/PolicyNotice';
import { UserCheck, ShieldAlert, GraduationCap } from 'lucide-react';

export const ValidationPortalPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              ISL Expert & Deaf Community Validation Portal
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              Governance & Accreditation
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Certified Deaf educators and ISL linguists audit, certify, and record phonological corrections for STEM candidate signs.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      {/* Governance Explanatory Notice */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl p-5 shadow-md flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1.5 max-w-2xl">
          <div className="flex items-center gap-2 text-indigo-300 font-bold text-xs uppercase tracking-wider">
            <GraduationCap size={16} />
            <span>Multi-Stage Community Accreditation Workflow</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Every candidate sign in SignBridge AI must undergo review by certified ISL interpreters or Deaf master signers before it can transition from <strong className="text-amber-300">NEEDS_REVIEW</strong> to <strong className="text-emerald-300">VERIFIED</strong>. Non-codified technical terms are flagged as <strong className="text-rose-300">UNSUPPORTED</strong> or <strong className="text-blue-300">EXPLANATION_REQUIRED</strong> to prevent ungrammatical synthetic signs.
          </p>
        </div>
        <div className="shrink-0 flex items-center gap-2 px-3 py-2 bg-white/10 rounded-xl border border-white/10 text-xs font-medium text-slate-200">
          <UserCheck size={16} className="text-emerald-400 shrink-0" />
          <span>Active Audit Trail: Multi-Signature</span>
        </div>
      </div>

      {/* Interactive Validation Panel */}
      <ReviewerValidationPanel />
    </div>
  );
};

export default ValidationPortalPage;

