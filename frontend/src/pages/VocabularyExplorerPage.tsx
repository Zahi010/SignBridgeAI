import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  ShieldAlert,
  Film,
  UserCheck,
  Building,
  Tag,
  ExternalLink,
  X,
  Sparkles
} from 'lucide-react';
import { api } from '../api/client';
import { ConceptDetail, Branch } from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { PolicyNotice } from '../components/common/PolicyNotice';
import { VideoPlayer } from '../components/video/VideoPlayer';

export const VocabularyExplorerPage: React.FC = () => {
  const [concepts, setConcepts] = useState<ConceptDetail[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBranchId, setSelectedBranchId] = useState<number | undefined>(undefined);
  const [selectedStatus, setSelectedStatus] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [selectedConcept, setSelectedConcept] = useState<ConceptDetail | null>(null);

  // Load branches
  useEffect(() => {
    api.getBranches().then(setBranches).catch(console.error);
  }, []);

  // Fetch vocabulary on filter change
  useEffect(() => {
    const fetchVocab = async () => {
      setLoading(true);
      try {
        const res = await api.getVocabulary({
          search: searchTerm || undefined,
          branch_id: selectedBranchId,
          validation_status: selectedStatus || undefined,
        });
        setConcepts(res.items);
      } catch (err) {
        console.error("Failed to load vocabulary", err);
      } finally {
        setLoading(false);
      }
    };

    const delayDebounceFn = setTimeout(() => {
      fetchVocab();
    }, 250);

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm, selectedBranchId, selectedStatus]);

  const activeSign = selectedConcept?.signs?.[0];

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              ISL Engineering Vocabulary Explorer
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
              Curated STEM Registry
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Browse verified signs, linguistic structures, and validation provenance across all branches.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm space-y-3">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {/* Search box */}
          <div className="relative md:col-span-1">
            <Search size={16} className="absolute left-3 top-3 text-slate-400" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search concepts, aliases..."
              className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-slate-50/50"
            />
          </div>

          {/* Branch filter */}
          <div>
            <select
              value={selectedBranchId || ''}
              onChange={(e) => setSelectedBranchId(Number(e.target.value) || undefined)}
              className="w-full text-xs px-3 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50/50 text-slate-700 font-medium"
            >
              <option value="">All Engineering Branches</option>
              {branches.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.name} ({b.code.toUpperCase()})
                </option>
              ))}
            </select>
          </div>

          {/* Validation Status Filter */}
          <div>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full text-xs px-3 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-slate-50/50 text-slate-700 font-medium"
            >
              <option value="">All Validation Statuses</option>
              <option value="verified">Verified Signs Only</option>
              <option value="partial">Partial Signs</option>
              <option value="explanation_needed">Pedagogical Explanation Needed</option>
              <option value="needs_review">Under Deaf Review</option>
              <option value="unsupported">Unsupported (Zero Fabrication)</option>
            </select>
          </div>
        </div>

        {/* Quick count indicator */}
        <div className="flex items-center justify-between text-xs text-slate-500 pt-1 border-t border-slate-100">
          <span>Showing {concepts.length} engineering concepts</span>
          {(searchTerm || selectedBranchId || selectedStatus) && (
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedBranchId(undefined);
                setSelectedStatus('');
              }}
              className="text-indigo-600 hover:text-indigo-800 font-medium"
            >
              Reset Filters
            </button>
          )}
        </div>
      </div>

      {/* Concept Grid */}
      {loading ? (
        <div className="p-12 text-center space-y-3">
          <div className="w-8 h-8 border-3 border-indigo-600/30 border-t-indigo-600 rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500">Loading STEM vocabulary...</p>
        </div>
      ) : concepts.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {concepts.map((concept) => (
            <div
              key={concept.id}
              onClick={() => setSelectedConcept(concept)}
              className="bg-white p-5 rounded-2xl border border-slate-200/90 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer flex flex-col justify-between space-y-3"
            >
              <div className="space-y-2">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-base font-bold text-slate-900">{concept.term}</h3>
                    <span className="text-[11px] text-slate-400 font-medium">
                      {concept.branch_name || "General Engineering"}
                    </span>
                  </div>
                  <StatusBadge status={concept.validation_status} size="sm" />
                </div>

                {concept.signs?.[0]?.sign_gloss && (
                  <div className="text-xs font-mono text-indigo-600 font-semibold bg-indigo-50/60 px-2 py-1 rounded inline-block">
                    Gloss: [{concept.signs[0].sign_gloss}]
                  </div>
                )}

                <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed">
                  {concept.definition}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                <span className="capitalize font-medium">{concept.category || "General"}</span>
                <span className="text-indigo-600 font-semibold hover:underline">
                  Inspect Details →
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="p-12 bg-white rounded-2xl border border-slate-200 text-center text-slate-500 text-xs">
          No concepts matched your search criteria.
        </div>
      )}

      {/* Modal / Detailed Drawer for Selected Concept */}
      {selectedConcept && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 space-y-6 shadow-2xl relative">
            <button
              onClick={() => setSelectedConcept(null)}
              className="absolute top-5 right-5 p-2 rounded-full text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition-colors"
            >
              <X size={20} />
            </button>

            {/* Header info */}
            <div className="space-y-2 pr-8">
              <div className="flex items-center gap-2">
                <h2 className="text-2xl font-extrabold text-slate-900">{selectedConcept.term}</h2>
                <StatusBadge status={selectedConcept.validation_status} size="md" />
              </div>
              <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 font-medium">
                <span>{selectedConcept.branch_name}</span>
                <span>·</span>
                <span>{selectedConcept.subject_name || "Core Subject"}</span>
                <span>·</span>
                <span className="capitalize">{selectedConcept.category}</span>
              </div>
            </div>

            {/* Definition & Technical Context */}
            <div className="space-y-3 p-4 bg-slate-50 rounded-2xl border border-slate-200/80 text-xs text-slate-700 leading-relaxed">
              <div>
                <strong className="text-slate-900 block mb-0.5">Formal Definition:</strong>
                <p>{selectedConcept.definition}</p>
              </div>
              {selectedConcept.technical_context && (
                <div className="pt-2 border-t border-slate-200/60">
                  <strong className="text-slate-900 block mb-0.5">Technical Engineering Context:</strong>
                  <p>{selectedConcept.technical_context}</p>
                </div>
              )}
            </div>

            {/* Authentic ISL Sign Details */}
            {activeSign ? (
              <div className="space-y-4">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
                  <Sparkles size={14} className="text-indigo-600" />
                  <span>Authentic ISL Sign Records & Accreditation</span>
                </h4>

                <div className="p-4 bg-indigo-50/50 border border-indigo-100 rounded-2xl space-y-3 text-xs">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-slate-500 block text-[10px] uppercase font-bold">Sign Gloss</span>
                      <span className="font-mono text-sm font-bold text-indigo-700">
                        {activeSign.sign_gloss}
                      </span>
                    </div>
                    <span className="px-2 py-0.5 bg-white rounded border border-indigo-200 text-indigo-700 font-medium">
                      {activeSign.regional_dialect || "Standard ISL"}
                    </span>
                  </div>

                  {activeSign.linguistic_notes && (
                    <div className="p-2.5 bg-white rounded-xl border border-indigo-100/80 leading-relaxed">
                      <strong className="text-slate-800">Linguistic Description: </strong>
                      {activeSign.linguistic_notes}
                    </div>
                  )}

                  {/* ISL Phonological Parameters Grid */}
                  <div className="p-3 bg-white rounded-xl border border-indigo-100/80 space-y-2">
                    <div className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">
                      Phonological & Articulatory Parameters
                    </div>
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-[11px]">
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-400 block text-[9px] uppercase font-bold">Dominant Hand</span>
                        <span className="font-semibold text-slate-800 capitalize">
                          {activeSign.dominant_hand || 'Unspecified'}
                        </span>
                      </div>
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-400 block text-[9px] uppercase font-bold">Handshape</span>
                        <span className="font-semibold text-slate-800">
                          {activeSign.handshape || 'Pending Review'}
                        </span>
                      </div>
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-400 block text-[9px] uppercase font-bold">Movement</span>
                        <span className="font-semibold text-slate-800">
                          {activeSign.movement || 'Stationary'}
                        </span>
                      </div>
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-400 block text-[9px] uppercase font-bold">Location</span>
                        <span className="font-semibold text-slate-800">
                          {activeSign.location || 'Neutral signing space'}
                        </span>
                      </div>
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-400 block text-[9px] uppercase font-bold">Orientation</span>
                        <span className="font-semibold text-slate-800">
                          {activeSign.orientation || 'Standard'}
                        </span>
                      </div>
                      <div className="bg-slate-50 p-2 rounded-lg border border-slate-100">
                        <span className="text-slate-400 block text-[9px] uppercase font-bold">Non-Manual Markers</span>
                        <span className="font-semibold text-indigo-700">
                          {activeSign.non_manual_markers || 'Neutral facial expression'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Provenance & Reviewer */}
                  <div className="pt-2 border-t border-indigo-100 space-y-1.5 text-[11px] text-slate-600">
                    <div className="flex items-center justify-between text-[10px] text-slate-400">
                      <span>Sign ID: <strong className="text-slate-700 font-mono">{activeSign.sign_id || `ISL-SIGN-${activeSign.id}`}</strong></span>
                      <span>Institution: <strong className="text-slate-700">{activeSign.source_institution || 'ISLRTC Guidelines'}</strong></span>
                    </div>
                    {activeSign.provenance && (
                      <div className="flex items-center gap-1.5">
                        <Building size={13} className="text-slate-400 shrink-0" />
                        <span>
                          <strong>Dataset Provenance: </strong>
                          {activeSign.provenance.name} ({activeSign.provenance.organization}) [{activeSign.provenance.license}]
                        </span>
                      </div>
                    )}
                    {activeSign.expert_review && (
                      <div className="flex items-center gap-1.5">
                        <UserCheck size={13} className="text-emerald-600 shrink-0" />
                        <span>
                          <strong>Deaf Master Reviewer: </strong>
                          {activeSign.expert_review.reviewer_name} — {activeSign.expert_review.reviewer_role}
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Video Player in Modal */}
                {activeSign.has_video && activeSign.video_url && (
                  <div className="space-y-2">
                    <span className="text-xs font-semibold text-slate-700 block">
                      Accredited Sign Video Demonstration:
                    </span>
                    <VideoPlayer
                      video={{
                        available: true,
                        title: `${selectedConcept.term} - ISL Sign`,
                        video_url: activeSign.video_url,
                        duration_seconds: 4.0,
                        source_attribution: activeSign.provenance?.name || "ISLRTC Pilot",
                        license: activeSign.provenance?.license || "Educational",
                        validation_status: activeSign.validation_status,
                      }}
                    />
                  </div>
                )}
              </div>
            ) : (
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-500 text-center">
                No sign record currently accredited. Awaiting deaf educator review.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

