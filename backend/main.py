"""
Value Intelligence Platform — FastAPI backend.

Single endpoint: POST /api/valutazione
Receives the full questionnaire payload from the frontend, persists to Supabase,
calls the 4 Delta RPCs, computes SQF / valuation / value gap / recommendations,
returns the complete result for Step4 Dashboard.

Run locally:
    cd backend
    pip install -r requirements.txt
    cp .env.example .env       # fill in Supabase creds
    uvicorn main:app --reload --port 8000
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import db
from scoring import score_all_capitals, compute_sqf
from valuation import compute_valuation, compute_value_gap
from recommendations import get_all_recommendations
from dashboard import build_dashboard_response

load_dotenv()


# ──────────────────────────────────────────────────────────────────────
# App
# ──────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Value Intelligence Platform API",
    description="Peer-benchmarked SME valuation engine (4-capital model, Delta algorithm)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('CORS_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# ──────────────────────────────────────────────────────────────────────
# Request payload — mirrors the frontend's 3-step form (camelCase)
# ──────────────────────────────────────────────────────────────────────
class ValutazionePayload(BaseModel):
    # Step 1 — Profile
    companyName: str
    sector:      str            # 'secTech' | 'secB2B' | ...
    lifecycle:   str            # 'lcStartup' | 'lcGrowth' | ...
    objective:   Optional[str]  = None
    horizon:     Optional[str]  = None
    assets:      List[str]      = Field(default_factory=list)

    # Step 2 — Financials (€k unless % stated)
    revenueY1:              float
    revenueY2:              float
    revenueY3:              float
    ebitda:                 float
    netFinancialPosition:   float
    techInvestment:         float = Field(ge=0, le=100)

    # Step 3 — Financial sliders
    recurringRevenue:    float = Field(ge=0, le=100)
    clientConcentration: float = Field(ge=0, le=100)

    # Step 3 — Human Capital
    keyManRisk:         int = Field(ge=1, le=5)
    spanOfControl:      int = Field(ge=1, le=5)
    skillInvestment:    int = Field(ge=1, le=5)
    talentRetention:    int = Field(ge=1, le=5)
    sopStandardization: int = Field(ge=1, le=5)

    # Step 3 — Technological Capital
    operationalDigitalization: int = Field(ge=1, le=5)
    dataStorage:               int = Field(ge=1, le=5)
    workflowAutomation:        int = Field(ge=1, le=5)
    proprietaryDataset:        int = Field(ge=1, le=5)
    crmAdoption:               int = Field(ge=1, le=5)

    # Step 3 — Relational Capital
    networkQuality:       int = Field(ge=1, le=5)
    partnershipStructure: int = Field(ge=1, le=5)
    brandAssets:          int = Field(ge=1, le=5)
    ecosystemReferrals:   int = Field(ge=1, le=5)
    repeatCustomers:      int = Field(ge=1, le=5)


# ──────────────────────────────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────────────────────────────
@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/api/valutazione')
def valutazione(payload: ValutazionePayload):
    """
    Full evaluation pipeline:
      1. Persist company profile + 4 capital responses to Supabase
      2. Call 4 Delta SQL RPCs to score every question on 1-10
      3. Aggregate to 4 capital scores, then weighted SQF
      4. Compute valuation, value gap, recommendations
      5. Return everything the Step4 Dashboard needs
    """
    try:
        sb = db.get_supabase()
        body = payload.model_dump()

        # 1. Resolve lookup IDs from frontend keys
        sector_id    = db.resolve_sector_id(payload.sector)
        lifecycle_id = db.resolve_lifecycle_id(payload.lifecycle)

        # 2. Insert company profile + 4 capital responses
        company_id = db.insert_company(sb, body, sector_id, lifecycle_id)
        ids = {
            'human':      db.insert_hc(sb, company_id, sector_id, lifecycle_id, body),
            'tech':       db.insert_tc(sb, company_id, sector_id, lifecycle_id, body),
            'relational': db.insert_rc(sb, company_id, sector_id, lifecycle_id, body),
            'financial':  db.insert_fc(sb, company_id, sector_id, lifecycle_id, body),
        }

        # 3. Score all 4 capitals via SQL RPCs (Delta algorithm)
        scoring = score_all_capitals(sb, ids)

        # 4. SQF (weighted average using sector weights)
        sqf_result = compute_sqf(scoring['capitals'], payload.sector)

        # 5. Valuation + Value Gap
        val = compute_valuation(
            payload.ebitda, payload.sector, sqf_result['sqf'], payload.assets
        )
        gap = compute_value_gap(
            payload.ebitda, payload.sector, sqf_result['sqf'], payload.assets
        )

        # 6. Recommendations (12-item lookup matrix)
        recs = get_all_recommendations(scoring['capitals'])

        # 7. Adapt to the Step4Dashboard's expected shape so the frontend
        #    works without any UI code changes.
        dashboard = build_dashboard_response(
            capital_scores=scoring['capitals'],
            sqf=sqf_result['sqf'],
            sector_key=payload.sector,
            valuation=val,
            value_gap=gap,
            recommendations=recs,
            objective=payload.objective,   # Idea A — reorder recs per user goal
        )

        # Return the dashboard fields at the top level (so the frontend can read
        # them directly) AND keep the clean internal shape under `_internal` for
        # debugging / future use.
        return {
            **dashboard,
            '_internal': {
                'company_id':       company_id,
                'sector':           payload.sector,
                'lifecycle':        payload.lifecycle,
                'capital_scores':   scoring['capitals'],
                'capital_details':  scoring['details'],
                'sqf':              sqf_result['sqf'],
                'sqf_norm':         sqf_result['sqf_norm'],
                'sector_weights':   sqf_result['weights'],
                'valuation':        val,
                'value_gap':        gap,
                'recommendations':  recs,
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Log full trace in real prod; for now bubble the message up
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
