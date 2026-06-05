import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useLanguage } from "../../i18n";

export const ScoreBar = ({ capital, actual, benchmark, gap }) => {
  const isPositive = gap >= 0;
  const { t } = useLanguage();
  const [hovered, setHovered] = useState(false);

  return (
    <div className="flex flex-col gap-3 w-full">
      <div className="flex justify-between items-center text-sm">
        <span className="font-semibold text-[var(--color-text-primary)]">{capital}</span>
        <span className={`font-mono text-xs font-semibold px-2 py-0.5 rounded-md ${isPositive ? "bg-[var(--color-bg-subtle)] text-[var(--color-text-primary)]" : "bg-red-50 text-red-600"}`}>
          {isPositive ? "+" : ""}{(gap * 100).toFixed(1)}% vs Bench
        </span>
      </div>

      {/* Bar track — positioning context for tooltip */}
      <div
        className="relative h-2 w-full"
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {/* Tooltip */}
        <AnimatePresence>
          {hovered && (
            <motion.div
              className="absolute bottom-5 left-1/2 -translate-x-1/2 z-50 bento-card p-3 min-w-[150px] flex flex-col gap-1.5 shadow-xl border border-[var(--color-border-subtle)] bg-[var(--color-bg-base)] pointer-events-none"
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 4 }}
              transition={{ duration: 0.15 }}
            >
              <p className="font-semibold text-xs text-[var(--color-text-primary)] border-b border-[var(--color-border-subtle)] pb-1.5 mb-0.5">{capital}</p>
              <div className="flex justify-between items-center gap-4 text-xs">
                <span className="text-[var(--color-text-secondary)]">{t("actual")}:</span>
                <strong className="text-[var(--color-accent-primary)] font-mono">
                  {(actual * 100).toFixed(0)}<span className="text-[10px] font-normal">/100</span>
                </strong>
              </div>
              <div className="flex justify-between items-center gap-4 text-xs">
                <span className="text-[var(--color-text-muted)]">{t("target")}:</span>
                <span className="text-[var(--color-text-secondary)] font-mono">
                  {(benchmark * 100).toFixed(0)}<span className="text-[10px] font-normal">/100</span>
                </span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Track */}
        <div className="absolute inset-0 bg-[var(--color-bg-subtle)] rounded-full overflow-hidden cursor-pointer">
          <motion.div
            className="absolute top-0 left-0 h-full bg-[var(--color-accent-primary)] rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${actual * 100}%` }}
            transition={{ duration: 1.2, ease: [0.22, 1, 0.36, 1] }}
          />
        </div>

        {/* Benchmark marker — outside overflow-hidden so dot is visible */}
        <motion.div
          className="absolute top-0 bottom-0 w-0.5 bg-[var(--color-border-active)] z-10 rounded-full"
          initial={{ left: 0, opacity: 0 }}
          animate={{ left: `${benchmark * 100}%`, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <div className="absolute -top-1 -translate-x-1/2 w-1.5 h-1.5 rounded-full bg-[var(--color-border-active)]" />
        </motion.div>
      </div>
    </div>
  );
};
