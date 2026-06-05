import { motion } from "framer-motion";
import { useEffect, useState } from "react";

export const KpiCard = ({ title, value, subtitle, footer, delay = 0, variant = "primary" }) => {
  const [count, setCount] = useState(0);
  
  const numericMatch = typeof value === "string" ? value.match(/^([^0-9]*)(-?[0-9]*\.?[0-9]+)(.*)$/) : null;
  const isNumericStr = numericMatch !== null;
  const numToAnimate = isNumericStr ? parseFloat(numericMatch[2]) : typeof value === "number" ? value : null;
  const prefix = isNumericStr ? numericMatch[1] : "";
  const suffix = isNumericStr ? numericMatch[3] : "";
  
  const decimals = numericMatch?.[2].includes(".") ? numericMatch[2].split(".")[1].length : 0;

  useEffect(() => {
    if (numToAnimate === null) return;
    const end = numToAnimate;
    const duration = 1000;
    const startTime = performance.now();

    let reqId;
    const animate = (time) => {
      const elapsed = time - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
      setCount(easeProgress * end);
      if (progress < 1) {
        reqId = requestAnimationFrame(animate);
      } else {
        setCount(end); // Ensure exact final value
      }
    };
    const t = setTimeout(() => {
      reqId = requestAnimationFrame(animate);
    }, delay * 1000 + 100);
    
    return () => {
      clearTimeout(t);
      cancelAnimationFrame(reqId);
    };
  }, [numToAnimate, delay]);

  const displayValue = numToAnimate !== null
    ? `${prefix}${count.toFixed(decimals)}${suffix}`
    : value;

  const colorVariants = {
    primary: "text-[var(--color-text-primary)]",
    secondary: "text-[var(--color-text-secondary)]",
    warning: "text-[var(--color-accent-warn)]",
    danger: "text-[var(--color-accent-danger)]",
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="bento-card p-6 flex flex-col gap-3 justify-between hover:bg-[var(--color-bg-subtle)]/50 transition-colors group"
    >
      <h3 className="text-xs font-semibold text-[var(--color-text-secondary)] tracking-wider uppercase group-hover:text-[var(--color-text-primary)] transition-colors">{title}</h3>
      <div className={`font-mono text-4xl lg:text-5xl font-bold tracking-tighter ${colorVariants[variant] || "text-[var(--color-text-primary)]"}`}>
        {displayValue}
      </div>
      {(subtitle || footer) && (
        <div className="flex flex-col gap-1 mt-2 pt-4 border-t border-[var(--color-border-subtle)]">
          {subtitle && <p className="text-sm font-medium text-[var(--color-text-primary)]">{subtitle}</p>}
          {footer && <p className="text-xs text-[var(--color-text-muted)]">{footer}</p>}
        </div>
      )}
    </motion.div>
  );
};
