import { motion } from "framer-motion";
import { useLanguage } from "../../i18n";

export const ActionCard = ({ index, action, delay = 0 }) => {
  const { t } = useLanguage();

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="p-6 rounded-xl border border-[var(--color-border-subtle)] bg-[var(--color-bg-base)] hover:bg-[var(--color-bg-subtle)] transition-all group flex flex-col gap-4 relative"
    >
      <div className="absolute top-0 left-0 w-1.5 h-full bg-[var(--color-accent-primary)] rounded-l-xl opacity-0 group-hover:opacity-100 transition-opacity" />
      
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div className="flex items-start gap-4">
          <span className="font-mono font-bold text-[var(--color-text-muted)] text-xl leading-none pt-0.5">
            {String(index).padStart(2, "0")}
          </span>
          <div className="flex flex-col gap-1.5">
            <h4 className="font-semibold text-[var(--color-text-primary)] text-lg">{action.title}</h4>
            <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{action.desc}</p>
          </div>
        </div>
        
        <div className="px-3 py-1.5 rounded-lg bg-[var(--color-accent-primary)] text-white font-mono text-sm font-bold whitespace-nowrap self-start">
          +{action.impact}% V
        </div>
      </div>
      
      <div className="pl-10 flex flex-wrap items-center gap-3 text-xs font-medium text-[var(--color-text-muted)] pt-2 border-t border-[var(--color-border-subtle)]">
        <span className="bg-[var(--color-bg-subtle)] px-2 py-1 rounded-md">{action.horizon}</span>
        <span className="bg-[var(--color-bg-subtle)] px-2 py-1 rounded-md text-[var(--color-text-primary)]">{action.sqf_delta}</span>
        <span className="bg-[var(--color-bg-subtle)] px-2 py-1 rounded-md uppercase tracking-wider">
          {action.capital === "financial" ? t("capitalFin") : 
           action.capital === "technological" ? t("capitalTech") : 
           action.capital === "human" ? t("capitalHum") : 
           action.capital === "relational" ? t("capitalRel") : action.capital}
        </span>
      </div>
    </motion.div>
  );
};
