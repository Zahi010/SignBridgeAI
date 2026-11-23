import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Languages,
  Mic,
  FileText,
  BookOpen,
  History,
  Sliders,
  SplitSquareVertical,
  Info,
  Home,
  ShieldCheck,
  GraduationCap,
  Award,
  Users,
  Scale,
  Sparkles,
  Building2
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const navItems = [
    { to: '/demo', label: 'Live Demonstration', icon: Sparkles, highlight: true },
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/translate', label: 'Text Translator', icon: Languages },
    { to: '/outreach', label: 'Institutional Outreach', icon: Building2 },
    { to: '/live-lecture', label: 'Live Lecture', icon: Mic },
    { to: '/documents', label: 'Document Translator', icon: FileText },
    { to: '/vocabulary', label: 'Vocabulary Explorer', icon: BookOpen },
    { to: '/validation', label: 'Governance & Validation', icon: ShieldCheck },
    { to: '/expert-review', label: 'Expert Review Portal', icon: Award },
    { to: '/community-evaluation', label: 'Deaf Community Portal', icon: Users },
    { to: '/validation-dashboard', label: 'Validation Analytics', icon: Scale },
    { to: '/history', label: 'Translation History', icon: History },
    { to: '/avatar-settings', label: 'Avatar Studio', icon: Sliders },
    { to: '/avatar-audit', label: 'Motion Fidelity Audit', icon: SplitSquareVertical },
    { to: '/about', label: 'Linguistic Policy & About', icon: Info },
  ];

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-white border-r border-slate-200/90 flex flex-col transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:z-auto ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Sidebar Header */}
        <div className="p-4 border-b border-slate-200/80 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-sm">
              SB
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900">SignBridge AI</h2>
              <p className="text-[10px] text-slate-500 font-medium">Deaf Engineering Platform</p>
            </div>
          </div>
        </div>

        {/* Navigation list */}
        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          <div className="px-3 pb-2 text-[10px] uppercase font-bold tracking-wider text-slate-400">
            Navigation
          </div>

          <NavLink
            to="/"
            onClick={onClose}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-indigo-50 text-indigo-700 font-bold'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`
            }
          >
            <Home size={16} />
            <span>Landing Page</span>
          </NavLink>

          <div className="pt-2 pb-1">
            <div className="px-3 pb-1 text-[10px] uppercase font-bold tracking-wider text-slate-400">
              Core Modules
            </div>
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-xs font-bold'
                      : item.highlight
                      ? 'text-indigo-600 bg-indigo-50/60 hover:bg-indigo-50 hover:text-indigo-800'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  }`
                }
              >
                <div className="flex items-center gap-3">
                  <Icon size={16} />
                  <span>{item.label}</span>
                </div>
                {item.highlight && (
                  <span className="text-[9px] uppercase font-extrabold px-1.5 py-0.2 bg-indigo-100 text-indigo-700 rounded">
                    Primary
                  </span>
                )}
              </NavLink>
            );
          })}
        </div>

        {/* Footer Policy Card */}
        <div className="p-3 border-t border-slate-100 bg-slate-50/80">
          <div className="p-3 bg-white border border-slate-200/90 rounded-xl space-y-1.5 shadow-2xs">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800">
              <ShieldCheck size={14} className="text-blue-600 shrink-0" />
              <span>Zero-Fabrication</span>
            </div>
            <p className="text-[10px] text-slate-500 leading-relaxed">
              Strict linguistic truth standard: Only verified ISL signs are certified. Non-existent signs are never synthesized.
            </p>
          </div>
        </div>
      </aside>
    </>
  );
};

