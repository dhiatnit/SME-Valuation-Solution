-- ============================================================
-- MIGRATION 02 — Add Tech Investment as 6th Financial KPI
-- Fixes Bug #2: the techInvestment slider now affects the score.
-- Safe to re-run (idempotent). No data loss.
-- ============================================================

-- ─────────────────────────────────────────────
-- 1. Relax the CHECK constraint so 'tech_invest' is allowed
-- ─────────────────────────────────────────────
ALTER TABLE financial_kpi_thresholds DROP CONSTRAINT IF EXISTS financial_kpi_thresholds_kpi_check;
ALTER TABLE financial_kpi_thresholds ADD CONSTRAINT financial_kpi_thresholds_kpi_check
  CHECK (kpi IN ('cagr','margin','debt','recurring','concentration','tech_invest'));


-- ─────────────────────────────────────────────
-- 2. Add 7 sector-specific thresholds for tech_invest (higher is better)
-- Source: Italian SME R&D/tech spend ratios (Mediobanca innovation index)
-- ─────────────────────────────────────────────
INSERT INTO financial_kpi_thresholds (kpi, sector_id, direction, t1, t2, t3, t4) VALUES
  ('tech_invest', 1, 'higher_better',  3,    8,   15,   25),    -- secTech
  ('tech_invest', 2, 'higher_better',  1,    3,    6,   10),    -- secB2B
  ('tech_invest', 3, 'higher_better',  1,    2,    4,    7),    -- secMfg
  ('tech_invest', 4, 'higher_better',  2,    5,   10,   15),    -- secHealth
  ('tech_invest', 5, 'higher_better',  0.5,  1.5,  3,    5),    -- secRetail
  ('tech_invest', 6, 'higher_better',  0.5,  1,    2,    4),    -- secReal
  ('tech_invest', 7, 'higher_better',  1,    3,    6,   10)     -- secOther
ON CONFLICT (kpi, sector_id) DO UPDATE SET
  direction = EXCLUDED.direction,
  t1 = EXCLUDED.t1, t2 = EXCLUDED.t2,
  t3 = EXCLUDED.t3, t4 = EXCLUDED.t4;


-- ─────────────────────────────────────────────
-- 3. Replace the financial Delta function to score 6 KPIs (was 5)
-- ─────────────────────────────────────────────
CREATE OR REPLACE FUNCTION score_financial_capital_delta(p_response_id uuid)
RETURNS TABLE(question text, raw_value numeric, bucketed int, cluster_mean numeric, delta_score numeric)
LANGUAGE sql STABLE AS $$
  -- 1. Derive the 6 KPIs from the user's row
  WITH t AS (
    SELECT id, sector_id, lifecycle_id,
           ROUND((SQRT(revenue_y3::numeric / NULLIF(revenue_y1,0)) - 1) * 100, 2)              AS cagr_pct,
           ROUND((ebitda::numeric / NULLIF(revenue_y3,0)) * 100, 2)                            AS margin_pct,
           CASE WHEN ebitda > 0
                THEN ROUND(-net_financial_position::numeric / ebitda, 2)
                ELSE NULL END                                                                  AS debt_ratio,
           recurring_revenue_pct                                                               AS recurring_pct,
           client_concentration_pct                                                            AS conc_pct,
           tech_investment_pct                                                                 AS tech_inv_pct
    FROM financial_capital_inputs WHERE id = p_response_id
  ),
  -- 2. Bucket user's KPIs to 1-5
  ub AS (
    SELECT t.*,
           bucket_kpi(t.cagr_pct,      'cagr',          t.sector_id) AS b_cagr,
           bucket_kpi(t.margin_pct,    'margin',        t.sector_id) AS b_margin,
           bucket_kpi(t.debt_ratio,    'debt',          t.sector_id) AS b_debt,
           bucket_kpi(t.recurring_pct, 'recurring',     t.sector_id) AS b_recurring,
           bucket_kpi(t.conc_pct,      'concentration', t.sector_id) AS b_conc,
           bucket_kpi(t.tech_inv_pct,  'tech_invest',   t.sector_id) AS b_tech_inv
    FROM t
  ),
  -- 3. Cluster means of bucketed values (same sector + lifecycle peers)
  peer AS (
    SELECT
      AVG(bucket_kpi(
        ROUND((SQRT(p.revenue_y3::numeric / NULLIF(p.revenue_y1,0)) - 1) * 100, 2),
        'cagr', p.sector_id)::numeric)                                                          AS mu_cagr,
      AVG(bucket_kpi(
        ROUND((p.ebitda::numeric / NULLIF(p.revenue_y3,0)) * 100, 2),
        'margin', p.sector_id)::numeric)                                                        AS mu_margin,
      AVG(bucket_kpi(
        CASE WHEN p.ebitda > 0 THEN ROUND(-p.net_financial_position::numeric / p.ebitda, 2) ELSE NULL END,
        'debt', p.sector_id)::numeric)                                                          AS mu_debt,
      AVG(bucket_kpi(p.recurring_revenue_pct,    'recurring',     p.sector_id)::numeric)        AS mu_recurring,
      AVG(bucket_kpi(p.client_concentration_pct, 'concentration', p.sector_id)::numeric)        AS mu_conc,
      AVG(bucket_kpi(p.tech_investment_pct,      'tech_invest',   p.sector_id)::numeric)        AS mu_tech_inv
    FROM financial_capital_inputs p
    JOIN ub ON p.sector_id = ub.sector_id AND p.lifecycle_id = ub.lifecycle_id
  )
  -- 4. Apply Delta to each of the 6 KPIs
  SELECT 'fq1_cagr'::text,             ub.cagr_pct,      ub.b_cagr,      ROUND(peer.mu_cagr,2),      ROUND(GREATEST(1,LEAST(10, 5.5 + 4.5 * (ub.b_cagr      - peer.mu_cagr)      / 4.0)), 2) FROM ub, peer UNION ALL
  SELECT 'fq2_margin',                 ub.margin_pct,    ub.b_margin,    ROUND(peer.mu_margin,2),    ROUND(GREATEST(1,LEAST(10, 5.5 + 4.5 * (ub.b_margin    - peer.mu_margin)    / 4.0)), 2) FROM ub, peer UNION ALL
  SELECT 'fq3_debt_burden',            ub.debt_ratio,    ub.b_debt,      ROUND(peer.mu_debt,2),      ROUND(GREATEST(1,LEAST(10, 5.5 + 4.5 * (ub.b_debt      - peer.mu_debt)      / 4.0)), 2) FROM ub, peer UNION ALL
  SELECT 'fq4_recurring_revenue',      ub.recurring_pct, ub.b_recurring, ROUND(peer.mu_recurring,2), ROUND(GREATEST(1,LEAST(10, 5.5 + 4.5 * (ub.b_recurring - peer.mu_recurring) / 4.0)), 2) FROM ub, peer UNION ALL
  SELECT 'fq5_client_concentration',   ub.conc_pct,      ub.b_conc,      ROUND(peer.mu_conc,2),      ROUND(GREATEST(1,LEAST(10, 5.5 + 4.5 * (ub.b_conc     - peer.mu_conc)      / 4.0)), 2) FROM ub, peer UNION ALL
  SELECT 'fq6_tech_investment',        ub.tech_inv_pct,  ub.b_tech_inv,  ROUND(peer.mu_tech_inv,2),  ROUND(GREATEST(1,LEAST(10, 5.5 + 4.5 * (ub.b_tech_inv  - peer.mu_tech_inv)  / 4.0)), 2) FROM ub, peer;
$$;


-- ─────────────────────────────────────────────
-- 4. SANITY CHECK (run after migration to confirm 6 KPIs now scored)
-- Expected: 42 thresholds (was 35), then the test below returns 6 rows per company
-- ─────────────────────────────────────────────
-- SELECT COUNT(*) FROM financial_kpi_thresholds;  -- should be 42
-- SELECT DISTINCT kpi FROM financial_kpi_thresholds ORDER BY kpi;
--   -- should list 6: cagr, concentration, debt, margin, recurring, tech_invest
