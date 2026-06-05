import { forwardRef } from "react";

export const Slider = forwardRef(({ label, error, min = 0, max = 100, step = 1, showValue = true, unit = "%", className = "", ...props }, ref) => {
  return (
    <div className={`flex flex-col gap-3 w-full ${className}`}>
      {label && (
        <div className="flex justify-between items-center">
          <label className="text-sm font-medium text-[var(--color-text-primary)]">{label}</label>
          {showValue && <span className="font-mono text-sm font-semibold text-[var(--color-text-primary)] bg-[var(--color-bg-subtle)] px-2 py-0.5 rounded-md">{props.value || 0}{unit}</span>}
        </div>
      )}
      <input
        type="range"
        ref={ref}
        min={min}
        max={max}
        step={step}
        className="w-full h-1.5 bg-[var(--color-bg-subtle)] rounded-full appearance-none cursor-pointer accent-[var(--color-accent-primary)] hover:accent-[var(--color-accent-second)] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-zinc-950/10"
        {...props}
      />
      <style>{`
        input[type=range]::-webkit-slider-thumb {
          appearance: none;
          width: 18px;
          height: 18px;
          border-radius: 50%;
          background: var(--color-accent-primary);
          box-shadow: 0 0 0 2px white, 0 0 0 4px rgba(9, 9, 11, 0.1);
          cursor: pointer;
          transition: transform 0.2s cubic-bezier(0.2, 0, 0, 1);
        }
        input[type=range]::-webkit-slider-thumb:hover {
          transform: scale(1.15);
        }
      `}</style>
      {error && <span className="text-[var(--color-accent-danger)] text-xs">{error.message}</span>}
    </div>
  );
});
Slider.displayName = "Slider";
