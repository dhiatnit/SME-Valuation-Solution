import { motion } from "framer-motion";
import { KpiCard } from "../dashboard/KpiCard";
import { RadarChart } from "../dashboard/RadarChart";
import { ScoreBar } from "../dashboard/ScoreBar";
import { ActionCard } from "../dashboard/ActionCard";
import { Button } from "../ui";
import { useLanguage } from "../../i18n";

export const Step4Dashboard = ({ result, onReset }) => {
  const { t } = useLanguage();

  if (!result) return null;

  const {
    estimated_value,
    value_min,
    value_max,
    multiple_used,
    value_gap_pct,
    gap_absolute,
    scores,
    benchmarks,
    gaps_vs_benchmark,
    quality_score,
    risk_index,
    top3_actions,
  } = result;

  const radarData = [
    { capital: t("capitalFin"), actual: scores.financial, benchmark: benchmarks.financial },
    { capital: t("capitalTech"), actual: scores.technological, benchmark: benchmarks.technological },
    { capital: t("capitalHum"), actual: scores.human, benchmark: benchmarks.human },
    { capital: t("capitalRel"), actual: scores.relational, benchmark: benchmarks.relational },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      className="w-full max-w-7xl mx-auto flex flex-col gap-6"
    >
      <div className="flex justify-between items-end mb-2">
        <div className="flex flex-col gap-1">
          <h2 className="font-display text-3xl font-bold tracking-tight text-[var(--color-text-primary)]">{t("s4Title")}</h2>
          <p className="text-[var(--color-text-secondary)]">{t("s4Desc")}</p>
        </div>
        <Button onClick={onReset} variant="outline" className="hidden sm:flex">{t("newAnalysis")}</Button>
      </div>

      {/* 4 KPI Cards (Bento grid style top row) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <KpiCard
          title={t("s4Val")}
          value={`€ ${(estimated_value / 1000000).toFixed(2)}M`}
          subtitle={`${t("valRange")}: € ${(value_min / 1000000).toFixed(2)}M - € ${(value_max / 1000000).toFixed(2)}M`}
          footer={`${t("multiplo")}: ${multiple_used}x EBITDA`}
          delay={0.1}
          variant="primary"
        />
        
        <KpiCard
          title={t("s4Gap")}
          value={`+${value_gap_pct.toFixed(1)}%`}
          subtitle={`€ ${(gap_absolute / 1000000).toFixed(2)}M ${t("s4GapPot")}`}
          delay={0.2}
          variant="secondary"
        />

        <KpiCard
          title={t("s4Qs")}
          value={`${quality_score} / 100`}
          subtitle={quality_score >= 50 ? t("s4QsAbove") : t("s4QsBelow")}
          delay={0.3}
          variant="primary"
        />

        <KpiCard
          title={t("s4Risk")}
          value={risk_index.label}
          subtitle={t("s4RiskSub")}
          delay={0.4}
          variant={risk_index.label === "LOW" ? "secondary" : risk_index.label === "MEDIUM" ? "warning" : "danger"}
        />
      </div>

      {/* Main Content Area (Bento big boxes) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Radar Chart (left col) */}
        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.6 }}
          className="lg:col-span-5 bento-card p-6 sm:p-8 flex flex-col h-full"
        >
          <h3 className="font-display text-xl font-bold tracking-tight text-[var(--color-text-primary)] mb-6">{t("s4Radar")}</h3>
          <div className="flex-1 flex items-center justify-center -mx-4">
            <RadarChart data={radarData} />
          </div>
        </motion.div>

        {/* Priority Actions (right col) */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="bento-card p-6 sm:p-8 flex flex-col h-full gap-6"
          >
            <h3 className="font-display text-xl font-bold tracking-tight text-[var(--color-text-primary)]">{t("s4Actions")}</h3>
            <div className="flex flex-col gap-4 h-full justify-between">
              {top3_actions.map((action, idx) => (
                <ActionCard key={idx} index={idx + 1} action={action} delay={0.7 + idx * 0.1} />
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Score Breakdown Area (bottom spanning row) */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.0, duration: 0.5 }}
        className="bento-card p-6 sm:p-8"
      >
        <h3 className="font-display text-xl font-bold tracking-tight text-[var(--color-text-primary)] mb-8">{t("s4Breakdown")}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-10">
          <ScoreBar capital={t("capitalFin")} actual={scores.financial} benchmark={benchmarks.financial} gap={gaps_vs_benchmark.financial} />
          <ScoreBar capital={t("capitalTech")} actual={scores.technological} benchmark={benchmarks.technological} gap={gaps_vs_benchmark.technological} />
          <ScoreBar capital={t("capitalHum")} actual={scores.human} benchmark={benchmarks.human} gap={gaps_vs_benchmark.human} />
          <ScoreBar capital={t("capitalRel")} actual={scores.relational} benchmark={benchmarks.relational} gap={gaps_vs_benchmark.relational} />
        </div>
      </motion.div>

      <div className="flex justify-center mt-6 sm:hidden">
        <Button onClick={onReset} variant="outline" className="w-full">{t("newAnalysis")}</Button>
      </div>
    </motion.div>
  );
};
