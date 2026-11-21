import React from 'react';
import { ShieldCheck, AlertCircle, Sparkles, HelpCircle, Lock, UserX } from 'lucide-react';
import { MotionVerificationStatus } from '../../types';

interface AnimationStatusBadgeProps {
  status: MotionVerificationStatus | string;
  className?: string;
  showTooltip?: boolean;
}

export const AnimationStatusBadge: React.FC<AnimationStatusBadgeProps> = ({
  status,
  className = '',
  showTooltip = true
}) => {
  let badgeConfig = {
    label: 'Not Implemented',
    description: 'No motion capture asset exists for this concept. Avatar remains in resting posture.',
    bg: 'bg-slate-800',
    text: 'text-slate-300',
    border: 'border-slate-700',
    icon: <UserX size={14} className="text-slate-400" />
  };

  switch (status) {
    case 'VERIFIED_ISL_MOTION':
      badgeConfig = {
        label: 'Verified ISL Motion',
        description: 'Authentic ISL motion capture verified and certified by an accredited Deaf linguistic expert.',
        bg: 'bg-emerald-950/80',
        text: 'text-emerald-300',
        border: 'border-emerald-700/60',
        icon: <ShieldCheck size={14} className="text-emerald-400" />
      };
      break;

    case 'PARTIALLY_VERIFIED_MOTION':
    case 'partial':
      badgeConfig = {
        label: 'Partially Verified Mocap',
        description: 'Captured from official ISLRTC video. Retargeted to 54-joint rig, pending formal Deaf expert review.',
        bg: 'bg-amber-950/80',
        text: 'text-amber-300',
        border: 'border-amber-700/60',
        icon: <AlertCircle size={14} className="text-amber-400" />
      };
      break;

    case 'REQUIRES_LINGUISTIC_REVIEW':
      badgeConfig = {
        label: 'Requires Linguistic Review',
        description: 'Pedagogical classifier animation sequence. Requires certification by an accredited Deaf educator.',
        bg: 'bg-blue-950/80',
        text: 'text-blue-300',
        border: 'border-blue-700/60',
        icon: <HelpCircle size={14} className="text-blue-400" />
      };
      break;

    case 'DEMO_ONLY':
      badgeConfig = {
        label: 'Demo Only (Fingerspelling)',
        description: 'Algorithmic fingerspelling demonstration. Not certified as authentic lexical ISL signing.',
        bg: 'bg-purple-950/80',
        text: 'text-purple-300',
        border: 'border-purple-700/60',
        icon: <Sparkles size={14} className="text-purple-400" />
      };
      break;

    case 'SOURCE_RESTRICTED':
      badgeConfig = {
        label: 'Source Restricted',
        description: 'Proprietary or restricted motion capture source; redistribution prohibited.',
        bg: 'bg-red-950/80',
        text: 'text-red-300',
        border: 'border-red-700/60',
        icon: <Lock size={14} className="text-red-400" />
      };
      break;

    case 'NOT_IMPLEMENTED':
    default:
      badgeConfig = {
        label: 'Resting Neutral Posture',
        description: 'Zero-Fabrication Policy: Arbitrary avatar gestures are prohibited when authentic data is unavailable.',
        bg: 'bg-slate-800',
        text: 'text-slate-300',
        border: 'border-slate-700',
        icon: <UserX size={14} className="text-slate-400" />
      };
      break;
  }

  return (
    <div
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${badgeConfig.bg} ${badgeConfig.text} ${badgeConfig.border} ${className}`}
      title={showTooltip ? badgeConfig.description : undefined}
    >
      {badgeConfig.icon}
      <span>{badgeConfig.label}</span>
    </div>
  );
};

