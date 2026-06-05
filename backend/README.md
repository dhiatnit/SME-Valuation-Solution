# Value Intelligence Platform — Backend

FastAPI backend that powers the SME valuation platform.
Implements the 8 team-approved methodology items on top of a Supabase (Postgres) database.

## Architecture (1 file per concern)

```
backend/
├── main.py             ← FastAPI app + POST /api/valutazione
├── config.py           ← All constants (multiples, weights, premiums, field maps)
├── db.py               ← Supabase client + inserts + RPC calls
├── scoring.py          ← Calls 4 Delta RPCs, computes SQF
├── valuation.py        ← Items 1, 2, 4, 5 — formula, gap, asset premiums
├── recommendations.py  ← Item 6 — 12-prescription lookup matrix
├── requirements.txt
├── .env.example
└── .gitignore
```

## What it does

For each `POST /api/valutazione` request:

1. **Persists** the company profile + 4 capital responses to Supabase
2. **Calls** 4 SQL Delta RPCs (`score_*_capital_delta`) → 1-10 scores per question
3. **Aggregates** to 4 capital scores → weighted **SQF** (1-10)
4. **Computes** current valuation, optimised valuation, value gap
5. **Returns** capital scores + valuation + recommendations for the dashboard

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # fill in Supabase URL + service role key
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI).

## Prerequisites

The Supabase project must have the schema from `Supabasesql/human_capital_migration.sql`
already applied. That migration creates:

- `sectors`, `lifecycles`, `companies`
- 4 capital response tables (HC, TC, RC, FC)
- `financial_kpi_thresholds` lookup
- `bucket_kpi()` helper
- 4 `score_*_capital_delta()` RPC functions
- ~1,000 seed rows

## API contract

### `POST /api/valutazione`

Request body (`ValutazionePayload`) matches the frontend's 3-step form, camelCase.

Response (truncated):
```json
{
  "company_id": "uuid",
  "capital_scores": {"human": 6.4, "tech": 7.1, "relational": 5.8, "financial": 6.9},
  "sqf": 6.71,
  "sqf_norm": 0.6344,
  "valuation": {
    "base_value_k": 4500,
    "sector_multiple": 7.5,
    "adjustment": 1.0806,
    "final_value_k": 4892.7
  },
  "value_gap": {
    "current_value_k": 4892.7,
    "optimised_value_k": 5400.0,
    "value_gap_k": 507.3,
    "value_gap_pct": 10.37
  },
  "recommendations": [
    {"capital": "human", "score": 6.4, "band": "ok", "text": "..."},
    ...
  ],
  "currency_unit": "€k"
}
```

## Methodology

All formulas, weights, thresholds, and recommendations are documented and
team-approved in `methodology_proposal.html`. Change `config.py` to tune any
calibration — the rest of the code adapts automatically.
