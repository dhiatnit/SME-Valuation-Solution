import { Radar, RadarChart as RechartsRadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { useLanguage } from "../../i18n";

const CustomTooltip = ({ active, payload, t }) => {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  return (
    <div className="bento-card p-4 min-w-[160px] flex flex-col gap-1.5 shadow-xl border border-[var(--color-border-subtle)] bg-[var(--color-bg-base)]">
      <p className="font-semibold text-sm text-[var(--color-text-primary)] border-b border-[var(--color-border-subtle)] pb-2 mb-1">{d.capital}</p>
      <div className="flex justify-between items-center gap-4 text-sm">
        <span className="text-[var(--color-text-secondary)]">{t("actual")}:</span>
        <strong className="text-[var(--color-accent-primary)] font-mono">{(d.actual * 100).toFixed(0)}<span className="text-xs font-normal">/100</span></strong>
      </div>
      <div className="flex justify-between items-center gap-4 text-sm">
        <span className="text-[var(--color-text-muted)]">{t("target")}:</span>
        <span className="text-[var(--color-text-secondary)] font-mono">{(d.benchmark * 100).toFixed(0)}<span className="text-xs font-normal">/100</span></span>
      </div>
    </div>
  );
};

export const RadarChart = ({ data }) => {
  const { t } = useLanguage();

  return (
    <div className="w-full h-[400px]">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsRadarChart cx="50%" cy="50%" outerRadius="60%" data={data}>
          <PolarGrid stroke="var(--color-border-subtle)" strokeDasharray="3 3" />
          <PolarAngleAxis 
            dataKey="capital" 
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12, fontWeight: 500 }} 
          />
          <PolarRadiusAxis angle={30} domain={[0, 1]} tick={false} axisLine={false} />
          <Tooltip content={<CustomTooltip t={t} />} cursor={false} />

          <Radar
            name={t("actual")}
            dataKey="actual"
            stroke="var(--color-accent-primary)"
            strokeWidth={2}
            fill="var(--color-accent-primary)"
            fillOpacity={0.15}
            isAnimationActive={true}
            animationDuration={1500}
            animationEasing="ease-out"
          />
          <Radar
            name={t("target")}
            dataKey="benchmark"
            stroke="var(--color-text-muted)"
            strokeWidth={1.5}
            fill="var(--color-text-muted)"
            fillOpacity={0.05}
            strokeDasharray="4 4"
            isAnimationActive={true}
            animationDuration={1500}
            animationEasing="ease-out"
          />
          <Legend 
            iconType="circle" 
            wrapperStyle={{ 
              fontSize: '12px', 
              color: 'var(--color-text-secondary)', 
              paddingTop: '20px' 
            }} 
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
};
