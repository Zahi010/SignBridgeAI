import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  History,
  Languages,
  Clock,
  ArrowRight,
  Filter,
  CheckCircle2,
  AlertCircle,
  Video,
  User,
  ShieldCheck
} from 'lucide-react';
import { api } from '../api/client';
import { TranslationHistoryItem } from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const HistoryPage: React.FC = () => {
  const [historyItems, setHistoryItems] = useState<TranslationHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>('');

  useEffect(() => {
    setLoading(true);
    api.getHistory(50)
      .then((data) => setHistoryItems(data))
      .catch((err) => console.error("Error loading history", err))
      .finally(() => setLoading(false));
  }, []);

  const filteredItems = filterStatus
    ? historyItems.filter((i) => i.status === filterStatus)
    : historyItems;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              Translation Session History
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
              Audit Trail
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Review past curriculum translations, detected concepts, and linguistic evaluation statuses.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      {/* Filter Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex items-center justify-between flex-wrap gap-3">
        <div className="flex items-center gap-2">
          <Filter size={16} className="text-slate-400" />
          <span className="text-xs font-semibold text-slate-700">Filter by Status:</span>
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="text-xs px-3 py-1.5 rounded-xl border border-slate-300 bg-slate-50/50 text-slate-700 font-medium focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="">All Statuses ({historyItems.length})</option>
            <option value="verified">Verified Only</option>
            <option value="partial">Partial</option>
            <option value="explanation_needed">Explanation Needed</option>
            <option value="needs_review">Needs Review</option>
            <option value="unsupported">Unsupported</option>
          </select>
        </div>

        <span className="text-xs text-slate-400">
          Showing {filteredItems.length} records
        </span>
      </div>

      {/* History List */}
      {loading ? (
        <div className="p-12 text-center text-xs text-slate-500 space-y-2">
          <div className="w-8 h-8 border-3 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin mx-auto" />
          <span>Loading translation history...</span>
        </div>
      ) : filteredItems.length > 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-2xs divide-y divide-slate-100">
          {filteredItems.map((item) => (
            <div
              key={item.id}
              className="p-5 hover:bg-slate-50/70 transition-colors space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="space-y-1">
                  <h3 className="text-sm font-bold text-slate-900">"{item.source_text}"</h3>
                  <div className="flex items-center gap-2 text-xs text-slate-400 font-medium">
                    <span>{item.branch_name || 'General Engineering'}</span>
                    <span>·</span>
                    <span>
                      {new Date(item.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })} at {new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>

                <StatusBadge status={item.status} size="md" />
              </div>

              {item.status_reason && (
                <p className="text-xs text-slate-600 leading-relaxed bg-slate-50/80 p-2.5 rounded-xl border border-slate-200/60">
                  {item.status_reason}
                </p>
              )}

              <div className="flex items-center justify-between text-xs text-slate-500 pt-1">
                <div className="flex items-center gap-4">
                  <span>Verified Concepts: <strong>{item.verified_signs_count}</strong></span>
                  <span>Unsupported: <strong>{item.unsupported_signs_count}</strong></span>
                  {item.has_video && (
                    <span className="text-emerald-600 font-semibold flex items-center gap-1">
                      <Video size={13} /> Video Available
                    </span>
                  )}
                  {item.has_avatar && (
                    <span className="text-blue-600 font-semibold flex items-center gap-1">
                      <User size={13} /> 3D Avatar
                    </span>
                  )}
                </div>

                <Link
                  to={`/translate`}
                  className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
                >
                  <span>Re-examine in Translator</span>
                  <ArrowRight size={13} />
                </Link>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-12 bg-white rounded-2xl border border-slate-200 text-center text-slate-500 text-xs">
          No translation history matching criteria.
        </div>
      )}
    </div>
  );
};

