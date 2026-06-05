import { Slider, QualitativeScale } from "../ui";
import { motion } from "framer-motion";
import { Controller } from "react-hook-form";
import { useLanguage } from "../../i18n";

export const Step3Questionnaire = ({ control, errors, watch }) => {
  const { t } = useLanguage();
  
  // Mock calculations for real-time preview
  const recurring = parseFloat(watch("recurringRevenue")) || 0;
  const concentration = parseFloat(watch("clientConcentration")) || 0;
  // Human Capital
  const keyManRisk         = parseFloat(watch("keyManRisk"))         || 3;
  const spanOfControl      = parseFloat(watch("spanOfControl"))      || 3;
  const skillInvestment    = parseFloat(watch("skillInvestment"))    || 3;
  const talentRetention    = parseFloat(watch("talentRetention"))    || 3;
  const sopStandardization = parseFloat(watch("sopStandardization")) || 3;
  // Technological Capital
  const opDigital          = parseFloat(watch("operationalDigitalization")) || 3;
  const dataStorage        = parseFloat(watch("dataStorage"))               || 3;
  const wfAutomation       = parseFloat(watch("workflowAutomation"))        || 3;
  const proprietaryDataset = parseFloat(watch("proprietaryDataset"))        || 3;
  const crmAdoption        = parseFloat(watch("crmAdoption"))               || 3;
  // Relational Capital
  const networkQuality       = parseFloat(watch("networkQuality"))       || 3;
  const partnershipStructure = parseFloat(watch("partnershipStructure")) || 3;
  const ecosystemRef         = parseFloat(watch("ecosystemReferrals"))   || 3;
  const brandAssets          = parseFloat(watch("brandAssets"))          || 3;
  const repeatCust           = parseFloat(watch("repeatCustomers"))      || 3;

  // Simple normalization mocks for the preview bars
  const normConcentration = concentration > 70 ? 0.1 : concentration > 50 ? 0.3 : concentration > 35 ? 0.5 : concentration > 20 ? 0.8 : 1.0;
  const normRecurring = recurring < 10 ? 0.1 : recurring < 25 ? 0.3 : recurring < 50 ? 0.6 : recurring < 75 ? 0.8 : 1.0;

  const finScore = (0.25 * normRecurring + 0.20 * normConcentration + 0.30) / 0.75;

  const normFounderDep = (5 - keyManRisk) / 4;
  const normSpan       = (spanOfControl - 1) / 4;
  const normSkill      = (skillInvestment - 1) / 4;
  const normRetention  = (talentRetention - 1) / 4;
  const normSop        = (sopStandardization - 1) / 4;
  const humScore = (
    normFounderDep * 0.35 +
    normSpan       * 0.25 +
    normRetention  * 0.20 +
    normSop        * 0.15 +
    normSkill      * 0.05
  );

  const normOpDigital       = (opDigital - 1) / 4;
  const normDataStorage     = (dataStorage - 1) / 4;
  const normAutomation      = (wfAutomation - 1) / 4;
  const normProprietaryData = (proprietaryDataset - 1) / 4;
  const normCrm             = (crmAdoption - 1) / 4;
  const techScore = (
    normOpDigital       * 0.25 +
    normAutomation      * 0.25 +
    normCrm             * 0.15 +
    normDataStorage     * 0.10 +
    normProprietaryData * 0.05
  ) / 0.80;  // parziale: esclude tech_investment (0.20) che viene dal backend

  const normNetwork     = (networkQuality - 1) / 4;
  const normPartnership = (partnershipStructure - 1) / 4;
  const normEco         = (ecosystemRef - 1) / 4;
  const normBrand       = (brandAssets - 1) / 4;
  const normRepeat      = (repeatCust - 1) / 4;
  const relScore = (
    normNetwork     * 0.30 +
    normEco         * 0.25 +
    normRepeat      * 0.20 +
    normPartnership * 0.15 +
    normBrand       * 0.10
  );

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="w-full max-w-6xl mx-auto flex flex-col lg:flex-row gap-6"
    >
      {/* Left Column: Quantitative */}
      <div className="flex-1 flex flex-col gap-6 h-full">
        <div className="bento-card p-8 sm:p-10 flex flex-col gap-8 h-full">
          
          <div className="flex flex-col gap-2">
            <h2 className="font-display text-3xl font-bold tracking-tight text-[var(--color-text-primary)]">{t("s3TitleQuant")}</h2>
            <p className="text-[var(--color-text-secondary)]">{t("s3DescQuant")}</p>
          </div>

          <div className="flex flex-col gap-10 mt-4">
            <Controller
              name="recurringRevenue"
              control={control}
              defaultValue={0}
              rules={{ required: true }}
              render={({ field }) => (
                <Slider
                  label={t("s3RecRev")}
                  min={0}
                  max={100}
                  value={field.value}
                  onChange={field.onChange}
                />
              )}
            />
            <Controller
              name="clientConcentration"
              control={control}
              defaultValue={0}
              rules={{ required: true }}
              render={({ field }) => (
                <Slider
                  label={t("s3Concentration")}
                  min={0}
                  max={100}
                  value={field.value}
                  onChange={field.onChange}
                />
              )}
            />
          </div>

          <div className="mt-auto bg-[var(--color-bg-subtle)] p-6 rounded-xl border border-[var(--color-border-subtle)] flex flex-col gap-6">
            <h3 className="text-xs font-semibold text-[var(--color-text-secondary)] tracking-wider uppercase">{t("s3Preview")}</h3>
            
            <div className="flex flex-col gap-4">
              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-[var(--color-text-primary)]">{t("capitalFin")}</span>
                  <span className="font-mono text-[var(--color-text-primary)]">{finScore.toFixed(2)}</span>
                </div>
                <div className="h-1.5 w-full bg-[var(--color-bg-base)] rounded-full overflow-hidden">
                  <motion.div 
                    className="h-full bg-[var(--color-accent-second)]" 
                    initial={{ width: 0 }} 
                    animate={{ width: `${finScore * 100}%` }} 
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-[var(--color-text-primary)]">{t("capitalHum")}</span>
                  <span className="font-mono text-[var(--color-text-primary)]">{humScore.toFixed(2)}</span>
                </div>
                <div className="h-1.5 w-full bg-[var(--color-bg-base)] rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-[var(--color-accent-primary)]"
                    initial={{ width: 0 }}
                    animate={{ width: `${humScore * 100}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-[var(--color-text-primary)]">{t("capitalTech")}</span>
                  <span className="font-mono text-[var(--color-text-primary)]">{techScore.toFixed(2)}</span>
                </div>
                <div className="h-1.5 w-full bg-[var(--color-bg-base)] rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-zinc-400"
                    initial={{ width: 0 }}
                    animate={{ width: `${techScore * 100}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium text-[var(--color-text-primary)]">{t("capitalRel")}</span>
                  <span className="font-mono text-[var(--color-text-primary)]">{relScore.toFixed(2)}</span>
                </div>
                <div className="h-1.5 w-full bg-[var(--color-bg-base)] rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-zinc-500"
                    initial={{ width: 0 }}
                    animate={{ width: `${relScore * 100}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column: Qualitative Scales */}
      <div className="flex-[1.5] bento-card p-8 sm:p-10 flex flex-col gap-8">
        <div className="flex flex-col gap-2">
          <h2 className="font-display text-2xl font-bold text-[var(--color-text-primary)]">{t("s3TitleQual")}</h2>
          <p className="text-[var(--color-text-secondary)]">{t("s3DescQual")}</p>
        </div>
        
        <div className="flex flex-col gap-10 overflow-y-auto max-h-[75vh] pr-2">

          {/* ── HUMAN CAPITAL ─────────────────── */}
          <div className="flex flex-col gap-6">
            <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--color-text-secondary)] border-b border-[var(--color-border-subtle)] pb-2">
              {t("s3HumanTitle")}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Controller name="keyManRisk" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3H1")} minLabel={t("s3H1Min")} maxLabel={t("s3H1Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="spanOfControl" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3H2")} minLabel={t("s3H2Min")} maxLabel={t("s3H2Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="skillInvestment" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3H3")} minLabel={t("s3H3Min")} maxLabel={t("s3H3Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="talentRetention" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3H4")} minLabel={t("s3H4Min")} maxLabel={t("s3H4Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="sopStandardization" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3H5")} minLabel={t("s3H5Min")} maxLabel={t("s3H5Max")} value={field.value} onChange={field.onChange} />} />
            </div>
          </div>

          {/* ── TECHNOLOGICAL CAPITAL ──────────── */}
          <div className="flex flex-col gap-6">
            <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--color-text-secondary)] border-b border-[var(--color-border-subtle)] pb-2">
              {t("s3TechTitle")}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Controller name="operationalDigitalization" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3T1")} minLabel={t("s3T1Min")} maxLabel={t("s3T1Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="dataStorage" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3T2")} minLabel={t("s3T2Min")} maxLabel={t("s3T2Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="workflowAutomation" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3T3")} minLabel={t("s3T3Min")} maxLabel={t("s3T3Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="proprietaryDataset" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3T4")} minLabel={t("s3T4Min")} maxLabel={t("s3T4Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="crmAdoption" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3T5")} minLabel={t("s3T5Min")} maxLabel={t("s3T5Max")} value={field.value} onChange={field.onChange} />} />
            </div>
          </div>

          {/* ── RELATIONAL CAPITAL ─────────────── */}
          <div className="flex flex-col gap-6">
            <h3 className="text-xs font-bold uppercase tracking-widest text-[var(--color-text-secondary)] border-b border-[var(--color-border-subtle)] pb-2">
              {t("s3RelTitle")}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Controller name="networkQuality" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3R1")} minLabel={t("s3R1Min")} maxLabel={t("s3R1Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="partnershipStructure" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3R2")} minLabel={t("s3R2Min")} maxLabel={t("s3R2Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="brandAssets" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3R3")} minLabel={t("s3R3Min")} maxLabel={t("s3R3Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="ecosystemReferrals" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3R4")} minLabel={t("s3R4Min")} maxLabel={t("s3R4Max")} value={field.value} onChange={field.onChange} />} />
              <Controller name="repeatCustomers" control={control} defaultValue="3" rules={{ required: true }}
                render={({ field }) => <QualitativeScale label={t("s3R5")} minLabel={t("s3R5Min")} maxLabel={t("s3R5Max")} value={field.value} onChange={field.onChange} />} />
            </div>
          </div>

        </div>
      </div>
    </motion.div>
  );
};
