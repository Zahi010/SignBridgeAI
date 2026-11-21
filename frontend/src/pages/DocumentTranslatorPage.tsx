import React, { useState } from 'react';
import {
  FileText,
  Upload,
  CheckCircle2,
  AlertCircle,
  FileCode,
  FileCheck,
  Layers,
  ArrowRight,
  Sparkles,
  Info
} from 'lucide-react';
import { api } from '../api/client';
import { DocumentUploadResponse } from '../types';
import { StatusBadge } from '../components/common/StatusBadge';
import { PolicyNotice } from '../components/common/PolicyNotice';
import { VideoPlayer } from '../components/video/VideoPlayer';
import { AvatarViewer } from '../components/avatar/AvatarViewer';
import { ConceptCard } from '../components/translator/ConceptCard';
import { ISLGrammarView } from '../components/translator/ISLGrammarView';
import { SemanticRelationsCard } from '../components/translator/SemanticRelationsCard';
import { PedagogicalExplanationCard } from '../components/translator/PedagogicalExplanationCard';
import { TranslationPlanCard } from '../components/translator/TranslationPlanCard';

export const DocumentTranslatorPage: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<DocumentUploadResponse | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file: File) => {
    setError(null);
    const validExtensions = ['.pdf', '.docx', '.pptx'];
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();

    if (!validExtensions.includes(ext)) {
      setError(`Invalid file format '${ext}'. Supported formats: PDF, DOCX, PPTX.`);
      setSelectedFile(null);
      return;
    }

    if (file.size > 15 * 1024 * 1024) {
      setError(`File exceeds maximum 15MB limit (${(file.size / (1024 * 1024)).toFixed(2)}MB).`);
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleUploadAndTranslate = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    try {
      const data = await api.uploadDocument(selectedFile);
      setResult(data);
    } catch (err: any) {
      console.error("Document upload error", err);
      setError(
        err?.response?.data?.detail || "Failed to process document. Please ensure the file is valid."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight">
              Engineering Document & Slide Translator
            </h1>
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-indigo-50 text-indigo-700 border border-indigo-100">
              PDF · DOCX · PPTX
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Extract technical curriculum materials from textbooks and presentation slides for ISL analysis.
          </p>
        </div>

        <PolicyNotice compact />
      </div>

      {/* Upload Drag & Drop Area */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
        <div
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer ${
            isDragging
              ? 'border-indigo-500 bg-indigo-50/50 scale-[0.99]'
              : selectedFile
              ? 'border-emerald-400 bg-emerald-50/20'
              : 'border-slate-300 hover:border-indigo-400 bg-slate-50/50'
          }`}
          onClick={() => document.getElementById('doc-upload-input')?.click()}
        >
          <input
            id="doc-upload-input"
            type="file"
            accept=".pdf,.docx,.pptx"
            className="hidden"
            onChange={handleFileChange}
          />

          <div className="flex flex-col items-center justify-center space-y-3">
            <div className="w-14 h-14 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center shadow-xs">
              {selectedFile ? <FileCheck size={28} className="text-emerald-600" /> : <Upload size={28} />}
            </div>

            {selectedFile ? (
              <div>
                <h4 className="text-sm font-bold text-slate-900">{selectedFile.name}</h4>
                <p className="text-xs text-slate-500 mt-0.5">
                  {(selectedFile.size / 1024).toFixed(1)} KB · Ready to analyze
                </p>
              </div>
            ) : (
              <div>
                <h4 className="text-sm font-bold text-slate-900">
                  Drag and drop your engineering document here
                </h4>
                <p className="text-xs text-slate-500 mt-1">
                  Supports <strong>.PDF</strong>, <strong>.DOCX</strong>, and <strong>.PPTX</strong> up to 15 MB
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Action Button & Error */}
        {error && (
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-rose-800 text-xs flex items-center gap-2">
            <AlertCircle size={16} className="shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex items-center justify-between pt-2">
          <span className="text-xs text-slate-500">
            PyMuPDF & python-docx engine
          </span>

          <button
            onClick={handleUploadAndTranslate}
            disabled={!selectedFile || loading}
            className="px-6 py-2.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-700 text-white font-bold text-xs rounded-xl shadow-md shadow-indigo-200 hover:shadow-lg hover:shadow-indigo-300 disabled:opacity-50 transition-all cursor-pointer flex items-center gap-2"
          >
            {loading ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Extracting & Translating...</span>
              </>
            ) : (
              <>
                <FileText size={15} />
                <span>Parse & Translate Document</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Upload and Parsing Result */}
      {result && (
        <div className="space-y-6">
          {/* Document Metrics Card */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center font-bold text-xs">
                  {result.file_type}
                </div>
                <div>
                  <h3 className="text-sm font-bold text-slate-900">{result.filename}</h3>
                  <p className="text-xs text-slate-400">
                    {(result.file_size_bytes / 1024).toFixed(1)} KB · Processed {new Date(result.uploaded_at).toLocaleTimeString()}
                  </p>
                </div>
              </div>

              <StatusBadge status={result.translation_summary.status} size="md" />
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Pages / Slides</span>
                <span className="text-lg font-bold text-slate-800">{result.page_or_slide_count}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Total Words</span>
                <span className="text-lg font-bold text-slate-800">{result.total_words}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Sentences</span>
                <span className="text-lg font-bold text-slate-800">{result.total_sentences}</span>
              </div>
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">Detected Concepts</span>
                <span className="text-lg font-bold text-indigo-600">{result.detected_concepts_count}</span>
              </div>
            </div>

            {/* Extracted Text Snippet */}
            <div className="space-y-1">
              <span className="text-xs font-semibold text-slate-600 uppercase tracking-wider">
                Extracted Text Preview:
              </span>
              <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 font-mono leading-relaxed max-h-32 overflow-y-auto">
                {result.extracted_text_preview}
              </div>
            </div>
          </div>

          {/* Section-by-Section Breakdown */}
          {result.sections && result.sections.length > 0 && (
            <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <div className="p-1.5 bg-indigo-50 text-indigo-600 rounded-lg">
                    <Layers size={18} />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Document Section Breakdown</h3>
                    <p className="text-xs text-slate-500">
                      Granular chapter, slide, and paragraph concept coverage analysis
                    </p>
                  </div>
                </div>

                {result.document_analysis && (
                  <div className="flex items-center gap-2 text-xs">
                    <span className="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 font-semibold border border-indigo-200">
                      Coverage: {result.document_analysis.coverage_percentage}%
                    </span>
                    <span className="text-slate-400 font-mono">
                      {result.document_analysis.total_sections} Sections
                    </span>
                  </div>
                )}
              </div>

              <div className="space-y-2.5">
                {result.sections.map((sec) => (
                  <div
                    key={sec.section_index}
                    className="p-3.5 bg-slate-50 border border-slate-200/80 rounded-xl space-y-2"
                  >
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <div className="flex items-center gap-2">
                        <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-mono text-[10px] font-bold flex items-center justify-center">
                          {sec.section_index}
                        </span>
                        <span className="font-bold text-xs text-slate-900">{sec.heading}</span>
                        <span className="text-[10px] text-slate-400 font-mono">({sec.sentence_count} sentences)</span>
                      </div>

                      <span
                        className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full border ${
                          sec.status === 'supported'
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                            : sec.status === 'explanation_required'
                            ? 'bg-amber-50 text-amber-700 border-amber-200'
                            : sec.status === 'unsupported'
                            ? 'bg-rose-50 text-rose-700 border-rose-200'
                            : 'bg-slate-100 text-slate-600 border-slate-200'
                        }`}
                      >
                        {sec.status.replace('_', ' ')}
                      </span>
                    </div>

                    <p className="text-xs text-slate-600 leading-relaxed font-mono">
                      {sec.text_preview}
                    </p>

                    {sec.detected_concepts.length > 0 && (
                      <div className="flex items-center gap-1.5 flex-wrap pt-1 text-[11px]">
                        <span className="text-slate-400 font-medium">Concepts:</span>
                        {sec.detected_concepts.map((c, idx) => (
                          <span
                            key={idx}
                            className="bg-white border border-slate-200 px-2 py-0.5 rounded text-indigo-700 font-mono font-medium"
                          >
                            {c}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Engineering Translation Plan for Document */}
          {result.translation_summary.translation_plan && (
            <TranslationPlanCard plan={result.translation_summary.translation_plan as any} />
          )}

          {/* ISL Grammar Restructuring for Document Snippet */}
          <ISLGrammarView
            glossSequence={result.translation_summary.isl_gloss_sequence}
            grammarNotes={result.translation_summary.grammar_notes}
          />

          {/* Semantic Engineering Concept Relationships */}
          {result.translation_summary.semantic_relations && result.translation_summary.semantic_relations.length > 0 && (
            <SemanticRelationsCard relations={result.translation_summary.semantic_relations} />
          )}

          {/* Pedagogical Explanations for Unsupported or Needs-Review Concepts */}
          {result.translation_summary.pedagogical_explanations && result.translation_summary.pedagogical_explanations.length > 0 && (
            <div className="space-y-3">
              {result.translation_summary.pedagogical_explanations.map((exp, idx) => (
                <PedagogicalExplanationCard key={idx} explanation={exp} />
              ))}
            </div>
          )}

          {/* Media Outputs */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-700 block">
                Primary Concept Video Output:
              </span>
              <VideoPlayer video={result.translation_summary.video_output} />
            </div>

            <div className="space-y-2">
              <span className="text-xs font-semibold text-slate-700 block">
                3D Signing Avatar Preview:
              </span>
              <AvatarViewer avatarData={result.translation_summary.avatar_output} />
            </div>
          </div>

          {/* Extracted Concepts */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-slate-900">
              Identified Curriculum Concepts in Document ({result.translation_summary.extracted_concepts.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {result.translation_summary.extracted_concepts.map((concept) => (
                <ConceptCard key={concept.id} concept={concept} />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

