import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Languages,
  BookOpen,
  FileText,
  Mic,
  TrendingUp,
  Clock,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ShieldCheck,
  ArrowRight,
  Layers,
  Sparkles,
  Cpu,
  GraduationCap
} from 'lucide-react';
import { api } from '../api/client';
import { Branch, VocabularyListResponse, TranslationHistoryItem } from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const DashboardPage: React.FC = () => {
  const [branches, setBranches] = useState<Branch[]>([]);
  const [vocabStats, setVocabStats] = useState<VocabularyListResponse | null>(null);
  const [recentTranslations, setRecentTranslations] = useState<TranslationHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      setLoading(true);
      try {
        const [bData, vData, hData] = await Promise.all([
          api.getBranches(),
          api.getVocabulary(),
          api.getHistory(5),
        ]);
        setBranches(bData);
        setVocabStats(vData);
        setRecentTranslations(hData);
      } catch (err) {
        console.error("Error loading dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboardData();
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-10">
      {/* Welcome & Quick Action Hero */}
      <div className="bg-gradient-to-r from-blue-700 via-indigo-700 to-indigo-900 rounded-3xl p-6 sm:p-8 text-white shadow-lg space-y-4 relative overflow-hidden">
        <div className="relative z-10 space-y-2 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-white/10 backdrop-blur-md rounded-full text-xs font-semibold text-indigo-100 border border-white/10">
            <GraduationCap size={14} />
            <span>SignBridge Student Dashboard · Academic Year 2026-27</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Welcome to Indian Sign Language STEM Bridge
          </h1>
          <p className="text-xs sm:text-sm text-indigo-100/90 leading-relaxed">
            Access curriculum translations, accredited engineering sign videos, and interactive 3D avatar visual representations.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <Link
              to="/translate"
              className="px-4 py-2.5 bg-white text-indigo-900 hover:bg-indigo-50 font-bold rounded-xl text-xs shadow-md transition-colors flex items-center gap-2"
            >
              <Languages size={15} />
              <span>Translate Text Now</span>
            </Link>
            <Link
              to="/live-lecture"
              className="px-4 py-2.5 bg-indigo-600/60 hover:bg-indigo-600 border border-white/20 text-white font-bold rounded-xl text-xs transition-colors flex items-center gap-2"
            >
              <Mic size={15} />
              <span>Join Live Lecture Room</span>
            </Link>
            <Link
              to="/documents"
              className="px-4 py-2.5 bg-indigo-600/60 hover:bg-indigo-600 border border-white/20 text-white font-bold rounded-xl text-xs transition-colors flex items-center gap-2"
            >
              <FileText size={15} />
              <span>Upload Lecture Slides</span>
            </Link>
          </div>
        </div>

        {/* Subtle decorative circles */}
        <div className="absolute right-0 top-0 bottom-0 w-80 bg-white/5 rounded-full blur-3xl pointer-events-none" />
      </div>

      {/* Honest Vocabulary & Knowledge Base Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-2xs space-y-1">
          <span className="text-xs text-slate-500 font-semibold uppercase tracking-wider">
            Total STEM Terms
          </span>
          <div className="text-2xl font-black text-slate-900">
            {vocabStats ? vocabStats.total : '21'}
          </div>
          <span className="text-[11px] text-slate-400 block">Across 5 engineering branches</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs text-emerald-700 font-semibold uppercase tracking-wider">
              Verified Signs
            </span>
            <CheckCircle2 size={16} className="text-emerald-600" />
          </div>
          <div className="text-2xl font-black text-emerald-600">
            {vocabStats ? vocabStats.verified_count : '12'}
          </div>
          <span className="text-[11px] text-slate-400 block">With certified deaf reviews</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs text-amber-700 font-semibold uppercase tracking-wider">
              In Deaf Review
            </span>
            <Clock size={16} className="text-amber-500" />
          </div>
          <div className="text-2xl font-black text-amber-600">
            {vocabStats ? vocabStats.partial_count : '8'}
          </div>
          <span className="text-[11px] text-slate-400 block">Compound/pedagogical terms</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-slate-200/90 shadow-2xs space-y-1">
          <div className="flex items-center justify-between">
            <span className="text-xs text-rose-700 font-semibold uppercase tracking-wider">
              Unsupported
            </span>
            <ShieldCheck size={16} className="text-rose-500" />
          </div>
          <div className="text-2xl font-black text-rose-600">
            {vocabStats ? vocabStats.unsupported_count : '1'}
          </div>
          <span className="text-[11px] text-slate-400 block">Fingerspelling & diagrams needed</span>
        </div>
      </div>

      {/* Main Grid: Recent Translations & Branches */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Recent Translations */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock size={18} className="text-indigo-600" />
              <h3 className="text-base font-bold text-slate-900">Recent Translation Queries</h3>
            </div>
            <Link
              to="/history"
              className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold flex items-center gap-1"
            >
              <span>View full history</span>
              <ArrowRight size={13} />
            </Link>
          </div>

          <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-2xs">
            {recentTranslations.length > 0 ? (
              <div className="divide-y divide-slate-100">
                {recentTranslations.map((item) => (
                  <div key={item.id} className="p-4 hover:bg-slate-50/80 transition-colors space-y-2">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="text-xs font-semibold text-slate-900">
                          "{item.source_text}"
                        </p>
                        <div className="flex items-center gap-2 text-[11px] text-slate-400 mt-0.5">
                          <span>{item.branch_name || 'Engineering'}</span>
                          <span>·</span>
                          <span>{new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                        </div>
                      </div>
                      <StatusBadge status={item.status} size="sm" />
                    </div>

                    <div className="flex items-center gap-3 text-[11px] text-slate-500 font-medium">
                      <span>Verified: {item.verified_signs_count}</span>
                      <span>Unsupported: {item.unsupported_signs_count}</span>
                      {item.has_video && (
                        <span className="text-emerald-600 font-semibold">Video Ready</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-8 text-center text-slate-400 text-xs">
                No recent translations yet. Submit your first engineering sentence!
              </div>
            )}
          </div>

          <PolicyNotice />
        </div>

        {/* Right Column: Engineering Branches & Modalities */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Layers size={18} className="text-indigo-600" />
              <h3 className="text-base font-bold text-slate-900">Curriculum Branches</h3>
            </div>
            <Link
              to="/vocabulary"
              className="text-xs text-indigo-600 hover:text-indigo-800 font-semibold"
            >
              Browse all
            </Link>
          </div>

          <div className="space-y-2.5">
            {branches.map((b) => (
              <div
                key={b.id}
                className="p-3.5 bg-white border border-slate-200/90 rounded-2xl shadow-2xs flex items-center justify-between hover:border-slate-300 transition-colors"
              >
                <div>
                  <h4 className="text-xs font-bold text-slate-900">{b.name}</h4>
                  <p className="text-[11px] text-slate-500">
                    {b.subject_count} subjects · {b.concept_count} technical concepts
                  </p>
                </div>
                <span className="text-[10px] uppercase font-bold font-mono px-2 py-1 bg-indigo-50 text-indigo-700 rounded-lg">
                  {b.code}
                </span>
              </div>
            ))}
          </div>

          {/* Supported Modalities Card */}
          <div className="p-4 bg-slate-900 text-white rounded-2xl space-y-3 shadow-md">
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles size={14} className="text-indigo-400" />
              <span>Input Modalities</span>
            </h4>
            <div className="space-y-2 text-xs text-slate-300">
              <div className="flex items-center justify-between">
                <span>Typed English</span>
                <span className="text-emerald-400 font-semibold">Operational</span>
              </div>
              <div className="flex items-center justify-between">
                <span>PDF Documents</span>
                <span className="text-emerald-400 font-semibold">Operational</span>
              </div>
              <div className="flex items-center justify-between">
                <span>DOCX & PPTX Slides</span>
                <span className="text-emerald-400 font-semibold">Operational</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Live Lecture Audio</span>
                <span className="text-indigo-400 font-semibold">Demo Pipeline</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

