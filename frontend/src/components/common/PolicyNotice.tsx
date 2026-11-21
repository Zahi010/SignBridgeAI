import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';

export const PolicyNotice: React.FC<{ compact?: boolean }> = ({ compact = false }) => {
  if (compact) {
    return (
      <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-50/80 border border-blue-200/60 rounded-lg text-xs text-blue-800">
        <ShieldCheck size={14} className="text-blue-600 shrink-0" />
        <span>
          <strong>Zero Fabricated Signs Policy:</strong> Only authenticated, peer-reviewed ISL linguistic data is presented.
        </span>
      </div>
    );
  }

  return (
    <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl flex items-start gap-3 shadow-sm">
      <div className="p-2 bg-blue-600 text-white rounded-lg shrink-0 mt-0.5">
        <ShieldCheck size={18} />
      </div>
      <div className="space-y-1">
        <div className="flex items-center gap-2">
          <h4 className="text-sm font-semibold text-blue-950">Zero Fabricated Signs Policy</h4>
          <span className="px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider bg-blue-200/80 text-blue-800 rounded">
            Mandatory Standard
          </span>
        </div>
        <p className="text-xs text-blue-800/90 leading-relaxed">
          Indian Sign Language (ISL) is a rich, natural language with autonomous grammar. 
          SignBridge AI never synthesizes fake signs, synthetic gestures, or artificial word-order swaps. 
          When an engineering term lacks national standardization, it is transparently reported as unsupported or pending deaf review.
        </p>
      </div>
    </div>
  );
};

