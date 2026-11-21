import React from 'react';
import { CheckCircle2, AlertCircle, HelpCircle, Clock, ShieldAlert } from 'lucide-react';
import { ValidationStatus } from '../../types';

interface StatusBadgeProps {
  status: ValidationStatus;
  size?: 'sm' | 'md' | 'lg';
  showIcon?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  size = 'md',
  showIcon = true,
}) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'verified':
        return {
          label: 'Verified ISL',
          bgColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
          dotColor: 'bg-emerald-500',
          icon: CheckCircle2,
        };
      case 'partial':
        return {
          label: 'Partial Sign',
          bgColor: 'bg-amber-50 text-amber-700 border-amber-200',
          dotColor: 'bg-amber-500',
          icon: AlertCircle,
        };
      case 'explanation_needed':
      case 'explanation_required':
        return {
          label: 'Pedagogical Explanation Needed',
          bgColor: 'bg-purple-50 text-purple-700 border-purple-200',
          dotColor: 'bg-purple-500',
          icon: HelpCircle,
        };
      case 'needs_review':
        return {
          label: 'Under Deaf Review',
          bgColor: 'bg-sky-50 text-sky-700 border-sky-200',
          dotColor: 'bg-sky-500',
          icon: Clock,
        };
      case 'demo_only':
        return {
          label: 'Demo Media Only',
          bgColor: 'bg-amber-50 text-amber-700 border-amber-200',
          dotColor: 'bg-amber-500',
          icon: AlertCircle,
        };
      case 'blocked':
        return {
          label: 'Blocked (Awaiting Data)',
          bgColor: 'bg-rose-50 text-rose-700 border-rose-200',
          dotColor: 'bg-rose-500',
          icon: ShieldAlert,
        };
      case 'not_implemented':
        return {
          label: 'Not Implemented',
          bgColor: 'bg-slate-100 text-slate-700 border-slate-300',
          dotColor: 'bg-slate-400',
          icon: AlertCircle,
        };
      case 'unsupported':
      default:
        return {
          label: 'Unsupported (Zero Fabrication)',
          bgColor: 'bg-rose-50 text-rose-700 border-rose-200',
          dotColor: 'bg-rose-500',
          icon: ShieldAlert,
        };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5 gap-1',
    md: 'text-xs px-2.5 py-1 gap-1.5',
    lg: 'text-sm px-3 py-1.5 gap-2',
  }[size];

  const iconSizes = {
    sm: 12,
    md: 14,
    lg: 16,
  }[size];

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full border shadow-sm ${config.bgColor} ${sizeClasses}`}
      title={`Validation Status: ${config.label}`}
    >
      {showIcon && <Icon size={iconSizes} className="shrink-0" />}
      <span>{config.label}</span>
    </span>
  );
};

