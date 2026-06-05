"""
VALUE INTELLIGENCE PLATFORM
main.py — FastAPI Backend

Avvio:
  pip install fastapi uvicorn
  uvicorn main:app --reload

Endpoint:
  POST /api/valutazione  →  esegue pipeline L1 + L2 + L3 + recommender
  GET  /health           →  verifica che il server giri
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# ── Import dei 3 livelli + recommender ────────
from normalizer  import normalize_all_inputs
from scorer      import run_scoring_model
from valuation   import calculate_value, calculate_value_gap
from recommender import generate_recommendations


# ─────────────────────────────────────────────
# APP
# ─────────────────────────────────────────────

app = FastAPI(
    title="Value Intelligence Platform",
    description="API per la valutazione strategica delle PMI",
    version="1.0.0"
)

# CORS — permette al frontend React (localhost:3000 o 5173)
# di chiamare il backend senza errori di cross-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────
# SCHEMA INPUT — quello che arriva dal frontend
# ─────────────────────────────────────────────

class ValutazioneInput(BaseModel):
    language: Optional[str] = "it"
    # Step 1 — Profilo
    company_name: str
    sector:       str
    lifecycle:    Optional[str] = None
    objective:    Optional[str] = None
    horizon:      Optional[str] = None
    assets:       Optional[List[str]] = []

    # Step 2 — Bilancio
    revenue_y1:             float
    revenue_y2:             float
    revenue_y3:             float
    ebitda:                 float
    net_financial_position: float
    tech_investment_pct:    float

    # Step 3 — Questionario quantitativo
    recurring_revenue_pct:    float
    client_concentration_pct: float

    # Step 3 — Human Capital (1-5)
    key_man_risk:           int
    span_of_control:        int
    skill_investment:       int
    talent_retention:       int
    sop_standardization:    int

    # Step 3 — Technological Capital (1-5)
    operational_digitalization: int
    data_storage:               int
    workflow_automation:        int
    proprietary_dataset:        int
    crm_adoption:               int

    # Step 3 — Relational Capital (1-5)
    network_quality:         int
    partnership_structure:   int
    brand_assets:            int
    ecosystem_referrals:     int
    repeat_customers:        int


# ─────────────────────────────────────────────
# ENDPOINT PRINCIPALE
# ─────────────────────────────────────────────

@app.post("/api/valutazione")
def valutazione(input_data: ValutazioneInput):
    """
    Pipeline completa:
      1. Normalizza gli input (L1)
      2. Calcola score per capitale e SQF (L2)
      3. Calcola valore in € e Value Gap (L3)
      4. Genera Top 3 raccomandazioni (recommender)
      5. Restituisce output completo per il dashboard
    """

    try:
        # ── LIVELLO 1 — Normalizzazione ───────
        raw = {
            "revenue_y1":                  input_data.revenue_y1,
            "revenue_y2":                  input_data.revenue_y2,
            "revenue_y3":                  input_data.revenue_y3,
            "ebitda":                      input_data.ebitda,
            "net_financial_position":      input_data.net_financial_position,
            "tech_investment_pct":         input_data.tech_investment_pct,
            "recurring_revenue_pct":       input_data.recurring_revenue_pct,
            "client_concentration_pct":    input_data.client_concentration_pct,
            # Human Capital
            "key_man_risk":                input_data.key_man_risk,
            "span_of_control":             input_data.span_of_control,
            "skill_investment":            input_data.skill_investment,
            "talent_retention":            input_data.talent_retention,
            "sop_standardization":         input_data.sop_standardization,
            # Technological Capital
            "operational_digitalization":  input_data.operational_digitalization,
            "data_storage":                input_data.data_storage,
            "workflow_automation":         input_data.workflow_automation,
            "proprietary_dataset":         input_data.proprietary_dataset,
            "crm_adoption":                input_data.crm_adoption,
            # Relational Capital
            "network_quality":             input_data.network_quality,
            "partnership_structure":       input_data.partnership_structure,
            "brand_assets":                input_data.brand_assets,
            "ecosystem_referrals":         input_data.ecosystem_referrals,
            "repeat_customers":            input_data.repeat_customers,
        }

        normalized = normalize_all_inputs(raw, input_data.sector)

        # Estrai i valori derivati calcolati dal L1
        # — servono al recommender per l'impatto dinamico
        ebitda_margin_pct = normalized["_ebitda_margin_pct"]
        cagr_pct          = normalized["_cagr_pct"]

        # ── LIVELLO 2 — Scoring ───────────────
        scoring = run_scoring_model(normalized, input_data.sector)

        sqf = scoring["sqf"]
        gf  = scoring["gf"]

        # ── LIVELLO 3 — Valutazione ───────────
        valuation = calculate_value(
            input_data.ebitda,
            input_data.sector,
            sqf,
            gf
        )

        value_gap = calculate_value_gap(
            input_data.ebitda,
            input_data.sector,
            sqf,
            gf
        )

        # ── RECOMMENDER — Top 3 azioni ────────
        # Passa ebitda_margin_pct e cagr_pct calcolati dal L1
        top3 = generate_recommendations(
            scores            = scoring["scores"],
            raw_inputs        = raw,
            ebitda_margin_pct = ebitda_margin_pct,   # ← calcolato dal L1
            cagr_pct          = cagr_pct,             # ← calcolato dal L1
            objective         = input_data.objective,
            lang              = input_data.language,
            sector            = input_data.sector
        )

        # ── OUTPUT ────────────────────────────
        return {
            # Valutazione
            "estimated_value":  valuation["value"],
            "value_min":        valuation["value_min"],
            "value_max":        valuation["value_max"],
            "multiple_used":    valuation["multiple_used"],

            # Value Gap
            "value_gap_pct":    value_gap["gap_pct"],
            "optimized_value":  value_gap["optimized_value"],
            "gap_absolute":     value_gap["gap_absolute"],

            # Score e indici (dal L2)
            "scores":            scoring["scores"],
            "sqf":               sqf,
            "gf":                gf,
            "quality_score":     scoring["quality_score"],
            "risk_index":        scoring["risk_index"],
            "scalability_index": scoring["scalability_index"],
            "benchmarks":        scoring["benchmarks"],
            "gaps_vs_benchmark": scoring["gaps_vs_benchmark"],

            # Dati calcolati utili per il frontend
            "ebitda_margin_pct": ebitda_margin_pct,
            "cagr_pct":          cagr_pct,
            "debt_ebitda_ratio": normalized["_debt_ebitda_ratio"],

            # Top 3 raccomandazioni
            "top3_actions": top3,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "message": "Value Intelligence Platform API running"}
