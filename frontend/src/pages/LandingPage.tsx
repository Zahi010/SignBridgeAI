import React from 'react';
import { Link } from 'react-router-dom';
import {
  Languages,
  BookOpen,
  FileText,
  Mic,
  ShieldCheck,
  CheckCircle2,
  Cpu,
  Zap,
  Cog,
  Building2,
  HardDrive,
  ArrowRight,
  Sparkles,
  Users,
  Compass
} from 'lucide-react';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const LandingPage: React.FC = () => {
  return (
    <div className="space-y-16 py-4 max-w-6xl mx-auto">
      {/* Hero Section */}
      <section className="text-center space-y-6 pt-6 sm:pt-10">
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-indigo-50 border border-indigo-200/80 rounded-full text-indigo-700 text-xs font-semibold shadow-2xs">
          <Sparkles size={14} className="text-indigo-600" />
          <span>Next-Generation Accessibility for Deaf Engineering Students</span>
        </div>

        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight sm:leading-tight">
          Bridging Engineering Education with{' '}
          <span className="bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-800 bg-clip-text text-transparent">
            Indian Sign Language
          </span>
        </h1>

        <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
          SignBridge AI translates spoken lectures, technical textbooks, lecture slides, and engineering explanations into verified Indian Sign Language (ISL) using human signing videos and interactive 3D avatars.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Link
            to="/translate"
            className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-indigo-700 text-white font-bold text-sm shadow-md shadow-indigo-200 hover:shadow-lg hover:shadow-indigo-300 transition-all flex items-center justify-center gap-2 group"
          >
            <span>Launch ISL Translator</span>
            <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            to="/dashboard"
            className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 font-bold text-sm shadow-xs transition-colors"
          >
            Open Student Dashboard
          </Link>
          <Link
            to="/live-lecture"
            className="w-full sm:w-auto px-6 py-3.5 rounded-xl bg-slate-100 text-slate-700 hover:bg-slate-200 font-bold text-sm transition-colors flex items-center justify-center gap-2"
          >
            <Mic size={16} />
            <span>Live Lecture Room</span>
          </Link>
        </div>

        <div className="pt-4 max-w-3xl mx-auto">
          <PolicyNotice />
        </div>
      </section>

      {/* Engineering Branches Grid */}
      <section className="space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
            Universal Engineering Branch Coverage
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 max-w-xl mx-auto">
            Standardized technical vocabulary curated for all major undergraduate engineering curricula.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          {[
            { name: "Computer Science", code: "CSE", icon: HardDrive, concepts: "OS, Deadlock, DBMS, Network", color: "from-blue-500 to-indigo-600" },
            { name: "Electronics & Comm.", code: "ECE", icon: Cpu, concepts: "Voltage, Circuit, Microprocessor", color: "from-indigo-500 to-purple-600" },
            { name: "Mechanical Eng.", code: "MECH", icon: Cog, concepts: "Machine, Force, Motion, Dynamics", color: "from-slate-700 to-slate-900" },
            { name: "Civil Engineering", code: "CIVIL", icon: Building2, concepts: "Structure, Foundation, Concrete", color: "from-amber-600 to-orange-700" },
            { name: "Electrical & Electronics", code: "EEE", icon: Zap, concepts: "Electricity, Transformer, Motor", color: "from-emerald-600 to-teal-700" },
          ].map((branch, i) => {
            const Icon = branch.icon;
            return (
              <div
                key={i}
                className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-sm transition-all text-left flex flex-col justify-between"
              >
                <div>
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${branch.color} text-white flex items-center justify-center mb-3 shadow-xs`}>
                    <Icon size={20} />
                  </div>
                  <h3 className="text-sm font-bold text-slate-900">{branch.name}</h3>
                  <span className="text-[10px] font-mono font-bold text-indigo-600 uppercase">
                    {branch.code}
                  </span>
                </div>
                <div className="pt-4 border-t border-slate-100 mt-4 text-[11px] text-slate-500">
                  <span className="text-slate-400 block text-[10px] uppercase font-semibold">Terms:</span>
                  <span className="text-slate-700 font-medium">{branch.concepts}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Input Formats / Capabilities */}
      <section className="bg-gradient-to-b from-slate-900 to-slate-950 text-white rounded-3xl p-8 sm:p-12 space-y-8 shadow-xl">
        <div className="text-center space-y-2 max-w-2xl mx-auto">
          <span className="px-3 py-1 bg-indigo-500/20 border border-indigo-400/30 rounded-full text-indigo-300 text-xs font-semibold">
            Multi-Modal Learning Modalities
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Designed for Modern Academic Workflows
          </h2>
          <p className="text-xs sm:text-sm text-slate-400">
            Deaf engineering students can consume complex curriculum materials across text, audio, and slides.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            {
              title: "Spoken Lectures",
              desc: "Real-time speech-to-text pipeline with ISL concept tagging and live gloss stream.",
              icon: Mic,
              link: "/live-lecture"
            },
            {
              title: "Typed English Text",
              desc: "Instant syntactic restructuring applying Topic-Comment and WH-final ISL rules.",
              icon: Languages,
              link: "/translate"
            },
            {
              title: "PDF & Slide Decks",
              desc: "Direct extraction from PyMuPDF, python-docx, and python-pptx files.",
              icon: FileText,
              link: "/documents"
            },
            {
              title: "ISL Vocabulary Explorer",
              desc: "Searchable technical STEM ontology with accredited video recordings and reviewer notes.",
              icon: BookOpen,
              link: "/vocabulary"
            },
          ].map((feat, i) => {
            const Icon = feat.icon;
            return (
              <Link
                key={i}
                to={feat.link}
                className="p-5 bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 rounded-2xl space-y-3 transition-colors block group"
              >
                <div className="w-10 h-10 rounded-xl bg-indigo-600/30 text-indigo-400 border border-indigo-500/30 flex items-center justify-center group-hover:scale-105 transition-transform">
                  <Icon size={20} />
                </div>
                <h3 className="text-sm font-bold text-white group-hover:text-indigo-300 transition-colors">
                  {feat.title}
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {feat.desc}
                </p>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Zero Fabricated Signs Manifesto Section */}
      <section className="bg-white rounded-3xl border border-slate-200 p-8 sm:p-10 shadow-sm space-y-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-3 max-w-2xl">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-bold border border-blue-100">
              <ShieldCheck size={14} className="text-blue-600" />
              <span>Linguistic Authenticity First</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Why We Strictly Refuse to Synthesize Signs
            </h2>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
              Unlike spoken words, sign languages operate in 3D spatial dimensions with autonomous linguistic syntax, directional classifier predicates, and subtle non-manual markers (facial expressions). 
              Fabricating gestures produces confusing, illegible pseudo-language. SignBridge AI marks uncertified terms honestly as <em>Unsupported</em> or <em>Under Deaf Review</em>.
            </p>
          </div>

          <div className="bg-slate-50 border border-slate-200/80 p-5 rounded-2xl space-y-2.5 max-w-sm shrink-0">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Translation Statuses:
            </h4>
            <div className="space-y-1.5 text-xs">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                <span className="font-semibold text-slate-800">Verified:</span>
                <span className="text-slate-500">Peer-reviewed ISL record</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                <span className="font-semibold text-slate-800">Partial:</span>
                <span className="text-slate-500">Compound elements validated</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-purple-500" />
                <span className="font-semibold text-slate-800">Explanation Needed:</span>
                <span className="text-slate-500">Pedagogical expansion</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-sky-500" />
                <span className="font-semibold text-slate-800">Needs Review:</span>
                <span className="text-slate-500">Active deaf educator trial</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                <span className="font-semibold text-slate-800">Unsupported:</span>
                <span className="text-slate-500">Zero fabrication standard</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

