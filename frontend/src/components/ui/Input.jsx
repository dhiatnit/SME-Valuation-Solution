import { forwardRef } from "react";

export const Input = forwardRef(({ label, error, className = "", rightIcon, ...props }, ref) => {
  return (
    <div className={`flex flex-col gap-2 w-full ${className}`}>
      {label && <label className="text-sm font-medium text-[var(--color-text-primary)]">{label}</label>}
      <div className="relative">
        <input
          ref={ref}
          className={`w-full bg-[var(--color-bg-base)] text-[var(--color-text-primary)] border border-[var(--color-border-subtle)] rounded-xl px-4 py-2.5 text-sm transition-all duration-200 input-glow placeholder-[var(--color-text-muted)] ${
            error ? "border-[var(--color-accent-danger)]" : "hover:border-[var(--color-border-active)]"
          } ${rightIcon ? "pr-10" : ""}`}
          {...props}
        />
        {rightIcon && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--color-text-muted)] flex items-center justify-center">
            {rightIcon}
          </div>
        )}
      </div>
      {error && <span className="text-[var(--color-accent-danger)] text-xs">{error.message}</span>}
    </div>
  );
});
Input.displayName = "Input";
