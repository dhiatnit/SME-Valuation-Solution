import { forwardRef } from "react";
import { motion } from "framer-motion";

export const QualitativeScale = forwardRef(({ label, minLabel, maxLabel, error, className = "", value, onChange, ...props }, ref) => {
  return (
    <div className={`flex flex-col gap-4 w-full p-6 bg-[var(--color-bg-subtle)] border border-transparent rounded-2xl transition-all duration-300 hover:bg-[var(--color-border-subtle)]/30 ${className}`}>
      {label && <label className="text-[var(--color-text-primary)] font-semibold text-sm">{label}</label>}
      <div className="flex flex-col gap-3">
        <div className="relative flex justify-between items-center w-full px-2">
          {/* Track background */}
          <div className="absolute top-1/2 left-2 right-2 h-1 bg-[var(--color-border-subtle)] rounded-full -translate-y-1/2 z-0" />
          
          {[1, 2, 3, 4, 5].map((val) => {
            const isSelected = String(value) === String(val);
            return (
              <label key={val} className="relative z-10 flex flex-col items-center cursor-pointer group py-2">
                <input
                  type="radio"
                  ref={ref}
                  value={val}
                  checked={isSelected}
                  onChange={onChange}
                  className="sr-only"
                  {...props}
                />
                <motion.div
                  animate={{ 
                    scale: isSelected ? 1.2 : 1,
                    backgroundColor: isSelected ? "var(--color-accent-primary)" : "var(--color-bg-base)",
                    borderColor: isSelected ? "var(--color-accent-primary)" : "var(--color-border-active)"
                  }}
                  transition={{ type: "spring", stiffness: 400, damping: 25 }}
                  className="w-4 h-4 rounded-full border-2 shadow-sm"
                />
              </label>
            );
          })}
        </div>
        <div className="flex justify-between text-xs text-[var(--color-text-secondary)] font-medium px-1">
          <span className="text-left w-1/3">{minLabel}</span>
          <span className="text-center w-1/3 opacity-50">3</span>
          <span className="text-right w-1/3">{maxLabel}</span>
        </div>
      </div>
      {error && <span className="text-[var(--color-accent-danger)] text-xs mt-1">{error.message}</span>}
    </div>
  );
});
QualitativeScale.displayName = "QualitativeScale";
