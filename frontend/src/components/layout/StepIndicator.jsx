import { motion } from "framer-motion";
import { useLanguage } from "../../i18n";

export const StepIndicator = ({ currentStep }) => {
  const { t } = useLanguage();

  const steps = [
    { num: 1, label: t("stepProfile") },
    { num: 2, label: t("stepFinancials") },
    { num: 3, label: t("stepQuiz") },
    { num: 4, label: t("stepDashboard") },
  ];

  return (
    <div className="w-full max-w-2xl mx-auto py-6">
      <div className="flex justify-between items-center relative">
        <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-[var(--color-border-active)] -translate-y-1/2 z-0" />
        <motion.div
          className="absolute top-1/2 left-0 h-0.5 bg-[var(--color-accent-primary)] -translate-y-1/2 z-0 origin-left"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: (currentStep - 1) / (steps.length - 1) }}
          transition={{ duration: 0.5, ease: "easeInOut" }}
        />

        {steps.map((step, idx) => {
          const isCompleted = step.num < currentStep;
          const isActive = step.num === currentStep;

          return (
            <div key={step.num} className="relative z-10 flex flex-col items-center gap-2">
              <motion.div
                initial={false}
                animate={{
                  backgroundColor: isCompleted || isActive ? "var(--color-accent-primary)" : "#FFFFFF",
                  borderColor: isCompleted || isActive ? "var(--color-accent-primary)" : "var(--color-text-muted)",
                  boxShadow: isActive ? "var(--shadow-glow-primary)" : "none",
                }}
                className={`w-8 h-8 rounded-full border-2 flex items-center justify-center transition-colors duration-300 ${
                  isCompleted ? "text-white" : isActive ? "text-white" : "text-[var(--color-text-muted)]"
                }`}
              >
                <span className="font-mono text-sm font-bold">{step.num}</span>
              </motion.div>
              <span
                className={`text-xs font-medium uppercase tracking-wider absolute top-full mt-2 transition-colors duration-300 ${
                  isActive ? "text-[var(--color-text-primary)]" : "text-[var(--color-text-muted)]"
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
