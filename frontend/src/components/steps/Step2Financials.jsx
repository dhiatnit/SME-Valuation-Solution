import { useState, useRef } from "react";
import { Input, Slider } from "../ui";
import { motion } from "framer-motion";
import { Controller } from "react-hook-form";
import { useLanguage } from "../../i18n";

export const Step2Financials = ({ register, control, errors, watch }) => {
  const { t } = useLanguage();
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const fileInputRef = useRef(null);
  
  const rev1 = parseFloat(watch("revenueY1")) || 0;
  const rev3 = parseFloat(watch("revenueY3")) || 0;
  const ebitda = parseFloat(watch("ebitda")) || 0;
  const nfp = parseFloat(watch("netFinancialPosition")) || 0;

  // CAGR calculation: ( (Rev3 / Rev1)^(1/2) ) - 1
  let cagr = 0;
  if (rev1 > 0 && rev3 > 0) {
    cagr = (Math.pow(rev3 / rev1, 0.5) - 1) * 100;
  }

  // EBITDA Margin calculation: EBITDA / Rev3
  let margin = 0;
  if (rev3 > 0 && ebitda > 0) {
    margin = (ebitda / rev3) * 100;
  }

  // Debt/EBITDA calculation: NFP / EBITDA
  let debtEbitda = null;
  if (ebitda > 0 && nfp !== 0) {
    debtEbitda = nfp / ebitda;
  }

  // Drag and Drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setUploadedFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      setUploadedFile(e.target.files[0]);
    }
  };

  const removeFile = (e) => {
    e.stopPropagation();
    setUploadedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="w-full max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-[1.5fr_1fr] gap-6"
    >
      {/* Left Column: Form Inputs */}
      <div className="flex flex-col gap-8 bento-card p-8 sm:p-10">
        
        <div className="flex flex-col gap-2">
          <h2 className="font-display text-3xl font-bold tracking-tight text-[var(--color-text-primary)]">{t("s2Title")}</h2>
          <p className="text-[var(--color-text-secondary)]">{t("s2Desc")}</p>
        </div>

        {/* Upload Box */}
        <div 
          className={`relative flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-xl transition-all cursor-pointer group
            ${dragActive 
              ? 'border-[var(--color-accent-primary)] bg-[var(--color-accent-primary)]/5 scale-[1.02] shadow-sm' 
              : 'border-[var(--color-border-subtle)] hover:bg-[var(--color-bg-subtle)] hover:border-[var(--color-border-default)]'
            }
            ${uploadedFile ? 'bg-[var(--color-bg-subtle)] border-solid border-[var(--color-border-default)] cursor-default hover:bg-[var(--color-bg-subtle)]' : ''}
          `}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => !uploadedFile && fileInputRef.current?.click()}
        >
          <input 
            ref={fileInputRef}
            type="file" 
            className="hidden" 
            accept=".pdf,.xlsx,.xls,.xml" 
            onChange={handleChange} 
          />
          
          {uploadedFile ? (
            <div className="flex items-center justify-between w-full gap-4 px-2">
              <div className="flex items-center gap-4 overflow-hidden">
                <div className="p-2.5 bg-[var(--color-bg-base)] rounded-xl shadow-sm border border-[var(--color-border-subtle)] flex-shrink-0">
                  <svg className="w-6 h-6 text-[var(--color-accent-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div className="flex flex-col overflow-hidden">
                  <span className="text-sm font-semibold text-[var(--color-text-primary)] truncate" title={uploadedFile.name}>
                    {uploadedFile.name}
                  </span>
                  <span className="text-xs font-mono text-[var(--color-text-muted)]">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
              </div>
              <button 
                type="button"
                onClick={removeFile}
                className="p-2 text-[var(--color-text-muted)] hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors flex-shrink-0"
                title={t("s2RemoveFile")}
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center gap-2.5 text-center pointer-events-none">
              <div className="p-3.5 bg-[var(--color-bg-base)] rounded-2xl shadow-sm border border-[var(--color-border-subtle)] mb-2 group-hover:scale-105 transition-transform">
                <svg className="w-6 h-6 text-[var(--color-text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              </div>
              <span className="font-semibold text-[var(--color-text-primary)] text-sm">{t("s2UploadTitle")}</span>
              <span className="text-xs text-[var(--color-text-secondary)]">{t("s2UploadDesc")}</span>
              <span className="text-[10px] text-[var(--color-text-muted)] mt-2 font-mono font-medium bg-[var(--color-bg-subtle)] px-2 py-1 rounded-md border border-[var(--color-border-subtle)] uppercase tracking-wider">
                {t("s2UploadFormats")}
              </span>
            </div>
          )}
        </div>

        <div className="h-px w-full bg-[var(--color-border-subtle)] my-2 relative">
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="bg-[var(--color-bg-base)] px-4 text-[10px] font-bold text-[var(--color-text-muted)] uppercase tracking-widest">
              {t("s2Or")}
            </span>
          </div>
        </div>

        <div className="flex flex-col gap-6">
          <Input
            label={t("s2Rev1")}
            type="number"
            placeholder="0"
            rightIcon={<span className="text-[var(--color-text-muted)] text-sm">€</span>}
            error={errors.revenueY1}
            {...register("revenueY1", { required: t("s2Req"), min: { value: 1, message: t("s2Min") } })}
          />
          <Input
            label={t("s2Rev2")}
            type="number"
            placeholder="0"
            rightIcon={<span className="text-[var(--color-text-muted)] text-sm">€</span>}
            error={errors.revenueY2}
            {...register("revenueY2", { required: t("s2Req"), min: { value: 1, message: t("s2Min") } })}
          />
          <Input
            label={t("s2Rev3")}
            type="number"
            placeholder="0"
            rightIcon={<span className="text-[var(--color-text-muted)] text-sm">€</span>}
            error={errors.revenueY3}
            {...register("revenueY3", { required: t("s2Req"), min: { value: 1, message: t("s2Min") } })}
          />
          <Input
            label={t("s2Ebitda")}
            type="number"
            placeholder="0"
            rightIcon={<span className="text-[var(--color-text-muted)] text-sm">€</span>}
            error={errors.ebitda}
            {...register("ebitda", { required: t("s2Req") })}
          />
          <Input
            label={t("s2NFP")}
            type="number"
            placeholder="0"
            rightIcon={<span className="text-[var(--color-text-muted)] text-sm">€</span>}
            error={errors.netFinancialPosition}
            {...register("netFinancialPosition", { required: t("s2Req") })}
          />
        </div>
      </div>

      {/* Right Column: Preview & Slider */}
      <div className="flex flex-col gap-6">
        <div className="bento-card p-8 flex flex-col gap-8">
          <h3 className="text-sm font-medium text-[var(--color-text-secondary)] tracking-wide uppercase">{t("s2Preview")}</h3>
          
          <div className="flex flex-col gap-6">
            <div className="flex justify-between items-center border-b border-[var(--color-border-subtle)] pb-4">
              <span className="text-[var(--color-text-primary)] font-medium">EBITDA Margin</span>
              <span className="font-mono text-3xl font-bold tracking-tighter text-[var(--color-text-primary)]">{margin.toFixed(1)}<span className="text-lg text-[var(--color-text-muted)]">%</span></span>
            </div>
            
            <div className="flex justify-between items-center border-b border-[var(--color-border-subtle)] pb-4">
              <span className="text-[var(--color-text-primary)] font-medium">Revenue CAGR</span>
              <span className="font-mono text-3xl font-bold tracking-tighter text-[var(--color-text-primary)]">{cagr.toFixed(1)}<span className="text-lg text-[var(--color-text-muted)]">%</span></span>
            </div>
            {debtEbitda !== null && (
              <div className="flex justify-between items-center border-b border-[var(--color-border-subtle)] pb-4">
                <span className="text-[var(--color-text-primary)] font-medium">Debt / EBITDA</span>
                <span className="font-mono text-3xl font-bold tracking-tighter text-[var(--color-text-primary)]">
                  {debtEbitda.toFixed(2)}<span className="text-lg text-[var(--color-text-muted)]">x</span>
                </span>
              </div>
            )}
          </div>

          <div className="p-4 bg-[var(--color-bg-subtle)] rounded-xl text-center">
            <p className="text-xs text-[var(--color-text-secondary)]">
              {t("s2PreviewDesc")}
            </p>
          </div>
        </div>

        <div className="bento-card p-8 flex flex-col gap-6">
          <h3 className="text-sm font-medium text-[var(--color-text-secondary)] tracking-wide uppercase">{t("s2Hybrid")}</h3>
          <Controller
            name="techInvestment"
            control={control}
            defaultValue={5}
            rules={{ required: true }}
            render={({ field }) => (
              <Slider
                label="Tech Investment / Revenue %"
                min={0}
                max={20}
                step={0.1}
                value={field.value}
                onChange={field.onChange}
              />
            )}
          />
          <p className="text-xs text-[var(--color-text-muted)] pt-2 border-t border-[var(--color-border-subtle)]">
            {t("s2HybridDesc")}
          </p>
        </div>
      </div>
    </motion.div>
  );
};
