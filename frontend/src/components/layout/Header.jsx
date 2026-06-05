import { StepIndicator } from "./StepIndicator";
import { useLanguage } from "../../i18n";
import { motion } from "framer-motion";

export const Header = ({ currentStep }) => {
  const { lang, setLang, t } = useLanguage();

  return (
    <header className="w-full sticky top-0 z-50 bg-[var(--color-bg-base)]/80 backdrop-blur-xl border-b border-[var(--color-border-subtle)]">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex flex-col">
            <h1 className="font-display font-semibold text-xl tracking-tight text-[var(--color-text-primary)]">
              {t("platformTitle")}
            </h1>
          </div>
          <div className="flex-1 w-full max-w-xl hidden md:block">
            <StepIndicator currentStep={currentStep} />
          </div>
          <div className="flex items-center gap-4">
            <div className="relative flex items-center p-[4px] rounded-[16px] border border-[var(--color-border-subtle)] bg-[var(--color-bg-base)] shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
              {/* Background pill that animates */}
              <motion.div
                className="absolute top-[4px] bottom-[4px] w-[calc(50%-4px)] bg-white rounded-[12px] shadow-[0_1px_4px_rgba(0,0,0,0.08),0_0_0_1px_rgba(0,0,0,0.02)] z-0"
                initial={false}
                animate={{
                  x: lang === 'it' ? "4px" : "calc(100% + 4px)"
                }}
                transition={{ type: "spring", stiffness: 500, damping: 35 }}
              />
              
              <button 
                onClick={() => setLang('it')}
                className={`relative z-10 px-5 py-1.5 text-[14px] font-bold tracking-wider transition-colors duration-200 cursor-pointer select-none outline-none ${lang === 'it' ? 'text-[var(--color-text-primary)]' : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]'}`}
              >
                IT
              </button>
              
              {/* Small vertical separator */}
              <div className="w-[1px] h-4 bg-[var(--color-border-subtle)] mx-0 relative z-10 opacity-60" />
              
              <button 
                onClick={() => setLang('en')}
                className={`relative z-10 px-5 py-1.5 text-[14px] font-bold tracking-wider transition-colors duration-200 cursor-pointer select-none outline-none ${lang === 'en' ? 'text-[var(--color-text-primary)]' : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)]'}`}
              >
                EN
              </button>
            </div>
          </div>
        </div>
        <div className="w-full mt-4 md:hidden">
          <StepIndicator currentStep={currentStep} />
        </div>
      </div>
    </header>
  );
};
