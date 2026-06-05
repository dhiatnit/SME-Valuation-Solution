import { Controller } from "react-hook-form";
import { Input, Select } from "../ui";
import { Briefcase, Building2, Cpu, Cross, ShoppingCart, Activity, LayoutGrid } from "lucide-react";
import { motion } from "framer-motion";
import { useLanguage } from "../../i18n";

export const Step1Profile = ({ register, control, errors }) => {
  const { t } = useLanguage();

  const SECTOR_OPTIONS = [
    { value: "secTech", label: t("secTech"), icon: <Cpu size={16} /> },
    { value: "secB2B", label: t("secB2B"), icon: <Briefcase size={16} /> },
    { value: "secMfg", label: t("secMfg"), icon: <Building2 size={16} /> },
    { value: "secHealth", label: t("secHealth"), icon: <Cross size={16} /> },
    { value: "secRetail", label: t("secRetail"), icon: <ShoppingCart size={16} /> },
    { value: "secReal", label: t("secReal"), icon: <Activity size={16} /> },
    { value: "secOther", label: t("secOther"), icon: <LayoutGrid size={16} /> },
  ];

  const LIFECYCLES = [
    { value: "lcStartup", label: t("lcStartup") },
    { value: "lcGrowth", label: t("lcGrowth") },
    { value: "lcMaturity", label: t("lcMaturity") },
    { value: "lcDecline", label: t("lcDecline") },
  ];

  const OBJECTIVES = [
    { value: "objOrganic", label: t("objOrganic") },
    { value: "objInvestors", label: t("objInvestors") },
    { value: "objExit", label: t("objExit") },
    { value: "objHandover", label: t("objHandover") },
    { value: "objStability", label: t("objStability") },
  ];

  const HORIZONS = [
    { value: "hor12", label: t("hor12") },
    { value: "hor35", label: t("hor35") },
    { value: "hor5", label: t("hor5") },
  ];

  const ASSETS = [
    { value: "assIP", label: t("assIP") },
    { value: "assBrand", label: t("assBrand") },
    { value: "assSoftware", label: t("assSoftware") },
    { value: "assContracts", label: t("assContracts") },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="w-full max-w-3xl mx-auto flex flex-col gap-10 bento-card p-8 sm:p-10"
    >
      <div className="flex flex-col gap-2">
        <h2 className="font-display text-3xl font-bold tracking-tight text-[var(--color-text-primary)]">{t("s1Title")}</h2>
        <p className="text-[var(--color-text-secondary)]">{t("s1Desc")}</p>
      </div>

      <div className="flex flex-col gap-8">
        <Input
          label={t("s1CompanyName")}
          placeholder="es. Tecno Srl"
          error={errors.companyName}
          {...register("companyName", { required: t("s1CompanyReq") })}
        />

        <Controller
          name="sector"
          control={control}
          rules={{ required: t("s1SectorReq") }}
          render={({ field }) => (
            <Select
              label={t("s1Sector")}
              placeholder={t("s1SectorPl")}
              options={SECTOR_OPTIONS}
              value={field.value}
              onChange={field.onChange}
              error={errors.sector}
            />
          )}
        />

        <div className="flex flex-col gap-3">
          <label className="text-sm font-medium text-[var(--color-text-primary)]">{t("s1Lifecycle")}</label>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {LIFECYCLES.map(({value, label}) => (
              <label key={value} className="relative cursor-pointer">
                <input
                  type="radio"
                  value={value}
                  className="peer sr-only"
                  {...register("lifecycle", { required: t("s1LifecycleReq") })}
                />
                <div className="w-full py-4 px-4 text-center rounded-xl border border-[var(--color-border-subtle)] bg-[var(--color-bg-base)] text-[var(--color-text-secondary)] transition-all duration-200 peer-checked:border-[var(--color-accent-primary)] peer-checked:bg-[var(--color-accent-primary)] peer-checked:text-white peer-checked:shadow-sm hover:border-[var(--color-border-active)]">
                  <span className="text-sm font-medium">{label}</span>
                </div>
              </label>
            ))}
          </div>
          {errors.lifecycle && <span className="text-[var(--color-accent-danger)] text-xs">{errors.lifecycle.message}</span>}
        </div>

        <div className="flex flex-col gap-3">
          <label className="text-sm font-medium text-[var(--color-text-primary)]">{t("s1Objective")}</label>
          <div className="flex flex-col gap-3">
            {OBJECTIVES.map(({value, label}) => (
              <label key={value} className="relative cursor-pointer group flex items-center p-4 rounded-xl border border-[var(--color-border-subtle)] bg-[var(--color-bg-base)] hover:border-[var(--color-border-active)] transition-all duration-200 peer-checked:border-[var(--color-accent-primary)]">
                <div className="flex items-center gap-4 w-full">
                  <div className="relative flex items-center justify-center w-5 h-5">
                    <input
                      type="radio"
                      value={value}
                      className="peer sr-only"
                      {...register("objective", { required: t("s1ObjectiveReq") })}
                    />
                    <div className="w-5 h-5 rounded-full border border-[var(--color-border-subtle)] peer-checked:border-[var(--color-accent-primary)] transition-colors" />
                    <div className="absolute w-3 h-3 rounded-full bg-[var(--color-accent-primary)] scale-0 peer-checked:scale-100 transition-transform duration-200" />
                  </div>
                  <span className="text-[var(--color-text-secondary)] font-medium text-sm transition-colors group-hover:text-[var(--color-text-primary)] peer-checked:text-[var(--color-text-primary)]">{label}</span>
                </div>
              </label>
            ))}
          </div>
          {errors.objective && <span className="text-[var(--color-accent-danger)] text-xs">{errors.objective.message}</span>}
        </div>

        <div className="flex flex-col gap-3">
          <label className="text-sm font-medium text-[var(--color-text-primary)]">{t("s1Horizon")}</label>
          <div className="flex rounded-xl border border-[var(--color-border-subtle)] overflow-hidden bg-[var(--color-bg-base)]">
            {HORIZONS.map(({value, label}) => (
              <label key={value} className="flex-1 relative cursor-pointer group">
                <input
                  type="radio"
                  value={value}
                  className="peer sr-only"
                  {...register("horizon", { required: t("s1HorizonReq") })}
                />
                <div className="w-full py-4 text-center border-r border-[var(--color-border-subtle)] last:border-r-0 peer-checked:bg-[var(--color-bg-subtle)] peer-checked:text-[var(--color-text-primary)] text-[var(--color-text-secondary)] transition-colors hover:bg-[var(--color-bg-subtle)]/50">
                  <span className="text-sm font-medium">{label}</span>
                </div>
              </label>
            ))}
          </div>
          {errors.horizon && <span className="text-[var(--color-accent-danger)] text-xs">{errors.horizon.message}</span>}
        </div>

        <div className="flex flex-col gap-3">
          <label className="text-sm font-medium text-[var(--color-text-primary)]">{t("s1Assets")}</label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-5 border border-[var(--color-border-subtle)] rounded-xl bg-[var(--color-bg-base)]">
            {ASSETS.map(({value, label}) => (
              <label key={value} className="flex items-center gap-3 cursor-pointer group">
                <div className="relative flex items-center justify-center">
                  <input
                    type="checkbox"
                    value={value}
                    className="peer sr-only"
                    {...register("assets")}
                  />
                  <div className="w-5 h-5 rounded-md border border-[var(--color-border-subtle)] peer-checked:border-[var(--color-accent-primary)] peer-checked:bg-[var(--color-accent-primary)] transition-colors flex items-center justify-center">
                    <svg className="w-3.5 h-3.5 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                </div>
                <span className="text-sm text-[var(--color-text-secondary)] group-hover:text-[var(--color-text-primary)] transition-colors">{label}</span>
              </label>
            ))}
          </div>
        </div>

      </div>
    </motion.div>
  );
};
