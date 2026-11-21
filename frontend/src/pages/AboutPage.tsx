import React from 'react';
import {
  ShieldCheck,
  BookOpen,
  Users,
  Compass,
  CheckCircle2,
  Code2,
  GraduationCap,
  Heart,
  Globe,
  Award
} from 'lucide-react';
import { PolicyNotice } from '../components/common/PolicyNotice';

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-16">
      {/* Header */}
      <div className="space-y-3">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 border border-indigo-200/80 rounded-full text-indigo-700 text-xs font-semibold">
          <GraduationCap size={14} />
          <span>About SignBridge AI · Engineering Accessibility Initiative</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Linguistic Authenticity in Deaf STEM Higher Education
        </h1>
        <p className="text-sm text-slate-600 leading-relaxed max-w-3xl">
          SignBridge AI is an open-source assistive platform engineered to make tertiary technical education accessible for deaf and hard-of-hearing engineering students across India.
        </p>
      </div>

      <PolicyNotice />

      {/* The Zero Fabricated Signs Policy */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-5">
        <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
          <div className="p-2 bg-blue-600 text-white rounded-xl">
            <ShieldCheck size={20} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              The Zero Fabricated Signs Policy (Core Linguistic Charter)
            </h2>
            <p className="text-xs text-slate-500">
              A foundational ethical commitment to linguistic validity and respect for deaf culture.
            </p>
          </div>
        </div>

        <div className="space-y-3 text-xs sm:text-sm text-slate-700 leading-relaxed">
          <p>
            Indian Sign Language (ISL) is a natural, living human language recognized under the Rights of Persons with Disabilities Act (RPwD 2016). 
            It possesses its own independent grammar, spatial syntax, classifier morphology, and non-manual linguistic markers.
          </p>
          <p>
            Historically, AI systems have made the grave linguistic error of assuming English text can simply be converted word-by-word into signs or re-arranged mechanically into Subject-Object-Verb (SOV) order. 
            This creates incomprehensible pseudo-signing that alienates deaf students and damages academic comprehension.
          </p>
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-2">
            <strong className="text-slate-900 block font-bold text-xs uppercase tracking-wider">
              Our 5 Strict Translation Status Classifications:
            </strong>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="font-bold text-emerald-700 block">1. Verified:</span>
                <p className="text-slate-600">
                  Concept has an accredited, certified ISL sign validated by deaf educators and documented in reputable corpora (e.g. ISLRTC STEM reference).
                </p>
              </div>
              <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="font-bold text-amber-700 block">2. Partial:</span>
                <p className="text-slate-600">
                  Compound components are verified, but specialized contextual subtleties require further academic corroboration.
                </p>
              </div>
              <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="font-bold text-purple-700 block">3. Explanation Needed:</span>
                <p className="text-slate-600">
                  Base sign exists, but advanced technical mechanism requires pedagogical elaboration rather than isolated glossing.
                </p>
              </div>
              <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1">
                <span className="font-bold text-sky-700 block">4. Needs Review:</span>
                <p className="text-slate-600">
                  Sign proposals submitted by deaf engineering cohorts undergoing formal validation trial.
                </p>
              </div>
              <div className="p-2.5 bg-white rounded-xl border border-slate-200 space-y-1 md:col-span-2">
                <span className="font-bold text-rose-700 block">5. Unsupported (Zero Fabrication Principle):</span>
                <p className="text-slate-600">
                  Engineering concepts (such as Deadlock in OS) currently lacking standardized single-sign equivalents are transparently labeled as unsupported. 
                  Fingerspelling and visual diagrams are advised rather than generating artificial synthetic gestures.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Multilingual & Branch Coverage Roadmap */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-5">
        <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
          <div className="p-2 bg-indigo-600 text-white rounded-xl">
            <Globe size={20} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Curriculum Branches & Language Expansion Roadmap
            </h2>
            <p className="text-xs text-slate-500">
              Multi-phase deployment across engineering disciplines and regional languages.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
            <strong className="text-slate-900 font-bold block text-sm">
              Engineering Disciplines (Phase 1)
            </strong>
            <ul className="space-y-1 text-slate-600">
              <li>• Computer Science & Engineering (CSE)</li>
              <li>• Electronics & Communication Engineering (ECE)</li>
              <li>• Mechanical Engineering (MECH)</li>
              <li>• Civil Engineering (CIVIL)</li>
              <li>• Electrical & Electronics Engineering (EEE)</li>
            </ul>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
            <strong className="text-slate-900 font-bold block text-sm">
              Spoken & Sign Language Milestones
            </strong>
            <ul className="space-y-1 text-slate-600">
              <li>• <strong>English (Initial Prototype):</strong> Technical terms and lecture syntax.</li>
              <li>• <strong>Malayalam (Milestone 2):</strong> Polytechnic & state technical university integration in Kerala.</li>
              <li>• <strong>Hindi (Milestone 3):</strong> Pan-India STEM technical vocabulary harmonization.</li>
              <li>• <strong>Regional ISL Dialects:</strong> Regional sign variation cataloging.</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Architecture & Tech Stack */}
      <section className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-5">
        <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
          <div className="p-2 bg-slate-800 text-white rounded-xl">
            <Code2 size={20} />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Modular Monolithic Architecture
            </h2>
            <p className="text-xs text-slate-500">
              Clean separation of concerns with modern frontend and robust Python backend.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">Frontend Stack</span>
            <p className="text-slate-600">React 18, TypeScript, Vite, Tailwind CSS, Lucide React, Axios, React Router</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">3D Graphics & Media</span>
            <p className="text-slate-600">Three.js, React Three Fiber, Drei, HTML5 Video Streaming, WebGL OrbitControls</p>
          </div>
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1.5">
            <span className="font-bold text-slate-900 block">Backend & Parsing</span>
            <p className="text-slate-600">Python 3.11/3.13, FastAPI, Pydantic v2, SQLAlchemy, SQLite, Alembic, PyMuPDF, python-docx, python-pptx</p>
          </div>
        </div>
      </section>
    </div>
  );
};

