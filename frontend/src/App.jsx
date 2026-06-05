import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from './components/layout/Header';
import { Step1Profile } from './components/steps/Step1Profile';
import { Step2Financials } from './components/steps/Step2Financials';
import { Step3Questionnaire } from './components/steps/Step3Questionnaire';
import { Step4Dashboard } from './components/steps/Step4Dashboard';
import { Button } from './components/ui';
import { submitValuation } from './hooks/useValuation';
import { useLanguage } from './i18n';

const DEMO = {
  companyName:         "Tecno Srl",
  sector:              "secB2B",
  lifecycle:           "lcGrowth",
  objective:           "objInvestors",
  horizon:             "hor35",
  assets:              ["assBrand"],
  revenueY1:           2800000,
  revenueY2:           3100000,
  revenueY3:           3500000,
  ebitda:              560000,
  netFinancialPosition: 450000,
  techInvestment:      3.2,
  recurringRevenue:    35,
  clientConcentration: 55,
  // Human Capital
  keyManRisk:           "4",
  spanOfControl:        "3",
  skillInvestment:      "2",
  talentRetention:      "3",
  sopStandardization:   "2",
  // Technological Capital
  operationalDigitalization: "3",
  dataStorage:               "3",
  workflowAutomation:        "2",
  proprietaryDataset:        "2",
  crmAdoption:               "3",
  // Relational Capital
  networkQuality:        "2",
  partnershipStructure:  "2",
  brandAssets:           "3",
  ecosystemReferrals:    "2",
  repeatCustomers:       "3",
};

export default function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingPhase, setLoadingPhase] = useState(0);
  const [valuationResult, setValuationResult] = useState(null);
  
  const { t, lang } = useLanguage();

  const { register, control, handleSubmit, formState: { errors }, watch, reset, trigger } = useForm({
    mode: "onChange"
  });

  const loadDemoData = () => {
    reset(DEMO);
  };

  const handleNext = async () => {
    let fieldsToValidate = [];
    if (currentStep === 1) {
      fieldsToValidate = ['companyName', 'sector', 'lifecycle', 'objective', 'horizon'];
    } else if (currentStep === 2) {
      fieldsToValidate = ['revenueY1', 'revenueY2', 'revenueY3', 'ebitda', 'netFinancialPosition', 'techInvestment'];
    } else if (currentStep === 3) {
      fieldsToValidate = [
        'recurringRevenue', 'clientConcentration',
        // Human Capital
        'keyManRisk', 'spanOfControl', 'skillInvestment', 'talentRetention', 'sopStandardization',
        // Technological Capital
        'operationalDigitalization', 'dataStorage', 'workflowAutomation', 'proprietaryDataset', 'crmAdoption',
        // Relational Capital
        'networkQuality', 'partnershipStructure', 'brandAssets', 'ecosystemReferrals', 'repeatCustomers',
      ];
    }

    const isValid = await trigger(fieldsToValidate);
    if (isValid) {
      if (currentStep < 3) {
        setCurrentStep((prev) => prev + 1);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else if (currentStep === 3) {
        handleSubmit(onSubmit)();
      }
    }
  };

  const handleBack = () => {
    if (currentStep > 1 && currentStep < 4) {
      setCurrentStep((prev) => prev - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const onSubmit = async (data) => {
    // If we're already on the dashboard (just switching language), don't show the loading screen
    const isLanguageSwitch = currentStep === 4;
    
    if (!isLanguageSwitch) {
      setIsLoading(true);
      setLoadingPhase(0);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    const interval = !isLanguageSwitch ? setInterval(() => {
      setLoadingPhase((p) => Math.min(p + 1, 2));
    }, 800) : null;

    try {
      let result;
      try {
        result = await submitValuation({
          ...data,
          language: lang
        });
        
        // Artificial delay for UX (only on initial submit, not on language change)
        if (!isLanguageSwitch) {
          await new Promise(resolve => setTimeout(resolve, 2400));
        }
      } catch (e) {
        console.warn("Backend not found, using Mock data");
        if (!isLanguageSwitch) {
          await new Promise(resolve => setTimeout(resolve, 2400));
        }
        result = {
          "estimated_value": 1962468,
          "value_min": 1766221,
          "value_max": 2158715,
          "multiple_used": 5.5,
          "value_gap_pct": 88.3,
          "optimized_value": 3697226,
          "gap_absolute": 1734758,
          "scores": { "financial": 0.595, "technological": 0.5, "human": 0.3375, "relational": 0.27 },
          "sqf": 0.9665,
          "gf": 0.66,
          "quality_score": 46,
          "risk_index": { "label": "MEDIUM", "color": "#fdcb6e" },
          "benchmarks": { "financial": 0.65, "technological": 0.55, "human": 0.60, "relational": 0.68 },
          "gaps_vs_benchmark": { "financial": -0.055, "technological": -0.05, "human": -0.2625, "relational": -0.41 },
          "top3_actions": [
            { "titleKey": "actTitle1", "descKey": "actDesc1", "impact": 14, "capital": "financial", "horizon": "18–24", "sqf_delta": "+0.12 SQF" },
            { "titleKey": "actTitle2", "descKey": "actDesc2", "impact": 10, "capital": "relational", "horizon": "12-18", "sqf_delta": "+0.08 SQF" },
            { "titleKey": "actTitle3", "descKey": "actDesc3", "impact": 8, "capital": "technological", "horizon": "18–24", "sqf_delta": "+0.05 SQF" }
          ]
        };
      }
      
      if (interval) clearInterval(interval);
      setValuationResult(result);
      setCurrentStep(4);
    } catch (error) {
      console.error(error);
      if (interval) clearInterval(interval);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    reset({});
    setValuationResult(null);
    setCurrentStep(1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Re-fetch data if language changes while on Dashboard
  useEffect(() => {
    if (currentStep === 4 && valuationResult) {
      handleSubmit(onSubmit)();
    }
  }, [lang]);

  const phases = [
    t("loadingNorm"),
    t("loadingScore"),
    t("loadingFinal")
  ];

  return (
    <div className="min-h-screen bg-[var(--color-bg-base)] text-[var(--color-text-primary)] font-body flex flex-col font-sans selection:bg-zinc-950 selection:text-white">
      <Header currentStep={currentStep} />

      <main className="flex-1 w-full max-w-screen-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 relative flex flex-col">
        <AnimatePresence mode="wait">
          {isLoading ? (
            <motion.div
              key="loading"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 flex flex-col items-center justify-center p-8 z-10 bg-[var(--color-bg-base)]/50 backdrop-blur-sm"
            >
              <div className="w-full max-w-md bento-card p-10">
                <h2 className="text-2xl font-display font-semibold tracking-tight mb-8 text-center text-[var(--color-text-primary)]">{t("processing")}</h2>
                <div className="flex flex-col gap-6">
                  {phases.map((phase, idx) => (
                    <div key={phase} className="flex flex-col gap-2">
                      <div className="flex justify-between text-sm font-medium">
                        <span className={idx <= loadingPhase ? "text-[var(--color-text-primary)]" : "text-[var(--color-text-muted)]"}>
                          {phase}
                        </span>
                        <span className="font-mono text-[var(--color-text-secondary)]">{idx < loadingPhase ? "100%" : idx === loadingPhase ? t("loadingTxt") : "0%"}</span>
                      </div>
                      <div className="h-1.5 w-full bg-[var(--color-bg-subtle)] rounded-full overflow-hidden relative">
                        <motion.div 
                          className="absolute h-full bg-[var(--color-accent-primary)] rounded-full" 
                          initial={{ width: 0 }} 
                          animate={{ width: idx < loadingPhase ? "100%" : idx === loadingPhase ? "60%" : "0%" }} 
                          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </motion.div>
          ) : (
            <div className="w-full h-full pb-24 md:pb-32 flex-1 flex flex-col">
              <AnimatePresence mode="wait">
                {currentStep === 1 && (
                  <Step1Profile key="step1" register={register} control={control} errors={errors} />
                )}
                {currentStep === 2 && (
                  <Step2Financials key="step2" register={register} control={control} errors={errors} watch={watch} />
                )}
                {currentStep === 3 && (
                  <Step3Questionnaire key="step3" control={control} errors={errors} watch={watch} />
                )}
                {currentStep === 4 && (
                  <Step4Dashboard key="step4" result={valuationResult} onReset={handleReset} />
                )}
              </AnimatePresence>
            </div>
          )}
        </AnimatePresence>
      </main>

      {!isLoading && currentStep < 4 && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 w-full max-w-xl px-4 z-40">
          <div className="bg-white/80 backdrop-blur-xl border border-[var(--color-border-subtle)] p-3 rounded-2xl shadow-2xl flex justify-between items-center ring-1 ring-black/5">
            <Button variant="ghost" onClick={loadDemoData} className="text-sm">
              {t("loadDemo")}
            </Button>
            <div className="flex gap-3">
              {currentStep > 1 && (
                <Button variant="outline" onClick={handleBack}>
                  {t("back")}
                </Button>
              )}
              <Button variant="primary" onClick={handleNext}>
                {currentStep === 3 ? t("analyze") : t("next")}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
