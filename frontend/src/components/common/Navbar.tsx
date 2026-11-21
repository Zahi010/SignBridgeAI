import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Sparkles,
  ShieldCheck,
  Activity,
  Layers,
  ChevronDown,
  BookOpen,
  HelpCircle,
  Menu,
  X
} from 'lucide-react';
import { api } from '../../api/client';

export const Navbar: React.FC<{ onToggleSidebar?: () => void }> = ({ onToggleSidebar }) => {
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'checking'>('checking');
  const location = useLocation();

  useEffect(() => {
    api.getHealth()
      .then((data) => {
        setHealthStatus(data.status === 'healthy' ? 'healthy' : 'degraded');
      })
      .catch(() => {
        setHealthStatus('degraded');
      });
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-4 lg:px-8 py-3.5 transition-all">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        {/* Left: Brand / Logo */}
        <div className="flex items-center gap-3">
          <button
            onClick={onToggleSidebar}
            className="lg:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100 transition-colors"
            aria-label="Toggle Navigation"
          >
            <Menu size={20} />
          </button>

          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-indigo-500 flex items-center justify-center text-white shadow-md shadow-indigo-200 group-hover:scale-105 transition-transform">
              <span className="font-bold text-lg tracking-tighter">SB</span>
            </div>
            <div>
              <span className="text-base font-extrabold bg-gradient-to-r from-blue-700 via-indigo-700 to-indigo-900 bg-clip-text text-transparent">
                SignBridge AI
              </span>
              <span className="hidden sm:inline-block ml-2 px-1.5 py-0.5 text-[10px] uppercase font-bold tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-100 rounded">
                STEM · ISL
              </span>
            </div>
          </Link>
        </div>

        {/* Center: Quick Shortcuts for Demonstration */}
        <nav className="hidden md:flex items-center gap-1 bg-slate-100/80 p-1 rounded-xl border border-slate-200/60 text-xs font-medium text-slate-600">
          <Link
            to="/dashboard"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              location.pathname === '/dashboard' ? 'bg-white text-indigo-700 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Dashboard
          </Link>
          <Link
            to="/translate"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              location.pathname === '/translate' ? 'bg-white text-indigo-700 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Translator
          </Link>
          <Link
            to="/live-lecture"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              location.pathname === '/live-lecture' ? 'bg-white text-indigo-700 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Live Lecture
          </Link>
          <Link
            to="/documents"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              location.pathname === '/documents' ? 'bg-white text-indigo-700 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Documents
          </Link>
          <Link
            to="/vocabulary"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              location.pathname === '/vocabulary' ? 'bg-white text-indigo-700 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Vocabulary
          </Link>
          <Link
            to="/validation"
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              location.pathname === '/validation' ? 'bg-white text-indigo-700 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Validation
          </Link>
        </nav>

        {/* Right: Policy & System Status */}
        <div className="flex items-center gap-3">
          {/* Zero Fabrication Badge */}
          <Link
            to="/about"
            className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-blue-50/90 hover:bg-blue-100/90 border border-blue-200/80 rounded-full text-xs font-semibold text-blue-800 transition-colors"
            title="Read about our strict Zero Fabricated Signs Policy"
          >
            <ShieldCheck size={14} className="text-blue-600" />
            <span>Zero Fabrication Policy</span>
          </Link>

          {/* Backend Status indicator */}
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200 text-xs">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                healthStatus === 'healthy'
                  ? 'bg-emerald-500 shadow-sm shadow-emerald-300 animate-pulse'
                  : healthStatus === 'degraded'
                  ? 'bg-rose-500'
                  : 'bg-amber-400'
              }`}
            />
            <span className="hidden sm:inline text-slate-500 font-medium">
              {healthStatus === 'healthy' ? 'API Online' : healthStatus === 'degraded' ? 'API Offline' : 'Connecting'}
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

