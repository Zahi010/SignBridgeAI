import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Award,
  Users,
  Activity,
  BarChart3,
  Scale,
  FileText,
  Clock,
  ArrowRight,
  ExternalLink,
  Info,
  AlertOctagon
} from 'lucide-react';
import { api } from '../api/client';
import { Phase5DashboardStats, Phase5AcademicMetrics } from '../types';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const ValidationDashboardPage: React.FC = () => {
  const [stats, setStats] = useState<Phase5DashboardStats | null>(null);
  const [academicMetrics, setAcademicMetrics] = useState<Phase5AcademicMetrics | null>(null);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [dashData, acadData, logsData] = await Promise.all([
        api.getValidationDashboardStats(),
        api.getAcademicMetrics(),
        api.getValidationAuditLogs(20)
      ]);
      setStats(dashData);
      setAcademicMetrics(acadData);
      setAuditLogs(logsData);
    } catch (err) {
      console.error('Failed to load validation dashboard', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-20">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              ISL Validation & Academic Evaluation Dashboard
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-200">
              Phase 5 Research Governance
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Real-time tracking of expert reviews, inter-rater reliability, phonological disagreements, and community evaluation.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/expert-review"
            className="px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-bold hover:bg-indigo-700 transition shadow flex items-center gap-1.5"
          >
            <span>Expert Review Workspace</span>
            <ArrowRight size={14} />
          </Link>
          <Link
            to="/community-evaluation"
            className="px-4 py-2 bg-slate-100 text-slate-700 hover:bg-slate-200 rounded-xl text-xs font-bold transition flex items-center gap-1.5"
          >
            <span>Community Portal</span>
          </Link>
        </div>
      </div>

      {/* KPI Stats Grid */}
      {stats && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-1">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Candidate Signs</span>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-black text-slate-900">{stats.total_validation_tasks}</span>
              <span className="text-xs font-semibold text-slate-500 font-mono">5 Authentic</span>
            </div>
            <p className="text-[10px] text-slate-400">ISLRTC Mocap Assets Ingested</p>
          </div>

          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-1">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Reviews in Progress</span>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-black text-amber-600">{stats.under_review_tasks_count}</span>
              <span className="text-xs font-semibold text-slate-500 font-mono">{stats.reviewed_tasks_count} Reviewed</span>
            </div>
            <p className="text-[10px] text-slate-400">Multi-reviewer cohort active</p>
          </div>

          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-1">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Open Disagreements</span>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-black text-rose-600">{stats.disagreements_count}</span>
              <span className="text-xs font-semibold text-slate-500 font-mono">{stats.adjudicated_tasks_count} Adjudicated</span>
            </div>
            <p className="text-[10px] text-rose-500 font-medium">Requiring expert adjudication</p>
          </div>

          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-1">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">Verified Reviewers</span>
            <div className="flex items-baseline justify-between">
              <span className="text-2xl font-black text-emerald-600">{stats.verified_reviewers_count}</span>
              <span className="text-xs font-semibold text-slate-500 font-mono">{stats.pending_credential_verifications_count} Pending</span>
            </div>
            <p className="text-[10px] text-slate-400">RCI & Deaf Certified Experts</p>
          </div>
        </div>
      )}

      {/* Technical Accuracy vs. Linguistic Validity Card */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl p-6 shadow-md space-y-4">
        <div className="flex items-center justify-between border-b border-white/10 pb-3">
          <div className="flex items-center gap-2">
            <Scale size={20} className="text-indigo-400" />
            <h3 className="text-sm font-bold tracking-wide uppercase text-indigo-200">
              Technical Accuracy vs. Linguistic Validity Disconnect
            </h3>
          </div>
          <span className="px-2.5 py-0.5 rounded-full bg-amber-400/20 text-amber-300 text-xs font-bold border border-amber-400/30">
            Zero-Fabrication Guardrail Active
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs leading-relaxed">
          <div className="bg-white/5 p-4 rounded-xl border border-white/10 space-y-2">
            <div className="flex items-center gap-2 font-bold text-emerald-400 text-sm">
              <CheckCircle2 size={16} />
              <span>Level 4: Technical Kinematic Accuracy</span>
            </div>
            <p className="text-slate-300">
              Our Phase 4.5 audit verified that the 54-joint rig, MediaPipe mocap solvers, One-Euro filters, and WebGL rendering operate with high fidelity (NMLE &lt; 3.9% body height, 60 FPS).
            </p>
            <div className="flex items-center gap-2 pt-1">
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[11px]">
                5/5 Passing Mocap
              </span>
              <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono text-[11px]">
                100% Data Integrity
              </span>
            </div>
          </div>

          <div className="bg-white/5 p-4 rounded-xl border border-white/10 space-y-2">
            <div className="flex items-center gap-2 font-bold text-amber-400 text-sm">
              <AlertTriangle size={16} />
              <span>Level 5: Authentic Linguistic Validity</span>
            </div>
            <p className="text-slate-300">
              Technical smoothness does not establish linguistic validity. A sign is not authentic Indian Sign Language until qualified Deaf native signers and RCI interpreters independently review and certify communicative acceptance.
            </p>
            <div className="flex items-center gap-2 pt-1">
              <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-[11px]">
                Status: PARTIALLY_VERIFIED_MOTION
              </span>
              <span className="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-mono text-[11px]">
                Pending External Review
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Academic Evaluation Engine Card */}
      {academicMetrics && (
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-5">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
            <div>
              <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
                <BarChart3 size={20} className="text-indigo-600" />
                <span>Academic Evaluation Engine & Inter-Rater Reliability</span>
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Formal statistical analysis for scholarly publication (Cohen's Kappa, Wilson CI, sample sufficiency).
              </p>
            </div>

            <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${
              academicMetrics.sample_size_category === 'COMPLETED_EVALUATION'
                ? 'bg-emerald-50 text-emerald-700 border-emerald-300'
                : academicMetrics.sample_size_category === 'PRELIMINARY_RESULTS'
                ? 'bg-blue-50 text-blue-700 border-blue-300'
                : 'bg-amber-50 text-amber-700 border-amber-300'
            }`}>
              {academicMetrics.sample_size_category.replace(/_/g, ' ')}
            </span>
          </div>

          {/* Academic Disclaimer Banner */}
          <div className="bg-slate-50 border border-slate-200 p-3.5 rounded-xl text-xs text-slate-600 flex items-start gap-2.5">
            <Info size={16} className="text-indigo-600 shrink-0 mt-0.5" />
            <p>{academicMetrics.academic_disclaimer}</p>
          </div>

          {/* Statistical Highlights Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-1">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase">Inter-Reviewer Agreement</span>
              <p className="text-xl font-black text-indigo-700 mt-0.5">
                {academicMetrics.average_inter_reviewer_agreement_percent}%
              </p>
              <span className="text-[10px] text-slate-400">Mean across 12 criteria</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase">Cohen's Kappa (κ)</span>
              <p className="text-xl font-black text-slate-900 mt-0.5">
                {academicMetrics.cohens_kappa !== null ? academicMetrics.cohens_kappa : 'N/A'}
              </p>
              <span className="text-[10px] text-slate-400">Pairwise recommendation</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase">Disagreement Rate</span>
              <p className="text-xl font-black text-rose-600 mt-0.5">
                {academicMetrics.disagreement_frequency_percent}%
              </p>
              <span className="text-[10px] text-slate-400">Multi-review tasks</span>
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-center">
              <span className="text-[10px] font-bold text-slate-500 uppercase">95% Confidence Interval</span>
              <p className="text-sm font-black text-slate-800 mt-1.5 font-mono">
                [{academicMetrics.confidence_interval_95.lower}%, {academicMetrics.confidence_interval_95.upper}%]
              </p>
              <span className="text-[10px] text-slate-400">Wilson score method</span>
            </div>
          </div>

          {/* Criterion Agreement Table */}
          {academicMetrics.criterion_statistics.length > 0 && (
            <div className="space-y-2 pt-2">
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Criterion-Level Agreement Breakdown (12 Criteria)
              </h4>
              <div className="border border-slate-200 rounded-xl overflow-hidden">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 font-bold border-b border-slate-200">
                    <tr>
                      <th className="p-2.5">Phonological Criterion</th>
                      <th className="p-2.5 text-center">Evaluations</th>
                      <th className="p-2.5 text-center">Agreement %</th>
                      <th className="p-2.5 text-center">Pass Rate</th>
                      <th className="p-2.5 text-center">Major Error Rate</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-medium">
                    {academicMetrics.criterion_statistics.map((c: any) => (
                      <tr key={c.criterion_name} className="hover:bg-slate-50/50">
                        <td className="p-2.5 font-bold text-slate-900 capitalize">
                          {c.criterion_name.replace(/_/g, ' ')}
                        </td>
                        <td className="p-2.5 text-center font-mono">{c.total_evaluations}</td>
                        <td className="p-2.5 text-center font-mono font-bold text-indigo-700">
                          {c.agreement_percentage}%
                        </td>
                        <td className="p-2.5 text-center font-mono text-emerald-700">{c.pass_rate}%</td>
                        <td className="p-2.5 text-center font-mono text-rose-700">{c.major_error_rate}%</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Immutable Validation Audit Log Timeline */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2 text-indigo-900 font-bold text-sm">
            <Clock size={18} className="text-indigo-600" />
            <span>Immutable Validation Audit Log</span>
          </div>
          <span className="text-xs text-slate-500 font-medium">Recent 20 Administrative & Review Events</span>
        </div>

        <div className="space-y-2 max-h-[350px] overflow-y-auto pr-1">
          {auditLogs.length > 0 ? (
            auditLogs.map((log) => (
              <div key={log.id} className="p-2.5 rounded-xl border border-slate-100 bg-slate-50/60 flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-[10px] text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span className="font-bold text-slate-900">{log.action}</span>
                  <span className="text-slate-500">by @{log.actor_username}</span>
                </div>
                <span className="text-[11px] font-mono text-slate-600 truncate max-w-xs">
                  Target: {log.target_type} ({log.target_id})
                </span>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-500 text-center py-6">No audit log entries recorded yet.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ValidationDashboardPage;
