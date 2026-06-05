"""
Scoring layer — orchestrates the 4 Delta RPC calls and computes SQF.

Item #7 implementation:
  - All 4 capitals already return 1-10 from their Delta functions
  - Capital score = average of 5 Delta scores per capital
  - SQF        = weighted average using sector-specific weights
  - SQF_norm   = (SQF - 1) / 9  →  used by valuation formula
"""
from config import SECTOR_WEIGHTS

CAPITALS = ('human', 'tech', 'relational', 'financial')


def get_financial_sub_score(financial_details: list, question_key: str) -> float:
    """
    Pull one specific KPI's Delta score (1-10) from the financial details list.
    Used to compute the Growth Factor (which needs CAGR + Recurring scores).
    Returns 5.5 (neutral) if not found.
    """
    for row in financial_details or []:
        if row.get('question') == question_key:
            return float(row['delta_score'])
    return 5.5


def average_delta(delta_rows: list) -> float:
    """Mean of the 5 delta_score values returned by a Delta RPC."""
    if not delta_rows:
        return 5.5  # neutral fallback (should never happen with valid data)
    return round(sum(float(r['delta_score']) for r in delta_rows) / len(delta_rows), 2)


def score_all_capitals(sb, ids: dict) -> dict:
    """
    Calls the 4 Delta RPCs and returns both detailed and aggregated scores.

    ids = {'human': uuid, 'tech': uuid, 'relational': uuid, 'financial': uuid}

    Returns:
      {
        'details':  {capital: [5 delta rows]},
        'capitals': {capital: aggregated_score_1_to_10},
      }
    """
    from db import call_delta  # lazy import — keeps scoring.py supabase-free for unit tests
    details = {cap: call_delta(sb, cap, ids[cap]) for cap in CAPITALS}
    capitals = {cap: average_delta(details[cap]) for cap in CAPITALS}
    return {'details': details, 'capitals': capitals}


def compute_sqf(capital_scores: dict, sector_key: str) -> dict:
    """
    Item #7 — Weighted SQF on 1-10 scale + normalised 0-1 version.

    capital_scores = {'human': 6.4, 'tech': 7.1, 'relational': 5.8, 'financial': 6.9}
    Returns {'sqf': 6.71, 'sqf_norm': 0.635, 'weights': {...}}
    """
    w = SECTOR_WEIGHTS[sector_key]
    sqf = (
        w['human']      * capital_scores['human']      +
        w['tech']       * capital_scores['tech']       +
        w['relational'] * capital_scores['relational'] +
        w['financial']  * capital_scores['financial']
    )
    sqf = round(sqf, 2)
    sqf_norm = round((sqf - 1) / 9, 4)
    return {'sqf': sqf, 'sqf_norm': sqf_norm, 'weights': w}
